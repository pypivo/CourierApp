import datetime
import json
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import Response

from db.courier_models.services import CourierServices
from .validation_models import CreateCourierDto

async def _add_couriers(body: List[CreateCourierDto], session: AsyncSession):
    async with session.begin():
        courier_services = CourierServices(session)
        couriers = await courier_services.add_couriers(body)
        couriers_response = {"couriers": couriers}
        return couriers_response

async def _get_limit_couriers(offset: int, limit: int, session: AsyncSession):
    async with session.begin():
        courier_services = CourierServices(session)
        couriers = await courier_services.get_limit_couriers(offset, limit)
        couriers_response = {"couriers": couriers, "limit": limit, "offset": offset}
        return couriers_response

async def _get_courier(courier_id: int, session: AsyncSession):
    async with session.begin():
        try:
            courier_services = CourierServices(session)
            courier = await courier_services.get_courier_by_id(courier_id=courier_id)
            return courier
        except HTTPException:
            return Response(status_code=404)

async def _get_courier_rating_in_date(courier_id: int, start_date: datetime.date, end_date: datetime.date, session: AsyncSession):
    async with session.begin():
        try:
            couriers_services = CourierServices(session)
            courier_rating = await couriers_services.get_courier_rating_in_date(courier_id, start_date, end_date)
            return courier_rating
        except HTTPException:
            return Response(status_code=404)