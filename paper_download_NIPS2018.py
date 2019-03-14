import requests

from bs4 import BeautifulSoup

import re

import urllib.request

import os

CONV_NAME = 'NIPS2018'
os.system(f'mkdir {CONV_NAME}')


# url ='https://papers.nips.cc/paper/7286-efficient-algorithms-for-non-convex-isotonic-regression-through-submodular-optimization.pdf'  

root = 'https://papers.nips.cc'

r = requests.get('https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018')

print(r.status_code)

print(r.headers['content-type']) 

print(r.encoding)

with open('response_NIPS2018.html','w',encoding='utf-8') as f:
    f.write(r.text)

soup = BeautifulSoup(r.text, features="html.parser")

index = 1
for block in soup.find_all('li'):
    href = block.a.get('href')

    m = re.match('^/paper/\d+-(.*)',href)
    if m:
        new_link = root + m.string
        

        # with open('response_pdf_NIPS2018.html','w',encoding='utf-8') as f:
        #     f.write(rr.text)

        try:
            rr = requests.get(new_link,timeout=30)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))            
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")


        rr_soup = BeautifulSoup(rr.text)

        for rr_block in rr_soup.find_all('a'):
            rr_href = rr_block.get('href')

            rr_m = re.match('^/paper/\d+-(.*).pdf$',rr_href)
            if rr_m:
                name = rr_m.group(1)

                pdf_link = root + rr_m.string
                
                file_path = f'{CONV_NAME}/{index}-{name}.pdf'
                if not os.path.exists(file_path):
                    urllib.request.urlretrieve(pdf_link, file_path) 

                print(f'download {file_path}')

                index += 1

                break





