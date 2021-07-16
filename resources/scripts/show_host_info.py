#!/usr/bin/python3
"""
.. _header1:
.. _header2:
show_host_info.py

Introduction
------------
This is the documentation for the script in reStructuredText format.

Usage:
------
.. argparse::
   :module: show_host_info
   :func: get_argument_parser
   :prog: show_host_info
"""

import argparse
import logging
import platform
import re
import socket
import sys
import subprocess

import json

__version_info__ = ('1', '0', '1')
__version__ = ".".join(__version_info__)

def get_argument_parser():
    """This function returns the argument parser"""

    description = ('This is a tool to show host information')
    argument_parser = argparse.ArgumentParser(description=description)

    argument_parser.add_argument('--version', '-v', action='version',
                                 version=__version__,
                                 help='Prints the version number.')
    argument_parser.add_argument('--version-json', action='version',
                                 version="{\"script\":\"%(prog)s\", \"version\":\""+__version__+"\"}",
                                 help='Prints the version number in json format.')
    argument_parser.add_argument('--logLevel', '-l', 
                                 choices=["fatal", "error", "warn", "info", "debug"],
                                 default="info", 
                                 help=('The logging level.'))

    return argument_parser

def fibonacci(n):
    """ Function for nth fibonacci, space optimized"""
    a = 0
    b = 1
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return 0
    elif n == 1:
        return b
    else:
        for i in range(1, n):
            c = a + b
            a = b
            b = c
        return b
        
def get_parsed_arguments(test_args=None):
    """Get the parsed arguments"""

    argument_parser = get_argument_parser()

    if test_args:
        return argument_parser.parse_args(test_args)
    else:
        return argument_parser.parse_args()


def exec_and_capture_output(command):
    """Execute a command and capture stdout."""

    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode(sys.stdout.encoding)


def get_ip_addresses():
    """Get the ip addresses of the current host."""

    ipaddresses = []
    try:
        for line in exec_and_capture_output(['ip', 'a']).split("\n"):
            match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ipaddresses.append(match.group(1))
    except SystemExit:
        raise
    except KeyboardInterrupt:
        raise
    except:
        ipaddresses.append("Could not determine ip address.")

    return ipaddresses


def _set_log_level(args):
    """Sets the logging level."""

    log_level = "info"
    if 'logLevel' in args:
        log_level = args.logLevel

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ]
    )

    if log_level.lower() == "fatal":
        logging.getLogger().setLevel(logging.CRITICAL)
    elif log_level.lower() == "error":
        logging.getLogger().setLevel(logging.ERROR)
    elif log_level.lower() == "warn":
        logging.getLogger().setLevel(logging.WARNING)
    elif log_level.lower() == "debug":
        logging.getLogger().setLevel(logging.DEBUG)
    else :
        logging.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':

    args = get_parsed_arguments()
    _set_log_level(args)

    hostname = socket.getfqdn()
    interfaces = get_ip_addresses()

    print("------------------------------------")
    print("Hostname: " + hostname)
    print("Platform: " + platform.platform())
    print("Interfaces:")
    for interface in interfaces:
        print(f"   {interface}")