class FatNode:
    """
    Узел в структуре fat node, хранящий состояние версии и ссылки на предыдущие версии.
    """
    def __init__(self, data, prev_node=None):
        """
        :param data: Данные для этого узла (состояние версии).
        :param prev_node: Ссылка на предыдущий узел (предшествующую версию).
        """
        self.data = data  # Состояние данных в текущем узле
        self.prev_node = prev_node  # Ссылка на предыдущий узел (если есть)


class PersistentListFatNode:
    """
    Класс для создания персистентного списка с ограничением на максимальный размер.

    Атрибуты:
    - max_size: Максимальный размер списка.
    - history: История версий списка.

    Методы:
    - add(item): Добавляет элемент в текущую версию списка.
    - remove(item): Удаляет элемент из текущей версии списка.
    - get(index): Возвращает элемент на заданном индексе в текущей версии списка.
    - get_version(version): Возвращает состояние списка на заданной версии.
    - update_version(version): Обновляет текущую версию списка на указанную.
    - clone(): Создает клонированную версию текущего списка.
    - _get_current_state(): Возвращает текущую версию списка.
    - insert(index, item): Вставляет элемент в список на указанную позицию.
    - pop(): Удаляет и возвращает последний элемент списка.
    - clear(): Очищает список.
    - check_is_empty(): Проверяет, пуст ли список.
    - size(): Возвращает текущий размер списка.
    - check_is_full(): Проверяет, полон ли список.

    Пример использования:
    >>> persistent_list = PersistentListFatNode(max_size=5)
    >>> persistent_list.add(1)  # Список: [1] -> версия 0
    >>> persistent_list.add(2)  # Список: [1, 2] -> версия 1
    >>> persistent_list.add(3)  # Список: [1, 2, 3] -> версия 2
    >>> persistent_list.add(4)  # Список: [1, 2, 3, 4] -> версия 3
    >>> persistent_list.remove(3)  # Удаление элемента 3
    >>> persistent_list.get(2)  # Ожидаемый результат: 3
    >>> persistent_list._get_current_state()  # Ожидаемый результат: [1, 2, 3]
    >>> cloned_list = persistent_list.clone()
    >>> cloned_list._get_current_state()  # Ожидаемый результат: [1, 2, 3]
    >>> persistent_list.get_version(3)  # Ожидаемый результат: [1, 2, 3, 4]
    >>> persistent_list.update_version(1)  # Обновляем текущую версию на 1
    >>> persistent_list._get_current_state()  # Ожидаемый результат: [1, 2]
    >>> for i, node in enumerate(persistent_list.history):
    >>>     print(f"Версия {i}: {node.data}")  # Печать истории версий
    """
    empty_array_message = "Список пуст"
    full_array_message = "Список полон"
    invalid_index_message = "Неверный индекс"
    invalid_version_message = "Неверная версия"

    def __init__(self, max_size=None):
        """
        Инициализирует список с указанными параметрами.
        :param max_size: Максимальный размер списка (если не указан,
        используется размер по умолчанию).
        """
        self.max_size = max_size or 2 ** 10  # Максимальный размер, по умолчанию 1024
        self.head = None  # Ссылка на голову списка (наиболее новая версия)
        self.history = []  # История ссылок на узлы (версии списка)

    def _get_current_state(self):
        """
        Возвращает текущее состояние списка (последнюю версию).
        :return: Текущее состояние списка.
        """
        if not self.head:
            return []
        return self.head.data

    def _check_index(self, index):
        """
        Проверяет, является ли индекс допустимым.
        :param index: Индекс для проверки.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        if index < 0 or index >= len(self._get_current_state()):
            raise IndexError(self.invalid_index_message)

    def check_is_empty(self):
        """
        Проверяет, пуст ли список.
        :return: True, если список пуст, иначе False.
        """
        return len(self._get_current_state()) == 0

    def size(self):
        """
        Возвращает текущий размер списка.
        :return: Размер списка.
        """
        return len(self._get_current_state())

    def check_is_full(self):
        """
        Проверяет, полон ли список.
        :return: True, если список полон, иначе False.
        """
        return len(self._get_current_state()) >= self.max_size

    def add(self, element):
        """
        Добавляет элемент в конец списка.
        :param element: Элемент, который необходимо добавить.
        :raises ValueError: Если список полон.
        """
        if self.check_is_full():
            raise ValueError(self.full_array_message)
        current_state = self._get_current_state()
        new_node = FatNode(current_state + [element], self.head)
        self.head = new_node
        self.history.append(new_node)

    def insert(self, index, element):
        """
        Вставляет элемент в список на указанную позицию.
        :param index: Индекс, куда нужно вставить элемент.
        :param element: Элемент, который нужно вставить.
        :raises IndexError: Если индекс недопустим.
        :raises ValueError: Если список полон.
        """
        if self.check_is_full():
            raise ValueError(self.full_array_message)
        current_state = self._get_current_state()
        if index > len(current_state):
            raise IndexError(self.invalid_index_message)
        new_state = current_state[:index] + [element] + current_state[index:]
        new_node = FatNode(new_state, self.head)
        self.head = new_node
        self.history.append(new_node)

    def remove(self, index):
        """
        Удаляет элемент по указанному индексу.
        :param index: Индекс элемента для удаления.
        :raises IndexError: Если индекс недопустим.
        """
        self._check_index(index)
        current_state = self._get_current_state()
        new_state = current_state[:index] + current_state[index + 1:]
        new_node = FatNode(new_state, self.head)
        self.head = new_node
        self.history.append(new_node)

    def get(self, index):
        """
        Возвращает элемент по указанному индексу.
        :param index: Индекс элемента.
        :return: Элемент на указанной позиции.
        :raises IndexError: Если индекс недопустим.
        """
        self._check_index(index)
        return self._get_current_state()[index]

    def pop(self):
        """
        Удаляет и возвращает последний элемент списка.
        :return: Удалённый элемент.
        :raises ValueError: Если список пуст.
        """
        if self.check_is_empty():
            raise ValueError(self.empty_array_message)
        current_state = self._get_current_state()
        new_state = current_state[:-1]
        new_node = FatNode(new_state, self.head)
        self.head = new_node
        self.history.append(new_node)
        return current_state[-1]

    def clear(self):
        """
        Очищает список, создавая новое пустое состояние.
        """
        new_node = FatNode([], self.head)
        self.head = new_node
        self.history.append(new_node)

    def clone(self):
        """
        Создаёт и возвращает новый список, который является копией текущего.
        :return: Клонированный список.
        """
        new_list = PersistentListFatNode(self.max_size)
        new_list.head = self.head
        new_list.history = self.history[:]
        return new_list

    def get_version(self, version):
        """
        Возвращает состояние списка на указанной версии.
        :param version: Номер версии.
        :return: Состояние списка в указанной версии.
        :raises ValueError: Если версия недопустима.
        """
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)
        return self.history[version].data

    def update_version(self, version):
        """
        Обновляет текущую версию списка на указанную.
        :param version: Номер версии, которую нужно сделать текущей.
        :raises ValueError: Если версия недопустима.
        """
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)

        self.head = self.history[version]

    def __getitem__(self, index):
        """
        Операция получения элемента по индексу (аналогично get).
        :param index: Индекс элемента.
        :return: Элемент на указанной позиции.
        """
        return self.get(index)

    def __setitem__(self, index, value):
        """
        Операция вставки или замены элемента по индексу.
        :param index: Индекс, на который нужно вставить или заменить элемент.
        :param value: Новый элемент.
        """
        self._check_index(index)
        current_state = self._get_current_state()
        new_state = current_state[:index] + [value] + current_state[index + 1:]
        new_node = FatNode(new_state, self.head)
        self.head = new_node
        self.history.append(new_node)