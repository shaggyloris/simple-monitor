#!/usr/bin/env python

import os
import subprocess
import platform
import socket
from datetime import datetime

from .. import db
from ..models import Hosts


def check_host(host):
    """
    Function to check a specific host when one is added to the database.
    """
    fqdn, port = host
    if port is None:
        test = ping_host(fqdn)
    else:
        test = check_sock(fqdn, port)
    timestamp = datetime.now()
    return test, timestamp


def check_hosts():
    """
    Function to check all hosts
    
    If host is up returns true, else will return false
    """
    hosts = Hosts.query.all()
    for host in hosts:
        fqdn = host.fqdn
        port = host.port
        if port is not None:
            test = check_sock(fqdn, port)
        else:
            test = ping_host(fqdn)
        timestamp = datetime.now()
        host.status = test
        host.last_checked = timestamp
        db.session.add(host)


def ping_host(hostname):
    os_type = platform.platform()
    with open(os.devnull, 'w'):
        try:
            if 'Windows' in os_type:
                response = subprocess.check_output(['ping', '-n', '1', hostname],
                                                   stderr=subprocess.STDOUT,
                                                   universal_newlines=True
                                                   )
            else:
                response = subprocess.check_output(['ping', '-c', '1', hostname],
                                                   stderr=subprocess.STDOUT,
                                                   universal_newlines=True
                                                   )
            if 'host unreachable' in response:
                is_up = False
            else:
                is_up = True
        except subprocess.CalledProcessError:
            is_up = False
    return is_up


def check_sock(hostname, port):
    try:
        r = socket.create_connection((hostname, port), 2)
    except socket.error:
        return False
    if r:
        return True


if __name__ == '__main__':
    check_hosts()
