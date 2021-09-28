# coding:utf-8

import datetime
import codecs
import requests
import os
import time
from pyquery import PyQuery as pq


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


def scrape(language, since):
    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}?since={since}'.format(language=language, since=since)
    r = requests.get(url, headers=HEADERS)
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
        url = "https://github.com" + url
        # ownerImg = i("p.repo-list-meta a img").attr("src")
        # print(ownerImg)
        result.add(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))
    return result


def job():
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'trending.md'.format(date=strdate)

    # create markdown file
    createMarkdown(strdate, filename)

    r = {}
    for lang in "python go javascript nim lua c".split(" "):
    # for lang in "python".split(" "):
        tset = set()
        # for since in "daily".split(" "):
        for since in "monthly weekly daily".split(" "):
            print(lang, since)
            tset.update(scrape(lang, since))
            r[lang] = tset
    from pprint import pprint
    pprint(r)

    with open(filename, 'w') as f:
        f.write("## " + strdate + "\n")
        for language, v in r.items():
            f.write('\n#### {language}\n'.format(language=language))
            for i in v:
                f.write(i)


if __name__ == '__main__':
    job()
