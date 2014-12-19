# Copyright (C) 2008 Abiquo Holdings S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import httpretty
import json
import unittest

from abiquo.client import Abiquo
from urlparse import parse_qs
from urlparse import urlparse

api = Abiquo(url="http://fake/api", auth=('user', 'name'))

def assert_request(expected_path, method=None, params=None, headers=None, 
    body=None, status=None):
    request = httpretty.last_request()

    if method:
        assert method == request.method
    if params:
        for param, value in params.items():
            assert param in request.querystring and value in request.querystring[param]
    if headers:
        assert all(item in request.headers.items() for item in headers.items())
    if body:
        assert body == request.body

    assert urlparse(request.path).path == expected_path

def register(method, uri, status, body):
    httpretty.register_uri(
        method=method, 
        uri=uri,
        body=body,
        status=status)

class TestClient(unittest.TestCase):
    def test_path_building(self):
        assert api.admin.datacenters.url == 'http://fake/api/admin/datacenters'
        assert api.admin.datacenters('1').url == 'http://fake/api/admin/datacenters/1'
        assert api.admin.datacenters(1).url == 'http://fake/api/admin/datacenters/1'
        assert api('admin', 'datacenters').url == 'http://fake/api/admin/datacenters'
        assert api('admin', 'datacenters', 1).url == 'http://fake/api/admin/datacenters/1'
        assert api.admin().url == 'http://fake/api/admin'

    def test_get(self):
        register('GET', 'http://fake/api/admin/datacenters/1', 200, '{}')
        register('GET', 'http://fake/api/admin/datacenters', 200, '{}')

        api.admin.datacenters.get()
        assert_request('/api/admin/datacenters', method='GET')

        api.admin.datacenters.get(id='1')
        assert_request('/api/admin/datacenters/1', method='GET')

        params = {'p1':'a','p2':'b'}
        api.admin.datacenters.get(id='1', params=params)
        assert_request('/api/admin/datacenters/1', method='GET', params=params)

        api.admin.datacenters.get(params=params)
        assert_request('/api/admin/datacenters', method='GET', params=params)

        headers = {'h1':'a', 'h2':'b'}
        api.admin.datacenters.get(id='1', headers=headers)
        assert_request('/api/admin/datacenters/1', method='GET', headers=headers)

        api.admin.datacenters.get(headers=headers)
        assert_request('/api/admin/datacenters', method='GET', headers=headers)

        api.admin.datacenters.get(id='1', headers=headers, params=params)
        assert_request('/api/admin/datacenters/1', method='GET', headers=headers, params=params)

        api.admin.datacenters.get(params=params, headers=headers)
        assert_request('/api/admin/datacenters', method='GET', headers=headers, params=params)

    def test_delete(self):
        register('DELETE', 'http://fake/api/admin/datacenters/1', 200, '{}')
        register('DELETE', 'http://fake/api/admin/datacenters', 200, '{}')

        api.admin.datacenters.delete()
        assert_request('/api/admin/datacenters', method='DELETE')

        api.admin.datacenters.delete(id='1')
        assert_request('/api/admin/datacenters/1', method='DELETE')

        params = {'p1':'a','p2':'b'}
        api.admin.datacenters.delete(id='1', params=params)
        assert_request('/api/admin/datacenters/1', method='DELETE', params=params)

        api.admin.datacenters.delete(params=params)
        assert_request('/api/admin/datacenters', method='DELETE', params=params)

        headers = {'h1':'a', 'h2':'b'}
        api.admin.datacenters.delete(id='1', headers=headers)
        assert_request('/api/admin/datacenters/1', method='DELETE', headers=headers)

        api.admin.datacenters.delete(headers=headers)
        assert_request('/api/admin/datacenters', method='DELETE', headers=headers)

        api.admin.datacenters.delete(id='1', headers=headers, params=params)
        assert_request('/api/admin/datacenters/1', method='DELETE', headers=headers, params=params)

        api.admin.datacenters.delete(params=params, headers=headers)
        assert_request('/api/admin/datacenters', method='DELETE', headers=headers, params=params)

    def test_post(self):
        register('POST', 'http://fake/api/admin/datacenters', 200, '{}')
        register('POST', 'http://fake/api/admin/datacenters/1', 200, '{}')

        api.admin.datacenters.post()
        assert_request('/api/admin/datacenters', method='POST')

        api.admin.datacenters.post(id='1')
        assert_request('/api/admin/datacenters/1', method='POST')

        params = {'p1':'a','p2':'b'}
        api.admin.datacenters.post(id='1', params=params)
        assert_request('/api/admin/datacenters/1', method='POST', params=params)

        api.admin.datacenters.post(params=params)
        assert_request('/api/admin/datacenters', method='POST', params=params)

        headers = {'h1':'a', 'h2':'b'}
        api.admin.datacenters.post(id='1', headers=headers)
        assert_request('/api/admin/datacenters/1', method='POST', headers=headers)

        api.admin.datacenters.post(headers=headers)
        assert_request('/api/admin/datacenters', method='POST', headers=headers)

        data = json.dumps({'id':1, 'name' : 'test'})
        api.admin.datacenters.post(id='1', data=data)
        assert_request('/api/admin/datacenters/1', method='POST', body=data)

        api.admin.datacenters.post(data=data)
        assert_request('/api/admin/datacenters', method='POST', body=data)

        api.admin.datacenters.post(id='1', data=data, params=params, headers=headers)
        assert_request('/api/admin/datacenters/1', method='POST', params=params, headers=headers, body=data)

        api.admin.datacenters.post(data=data, params=params, headers=headers)
        assert_request('/api/admin/datacenters', method='POST', params=params, headers=headers, body=data)

    def test_put(self):
        register('PUT', 'http://fake/api/admin/datacenters', 200, '{}')
        register('PUT', 'http://fake/api/admin/datacenters/1', 200, '{}')

        api.admin.datacenters.put()
        assert_request('/api/admin/datacenters', method='PUT')

        api.admin.datacenters.put(id='1')
        assert_request('/api/admin/datacenters/1', method='PUT')

        params = {'p1':'a','p2':'b'}
        api.admin.datacenters.put(id='1', params=params)
        assert_request('/api/admin/datacenters/1', method='PUT', params=params)

        api.admin.datacenters.put(params=params)
        assert_request('/api/admin/datacenters', method='PUT', params=params)

        headers = {'h1':'a', 'h2':'b'}
        api.admin.datacenters.put(id='1', headers=headers)
        assert_request('/api/admin/datacenters/1', method='PUT', headers=headers)

        api.admin.datacenters.put(headers=headers)
        assert_request('/api/admin/datacenters', method='PUT', headers=headers)

        data = json.dumps({'id':1, 'name' : 'test'})
        api.admin.datacenters.put(id='1', data=data)
        assert_request('/api/admin/datacenters/1', method='PUT', body=data)

        api.admin.datacenters.put(data=data)
        assert_request('/api/admin/datacenters', method='PUT', body=data)

        api.admin.datacenters.put(id='1', data=data, params=params, headers=headers)
        assert_request('/api/admin/datacenters/1', method='PUT', params=params, headers=headers, body=data)

        api.admin.datacenters.put(data=data, params=params, headers=headers)
        assert_request('/api/admin/datacenters', method='PUT', params=params, headers=headers, body=data)

    def test_no_json_response(self):
        register('POST', 'http://fake/api/admin/racks', 200, '<dc></dc>')
        sc, dto = api.admin.racks.post()
        assert_request('/api/admin/racks', method='POST')
        assert sc == 200
        assert dto == None

    def test_parent_headers(self):
        register('POST', 'http://fake/api', 200, '{}')

        cli = Abiquo(url="http://fake/api", auth=('user', 'name'), headers={'h1':'a'})

        cli.post()
        assert_request('/api', method='POST', headers={'h1':'a'})

        cli.post(headers={'h1':'c'})
        assert_request('/api', method='POST', headers={'h1':'c'})

        cli.post(headers={'h2':'b'})
        assert_request('/api', method='POST', headers={'h1':'a', 'h2':'b'})

        cli.post(headers={'h1':'c', 'h2':'b'})
        assert_request('/api', method='POST', headers={'h1':'c', 'h2':'b'})

if __name__ == '__main__':
    httpretty.enable()
    unittest.main()
    httpretty.disable()
