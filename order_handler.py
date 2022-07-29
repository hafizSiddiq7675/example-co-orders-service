import json
from src.exampleco.exampleco.models.database.services import Service, ServiceSchema
from src.exampleco.exampleco.models.database.order_items import OrderItem
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.orders import Order, OrderSchema


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = Session.query(Order).filter(Order.status==Order.STATUS_ACTIVE).all()
    results = orders_schema.dump(orders)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


# pylint: disable=unused-argument
def create_order(event, context):
    """
    this function creates an order in the database
    """
    body = json.loads(event["body"])
    try:
        order = Order(description=body.get("description", None))
        Session.add(order)
        Session.commit()
        for service_id in body.get('services', []):
            order_item = OrderItem(order_id=order.id, service_id=service_id)
            print("order_item", order.id)
            Session.add(order_item)
            Session.commit()
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"success": False, "error": str(e)})}
    response = {"statusCode": 201, "body": json.dumps({"success": True, "message": "Order created"})}
    return response


# pylint: disable=unused-argument
def delete_order(event, context):
    order_id = event['pathParameters']['id']
    print('order_id', order_id)
    instance = Session.query(Order).filter(Order.id == order_id).first()
    if instance:
        instance.status = Order.STATUS_DELETED
        Session.commit()
        response = {"statusCode": 200, "body": json.dumps({"success": True, "message": "Order deleted"})}
    else:
        response = {"statusCode": 400, "body": json.dumps({"success": False, "message": "Not Found"})}
    return response


# pylint: disable=unused-argument
def update_order(event, context):
    order_id = event['pathParameters']['id']
    order = Session.query(Order).filter(Order.id == order_id and Order.status == Order.STATUS_ACTIVE).first()
    if order:
        body = json.loads(event["body"])
        order.description = body.get("description", None)
        Session.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        Session.commit()
        for service_id in body.get('services', []):
            order_item = OrderItem(order_id=order.id)
            Session.add(order_item)
            Session.commit()
        response = {"statusCode": 200, "body": json.dumps({"success": True, "message": "Order updated"})}
    else:
        response = {"statusCode": 400, "body": json.dumps({"success": False, "message": "Not Found"})}
    return response