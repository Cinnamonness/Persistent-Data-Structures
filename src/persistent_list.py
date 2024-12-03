class Node:
    """
    Узел двусвязного списка.

    Атрибуты:
        value (any): Значение, хранящееся в узле.
        prev (Node, optional): Ссылка на предыдущий узел списка (по умолчанию None).
        next_node (Node, optional): Ссылка на следующий узел списка (по умолчанию None).
    """

    def __init__(self, value=None, prev=None, next_node=None):
        """
        Инициализирует новый узел.

        Параметры:
            value (any, optional): Значение для хранения в узле (по умолчанию None).
            prev (Node, optional): Ссылка на предыдущий узел (по умолчанию None).
            next_node (Node, optional): Ссылка на следующий узел (по умолчанию None).
        """
        self.value = value
        self.prev = prev
        self.next_node = next_node


class PersistentLinkedList:
    """
    Персистентный двусвязный список с поддержкой версий через метод path copying.

    Атрибуты:
        max_size (int): Максимальное количество элементов в списке (по умолчанию 1024).
        head (Node): Ссылка на первый узел списка.
        tail (Node): Ссылка на последний узел списка.
        size_ (int): Текущее количество элементов в списке.
        history (list): История версий списка с их состоянием.

    Методы:
        size(): Возвращает текущее количество элементов в списке.
        check_is_empty(): Проверяет, пуст ли список.
        check_is_full(): Проверяет, достиг ли список максимального размера.
        add(value): Добавляет элемент в конец списка.
        add_first(value): Добавляет элемент в начало списка.
        remove(index): Удаляет элемент по индексу.
        insert(index, value): Вставляет элемент в список по указанному индексу.
        get(version=None, index=None): Возвращает элемент по индексу из указанной версии.
        get_version(version): Возвращает состояние списка на указанной версии.
        update_version(version): Обновляет текущую версию списка до указанной.
        clear(): Очищает список, создавая новую версию.
    """
    empty_message = "Список пуст"
    full_message = "Список полон"
    invalid_index_message = "Неверный индекс"
    invalid_version_message = "Неверная версия"

    def __init__(self, max_size=None):
        """
        Инициализирует новый персистентный список.

        Параметры:
            max_size (int, optional): Максимальное количество элементов в списке.
                                     Если не указано, используется значение по умолчанию 1024.
        """
        self.max_size = max_size or 2 ** 10
        self.head = None
        self.tail = None
        self.size_ = 0
        self.history = [{"version": 0, "head": None, "tail": None}]  # Первая версия

    def _copy_node(self, node):
        """
        Создает копию указанного узла.

        Параметры:
            node (Node): Узел для копирования.

        Возвращает:
            Node: Новый узел с таким же значением.
        """
        if not node:
            return None
        return Node(value=node.value)

    def _copy_list(self):
        """
        Создает копию текущего состояния списка для новой версии.

        Возвращает:
            tuple: Кортеж из ссылок на голову и хвост нового списка.
        """
        if not self.head:
            return None, None

        new_head = self._copy_node(self.head)
        current_old = self.head.next_node
        current_new = new_head

        while current_old:
            new_node = self._copy_node(current_old)
            current_new.next_node = new_node
            new_node.prev = current_new
            current_new = new_node
            current_old = current_old.next_node

        return new_head, current_new

    def size(self):
        """
        Возвращает текущее количество элементов в списке.

        Возвращает:
            int: Число элементов в списке.
        """
        return self.size_

    def check_is_empty(self):
        """
        Проверяет, пуст ли список.

        Возвращает:
            bool: True, если список пуст; иначе False.
        """
        return self.size_ == 0

    def check_is_full(self):
        """
        Проверяет, достиг ли список максимального размера.

        Возвращает:
            bool: True, если список полон; иначе False.
        """
        return self.size_ >= self.max_size

    def _check_index(self, index):
        """
        Проверяет корректность переданного индекса.

        Параметры:
            index (int): Индекс, который нужно проверить.

        Исключения:
            IndexError: Выбрасывается, если индекс выходит за пределы
            допустимого диапазона (меньше 0 или больше либо равен текущему размеру списка).

        Примечание:
            Метод используется для проверки индекса перед операциями вставки,
            удаления или получения элемента.
        """
        if index < 0 or index >= self.size_:
            raise IndexError(self.invalid_index_message)

    def save_to_history(self):
        """
        Сохраняет текущее состояние списка в историю версий.
        """
        new_head, new_tail = self._copy_list()
        last_version = self.history[-1]["version"]
        self.history.append({
            "version": last_version + 1,
            "head": new_head,
            "tail": new_tail,
        })

    def add(self, value):
        """
        Добавляет элемент в конец списка.

        Параметры:
            value (any): Значение для добавления.

        Исключения:
            ValueError: Если список достиг максимального размера.
        """
        if self.check_is_full():
            raise ValueError(self.full_message)

        new_node = Node(value=value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next_node = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size_ += 1
        self.save_to_history()

    def add_first(self, value):
        """
        Добавляет элемент в начало списка.

        Параметры:
            value (any): Значение для добавления.

        Исключения:
            ValueError: Если список достиг максимального размера.
        """
        if self.check_is_full():
            raise ValueError(self.full_message)

        new_node = Node(value=value, next_node=self.head)
        if self.head:
            self.head.prev = new_node
        self.head = new_node
        if not self.tail:
            self.tail = new_node

        self.size_ += 1
        self.save_to_history()

    def remove(self, index):
        """
        Удаляет элемент по индексу.

        Параметры:
            index (int): Индекс элемента для удаления.

        Исключения:
            ValueError: Если список пуст.
            IndexError: Если индекс недействителен.

        Возвращает:
            any: Значение удаленного элемента.
        """
        if self.check_is_empty():
            raise ValueError(self.empty_message)
        if index < 0 or index >= self.size_:
            raise IndexError(self.invalid_index_message)

        current = self.head
        for _ in range(index):
            current = current.next_node

        value = current.value

        if current.prev:
            current.prev.next_node = current.next_node
        else:
            self.head = current.next_node

        if current.next_node:
            current.next_node.prev = current.prev
        else:
            self.tail = current.prev

        self.size_ -= 1
        self.save_to_history()
        return value

    def insert(self, index, value):
        """
        Вставляет элемент в список по указанному индексу.

        Параметры:
            index (int): Индекс, на который нужно вставить элемент.
            value (any): Значение для вставки.

        Исключения:
            ValueError: Если список достиг максимального размера.
            IndexError: Если индекс недействителен.
        """
        if self.check_is_full():
            raise ValueError(self.full_message)
        if index == 0:
            self.add_first(value)
        elif index == self.size():
            self.add(value)
        else:
            self._check_index(index)
            current = self.head
            for _ in range(index):
                current = current.next_node
            new_node = Node(value=value, prev=current.prev, next_node=current)
            current.prev.next_node = new_node
            current.prev = new_node
            self.save_to_history()

    def get(self, version=None, index=None):
        """
        Возвращает элемент по индексу на указанной версии.

        Параметры:
            version (int, optional): Версия списка для получения
            (по умолчанию текущая версия).
            index (int, optional): Индекс элемента для получения
            (по умолчанию None).

        Возвращаемое значение:
            any: Значение элемента на указанной версии.
        """
        if version is None:
            version = len(self.history) - 1  # Текущая версия
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)
        state = self.history[version]
        current = state["head"]

        if index is None:
            result = []
            while current:
                result.append(current.value)
                current = current.next_node
            return result

        if index < 0 or index >= self.size_:
            raise IndexError(self.invalid_index_message)

        for _ in range(index):
            current = current.next_node
        return current.value

    def get_version(self, version):
        """Возвращает состояние списка на указанной версии."""
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)

        target_version = self.history[version]
        state = []
        current = target_version["head"]
        while current:
            state.append(current.value)
            current = current.next_node
        return state

    def update_version(self, version):
        """Обновляет текущую версию списка до указанной."""
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)

        target_version = self.history[version]
        self.head = target_version["head"]
        self.tail = target_version["tail"]
        self.size_ = len(self.get_version(version))
        self.history = self.history[:version + 1]

    def clear(self):
        """
        Очищает список, удаляя все элементы.
        """
        self.head = None
        self.tail = None
        self.size_ = 0

        self.history.append({
            "version": self.history[-1]["version"] + 1,
            "change": {"action": "clear"},
            "head": self.head,
            "tail": self.tail,
        })
