import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship

from ..base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weight = Column(Float, nullable=False)
    regions = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)

    delivery_hours = relationship("OrderDeliveryHours", backref="order", lazy='selectin')
    completed_time = relationship("CompletedOrders", back_populates="order", lazy='selectin')

class OrderDeliveryHours(Base):
    __tablename__ = 'delivery_hours'

    order_id = Column(ForeignKey("orders.id"), primary_key=True)
    delivery_hours = Column(String, nullable=False)

class CompletedOrders(Base):
    __tablename__ = 'completed_orders'

    order_id = Column(ForeignKey("orders.id"), primary_key=True)
    courier_id = Column(ForeignKey('couriers.id'), nullable=False)
    complete_time = Column(TIMESTAMP(timezone=datetime.timezone.utc), nullable=False)

    order = relationship("Order", back_populates="completed_time", lazy="selectin")



