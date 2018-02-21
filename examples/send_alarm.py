import argparse
import sys
import logging
from alarmmanager.connection import RabbitMqClientConnection
from alarmmanager.alarm import Alarm, AlarmSeverity
from alarmmanager.connection import LOGGER as CLIENT_LOGGER

__author__ = "Manuel Gavidia"
__copyright__ = "Manuel Gavidia"
__license__ = "GPL-3.0"

def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="DOJOT Alarm publish example")
    parser.add_argument(
        dest="host",
        help="Alarm manager host",
        type=str)
    return parser.parse_args(args)

def main():
    logging.basicConfig(level=logging.ERROR)
    CLIENT_LOGGER.setLevel(logging.DEBUG)
    args = parse_args(sys.argv[1:])
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

if __name__ == "__main__":
    main()
