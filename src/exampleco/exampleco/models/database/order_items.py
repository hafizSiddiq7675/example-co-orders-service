from email.policy import default
from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP, ForeignKey
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema

from . import Base

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self) -> str:
        return "<OrderItem(created_on='{}', order_id='{}')>".format(self.created_on, self.order_id)


class OrderItemSchema(SQLAlchemySchema):
    class Meta:
        model = OrderItem
        load_instance = True

    id = fields.Integer()
    order_id = fields.Integer()
    created_on = fields.DateTime()
    modified_on = fields.DateTime()