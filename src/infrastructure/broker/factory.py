from faststream.rabbit import RabbitBroker

from core import settings


def create_rabbit_broker() -> RabbitBroker:
    return RabbitBroker(settings.rabbitmq.dsn)
