import datetime
from typing import List
from typing import Sequence

from fastapi.exceptions import HTTPException
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import Row
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio.result import Result

from .models import Courier, CourierDistrict, CourierWorkTime
from ..order_models.models import Order, CompletedOrders
from api.courier_api.validation_models import CreateCourierDto


class CourierServices:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_couriers(self, couriers_params: List[CreateCourierDto]):
        couriers_represented = []
        for courier_param in couriers_params:

            courier_param: CreateCourierDto
            new_courier = Courier(courier_type=courier_param.courier_type.value)
            self.db_session.add(new_courier)
            await self.db_session.flush()

            for district in courier_param.regions:
                new_courier_district = CourierDistrict(courier_id=new_courier.id, district_id=district)
                self.db_session.add(new_courier_district)

            for work_time in courier_param.working_hours:
                new_work_time = CourierWorkTime(courier_id=new_courier.id, work_time=work_time)
                self.db_session.add(new_work_time)

            couriers_response = {"courier_id": new_courier.id, "courier_type": courier_param.courier_type.value,
                                 "regions": courier_param.regions, "working_hours": courier_param.working_hours}
            couriers_represented.append(couriers_response)

        await self.db_session.commit()
        return couriers_represented

    async def get_courier_by_id(self, courier_id: int) -> dict:
        rs: Result = await self.db_session.execute(select(Courier).where(Courier.id == courier_id))
        courier: Courier = rs.scalar()
        if courier is not None:
            work_time = _take_work_time(courier.work_time)
            district = _take_district_id(courier.district)
            return {"courier_id": courier.id, "courier_type": courier.courier_type.value,
                    "regions": district, "working_hours": work_time}
        else:
            raise HTTPException(status_code=404)

    async def get_limit_couriers(self, offset: int, limit: int) -> list:
        rs: Result = await self.db_session.execute(select(Courier).limit(limit).offset(offset))
        couriers = rs.scalars().all()

        couriers_represented = []
        for courier in couriers:
            work_time = _take_work_time(courier.work_time)
            district = _take_district_id(courier.district)
            couriers_represented.append({"courier_id": courier.id, "courier_type": courier.courier_type.value,
                                         "regions": district, "working_hours": work_time})
        return couriers_represented

    async def get_courier_rating_in_date(self, courier_id: int, start_date: datetime.date, end_date: datetime.date):
        rs_courier: Result = await self.db_session.execute(select(Courier).where(Courier.id == courier_id))
        courier: Courier = rs_courier.scalar()

        if courier is not None:
            work_time = _take_work_time(courier.work_time)
            district = _take_district_id(courier.district)
            response_courier = {"courier_id": courier.id, "courier_type": courier.courier_type.value,
                                "regions": district, "working_hours": work_time}
            rs_completed: Result = await self.db_session.execute(select(CompletedOrders).
                                                                 where(and_(CompletedOrders.complete_time.
                                                                       between(start_date, end_date)),
                                                                       CompletedOrders.courier_id == courier.id))
            completed_orders = rs_completed.scalars().all()
            if completed_orders:
                co: CompletedOrders
                response_courier["rating"] = _count_rating(completed_orders, courier.courier_type,
                                                           start_date, end_date)
                response_courier["earnings"] = _count_earnings(completed_orders, courier.courier_type)
            return response_courier
        else:
            raise HTTPException(status_code=404)

def _count_rating(completed_orders, courier_type, start_date: datetime.date, end_date: datetime.date):
    td = end_date - start_date
    rating = (len(completed_orders)/int(td.total_seconds()//3600))
    if courier_type.value == "FOOT": C = 3
    elif courier_type.value == "BIKE": C = 2
    else: C = 1
    return rating * C

def _count_earnings(completed_orders, courier_type):
    earnings = sum((co.order.cost for co in completed_orders))
    if courier_type.value == "FOOT": C = 2
    elif courier_type.value == "BIKE": C = 3
    else: C = 4
    return earnings * C

def _take_work_time(works_time: Sequence[Row[CourierWorkTime]]) -> List[str]:
    works_time_represented = []
    for work_time in works_time:
        works_time_represented.append(work_time.work_time)
    return works_time_represented

def _take_district_id(districts: Sequence[Row[CourierDistrict]]) -> List[int]:
    district_represented = []
    for district in districts:
        district_represented.append(district.district_id)
    return district_represented








