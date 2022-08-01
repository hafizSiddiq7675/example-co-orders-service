import pytest
from src.exampleco.exampleco.models.database.services import Service, ServiceSchema
from src.exampleco.exampleco.models.database.order_items import OrderItem
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.orders import Order, OrderSchema
from order_handler import update_order
import json


@pytest.fixture()
def order():
    """
    Create inactive order in the database
    """
    order = Order(description="Test", status=Order.STATUS_DELETED)
    Session.add(order)
    Session.commit()
    yield order
    Session.delete(order)


class TestOrders:
    
    def test_order_update_for_existing_order(self, order):
        """
        Test that an order can be updated
        """
        body = json.dumps({"description": "Test", "services": [1]})
        event = {"body": body, "pathParameters": {"id": order.id}}
        response = update_order(event, None)
        assert response.get('statusCode') == 400
        