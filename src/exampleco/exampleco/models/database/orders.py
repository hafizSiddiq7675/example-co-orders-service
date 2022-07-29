from email.policy import default
from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP
from sqlalchemy.orm import relationship
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema


from . import Base

class Order(Base):
    __tablename__ = 'orders'
    STATUS_ACTIVE = 'active'
    STATUS_DELETED = 'deleted'
    id = Column(Integer, primary_key=True)
    description = Column(TEXT, nullable=True)
    status = Column(String(128), nullable=False, default=STATUS_ACTIVE)
    items = relationship("OrderItem")
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )
    def __repr__(self) -> str:
        return "<Order(created_on='{}', description='{}')>".format(self.created_on, self.description)


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = fields.Integer()
    description = fields.String()
    status = fields.String()
    items = fields.Nested("OrderItemSchema", many=True)
    created_on = fields.DateTime()
    modified_on = fields.DateTime()