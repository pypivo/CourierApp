import json
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import Response

from db.order_models.services import OrderServices
from .validation_models import CreateOrderDto, CompletedOrderDto

async def _add_order(body: List[CreateOrderDto], session: AsyncSession):
    async with session.begin():
        order_services = OrderServices(session)
        orders = await order_services.add_order(body)
        return orders

async def _get_limit_orders(offset: int, limit: int, session: AsyncSession):
    async with session.begin():
        order_services = OrderServices(session)
        orders = await order_services.get_limit_orders(offset=offset, limit=limit)
        return orders

async def _get_order(order_id: int, session: AsyncSession):
    async with session.begin():
        try:
            order_services = OrderServices(session)
            order = await order_services.get_order_by_id(order_id)
            return order
        except HTTPException:
            return Response(status_code=404)

async def _add_completed_time(body: List[CompletedOrderDto], session: AsyncSession):
    async with session.begin():
        try:
            order_services = OrderServices(db_session=session)
            response_completed_orders = await order_services.add_completed_orders(completed_orders=body)
            return response_completed_orders
        except HTTPException:
            return Response(status_code=400)
