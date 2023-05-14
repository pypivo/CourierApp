
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ..base import Base
from CourierApp.api.courier_api.validation_models import CourierTypeEnum


class Courier(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    courier_type = Column(Enum(CourierTypeEnum))

    district = relationship("CourierDistrict", backref="courier", lazy='selectin')
    work_time = relationship("CourierWorkTime", backref="courier", lazy='selectin')


class CourierDistrict(Base):
    __tablename__ = 'districts'

    courier_id = Column(ForeignKey('couriers.id'), primary_key=True)
    district_id = Column(Integer, nullable=False, primary_key=True)

class CourierWorkTime(Base):
    __tablename__ = 'work_times'

    courier_id = Column(ForeignKey('couriers.id'), primary_key=True)
    work_time = Column(String, nullable=False, primary_key=True)

