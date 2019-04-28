import re
import sys
import os
import json

import ast
import requests

PROG = re.compile(r'.txt')
PROG_ID = re.compile(r'http\:\/\/goods\.ruten\.com\.tw\/item\/show\?([0-9]+)')
PROG_BR = re.compile(r"<br />")


def get_filenames(input_dir):
    for (_, _, filenames) in os.walk(input_dir):
        pass
    output = []
    for filename in filenames:
        if len(PROG.findall(filename)) > 0:
            output.append(os.path.join(input_dir, filename))
    return output


def get_ids(path):
    with open(path, "r") as filep:
        string = filep.read()
    return PROG_ID.findall(string)


def to_chinese(input_):
    if isinstance(input_, str):
        input_ = input_.encode("utf-8").decode("utf-8")
    elif isinstance(input_, list):
        for i, element in enumerate(input_):
            input_[i] = to_chinese(element)
    elif isinstance(input_, dict):
        for k, v in input_.items():
            input_[k] = to_chinese(v)
    return input_


def crawl_one_page(url, id_, page):
    page_url = "{}?g={:014d}&p={}&s=10".format(url, id_, page)
    req = requests.get(
        page_url,
        headers={
            'user-agent': 'MozillaOHOHOH',
            'content-type': 'application/json',
        },
        cookies={'_ts_id':  '99'},
    )

    if req.status_code == 200:
        data = req.json()
        if data['data']['qna'] is not None:
            data = to_chinese(data)
            with open(
                    "/home/en/ruten_qa/{}_p{}.json".format(id_, page),
                    "w",
                    encoding='utf-8',
                ) as filep:
                    json.dump(data, filep, ensure_ascii=False, indent=2)
            return True
    return False  
            


def main():
    filepaths = get_filenames("/home/en/ruten_qa/ruten_urls/")
    count = 0
    for path in filepaths:
        ids = get_ids(path=path)
        for id_ in ids:
            if count % 100 == 0:
                print("count = {}, id = {}, path = {}".format(count, id_, path))
            for page_num in range(1, 100):
                check = crawl_one_page(
                    url='https://mybid.ruten.com.tw/api/items/goods_qna.php',
                    id_=int(id_),
                    page=page_num,
                )
                if not check:
                    break
            count += 1


if __name__ == '__main__':
    main()
