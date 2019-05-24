# BSD 3-Clause License
#
# Copyright (c) 2018, Pruthvi Kumar All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest
import time

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"


class PromWatch(object):
    """
    This is the middleware wired to main executor. This middleware generates prometheus metrics for all PROTON routes.
    """

    def __init__(self):

        self.registry = CollectorRegistry()
        self.requests = Counter(
            'http_total_request',
            'Counter of total HTTP requests',
            ['method', 'path', 'status'],
            registry=self.registry)

        self.request_historygram = Histogram(
            'request_latency_seconds',
            'Histogram of request latency',
            ['method', 'path', 'status'],
            registry=self.registry)

    def process_response(self, req, resp, resource, req_succeeded):
        resp_time = time.time() - req.context['start_time']
        self.requests.labels(method=req.method, path=req.path, status=resp.status).inc()
        self.request_historygram.labels(method=req.method, path=req.path, status=resp.status).observe(resp_time)

    def on_get(self, req, resp):
        """
        Sink for prometheus to collect all logs periodically.
        :param req: Falcon request object
        :param resp: Falcon response object
        :return: Prom logs.
        """
        data = generate_latest(self.registry)
        resp.content_type = 'text/plain; version=0.0.4; charset=utf-8'
        resp.body = str(data.decode('utf-8'))



