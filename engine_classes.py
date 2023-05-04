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

    def get_request(self, page: int = 10):
        params = {
            'text': 'NAME:Аналитик',  # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }

        for page in range(0, page):
            # Преобразуем текст ответа запроса в справочник Python
            jsObj = json.loads(self.get_request(page))
            # Создаем новый документ, записываем в него ответ запроса, после закрываем
            with open("data_file.json", "w", encoding="UTF-8") as file:
                json.dump(jsObj, file)
            # Проверка на последнюю страницу, если вакансий меньше 1000
            if (jsObj['pages'] - page) <= 1000:
                break

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data

    def get_vacancies(self):
        api_url = 'https://api.hh.ru/vacancies'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/58.0.3029.110 Safari/537.3'}
        params = {'text': 'Python разработчик', 'per_page': 100}  # параметры запроса (название вакансии)

        vacancies = []
        page = 0

        while len(vacancies) < 1000:
            page += 1
            params['page'] = page
            response = requests.get(api_url, headers=headers, params=params)  # выполнение запроса

            if response.ok:  # проверяем успешность запроса
                data = response.json()  # получаем список вакансий в формате JSON
                if len(data['items']) == 0:
                    break
                else:
                    vacancies += data['items']
            else:
                print('Ошибка выполнения запроса 1')
                break

            count = 1

            for vacancy in vacancies:
                salary = vacancy['salary']  # получаем информацию о зарплате
                if salary is not None:
                    if salary['currency'] == 'RUR':  # выводим только зарплату в рублях
                        # выводим наименование вакансии и зарплату
                        print(count, ')', vacancy['name'], salary['from'], '-', salary['to'], salary['currency'])
                        count += 1
                    else:
                        print(count, ')', vacancy['name'], 'Зарплата не указана')
                        count += 1

                    with open("list_of_vacancies.json", "w", encoding="UTF-8") as file:
                        json.dump(vacancy, file)
            else:
                print('Ошибка выполнения запроса 2')


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
