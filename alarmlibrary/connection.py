import logging
import pika
import json
from alarmlibrary.alarm import Alarm
from alarmlibrary.exceptions import ConnectionClosed, InvalidAlarm, AuthenticationError, AlarmManagerException

LOGGER = logging.getLogger(__name__)

# Exchange hard-coded declared as durable
DEFAULT = {
    'EXCHANGE': 'alarms.exchange',
    'EXCHANGE_TYPE': 'direct',
    'ROUTING_KEY': 'alarms',
    'HOST': 'localhost',
    'PORT': 5672,
    'USER': 'guest',
    'PASSWORD': 'guest'
}


class RabbitMqClientConnection(object):
    def __init__(self, exchange=DEFAULT['EXCHANGE'], exchange_type=DEFAULT['EXCHANGE_TYPE'],
                 default_routing_key=DEFAULT['ROUTING_KEY']):
        self._exchange = exchange
        self._exchange_type = exchange_type
        self._default_routing_key = default_routing_key
        self._connection = None
        self._channel = None

    def open(self, host=DEFAULT['HOST'], port=DEFAULT['PORT'],
             user=DEFAULT['USER'], password=DEFAULT['PASSWORD']):
        try:
            LOGGER.debug("Trying to connect to host=%s, port=%d, user=%s, password=%s",
                         host, port, user, password)
            credentials = pika.PlainCredentials(user, password)
            parameters = pika.ConnectionParameters(host, port, '/', credentials)
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self._exchange,
                                           exchange_type=self._exchange_type,
                                           durable=True)
        except pika.exceptions.ProbableAuthenticationError:
            raise AuthenticationError("Invalid credentials: user=%s passwd=%s" % (user, password))
        except pika.exceptions.ConnectionClosed:
            raise ConnectionClosed("Could not connect to %s:%s", )
        except Exception as ex:
            LOGGER.error(ex.message)
            raise AlarmManagerException(ex.message)

    def is_open(self):
        return self._channel.is_open and self._connection.is_open

    def close(self):
        if self._channel.is_open:
            self._channel.close()
        if self._connection.is_open:
            self._connection.close()

    def send(self, alarm, routing_key=None):
        if self._connection.is_open and self._channel.is_open:
            if isinstance(alarm, Alarm):
                if not routing_key:
                    routing_key = self._default_routing_key
                message = alarm.serialize()
                parsed = json.loads(message)
                LOGGER.debug("Sending : exchange=%s routingkey=%s\nalarm= %s",
                             self._exchange, routing_key,
                             json.dumps(parsed, indent=2))
                self._channel.basic_publish(exchange=self._exchange,
                                            routing_key=routing_key,
                                            body=message)
            else:
                raise InvalidAlarm("Invalid alarm type, it must be Alarm")
        else:
            raise ConnectionClosed("Connection closed")
