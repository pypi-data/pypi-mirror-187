# -*- coding: utf-8 -*-
#
#  Copyright 2023 sferriol <s.ferriol@ip2i.in2p3.fr>
import socket


def unused_port():
    """Return an unsued port
    """
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    _, port = sock.getsockname()
    sock.close()
    return port
