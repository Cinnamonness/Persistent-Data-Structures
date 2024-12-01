class Node:
    """Узел двусвязного списка.

    Атрибуты:
        value: Значение, хранимое в узле.
        prev: Указатель на предыдущий узел.
        next_node: Указатель на следующий узел.
    """
    def __init__(self, value=None, prev=None, next_node=None):
        self.value = value
        self.prev = prev
        self.next_node = next_node


class PersistentLinkedList:
    """
    Персистентный двусвязный список, реализующий метод
    path copying.

    Этот класс реализует двусвязный список, сохраняющий
    историю состояний, позволяя получать доступ
    к предыдущим версиям списка. Все изменения списка
    сохраняются, чтобы можно было вернуться
    к любому предыдущему состоянию.

    Атрибуты:
        max_size: Максимальный размер списка (по умолчанию 1024).
        head: Указатель на первый узел списка.
        tail: Указатель на последний узел списка.
        history: Список, хранящий все версии списка.

    Методы:
        __init__(max_size=None): Инициализация списка
        с заданным максимальным размером.
        size(): Возвращает размер списка.
        check_is_empty(): Проверяет, пуст ли список.
        add(value): Добавляет элемент в конец списка.
        add_first(value): Добавляет элемент в начало списка.
        insert(index, value): Вставляет элемент по указанному индексу.
        remove(index): Удаляет элемент по индексу.
        remove_first(): Удаляет первый элемент списка.
        remove_last(): Удаляет последний элемент списка.
        get(index): Получает элемент по индексу.
        clear(): Очищает список.
        get_version(version): Получает список в определенной версии.
        update_version(version): Обновляет текущую версию до указанной.
        clone(): Создает копию списка.
        __getitem__(index): Доступ к элементу по индексу (аналог get).
        __setitem__(index, value): Заменяет элемент по индексу.
    """

    empty_message = "Список пуст"
    full_message = "Список полон"
    invalid_index_message = "Неверный индекс"
    invalid_version_message = "Неверная версия"

    def __init__(self, max_size=None):
        """
        Инициализация персистентного двусвязного списка.

        Параметры:
            max_size (int, optional): Максимальный размер списка.
            По умолчанию равен 1024.
        """
        self.max_size = max_size or 2 ** 10
        self.head = None  # Голова списка
        self.tail = None  # Хвост списка
        self.history = []  # История состояний списка

    def _get_current_state(self):
        """
        Возвращает текущее состояние списка (последнюю версию).

        Возвращаемое значение:
            list: Текущее состояние списка (список значений).
        """
        if not self.history:
            return []
        return self.history[-1]

    def _check_index(self, index):
        """
        Проверяет, является ли индекс допустимым.

        Параметры:
            index (int): Индекс для проверки.

        Исключения:
            IndexError: Если индекс выходит за пределы списка.
        """
        if index < 0 or index >= self.size():
            raise IndexError(self.invalid_index_message)

    def check_is_empty(self):
        """
        Проверяет, пуст ли список.

        Возвращаемое значение:
            bool: True, если список пуст, иначе False.
        """
        return self.size() == 0

    def size(self):
        """
        Возвращает количество элементов в списке.

        Возвращаемое значение:
            int: Размер списка.
        """
        size = 0
        current = self.head
        while current:
            size += 1
            current = current.next_node
        return size

    def add(self, value):
        """
        Добавляет элемент в конец списка.

        Параметры:
            value: Значение для добавления.

        Исключения:
            ValueError: Если список достиг максимального размера.
        """
        if self.size() >= self.max_size:
            raise ValueError(self.full_message)
        new_node = Node(value=value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next_node = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.save_to_history()

    def insert(self, index, value):
        """
        Вставляет элемент в список по указанному индексу.

        Параметры:
            index (int): Индекс, на который нужно вставить элемент.
            value: Значение для вставки.

        Исключения:
            ValueError: Если список достиг максимального размера.
            IndexError: Если индекс недействителен.
        """
        if self.size() >= self.max_size:
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

    def add_first(self, value):
        """
        Добавляет элемент в начало списка.

        Параметры:
            value: Значение для добавления в начало.

        Исключения:
            ValueError: Если список достиг максимального размера.
        """
        if self.size() >= self.max_size:
            raise ValueError(self.full_message)
        new_node = Node(value=value, next_node=self.head)
        if self.head:
            self.head.prev = new_node
        self.head = new_node
        if not self.tail:
            self.tail = new_node
        self.save_to_history()

    def remove(self, index):
        """
        Удаляет элемент по индексу.

        Параметры:
            index (int): Индекс элемента для удаления.

        Исключения:
            IndexError: Если индекс недействителен.
            ValueError: Если список пуст.
        """
        self._check_index(index)
        if index == 0:
            self.remove_first()
        elif index == self.size() - 1:
            self.remove_last()
        else:
            current = self.head
            for _ in range(index):
                current = current.next_node
            current.prev.next_node = current.next_node
            if current.next_node:
                current.next_node.prev = current.prev
            self.save_to_history()

    def remove_first(self):
        """
        Удаляет первый элемент списка.

        Исключения:
            ValueError: Если список пуст.
        """
        if self.check_is_empty():
            raise ValueError(self.empty_message)
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next_node
            self.head.prev = None
        self.save_to_history()

    def remove_last(self):
        """
        Удаляет последний элемент списка.

        Исключения:
            ValueError: Если список пуст.
        """
        if self.check_is_empty():
            raise ValueError(self.empty_message)
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next_node = None
        self.save_to_history()

    def get(self, index):
        """
        Возвращает элемент по индексу.

        Параметры:
            index (int): Индекс элемента для получения.

        Возвращаемое значение:
            value: Значение элемента по индексу.

        Исключения:
            IndexError: Если индекс недействителен.
        """
        self._check_index(index)
        current = self.head
        for _ in range(index):
            current = current.next_node
        return current.value

    def clear(self):
        """
        Очищает список.

        Сбрасывает все элементы и историю изменений.
        """
        self.head = self.tail = None
        self.save_to_history()

    def save_to_history(self):
        """
        Сохраняет текущее состояние списка в историю.

        Состояние представлено списком значений всех элементов в списке.
        """
        current_state = []
        current = self.head
        while current:
            current_state.append(current.value)
            current = current.next_node
        self.history.append(current_state)

    def get_version(self, version):
        """
        Возвращает версию списка.

        Параметры:
            version (int): Индекс версии для получения.

        Возвращаемое значение:
            list: Состояние списка на указанной версии.

        Исключения:
            ValueError: Если версия недействительна.
        """
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)
        return self.history[version]

    def update_version(self, version):
        """
        Обновляет текущую версию списка.

        Параметры:
            version (int): Индекс версии для обновления.

        Исключения:
            ValueError: Если версия недействительна.
        """
        if version < 0 or version >= len(self.history):
            raise ValueError(self.invalid_version_message)
        state = self.history[version]
        self.clear()
        for value in state:
            self.add(value)

    def clone(self):
        """
        Создает копию списка, включая все элементы.

        Возвращаемое значение:
            PersistentLinkedList: Новый персистентный список, идентичный текущему.
        """
        new_list = PersistentLinkedList(self.max_size)
        current = self.head
        while current:
            new_list.add(current.value)
            current = current.next_node
        return new_list

    def __getitem__(self, index):
        """
        Доступ к элементу по индексу (аналог метода get).

        Параметры:
            index (int): Индекс элемента для получения.

        Возвращаемое значение:
            value: Значение элемента.
        """
        return self.get(index)

    def __setitem__(self, index, value):
        """
        Заменяет элемент по индексу.

        Параметры:
            index (int): Индекс элемента для замены.
            value: Новое значение для замены.
        """
        self.remove(index)
        self.insert(index, value)
