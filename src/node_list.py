class FatNode:
    """
    Узел двусвязного списка в структуре fat node, хранящий данные, ссылки на соседние узлы
    и версию узла.
    """
    def __init__(self, data, prev_node=None, next_node=None):
        """
        :param data: Данные для этого узла (состояние версии).
        :param prev_node: Ссылка на предыдущий узел.
        :param next_node: Ссылка на следующий узел.
        """
        self.data = data  # Состояние данных в текущем узле
        self.prev_node = prev_node  # Ссылка на предыдущий узел
        self.next_node = next_node  # Ссылка на следующий узел


class PersistentLinkedListFatNode:
    """
    Класс для создания персистентного двусвязного списка
    с ограничением на максимальный размер.

    Атрибуты:
    - max_size: Максимальный размер списка.
    - history: История версий списка.

    Методы:
    - add(item): Добавляет элемент в конец текущей версии списка.
    - insert(index, item): Вставляет элемент на указанную позицию.
    - remove(index): Удаляет элемент по указанному индексу.
    - get(index): Возвращает элемент на заданном индексе в текущей версии списка.
    - get_version(version): Возвращает состояние списка на указанной версии.
    - update_version(version): Обновляет текущую версию списка на указанную.
    - size(): Возвращает текущий размер списка.
    - check_is_empty(): Проверяет, пуст ли список.
    - check_is_full(): Проверяет, полон ли список.
    """

    empty_array_message = "Список пуст"
    full_array_message = "Список полон"
    invalid_index_message = "Неверный индекс"
    invalid_version_message = "Неверная версия"

    def __init__(self, max_size=None):
        """
        Инициализирует двусвязный список с указанными параметрами.
        :param max_size: Максимальный размер списка.
        """
        self.max_size = max_size or 2 ** 10
        self.head = None
        self.tail = None
        self.history = []

    def _get_current_state(self):
        """
        Возвращает текущее состояние списка (последнюю версию).
        :return: Список элементов в текущей версии.
        """
        state = []
        current = self.head
        while current:
            state.append(current.data)
            current = current.next_node
        return state

    def check_is_empty(self):
        """
        Проверяет, пуст ли список.
        :return: True, если список пуст, иначе False.
        """
        return self.head is None

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
        return self.size() >= self.max_size

    def add(self, item):
        """
        Добавляет элемент в конец списка.
        :param item: Элемент, который необходимо добавить.
        """
        if self.check_is_full():
            raise ValueError(self.full_array_message)
        new_node = FatNode(item, prev_node=self.tail)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next_node = new_node
        self.tail = new_node
        self.history.append(self._clone_state())

    def insert(self, index, item):
        """
        Вставляет элемент в список на указанную позицию.
        :param index: Индекс для вставки.
        :param item: Элемент для вставки.
        """
        if self.check_is_full():
            raise ValueError(self.full_array_message)
        if index < 0 or index > self.size():
            raise IndexError(self.invalid_index_message)

        if index == 0:  # Вставка в начало
            new_node = FatNode(item, next_node=self.head)
            if self.head:
                self.head.prev_node = new_node
            self.head = new_node
            if not self.tail:
                self.tail = new_node
        elif index == self.size():  # Вставка в конец
            self.add(item)
            return
        else:  # Вставка в середину
            current = self.head
            for _ in range(index):
                current = current.next_node
            new_node = FatNode(item, prev_node=current.prev_node, next_node=current)
            current.prev_node.next_node = new_node
            current.prev_node = new_node
        self.history.append(self._clone_state())

    def remove(self, index):
        """
        Удаляет элемент по указанному индексу.
        :param index: Индекс элемента для удаления.
        """
        if self.check_is_empty():
            raise ValueError(self.empty_array_message)
        if index < 0 or index >= self.size():
            raise IndexError(self.invalid_index_message)

        if index == 0:  # Удаление из начала
            if self.head == self.tail:  # Единственный элемент
                self.head = self.tail = None
            else:
                self.head = self.head.next_node
                self.head.prev_node = None
        elif index == self.size() - 1:  # Удаление из конца
            self.tail = self.tail.prev_node
            if self.tail:
                self.tail.next_node = None
        else:  # Удаление из середины
            current = self.head
            for _ in range(index):
                current = current.next_node
            current.prev_node.next_node = current.next_node
            current.next_node.prev_node = current.prev_node
        self.history.append(self._clone_state())

    def get(self, index):
        """
        Возвращает элемент по индексу.
        :param index: Индекс элемента.
        :return: Элемент на указанной позиции.
        """
        if index < 0 or index >= self.size():
            raise IndexError(self.invalid_index_message)
        current = self.head
        for _ in range(index):
            current = current.next_node
        return current.data

    def _clone_state(self):
        """
        Клонирует текущее состояние списка.
        :return: Список узлов, представляющий текущее состояние.
        """
        state = []
        current = self.head
        while current:
            node_copy = FatNode(current.data)
            state.append(node_copy)
            if len(state) > 1:
                state[-2].next_node = node_copy
                node_copy.prev_node = state[-2]
            current = current.next_node
        return state[0] if state else None

    def get_version(self, version):
        """
        Возвращает состояние списка на указанной версии.
        :param version: Номер версии.
        :return: Список элементов в указанной версии.
        """
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)
        state = []
        current = self.history[version]
        while current:
            state.append(current.data)
            current = current.next_node
        return state
