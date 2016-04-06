# Copyright (c) 2016 Kyle Isom <coder@kyleisom.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""The api module provides remote access to the CFSSL API."""


import json
import requests

import cfssl.errors as errors


class Client(object):
    """Client provides remote access to a CFSSL server."""

    valid = False

    def __init__(self, remote, ssl=False):
        """
        Initialise a client that will talk to the remote specified as
        an argument.
        """

        if remote == "":
            return
        if ssl:
            if not remote.startswith('https://'):
                remote = 'https://' +  remote
        else:
            if not remote.startswith('http://'):
                remote = 'http://' +  remote
        self.remote = remote
        self.valid = True

    def _endpoint_(self, action):
        """Returns the appropriate endpoint for action."""
        return self.remote + '/api/v1/cfssl/' + action

    def sign(self, certificate_request, profile='', label=''):
        """
        Request the remote CFSSL server sign the certificate request. For
        example,

        {
            "certificate_request": "-----BEGIN CERTIFICATE REQUEST-----\n..."
            "profile": "client",
            "label": ""
        }


        """
        jso = {
            'certificate_request': certificate_request,
            'profile': profile,
            'label': label
        }

        req = requests.post(self._endpoint_('sign'), json=jso)
        response = json.loads(req.content)
        if response[u'success']:
            return response[u'result'][u'certificate']
        else:
            raise errors.ResponseFailure(response[u'errors'][0])

    def genkey(self, certificate_request):
        """
        Request the remote CFSSL server generate a key and CSR. The request
        should be a valid JSON CSR structure. For example,

        {
            "CN": "Test Common Name",
            "names": [
                {
                    "C": "US",
                    "ST": "California",
                    "L": "San Francisco",
                    "O": "CloudFlare, Inc.",
                    "OU": "Systems Engineering"
                },
                {
                    "C": "GB",
                    "ST": "London",
                    "L": "London",
                    "O": "CloudFlare, Inc",
                    "OU": "Systems Engineering"
                }
            ],
            "hosts": [
                "cloudflare.com",
                "www.cloudflare.com",
                "192.168.0.1"
            ],
            "key": {
                "algo": "ecdsa",
                "size": 256
            }
        }

        """
        req = requests.post(self._endpoint_('newkey'), json=certificate_request)
        response = json.loads(req.content)
        if response[u'success']:
            return response[u'result']
        else:
            raise errors.ResponseFailure(response[u'errors'][0])

    def gencert(self, certificate_request):
        """
        Request the remote CFSSL server generate a key, CSR, and certificate.
        The request should be a valid JSON certificate request structure.
        For example,

        {
            "request": {
                "CN": "Test Common Name",
                "names": [
                    {
                        "C": "US",
                        "ST": "California",
                        "L": "San Francisco",
                        "O": "CloudFlare, Inc.",
                        "OU": "Systems Engineering"
                    },
                    {
                        "C": "GB",
                        "ST": "London",
                        "L": "London",
                        "O": "CloudFlare, Inc",
                        "OU": "Systems Engineering"
                    }
                ],
                "hosts": [
                    "cloudflare.com",
                    "www.cloudflare.com",
                    "192.168.0.1"
                ],
                "key": {
                    "algo": "ecdsa",
                    "size": 256
                }
            },
            "profile": "www",
            "label": "external"
        }


        """
        req = requests.post(self._endpoint_('newcert'), json=certificate_request)
        response = json.loads(req.content)
        if response[u'success']:
            return response[u'result']
        else:
            raise errors.ResponseFailure(response[u'errors'][0])

