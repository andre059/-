import json
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, file_path: str):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.isfile('Users/aa/Desktop/Курсовой проект по ООП'):
            raise FileNotFoundError("Файл json отсутствует")
        with open(self.__data_file, 'r', encoding="utf8") as file:
            json_reader = json.load(file)
            print(len(json_reader))
            if not isinstance(json_reader, list):
                raise Exception('Файл должен содержать список')

    def select(self, query: dict):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        result = []
        with open(self.__data_file, 'r', encoding="UTF-8") as file:
            data = json.load(file)  # считывает файл и возвращает объекты Python

        if not query:
            return data

        for item in data:
            for key, value in query.items():
                if item.get(key) == value:
                    result.append(item)

        return result

# if __name__ == '__main__':
# df = Connector('data_file_HH.json')

# data_for_file = {'id': 1, 'title': 'tet'}
# df.insert(data_for_file)

# d = {"from": "SuperJob"}
# data_from_file = df.select(dict())
# assert data_from_file == [data_for_file]

# df.delete({'id': 1})
# data_from_file = df.select(dict())
# assert data_from_file == []
