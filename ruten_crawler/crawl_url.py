from os.path import join
import requests
from bs4 import BeautifulSoup


def crawl_one_page(class_num: int, url: str, page: int, output_dir: str):
    page_url = "{}&p={}".format(url, page)
    req = requests.get(
        page_url,
        headers={
            'user-agent': 'Mozilla BABABA',
            'encoding': 'UTF-8',
        },
        cookies={
            '_ts_id': '999999999999999999',
            'adultchk': 'ok',  # for AdultOnly products
        },
    )
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        targets = soup.find_all('a', class_="item-name-anchor")
        if len(targets) > 0:
            output = []
            for element in targets:
                output.append(element['href'])
            with open(
                join(output_dir, "{}_p{}.txt".format(class_num, page)),
                "w",
            ) as filep:
                filep.write("\n".join(output))
            return True
    return False


def main():
    for num in range(0, 30):
        if num % 10 == 0:
            print("class {}".format(num))
        url = 'http://class.ruten.com.tw/category/rank_list.php?class=%04d' % num
        for page_num in range(1, 100):
            check = crawl_one_page(
                class_num=num,
                url=url,
                page=page_num,
                output_dir=f"./urls_{page_num}",
            )
            if not check:
                break


if __name__ == '__main__':
    main()
