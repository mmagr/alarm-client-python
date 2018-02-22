import json
from collections import OrderedDict
from enum import Enum


class AlarmSeverity(Enum):
    WARNING = 0
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3
    CLEAR = 4


class Alarm(object):

    def __init__(self, domain, severity, timestamp, namespace="", description=""):
        if not isinstance(severity, AlarmSeverity):
            raise ValueError('Invalid severity value, it must be AlarmSeverity')

        self._domain = domain
        self._severity = severity
        self._timestamp = long(timestamp)
        self._namespace = namespace
        self._description = description

        self._primary_subject = dict()
        self._additional_data = dict()

        severity_to_string = {
            AlarmSeverity.WARNING: 'Warning',
            AlarmSeverity.MINOR: 'Minor',
            AlarmSeverity.MAJOR: 'Major',
            AlarmSeverity.CRITICAL: 'Critical',
            AlarmSeverity.CLEAR: 'Clear'
        }

        self._str_severity = severity_to_string[severity]

    @property
    def domain(self):
        return self._domain

    @property
    def severity(self):
        return self._domain

    @property
    def timestamp(self):
        return self._domain

    @property
    def namespace(self):
        return self._domain

    @property
    def description(self):
        return self._domain

    @namespace.setter
    def namespace(self, value):
        self._namespace = value

    @description.setter
    def description(self, value):
        self._description = value

    def add_primary_subject(self, key, value):
        self._primary_subject[key] = value

    def add_additional_data(self, key, value):
        self._additional_data[key] = value

    def get_primary_subject(self, key):
        return self._primary_subject[key]

    def get_additional_data(self, key):
        return self._additional_data[key]

    def remove_primary_subject(self, key):
        if key in self._primary_subject:
            del self._primary_subject[key]

    def remove_additional_data(self, key):
        if key in self._additional_data:
            del self._additional_data[key]

    def serialize(self):
        """
        Alarm JSON format:
        {
            "namespace": "OpenFlow",
            "domain": "SecureChannelDown",
            "primarySubject": {
                "dpid": "012345678",
            },
            "additionalData": {
                "nports": "10"
            },
            "severity": "Critical",
            "eventTimestamp": 1412381203989
        }
        """

        data = OrderedDict()
        data['namespace'] = self._namespace
        data['domain'] = self._domain
        data['primarySubject'] = self._primary_subject
        data['additionalData'] = self._additional_data
        data['severity'] = self._str_severity
        data['eventTimestamp'] = self._timestamp

        return json.dumps(data)
