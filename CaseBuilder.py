# -*- coding: utf-8 -*-
import yaml
import utils
from collections import OrderedDict
# -*- coding:utf-8 -*-
import os
import yaml
from allpairspy import AllPairs
from ESconnect import ElasticObj

current_path = os.path.abspath(os.path.dirname(__file__))


class CaseBuilder():
    # 生成正交表用例參數組合
    def get_pairs_parameters(self, parameters):
        allParameters = []
        for i, pairs in enumerate(AllPairs(parameters)):
            allParameters.append(pairs)
        return allParameters

    # httprunner用例步骤
    def general_teststep(self, step_name, params, url):
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

    # httprunner用例模板
    def general_template(self, yml_name, conf_name, base_url, variables, teststep):
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

    # 生成httprunner用例文件
    def general_yaml(self, yamlpath, casepath):
        for root, dirs, files in os.walk(yamlpath):
            for filename in files:
                with open(os.path.join(yamlpath, filename), 'r', encoding='UTF-8') as f:
                    temp = yaml.load(f.read(), Loader=yaml.FullLoader)
                ymlcase_name = os.path.join(casepath, 'case_' + filename)
                conf_name = temp["conf_name"]
                base_url = temp["base_url"]
                url = temp["url"]
                variables = {}
                teststeps = []

                # 根據正交參數組合生成用例
                parameters = OrderedDict(temp["parameters"])
                pairs_parameters = self.get_pairs_parameters(parameters)
                for i in pairs_parameters:
                    params = {}
                    step_name = temp["step_name"]
                    for k in parameters.keys():
                        params[k] = getattr(i, k)
                        step_name += k + ":" + params[k] + " "
                    step = self.general_teststep(step_name, params, url)
                    print(params)
                    teststeps.append(step)
                print(teststeps)
                if teststeps == []:
                    teststeps = {
                        "name": conf_name,
                        "request": {
                            "headers": {
                                "User-Agent": "iOS 11.4 iPhone7,1 TW-zh-Hant car8891 3.5.0 com.Addcn.car8891"
                            },
                            "method": "GET",
                            "params": '',
                            "url": url
                        },
                        "validate": [{"eq": ["status_code", 200]}],
                    }
                self.general_template(ymlcase_name, conf_name, base_url, variables, teststeps)

    # 新增接口配置模板
    def general_source_template(self, yml_name, base_url, url, parameters, yamlpath):
        dataMap = {
            'conf_name': '',
            'base_url': base_url,
            'url': url,
            'step_name': '',
            "parameters": parameters,
        }
        f = open(os.path.join(yamlpath, yml_name), "w+", encoding="utf-8")
        yaml.dump(dataMap, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        f.close()

    # 生成新增接口配置文件
    def general_new_source_data(self, yamlpath, urlpath):
        base_url = "https://www.8891.com.tw"
        parameters = []
        with open(os.path.join(urlpath, 'new_uri.yml'), 'r', encoding='UTF-8') as f:
            url = yaml.load(f.read(), Loader=yaml.FullLoader)
            new_source_data = set(url["url"])
        for i in new_source_data:
            # print(new_source_data)
            doc_name = i.replace('/', '') + '.yml'
            es = ElasticObj("access-2019.12.25")
            _searched = es.get_data_by_body(i, 1)
            keys = dict(es.get_allParameter(_searched))
            # print(i, keys)
            self.general_source_template(doc_name, base_url, i, keys, yamlpath)


if __name__ == '__main__':
    yamlpath = os.path.join(current_path, 'source_data')
    newcasepath = os.path.join(current_path, 'new_source_data')
    casepath = os.path.join(current_path, 'cases')
    urlpath = os.path.join(current_path, 'url')
    builder = CaseBuilder()
    # 生成未覆蓋的接口配置文件
    # builder.general_new_source_data(newcasepath, urlpath)

    # 生成用例文件
    builder.general_yaml(yamlpath, casepath)
    # builder.general_yaml(newcasepath, casepath)




















    # yamlpath = os.path.join(current_path, 'source_data')
    # casepath = os.path.join(current_path, 'cases')
    # for root, dirs, files in os.walk(yamlpath):
    #     for filename in files:
    #         with open(os.path.join(yamlpath, filename), 'r', encoding='UTF-8') as f:
    #             temp = yaml.load(f.read(), Loader=yaml.FullLoader)
    #         ymlcase_name = os.path.join(casepath, 'case_' + filename)
    #         conf_name = temp["conf_name"]
    #         base_url = temp["base_url"]
    #         variables = {}
    #         url = temp["url"]
    #         parameters = OrderedDict(temp["parameters"])
    #         teststeps = []
    #         pairs_parameters = utils.get_pairs_parameters(parameters)
    #         for i in pairs_parameters:
    #             params = {}
    #             step_name = temp["step_name"]
    #             for k in parameters.keys():
    #                 params[k] = getattr(i, k)
    #                 step_name += k + ":" + params[k] + " "
    #             step = utils.get_teststep(step_name, params, url)
    #             print(params)
    #             teststeps.append(step)
    #         print(teststeps)
    #         utils.general_yaml(ymlcase_name, conf_name, base_url, variables, teststeps)

    # with open("newtree.yaml", "rt", encoding="utf-8") as in_file:
    #     yaml.dump(dataMap, in_file)

    # f = open('newtree.yaml', "wt", encoding="utf-8")
    # yaml.dump(dataMap, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    # f.close()
    #
    # conf_name = "首页-獲取最新出售和嚴選"
    # base_url = "https://www.8891.com.tw"
    # variables = {}
    # url = "/api/v3/Home/autos"
    # parameters = OrderedDict({'api': ['3.6', '3.7', '3.8', '4.1', '4.2', '4.3'],
    #                           'filter': ["recently", 'topdealer', 'audiOrgani'],
    #                           })
    # teststeps = []
    # ap = utils.test_parameters(parameters)
    # for i in ap:
    #     params = {}
    #     step_name = "/api/v3/Home/autos首页-"
    #     for k in parameters.keys():
    #         params[k] = getattr(i, k)
    #         step_name += k + ":" + params[k]+" "
    #     step = utils.get_teststep(step_name, params, url)
    #     print(params)
    #     teststeps.append(step)
    # print(teststeps)
    # utils.general_yaml(conf_name, base_url, variables, teststeps)
    #
    # conf_name = "列表頁-獲取物件列表"
    # base_url = "https://www.8891.com.tw"
    # variables = {}
    # url = "/api/v3/newAutos/getList"
    # parameters = OrderedDict({'api': ['3.6', '3.7', '3.8', '4.1', '4.2', '4.3'],
    #                           'sort': ['', 'recently', 'topdealer', 'audiOrgani'],
    #                           'bid': ['', '27'],
    #                           'mid': ['', '9160'],
    #                           'price': ['', '-25', '25-35', '35-50', '50-100', '100-'],
    #                           'feature': ['', 'is_audit', 'is_report', 'is_check', 'is_week', 'is_video'],
    #                           'region': ['', '1'],
    #                           'orgIds': ['', '1'],
    #                           'role': ['', '1'],
    #                           'gas': ['', '-1100', '1100-1600', '1600-1800', '1800-2000', '2000-2400', '2400-3500',
    #                                   '3500-'],
    #                           'tab': ['', '0', '1', '2', '3'],
    #                           'autoTypes': ['', '1', '2', '3', '6', '5'],
    #                           'year': ['', '2019-2020', '2018-2019', '2017-2018', '2015-2017', '2012-2015',
    #                                    '1970-2012'],
    #                           'door': ['', '0', '1', '2', '3', '4'],
    #                           'chair': ['', '2', '3', '4', '5', '6', '7', '8'],
    #                           'color': ['', '0', '1', '2', '3', '4', '5', '8', '9', '10', '11', '13', '15'],
    #                           'fuel': ['', '0', '1', '2', '3', '4'],
    #                           'drive': ['', '2', '4'],
    #                           'topdealer': ['', '1', '0'],
    #                           'active': ['', '2019YearEnd'],
    #                           'page': ['', '1', '2'],
    #                           })
    # teststeps = []
    # ap = utils.test_parameters(parameters)
    # for i in ap:
    #     params = {}
    #     step_name = "/api/v3/newAutos/getList列表頁-"
    #     for k in parameters.keys():
    #         params[k] = getattr(i, k)
    #         step_name += k + ":" + params[k] + " "
    #     step = utils.get_teststep(step_name, params, url)
    #     print(params)
    #     teststeps.append(step)
    # print(teststeps)
    # utils.general_yaml(conf_name, base_url, variables, teststeps)

    # conf_name = "車行列表-獲取車行列表"
    # base_url = "https://www.8891.com.tw"
    # variables = {}
    # url = "/api/v3/Shop/getList"
    # parameters = OrderedDict({'api': ['3.6', '3.7', '3.8', '4.1', '4.2', '4.3'],
    #                           'page': ['','1', '2'],
    #                           'limit': ['','10'],
    #                           'sort': ['','distance-asc'],
    #                           'region': ['','1','3'],
    #                           'topdealer': ['','1', '0'],
    #                           'active': ['','2019YearEnd'],
    #                           'key':['','SUM'],
    #                           'lat': ['23.122'],
    #                           'lng': ['188.123'],
    #                           })
    # teststeps = []
    # ap = utils.test_parameters(parameters)
    # for i in ap:
    #     params = {}
    #     step_name = "/api/v3/Shop/getList車行列表頁-"
    #     for k in parameters.keys():
    #         params[k] = getattr(i, k)
    #         step_name += k + ":" + params[k] + " "
    #     step = utils.get_teststep(step_name, params, url)
    #     print(params)
    #     teststeps.append(step)
    # print(teststeps)
    # utils.general_yaml(conf_name, base_url, variables, teststeps)
