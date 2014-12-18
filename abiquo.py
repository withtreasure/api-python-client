import requests

class Abiquo(object):
    def __init__(self, url, auth=None, headers=None):
        self.url = url
        self.auth = auth
        self.headers = {url : headers}
        self.session = requests.session()

    def __getattr__(self, key):      
        try:
            return self.__dict__[key]
        except KeyError:
            self.__dict__[key] = Abiquo(join_url(self.url, key), auth=self.auth)
            return self.__dict__[key]

    def get(self, id=None, params=None, headers=None):
        return self._request('get', self.url if not id else join_url(self.url, id), 
            params=params, headers=headers)

    def post(self, id=None, params=None, headers=None, data=None):
        return self._request('post', self.url if not id else join_url(self.url, id), 
            params=params, headers=headers, data=data)

    def _request(self, method, url, params=None, headers=None, data=None):
        # TODO check status_code
        # TODO return empty?
        # TODO ErrorDto case
        parent_headers = self.headers[url] if url in self.headers else {}

        response = self.session.request(method, 
                                        url, 
                                        auth=self.auth, 
                                        params=params, 
                                        headers=merge_headers(parent_headers, headers), 
                                        data=data)
        if len(response.text) > 0:
            return ObjectDto(response.json(), auth=self.auth)

        return None

class ObjectDto(object):
    def __init__(self, json, auth=None):
        self.json = json
        self.auth = auth

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as ex:
            try:
                return self.json[key]
            except:
                raise ex

    def __len__(self):
        try:
            return len(self.json['collection'])
        except KeyError:
            raise TypeError('object has no len()')

    def __iter__(self):
        try:
            for json in self.json['collection']:
                yield ObjectDto(json, self.auth)
        except KeyError:
            raise TypeError('object is not iterable')

    def __getitem__(self, index):
        try:
            return ObjectDto(self.json['collection'][index], self.auth)
        except KeyError:
            raise TypeError("object has no attribute '__getitem__'")

    def follow(self, rel):
        link = next((link for link in self.json['links'] if link['rel'] == rel), None)
        if not link:
            raise KeyError("link with rel %s not found" % rel)
        return Abiquo(url=link['href'], auth=self.auth, headers={'Accept' : link['type']})

def join_url(*args):
    return "/".join(args)

def merge_headers(x, y):
    if x and y:
        return dict(x + y)
    elif x:
        return x
    elif y:
        return y
    
    return None
