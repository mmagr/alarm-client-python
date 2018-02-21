# Alarm Manager Python Client

[![License badge](https://img.shields.io/badge/license-GPL-blue.svg)](https://opensource.org/licenses/GPL-3.0)

This library implements an Alarm Manager python client for sending alarms to it
through RabbitMQ.

## How does it work

The client handles the connection and sends a JSON formatted alarm event to the
RabbitMQ instance of Alarm Manager.

### Sending messages to Alarm Manager

Alarms are JSON messages :

```json
{
  "additionalData": {
    "username": "bob",
    "reason": "hell upon us",
    "userid": "1"
  },
  "domain": "AuthenticationError",
  "severity": "Minor",
  "namespace": "dojot.auth",
  "eventTimestamp": 1,
  "primarySubject": {
    "instance_id": "4",
    "module_name": "My beautiful module"
  }
}
```

And we send it through :
```python
client = RabbitMqClientConnection()
client.open(args.host)
alarm = Alarm(  domain="AuthenticationError", namespace="dojot.auth",
                severity=AlarmSeverity.MINOR, timestamp=1,
                description="description to be written")
alarm.add_primary_subject("instance_id", "4")
alarm.add_primary_subject("module_name", "My beautiful module")
alarm.add_additional_data("userid", "1")
alarm.add_additional_data("username", "bob")
alarm.add_additional_data("reason", "hell upon us")
client.send(alarm)
client.close();
```

When no more alarms are to be sent, the connection should be closed using:
```python
client.close();
```
