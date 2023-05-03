import json
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

    def get_request(self, page=None):
        params = {
            'text': 'NAME:Аналитик',  # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data

    for page in range(0, 20):
        # Преобразуем текст ответа запроса в справочник Python
        jsObj = json.loads(get_request(page))
        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        with open("data_file.json", "w", encoding="UTF-8") as file:
            json.dump(jsObj, file)
        # Проверка на последнюю страницу, если вакансий меньше 2000
        if (jsObj['pages'] - page) <= 1:
            break

    def get_vacancies(self, **kwargs):
        # Проходимся по непосредственно списку вакансий
        for v in self.jsObj['items']:
            # Обращаемся к API и получаем детальную информацию по конкретной вакансии
            req = requests.get(v['url'])
            data = req.content.decode()
            req.close()

            # Создаем файл в формате json с идентификатором вакансии в качестве названия
            # Записываем в него ответ запроса и закрываем файл
            fileName = 'list_of_vacancies.json'.format(v['id'])
            f = open(fileName, mode='w', encoding='utf8')
            f.write(data)
            f.close()

        url = "https://api.hh.ru/vacancies?text={}&area={}&period={}&page={}".format(
            kwargs.get("text"),
            kwargs.get("area"),
            kwargs.get("period"),
            kwargs.get("page")
        )
        headers = {"Authorization": self.secret_key}
        response = requests.get(url, headers=headers)
        vacancies = response.json().get("items")
        return vacancies



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
# с.get_vacancies()
# areas = get_request()
rt.get_vacancies()
