import requests

from bs4 import BeautifulSoup

import re

import urllib.request

import os

import PyPDF2

from easydict import EasyDict as edict

CONV_NAME = 'ICLR2018'
papertypes = ['Poster', 'Workshop', 'Oral']

os.makedirs(CONV_NAME, exist_ok=True)


url = 'https://iclr.cc/Conferences/2018/Schedule?type='

for papertype in papertypes:
    os.makedirs(os.path.join(CONV_NAME, papertype), exist_ok=True)

    url = url + papertype

    r = requests.get(url)

    print(r.status_code)

    print(r.headers['content-type'])

    print(r.encoding)

    with open(f'response_{CONV_NAME}_{papertype}.html','w',encoding='utf-8') as f:
        f.write(r.text)

    # r = edict()
    # with open(f'response_{CONV_NAME}_{papertype}.html','w',encoding='utf-8') as f:
    #     r.text = f.readlines()
    soup = BeautifulSoup(r.text, features="html.parser")

    index = 1
    for block in soup.find_all('div', onclick=re.compile('showDetail\(\d+\)')):

        papername = block.find(attrs={'class': 'maincardBody'})

        if papername is None:
            badreason = 'No Paper Name Found'
            print(f'{badreason}, continue')
            continue

        papername = papername.string

        href = block.find(attrs={'href': re.compile('https://openreview\.net/forum\?id=(.*)'), 'title':'PDF'})
        if href is None:
            badreason = 'No href Found'
            print(f'{badreason}, continue')
            continue

        href = href.get('href').replace('forum', 'pdf')

        file_path = os.path.join(CONV_NAME, papertype, f'{papername}.pdf')

        index += 1

        try:
            PyPDF2.PdfFileReader(open(file_path, "rb"))
            print(f'[{index:05d}] already exists:     {file_path}')
        except:

            try:
                urllib.request.urlretrieve(href, file_path)
                print(f'[{index:05d}] download finished:  {file_path} ')
            except:
                badreason = f'Can Not Download at {href} to {file_path}'
                print(f'{badreason}, continue')



        #             if not os.path.exists(file_path):
        #                 urllib.request.urlretrieve(pdf_link, file_path)

        # m = re.match('^/paper/\d+-(.*)',href)
        # if m:
        #     new_link = root + m.string
        #
        #
        #     # with open('response_pdf_NIPS2018.html','w',encoding='utf-8') as f:
        #     #     f.write(rr.text)
        #
        #     try:
        #         rr = requests.get(new_link,timeout=30)
        #     except requests.ConnectionError as e:
        #         print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        #         print(str(e))
        #         continue
        #     except requests.Timeout as e:
        #         print("OOPS!! Timeout Error")
        #         print(str(e))
        #         continue
        #     except requests.RequestException as e:
        #         print("OOPS!! General Error")
        #         print(str(e))
        #         continue
        #     except KeyboardInterrupt:
        #         print("Someone closed the program")
        #
        #
        #     rr_soup = BeautifulSoup(rr.text)
        #
        #     for rr_block in rr_soup.find_all('a'):
        #         rr_href = rr_block.get('href')
        #
        #         rr_m = re.match('^/paper/\d+-(.*).pdf$',rr_href)
        #         if rr_m:
        #             name = rr_m.group(1)
        #
        #             pdf_link = root + rr_m.string
        #
        #             file_path = f'{CONV_NAME}/{index}-{name}.pdf'
        #             if not os.path.exists(file_path):
        #                 urllib.request.urlretrieve(pdf_link, file_path)
        #
        #             print(f'download {file_path}')
        #
        #             index += 1
        #
        #             break
        #
        #
        #
        #
        #
