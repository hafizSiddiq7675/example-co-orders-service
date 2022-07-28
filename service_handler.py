import json
from src.exampleco.exampleco.models.database import Session
from src.exampleco.exampleco.models.database.services import Service, ServiceSchema


def get_service(service_id):
    services_schema = ServiceSchema(many=False)
    service = Session.query(Service).filter(Service.id == service_id).first()
    results = services_schema.dump(service)
    return results


def get_services():
    services_schema = ServiceSchema(many=True)
    services = Session.query(Service).all()
    results = services_schema.dump(services)
    return results


# pylint: disable=unused-argument
def get_service_by_id(event, context):
    """Get a service by id"""
    service_id = event['pathParameters']['id']
    results = get_service(service_id)
    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


# pylint: disable=unused-argument
def get_all_services(event, context):
    """ Get All Services from the database """
    results = get_services()
    response = {"statusCode": 200, "body": json.dumps(results)}

    return response
