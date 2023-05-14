from enum import Enum
from typing import List

from pydantic import BaseModel, constr

class CourierTypeEnum(Enum):
    FOOT = 'FOOT'
    BIKE = 'BIKE'
    AUTO = 'AUTO'

    def __str__(self):
        return self.value

work_time_scheme = constr(regex=r"^([01]\d|2[0-3]):([0-5]\d)-([01]\d|2[0-3]):([0-5]\d)$")

class CreateCourierDto(BaseModel):
    courier_type: CourierTypeEnum
    regions: List[int]
    working_hours: List[work_time_scheme]

class CreateCourierRequest(BaseModel):
    couriers: List[CreateCourierDto]

class CourierDto(BaseModel):
    courier_id: int
    courier_type: CourierTypeEnum
    regions: List[int]
    working_hours: List[work_time_scheme]

class CreateCourierResponse(BaseModel):
    couriers: List[CourierDto]

class LimitCouriersDto(BaseModel):
    limit: int
    offset: int
    couriers: List[CourierDto]

class CourierWithRating(CourierDto):
    rating: int
    earnings: int