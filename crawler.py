#!/usr/bin/env python3
# encoding: utf-8
"""
@author: Daniel Fuchs

CS3001: Data Science - Extra Homework: Web Crawler
"""

from urllib import request as reqs
import re
import bs4
import time
import random
import hashlib


def crawl(root_urls, crawl_limit=10):
    url_counter = 0
    VISITED = set()
    FRONTIER = set()
    DISCOVERED = set()
    regex_mst = re.compile(".*mst\.edu.*")

    for root in root_urls:
        FRONTIER.add(root)

    while FRONTIER and crawl_limit > url_counter:
        target_url = FRONTIER.pop()
        VISITED.add(target_url)
        url_counter += 1

        print("Now crawling %s..." % target_url)

        try:
            full_request = reqs.Request(
                target_url,
                data=None,
                headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36' }
            )
            response = reqs.urlopen(full_request)
        except:
            print('!! Could not access url %s' % target_url)
            continue

        if response.info().get('Content-Type')[:9] == 'text/html':
            data = response.read().decode()
            output_file = open('pages/' + hashlib.md5(data.encode('utf-8')).hexdigest() + '.html', 'w+')
            output_file.write(data)
            output_file.close()
            soup = bs4.BeautifulSoup(data, 'lxml')
            for link in soup.find_all('a'):
                joined_link = reqs.urljoin(target_url, link.get('href'))
                if str(joined_link).startswith('http') and \
                   regex_mst.match(joined_link) and \
                   joined_link not in VISITED and \
                   joined_link not in FRONTIER and \
                   joined_link not in DISCOVERED:
                        DISCOVERED.add(joined_link)
            FRONTIER = FRONTIER.union(DISCOVERED)
            DISCOVERED.clear()
            time.sleep(random.randrange(3, 7))


if __name__ == '__main__':
    root = {'https://www.mst.edu'}
    crawl(root, 10)
