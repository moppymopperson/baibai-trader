#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A dummy market and server that always returns the same price
"""
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests

from .Authenticator import Authenticator
from ..PriceSample import PriceSample

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if 'current_price' in self.path:
            self.wfile.write('{"price":100}'.encode('utf_8'))

        if 'balance' in self.path:
            self.wfile.write('{"balance": 1000'.encode('utf_8'))

        if 'holdings' in self.path:
            self.wfile.write('{"holdings": 5'.encode('utf_8'))


class DummyAuthenticator(Authenticator):
    
    server_process = None

    def start_server(self):
        # In the new process __name__ == "__main__". See bottom of file.
        print('Starting server at http://localhost:8080')
        command = 'python -m bitbaibai.Markets.DummyAuthenticator'
        self.server_process = os.popen(command)

    def stop_server(self):
        print('Stopping server')
        if self.server_process is not None:
            self.server_process.kill()

    def target_currency(self):
        return "XBT"

    def price_currency(self):
        return "USD"

    def get_account_balance(self):
        r = requests.get('http://localhost:8080/balance')
        return r.json()['balance']

    def get_holdings(self):
        r = requests.get('http://localhost:8080/holdings')
        return r.json()['holdings']

    def get_current_price(self):
        r = requests.get('http://localhost:8080/current_price')
        price = r.json()['price']
        return PriceSample(price, datetime.now(), 
                           self.target_currency(), 
                           self.price_currency())

    def buy(self):
        pass

    def sell(self):
        pass

# When this file is run as a script instead of loaded as module, start server
if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Starting server at http://localhost:8080')
    server.serve_forever()