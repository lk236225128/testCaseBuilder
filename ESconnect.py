from __future__ import print_function
from elasticsearch import Elasticsearch
from collections import OrderedDict
from elasticsearch.helpers import bulk
import re
from urllib.parse import urlparse
import urllib.parse
import utils
from allpairspy import AllPairs
import os
import yaml

current_path = os.path.abspath(os.path.dirname(__file__))


class ElasticObj(object):

    def __init__(self, index_name, ip="220.228.175.145"):
        '''

        :param index_name: 索引名称
        '''
        self.index_name = index_name
        # self.index_type = index_type
        # self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)
        self.es = Elasticsearch([ip], port=9200)
        self.urlpath = os.path.join(current_path, 'url')

    def get_es_log_uri(self, es, index_name, size):
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "host.keyword": {
                                    "value": "www.8891.com.tw"
                                }
                            }
                        },
                        {
                            "exists": {
                                "field": "request_uri.keyword"
                            }
                        },
                        {"prefix": {
                            "request_uri.keyword": {
                                "value": "/api/"
                            }
                        }}
                    ]
                }
            },
            "collapse": {
                "field": "request_uri.keyword"
            },
            "script_fields": {
                "real_request_uri": {
                    "script": {
                        "lang": "painless",
                        "source": "String str = doc['request_uri.keyword'].value;int pos = str.indexOf('?');return pos > 0 ? str.substring(0,pos) : str;"
                    }
                }
            },
            "sort": [
                {
                    "@timestamp": {
                        "order": "asc"
                    }
                },
                {
                    "request_uri.keyword": {
                        "order": "asc"
                    }
                }
            ],
            "size": size
        }
        searched = es.search(index=index_name, body=body)
        return searched

    def get_base_url(self):
        with open(os.path.join(self.urlpath, 'uri.yml'), 'r', encoding='UTF-8') as f:
            url = yaml.load(f.read(), Loader=yaml.FullLoader)
            baseurl = set(url["url"])
        return baseurl

    def general_new_url(self, new_uri):
        dataMap = {
            'url': new_uri
        }
        f = open(os.path.join(self.urlpath, 'new_uri.yml'), "w+", encoding="utf-8")
        yaml.dump(dataMap, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        print("新增接口生成success")
        f.close()

    def add_new_url(self, newurl):
        baseurl = self.get_base_url()
        add_url = newurl - baseurl
        self.general_new_url(list(add_url))

    def get_new_url(self, _searched):
        newurl = set()
        for hit in _searched['hits']['hits']:
            real_request_uri = hit['fields']['real_request_uri']
            newurl.add(real_request_uri[0])
        return newurl

    def get_GET_parameter_keys(self, link):
        return urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)

    def get_es_search_result(self, es, index_name, uri, size):
        body = {
            "query": {
                "match_phrase": {
                    # "request_uri": "/api/v1/history/list"
                    "request_uri": uri
                }
            },
            "size": size,
            "sort": [
                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }
            ]
        }
        _searched = es.search(index=index_name, body=body)
        return _searched

    def get_allParameter(self, _searched):
        allParameter = OrderedDict()
        for hit in _searched['hits']['hits']:
            status = hit['_source']['status']
            request_method = hit['_source']['method']
            content_type = hit['_source']['content_type']
            http_user_agent = hit['_source']['http_user_agent']
            request_host = hit['_source']['host']

            request_uri = hit['_source']['request_uri']
            request_uri = urllib.parse.unquote(request_uri)
            parameter = OrderedDict(self.get_GET_parameter_keys(request_uri))
            # 把所有當前路由的參數匯總在allParameter中
            for k, v in parameter.items():
                if k not in allParameter.keys():
                    if k not in ['device_id', 'token', 'drivice_id', 'bid', 'mid']:
                        allParameter[k.replace("[]", "")] = v
                else:
                    if v[0] not in allParameter[k]:
                        allParameter[k].append(v[0])
        print(allParameter)
        return allParameter

    def get_AllPairs(self, _searched):
        allParameter = self.get_allParameter(_searched)
        pairsParameters = []
        for i, pairs in enumerate(AllPairs(allParameter)):
            pairsParameters.append(pairs)
        return pairsParameters

    def get_data_by_body(self, uri, size):
        _searched = self.get_es_search_result(self.es, self.index_name, uri, size)
        return _searched
        # print("_searched", _searched)
        # print(self.get_allParameter(_searched))
        # print(self.get_AllPairs(_searched))

    def get_url_by_ES(self, size):
        _searched = self.get_es_log_uri(self.es, self.index_name, size)
        return _searched


if __name__ == '__main__':
    size = 100
    obj = ElasticObj("access-2019.12.25")
    _searched = obj.get_url_by_ES(size)
    newurl = obj.get_new_url(_searched)
    obj.add_new_url(newurl)







    # uri = "/api/v3/app/update/"

    # _searched = obj.get_data_by_body(uri,size)
    # print(_searched)
    # print(obj.get_allParameter(_searched))


    # url = 'https://c.8891.com.tw/api/v1/history/list?api=2.10.1&device_id=025c15c8-cfb9-47d8-bc7f-ad621d63e3b7&token=36b566cd081f09176b316bc410&ats=1577259119&device_id=025c15c8-cfb9-47d8-bc7f-ad621d63e3b7'
    # result = urllib.parse.urlsplit(url)
    # result=utils.get_GET_parameter_keys(url)
    # print(utils.get_GET_parameter_keys(url))
    # print(result.keys())
    # print(result.values())
    # for i in result.keys():
    #     print(i,result[i][0])
    # parameters = OrderedDict({'api': ['4.3', '3.7', '2.10.1'], 'bid': ['24'],
    #                           'mid': ['10518'],
    #                           'year': ['2014-2015'], 'touch': ['1'],
    #                           'page': ['1', '6(null)', '2(null)', '107'], 'sort': ['top', 'price-desc'],
    #                           'price': ['-10']})
    # print(utils.get_AllPairs(parameters))
