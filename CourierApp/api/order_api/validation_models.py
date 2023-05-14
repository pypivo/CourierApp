from typing import List, Union
from datetime import datetime

from pydantic import BaseModel, constr


delivery_time_scheme = constr(regex=r"^([01]\d|2[0-3]):([0-5]\d)-([01]\d|2[0-3]):([0-5]\d)$")
class CreateOrderDto(BaseModel):
    weight: float
    regions: int
    cost: int
    delivery_hours: List[delivery_time_scheme]

class CreateOrdersRequest(BaseModel):
    orders: List[CreateOrderDto]

class CompletedOrderDto(BaseModel):
    order_id: int
    courier_id: int
    complete_time: datetime

class CompletedOrdersRequest(BaseModel):
    complete_info: List[CompletedOrderDto]

class NotCompletedOrderResponse(CreateOrderDto):
    order_id: int

class CompletedOrderResponse(NotCompletedOrderResponse):
    completed_time: datetime







