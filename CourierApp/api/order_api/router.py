import json
from typing import List, Union

from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from .validation_models import CreateOrderDto, CreateOrdersRequest, CompletedOrdersRequest,\
    CompletedOrderDto, CompletedOrderResponse, NotCompletedOrderResponse
from .services import _add_order, _get_order, _get_limit_orders, _add_completed_time
from ..rate_limiter import limiter

order_router = APIRouter(prefix="/order")

@order_router.post('', response_model=List[NotCompletedOrderResponse])
@limiter()
async def add_orders(orders: CreateOrdersRequest, session: AsyncSession = Depends(get_db)):
    return await _add_order(body=orders.orders, session=session)

@order_router.get('', response_model=List[Union[CompletedOrderResponse, NotCompletedOrderResponse]])
@limiter()
async def get_limit_orders(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_db)):
    return await _get_limit_orders(offset=offset, limit=limit, session=session)

@order_router.get('/{order_id}', response_model=Union[CompletedOrderResponse, NotCompletedOrderResponse])
@limiter()
async def get_order(order_id: int, session: AsyncSession = Depends(get_db)):
    return await _get_order(order_id, session)

@order_router.post('/complete', response_model=List[CompletedOrderResponse])
@limiter()
async def complete_orders(completed_orders: CompletedOrdersRequest, session: AsyncSession = Depends(get_db)):
    return await _add_completed_time(body=completed_orders.complete_info, session=session)