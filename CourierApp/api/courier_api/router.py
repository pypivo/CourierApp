import datetime
import json
from typing import List, Union

from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from .services import _add_couriers, _get_courier, _get_limit_couriers, _get_courier_rating_in_date
from .validation_models import CreateCourierRequest, CourierDto, LimitCouriersDto, \
    CourierWithRating, CreateCourierResponse
from ..rate_limiter import limiter
from db.engine import get_db

courier_router = APIRouter(prefix="/couriers")

@courier_router.post('', response_model=CreateCourierResponse)
@limiter()
async def add_couriers(couriers: CreateCourierRequest, session: AsyncSession = Depends(get_db)):
    return await _add_couriers(body=couriers.couriers, session=session)


@courier_router.get('')
@limiter()
async def get_limit_couriers(limit: int = 1, offset: int = 0, session: AsyncSession = Depends(get_db)):
    return await _get_limit_couriers(offset, limit, session=session)


@courier_router.get('/{courier_id}', response_model=CourierDto)
@limiter()
async def get_courier(courier_id: int, session: AsyncSession = Depends(get_db)):
    return await _get_courier(courier_id, session)


@courier_router.get('/meta-info/{courier_id}', response_model=Union[CourierWithRating, CourierDto])
@limiter()
async def get_courier_rating_in_date(courier_id: int, startDate: datetime.date, endDate: datetime.date,
                                     session: AsyncSession = Depends(get_db)):
    return await _get_courier_rating_in_date(courier_id, startDate, endDate, session)