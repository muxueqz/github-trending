# coding:utf-8

import marshal
import datetime
import requests
import os
from time import sleep, time
from pyquery import PyQuery as pq
from random import randrange


def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def createMarkdown(date, filename):
    with open(filename, 'w') as f:
        f.write("## " + date + "\n")

# github_site = 'https://github.com'
github_sites = ['https://github.com.cnpmjs.org',
    'https://hub.fastgit.org'
]
sleep_time = 3

def scrape(language, since):
    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }
    random_nodeid = randrange(len(github_sites))
    github_site = github_sites[random_nodeid]

    url = '{github_site}/trending/{language}?since={since}'.format(
        language=language, since=since, github_site=github_site)
    r = requests.get(url, headers=HEADERS)
    print(github_site, r.status_code)
    assert r.status_code == 200
    
    d = pq(r.content)
    items = d('div.Box article.Box-row')

    result = set()
    # codecs to solve the problem utf-8 codec like chinese

    for item in items:
        i = pq(item)
        title = i(".lh-condensed a").text()
        owner = i(".lh-condensed span.text-normal").text()
        description = i("p.col-9").text()
        url = i(".lh-condensed a").attr("href")
        # url = github_site + url
        url = 'https://github.com' + url
        # ownerImg = i("p.repo-list-meta a img").attr("src")
        # print(ownerImg)
        result.add(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))
    return result


def job():
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'trending.md'.format(date=strdate)

    cache_file = './scraper.cache'
    try:
        with open(cache_file, 'rb') as _fd:
            cache = marshal.load(_fd)
    except:
        cache = {}
    now_timestamp = time()

    langs = "python go javascript nim lua c c++ coffeescript crystal cython rust shell zig swift".split(" ")
    # langs = "coffeescript crystal cython rust shell zig".split(" ")
    r = {}
    # create markdown file
    with open(filename, 'a') as f:
        f.write("## " + strdate + "\n")

        for lang in langs:
            tset = set()
            for since in "monthly weekly daily".split(" "):
                print(lang, since)
                count = 0
                while count < 10:
                    try:
                        tset.update(scrape(lang, since))
                        count = 666
                    except:
                        pass
                    count += 1

                r[lang] = tset
            f.write('\n#### {language}\n'.format(language=lang))
            for i in tset:
                if now_timestamp - cache.get(i, 0) > 60 * 60 * 24 * 30:
                    f.write(i)
                    cache[i] = now_timestamp
            f.flush()
            sleep(sleep_time)
    from pprint import pprint
    pprint(r)
    with open(cache_file, 'wb') as _fd:
        marshal.dump(cache, _fd)


if __name__ == '__main__':
    job()
