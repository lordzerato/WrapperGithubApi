import json
from aiokafka import AIOKafkaProducer # type: ignore
from aiokafka.errors import KafkaError # type: ignore
from app.core.config import settings
from app.core.logger import logger
from app.models.types import JSON

KAFKA_SERVER = settings.KAFKA_SERVER
producer: AIOKafkaProducer | None = None

async def kafka_start() -> None:
    """Initialize the Kafka producer."""
    global producer
    try:
        if KAFKA_SERVER:
            producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
            logger.info("Success initialize Kafka producer. Kafka will be enabled.")
        else:
            logger.warning("KAFKA_SERVER not set or missing. Kafka will be disabled.")
    except KafkaError as e:
        logger.warning(f"Failed to initialize Kafka producer: {e}. Kafka will be disabled.")
    if not producer:
        return None
    try:
        await producer.start()
        logger.info("Kafka producer started.")
    except KafkaError as e:
        logger.warning(f"Failed to start Kafka producer: {e}")

async def kafka_stop() -> None:
    """Shutdown the Kafka producer."""
    if not producer:
        return None
    try:
        await producer.stop()
        logger.info("Kafka producer stopped.")
    except KafkaError as e:
        logger.warning(f"Failed to stop Kafka producer: {e}")

async def producer_send(topic: str, value: JSON) -> None:
    """Publish a message to a Kafka topic."""
    if not producer:
        return None
    try:
        await producer.send_and_wait(topic, json.dumps(value).encode('utf-8'))
        logger.info("Publish message successfully")
    except KafkaError as e:
        logger.warning(f"Failed to send message to Kafka: {e}")