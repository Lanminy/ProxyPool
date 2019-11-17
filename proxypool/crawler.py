#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from lxml import etree

from proxypool.utils import get_page


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_kdaili(self, page_count=5):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            time.sleep(1)
            html = get_page(url)
            if html:
                html = etree.HTML(html)
                tr_list = html.xpath('//div[@id="list"]/table/tbody/tr')
                for tr in tr_list:
                    ip = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    proxy = ':'.join([ip, port])
                    yield proxy

    def crawl_88ip(self, page_count=5):
        start_url = 'http://www.89ip.cn/index_{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            if html:
                html = etree.HTML(html)
                tr_list = html.xpath('//table[@class="layui-table"]/tbody/tr')
                for tr in tr_list:
                    ip = tr.xpath('./td[1]/text()')[0].strip()
                    port = tr.xpath('./td[2]/text()')[0].strip()
                    proxy = ':'.join([ip, port])
                    yield proxy
