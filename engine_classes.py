import json
import os

import requests

from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def get_request(self, page: int = 11):
        params = {'per_page': 100, 'only_with_salary': True}

        items: list[dict] = []

        for page in range(0, page):
            params['page'] = page
            response = requests.get('https://api.hh.ru/vacancies', params)
            response.raise_for_status()

            data = response.json()
            items.extend(data['items'])

            with open("data_file.json", "w", encoding="UTF-8") as file:
                json.dump(items, file)

        return items

    def get_vacancies(self):
        count = 0

        with open("data_file.json", "r", encoding="UTF-8") as file:
            data = json.load(file)

        for vacancy in data:
            if vacancy.get('salary') is not None:
                if vacancy.get('salary').get('currency') == 'RUR':  # выводим только зарплату в рублях
                    count += 1
                    # выводим наименование вакансии и зарплату
                    # print(count, ')', vacancy['name'], vacancy['from'], '-', vacancy['to'], vacancy['currency'])
                    print(count, ')', vacancy['name'])
                else:
                    count += 1
                    print(count, ')', vacancy['name'], 'Зарплата не указана')

            with open("list_of_vacancies.json", "w", encoding="UTF-8") as f:
                json.dump(vacancy, f)


class SuperJob(Engine):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def get_request(self, **kwargs):
        url = "https://api.superjob.ru/2.0/vacancies?keyword={}&town={}&date_published={}&page={}".format(
            kwargs.get("keyword"),
            kwargs.get("town"),
            kwargs.get("date_published"),
            kwargs.get("page")
        )
        headers = {"X-Api-App-Id": self.secret_key}
        response = requests.get(url, headers=headers)
        vacancies = response.json().get("objects")
        return vacancies


rt = HH('OauthToken')
# rt.get_request()
# areas = get_request()
rt.get_vacancies()



