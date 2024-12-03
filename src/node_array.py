class FatNode:
    """
    Класс для представления узла в персистентном массиве.
    Каждый узел хранит данные и ссылку на предыдущую версию массива.
    """
    def __init__(self, data=None, previous=None):
        """
        Инициализирует узел.

        :param data: Данные, хранимые в узле (по умолчанию пустой список).
        :param previous: Ссылка на предыдущую версию узла (по умолчанию None).
        """
        self.data = data if data is not None else []
        self.previous = previous


class PersistentArray:
    """
    Класс для реализации персистентного массива с помощью метода Fat Node.

    Этот класс позволяет создавать массивы, где каждая операция, изменяющая
    массив (например, добавление, удаление элементов), создает новую версию
    массива, сохраняя доступ к предыдущим версиям.
    """
    def __init__(self, max_size=1024, default_value=0):
        """
        Инициализирует персистентный массив с возможностью добавления новых версий.

        :param max_size: Максимальный размер массива (по умолчанию 1024).
        :param default_value: Значение по умолчанию для элементов массива (по умолчанию 0).
        """
        self.max_size = max_size
        self.default_value = default_value
        initial_node = FatNode([])
        self.nodes = [initial_node]
        self.current_node = initial_node
        self.size = 0

    def __getitem__(self, index):
        """
        Получает элемент массива из текущей версии по указанному индексу.

        :param index: Индекс элемента, который нужно получить.
        :return: Элемент массива по указанному индексу.
        :raises ValueError: Если индекс выходит за пределы текущей версии массива.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Неверный индекс")
        return self.current_node.data[index]

    def get(self, version, index):
        """
        Получает элемент массива из указанной версии по индексу.

        :param version: Версия массива, из которой нужно получить элемент.
        :param index: Индекс элемента, который нужно получить.
        :return: Элемент массива по указанному индексу.
        :raises ValueError: Если индекс или версия массива неверны.
        """
        node = self._get_node(version)
        if index < 0 or index >= len(node.data):
            raise ValueError("Неверный индекс")
        return node.data[index]

    def _get_node(self, version):
        """
        Получает узел, соответствующий указанной версии массива.

        :param version: Версия массива, узел которой нужно получить.
        :return: Узел, соответствующий указанной версии.
        :raises ValueError: Если версия неверна.
        """
        if version < 0 or version >= len(self.nodes):
            raise ValueError("Неверная версия")
        return self.nodes[version]

    def add(self, value):
        """
        Добавляет элемент в текущую версию массива и создает новую версию.

        :param value: Значение, которое нужно добавить в массив.
        :raises ValueError: Если размер массива превышает максимальный размер.
        """
        if self.size >= self.max_size:
            raise ValueError("Превышен максимальный размер массива")
        new_data = self.current_node.data + [value]
        new_node = FatNode(new_data, self.current_node)
        self.nodes.append(new_node)
        self.current_node = new_node
        self.size += 1

    def pop(self, index):
        """
        Удаляет элемент из текущей версии массива по указанному индексу и возвращает его.

        :param index: Индекс элемента, который нужно удалить.
        :return: Удаленный элемент.
        :raises ValueError: Если индекс выходит за пределы массива.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Неверный индекс")
        removed_value = self.current_node.data[index]
        new_data = self.current_node.data[:index] + self.current_node.data[index+1:]
        new_node = FatNode(new_data, self.current_node)
        self.nodes.append(new_node)
        self.current_node = new_node
        self.size -= 1
        return removed_value

    def __setitem__(self, index, value):
        """
        Обновляет элемент массива в текущей версии по указанному индексу.

        :param index: Индекс элемента, который нужно обновить.
        :param value: Новое значение для элемента.
        :raises ValueError: Если индекс выходит за пределы массива.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Неверный индекс")
        new_data = self.current_node.data[:]
        new_data[index] = value
        new_node = FatNode(new_data, self.current_node)
        self.nodes.append(new_node)
        self.current_node = new_node

    def insert(self, index, value):
        """
        Вставляет элемент в текущую версию массива в указанную позицию.

        :param index: Индекс, в который нужно вставить элемент.
        :param value: Значение, которое нужно вставить.
        :raises ValueError: Если индекс выходит за пределы массива или массив переполнен.
        """
        if self.size >= self.max_size:
            raise ValueError("Превышен максимальный размер массива")
        if index < 0 or index > self.size:
            raise ValueError("Неверный индекс")
        new_data = self.current_node.data[:index] + [value] + self.current_node.data[index:]
        new_node = FatNode(new_data, self.current_node)
        self.nodes.append(new_node)
        self.current_node = new_node
        self.size += 1

    def remove(self, index):
        """
        Удаляет элемент из текущей версии массива по указанному индексу.

        :param index: Индекс элемента, который нужно удалить.
        :raises ValueError: Если индекс выходит за пределы массива.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Неверный индекс")
        new_data = self.current_node.data[:index] + self.current_node.data[index+1:]
        new_node = FatNode(new_data, self.current_node)
        self.nodes.append(new_node)
        self.current_node = new_node
        self.size -= 1

    def get_size(self):
        """
        Получает размер текущей версии массива.

        :return: Количество элементов в текущей версии массива.
        """
        return self.size

    def check_is_empty(self):
        """
        Проверяет, пуст ли текущий массив.

        :return: True, если массив пуст, иначе False.
        """
        return self.size == 0

    def check_is_full(self):
        """
        Проверяет, достигнут ли максимальный размер массива.

        :return: True, если массив полон, иначе False.
        """
        return self.size >= self.max_size

    def get_version(self, version):
        """
        Получает состояние массива для указанной версии.

        :param version: Версия массива, которую нужно вернуть.
        :return: Состояние массива для указанной версии.
        :raises ValueError: Если версия неверна.
        """
        node = self._get_node(version)
        return node.data

    def update_version(self, version):
        """
        Обновляет текущую версию массива до указанной.

        :param version: Версия, до которой нужно обновить массив.
        """
        self.current_node = self._get_node(version)
        self.size = len(self.current_node.data)
