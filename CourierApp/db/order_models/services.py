from typing import List
from typing import Sequence

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import Row
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio.result import Result

from .models import Order, OrderDeliveryHours, CompletedOrders
from ..courier_models.models import Courier
from api.order_api.validation_models import CreateOrderDto, CompletedOrderDto, CompletedOrderResponse


class OrderServices:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_order(self, orders_params: List[CreateOrderDto]):
        orders_represented = []

        for order in orders_params:
            order: CreateOrderDto
            new_order = Order(weight=order.weight, regions=order.regions,
                              cost=order.cost)
            self.db_session.add(new_order)
            await self.db_session.flush()

            for delivery_hours in order.delivery_hours:
                new_order_delivery_hours = OrderDeliveryHours(order_id=new_order.id, delivery_hours=delivery_hours)
                self.db_session.add(new_order_delivery_hours)

            response_order = {"order_id": new_order.id, "weight": order.weight, "regions": order.regions,
                              "delivery_hours": order.delivery_hours, "cost": order.cost}
            orders_represented.append(response_order)

        await self.db_session.commit()
        return orders_represented

    async def get_limit_orders(self, offset: int, limit: int) -> List[dict]:
        rs: Result = await self.db_session.execute(select(Order).limit(limit).offset(offset))
        orders = rs.scalars().all()

        orders_represented = []
        for order in orders:
            orders_represented.append(create_order_response(order))
        return orders_represented

    async def get_order_by_id(self, order_id: int):
        rs: Result = await self.db_session.execute(select(Order).where(Order.id == order_id))
        order: Order = rs.scalar()

        if order is not None:
            return create_order_response(order)
        else:
            raise HTTPException(status_code=404)

    async def add_completed_orders(self, completed_orders: List[CompletedOrderDto]) -> List[dict]:
        response_completed_orders = []

        for completed_order in completed_orders:

            courier_rs: Result = await self.db_session.execute(select(Courier).
                                                               where(Courier.id == completed_order.courier_id))
            order_rs: Result = await self.db_session.execute(select(Order).
                                                             where(Order.id == completed_order.order_id))

            courier, order = courier_rs.scalar(), order_rs.scalar()
            if courier and order and not order.completed_time:
                new_completed_order = CompletedOrders(order_id=completed_order.order_id,
                                                      courier_id=completed_order.courier_id,
                                                      complete_time=completed_order.complete_time)
                self.db_session.add(new_completed_order)

                delivery_hours = _take_delivery_hours(order.delivery_hours)
                response_order = {"order_id": order.id, "weight": order.weight,
                                  "regions": order.regions,  "delivery_hours": delivery_hours,
                                  "cost": order.cost, "completed_time": new_completed_order.complete_time}
                response_completed_orders.append(response_order)
            else:
                raise HTTPException(status_code=400)

        await self.db_session.commit()
        return response_completed_orders

def create_order_response(order: Order):
    delivery_hours = _take_delivery_hours(order.delivery_hours)
    response_order = {"order_id": order.id, "weight": order.weight, "regions": order.regions,
                      "delivery_hours": delivery_hours, "cost": order.cost}
    if order.completed_time:
        response_order["completed_time"] = order.completed_time[0].complete_time
    return response_order

def _take_delivery_hours(delivery_hours: Sequence[Row[OrderDeliveryHours]]) -> List[str]:
    delivery_hours_represented = []
    # переименовать
    for delivery_hour in delivery_hours:
        delivery_hours_represented.append(delivery_hour.delivery_hours)
    return delivery_hours_represented
