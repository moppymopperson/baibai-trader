#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This server watches for changes in log files and sends out updates to
subscribers via web sockets.
"""
import time
import subprocess
import select
import threading
from websocket_server import WebsocketServer
from bitbaibai.utils import build_logger


class TickerServer:

    def __init__(self, filepath):
        self._log = build_logger('server_log', 'server_log.log')
        self.watched_file = filepath
        self._server = WebsocketServer(3000, host='127.0.0.1')
        self._server.set_fn_new_client(self.client_connected)
        self._server.set_fn_client_left(self.client_disconnected)
        self.watch_file(filepath)
        self._log.info('Ticker server running!')
        self._server.serve_forever()

    def client_connected(self, client, _):
        self._log.info('Client connected!')
        self.send_all_lines(client, self.watched_file)

    def client_disconnected(self, client, server):
        self._log.info('Client disconnected!')

    def send_all_lines(self, client, file):
        with open(file, 'r') as f:
            for line in f:
                #self._server.send_message(client, line)
                pass

    def received_messsage(self, client, server, message):
        self._log.info('Server received message: ' + str(message))

    def watch_file(self, filepath):
        self._log.info('Watching file: ' + filepath)
        tail = subprocess.Popen(['tail', '-F', filepath],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        poll = select.poll()
        poll.register(tail.stdout)
        threading.Timer(1.0, self._check_for_new_lines(poll, tail)).start()

    def _check_for_new_lines(self, poll, tail):
        self._log.info('polling')
        if poll.poll(1):
            line = tail.stdout.readline()
            self._log.info('new line!: ' + str(line))
            self._server.send_message_to_all(line)
        time.sleep(1)
        threading.Timer(1.0, self._check_for_new_lines(poll, tail)).start()
