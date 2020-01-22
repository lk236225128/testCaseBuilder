from __future__ import print_function
import urllib.parse
from allpairspy import AllPairs
from collections import OrderedDict
import yaml


def get_GET_all_url():
    pass


def get_es_search_result(es, index_name, uri, size):
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


def get_AllPairs(_searched):
    allParameter = OrderedDict()
    for hit in _searched['hits']['hits']:
        status = hit['_source']['status']
        request_method = hit['_source']['method']
        content_type = hit['_source']['content_type']
        http_user_agent = hit['_source']['http_user_agent']
        request_host = hit['_source']['host']

        request_uri = hit['_source']['request_uri']
        request_uri = urllib.parse.unquote(request_uri)
        parameter = OrderedDict(get_GET_parameter_keys(request_uri))
        # 把所有當前路由的參數匯總在allParameter中
        for k, v in parameter.items():
            if k not in allParameter.keys():
                if k not in ['device_id', 'token', 'drivice_id', 'bid', 'mid']:
                    allParameter[k.replace("[]", "")] = v
            else:
                if v[0] not in allParameter[k]:
                    allParameter[k].append(v[0])
    pairsParameters = []
    for i, pairs in enumerate(AllPairs(allParameter)):
        pairsParameters.append(pairs)
    return pairsParameters


def get_GET_parameter_keys(link):
    return urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)


def get_GET_parameter_values():
    pass


def general_yaml(yml_name,conf_name,base_url,variables,teststep):
    dataMap = {
        'config': {
            "name": conf_name,
            "base_url": base_url,
            "variables": variables
        },
        "teststeps": teststep
    }
    f = open(yml_name, "w+", encoding="utf-8")
    yaml.dump(dataMap, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    f.close()


def get_pairs_parameters(parameters):
    allParameters=[]
    for i, pairs in enumerate(AllPairs(parameters)):
        # print("{:2d}: {}".format(i, pairs))
        allParameters.append(pairs)
    return allParameters

def get_teststep(step_name,params,url):
    teststep = {
        "name": step_name,
        "request": {
            "headers": {
                "User-Agent": "iOS 11.4 iPhone7,1 TW-zh-Hant car8891 3.5.0 com.Addcn.car8891"
            },
            "method": "GET",
            "params": params,
            "url": url
        },
        "validate": [{"eq": ["status_code", 200]}],
    }
    return teststep

def get_every_params(k,parameters,step_name,):
    pass

