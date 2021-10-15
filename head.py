from bs4 import BeautifulSoup
import requests
import json
import os
import time
from datetime import datetime

if not os.path.exists("blank"):
    os.mkdir("blank")

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'User-Agent': '' #используйте юзер агент своего браузера
}


def get_job_url(url):
    """
    :param url: урл странички поиска
    :return: все ссылки на вакансии на этой страничке
    """
    job_urls = []
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    h2_list = soup.find_all('h2', class_='')
    a_list = []
    for job in h2_list:
        a_list.append(job.find('a'))
    for item in a_list:
        try:
            job_urls.append('https://www.work.ua' + item.get('href'))
        except Exception:
            continue
    return job_urls


def get_max_page(url):
    """
    Нет возможности чтобы получить количество страниц с вакансиями напрямую =\
    :param url: урл странички с запросом
    :return: количество страниц с вакансиями.
    """
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    m_p = soup.find('ul', class_='pagination hidden-xs').find_all('a')
    max_page = 0
    for item in m_p:
        if item.text.isnumeric():
            num = int(item.text)
            if num > max_page:
                max_page = num
    return max_page


def search_job(url=f'https://www.work.ua/jobs-it-python/'):
    """
    :param url: урл поиска
    :return: возвращает все ссылки на вакансии
    """
    max_page = get_max_page(url)
    all_job_url = []
    for page in range(1, max_page+1):
        print(f'Страница {page} в обработке...')
        time.sleep(1)
        all_job_url.extend(get_job_url(f'{url}?page={page}'))
    return all_job_url


def get_information(urls):
    """
    :param urls: сслыки на вакансии
    :return: данные о каждой вакансии
    """
    print('Извлечение данных...')
    count = 0
    vacancies_information = []
    for url in urls:
        try:
            req = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            id_v = url.split('/')[-2]
            vacancy = soup.find('h1', id='h1-name').text
            company = soup.find('span', class_='glyphicon glyphicon-company text-black glyphicon-large').next_sibling.next_sibling.find('b').text
            city = soup.find('span', class_='glyphicon glyphicon-map-marker text-black glyphicon-large').next_sibling.strip()
            requirements = soup.find('span', class_='glyphicon glyphicon-tick text-black glyphicon-large').next_sibling.strip().split('.')
            requirements = list(map(str.strip, requirements))
            vacancies_information.append(
                {
                    'id': id_v,
                    'vacancy': vacancy,
                    'company': company,
                    'city': city,
                    'requirements': '. '.join(requirements)
                }
            )
            count += 1
        except Exception:
            print(f'{url} не обработан.')
            continue
    print(f'{count} вакансий было обработано. Запись в файл началась...')
    return vacancies_information

def main():
    """
    Записываем все данные в json файл под текущей датой
    """
    cur_date = datetime.now().strftime("%d_%m_%Y")
    with open(fr"blank\vacancies_information_{cur_date}.json", "a", encoding='utf-8') as file:
        json.dump(get_information(search_job()), file, indent=4, ensure_ascii=False)
    time.sleep(2)
    print('Запись закончена...')


if __name__ == '__main__':
    main()
