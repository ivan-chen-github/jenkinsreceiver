import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime
import json
from pykafka import KafkaClient

#functions here
def listHouse(body):
    """ Received a new house listing """

    trace = str(uuid.uuid4())
    body['trace_id'] = trace
    logger.debug("Received event listHouse request with a trace id of " + trace)

    # url = app_config["post_list"]["url"]
    # r = requests.post(url, json = body)

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = { "type": "listHouse",
        "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


    # logger.debug(f"Returned event listhouse response (Id: {trace}) with status {r.status_code}")

    return NoContent, 201

def bookHouse(body):
    """ Receives a booking """

    trace = str(uuid.uuid4())
    body['trace_id'] = trace
    logger.debug("Received event bookHouse request with a trace id of " + trace)
    
    # url = app_config["post_book"]["url"]
    # r = requests.post(url, json = body)

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = { "type": "bookHouse",
        "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


    # logger.debug(f"Returned event bookHouse response (Id: {trace}) with status {r.status_code}")

    return NoContent, 201

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)