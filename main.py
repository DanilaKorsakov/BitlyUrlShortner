import os
import requests
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, link):
    headers = {"Authorization": f"{token}"}
    url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {"long_url": link}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, link):
    parsed_link = urlparse(link)
    short_link= f"{parsed_link.netloc}{parsed_link.path}"

    headers = {"Authorization": f"{token}"}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(link, token):
    parsed_link = urlparse(link)
    short_link= f"{parsed_link.netloc}{parsed_link.path}"

    headers = {"Authorization": f"{token}"}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    user_link = args.link
    try:
        if is_bitlink(user_link, bitly_token):
            print(f'Количество переходов по ссылке битли: {count_clicks(bitly_token, user_link)}')
        else:
            print('Битлинк', shorten_link(bitly_token, user_link))
    except requests.HTTPError as error:
        print(error)


if __name__ == "__main__":
    main()
