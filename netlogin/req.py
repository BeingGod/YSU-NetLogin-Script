import urllib.request
import urllib.parse

# 封装post请求
def post(url,headers={},data={}):
    data = bytes(urllib.parse.urlencode(data),encoding='utf-8')
    request = urllib.request.Request(url,headers=headers,data=data)
    response = urllib.request.urlopen(request)
    return response

# 封装get请求
def get(url,headers={}):
    request = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(request)
    return response