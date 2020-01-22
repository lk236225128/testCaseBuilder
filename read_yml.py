# -*- coding:utf-8 -*-
import os
import yaml

current_path = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    urlpath = os.path.join(current_path, 'url')
    with open(os.path.join(urlpath, 'uri.yml'), 'r', encoding='UTF-8') as f:
        url = yaml.load(f.read(), Loader=yaml.FullLoader)
        a = set(url["url"])

    with open(os.path.join(urlpath, 'new_uri.yml'), 'r', encoding='UTF-8') as f:
        newurl = yaml.load(f.read(), Loader=yaml.FullLoader)
        b = set(newurl["url"])

    # yamlpath = os.path.join(current_path, 'cases')
    # for root, dirs, files in os.walk(yamlpath):
    #     for filename in files:
    #         with open(os.path.join(yamlpath, filename), 'r', encoding='UTF-8') as f:
    #             temp = yaml.load(f.read(), Loader=yaml.FullLoader)
