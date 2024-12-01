class PersistentList:
    """
    Персистентный двухсвязный список,
    реализующий метод path copying.

    Этот список сохраняет историю изменений и позволяет
    получать доступ к предыдущим версиям списка.
    Операции вставки, удаления и доступа к элементам поддерживают
    создание новых версий списка, сохраняя при этом
    неизменными предыдущие.

    Примеры использования:
    >>> p_list = PersistentList()  # Создаем пустой список
    # Добавляем элементы в список
    >>> p_list.add(1) # Добавляем элемент 1 -> версия 0
    >>> p_list.add(2) # Добавляем элемент 1 -> версия 1
    >>> p_list.add(3) # Добавляем элемент 1 -> версия 2
    >>> p_list._get_current_state() # Текущее состояние списка
    [1, 2, 3]
    >>> p_list.get(1) # Получение элемента по индексу
    2
    >>> p_list.remove(1) #Удаляем элемент по индексу -> версия 3
    >>> p_list._get_current_state()
    [1, 3]
    >>> p_list.get_version(2) # Состояние списка на версии 2
    [1, 2, 3]
    >>> p_list.get_version(3) # Состояние списка на версии 3
    [1, 3]
    >>> p_list.update_version(3) # Обновляем текущую версию
    >>> p_list._get_current_state()
    [1, 3]

    Traceback (most recent call last):
        ...
    IndexError: Неверный индекс

    Атрибуты:
    - max_size: максимальный размер списка.
    - depth: глубина структуры для хранения данных.
    - bits_for_level: количество бит на один элемент.
    - history: история состояний списка.

    Методы:
    - add(element): Добавляет элемент в конец списка.
    - insert(index, element): Вставляет элемент в список на указанную позицию.
    - remove(index): Удаляет элемент по указанному индексу.
    - get(index): Возвращает элемент по указанному индексу.
    - pop(): Удаляет и возвращает последний элемент.
    - clear(): Очищает список.
    - clone(): Создает и возвращает копию списка.
    - get_version(version): Возвращает состояние списка на указанной версии.
    - update_version(version): Обновляет текущую версию списка на указанную.
    """
    empty_array_message = "Список пуст"
    full_array_message = "Список полон"
    invalid_index_message = "Неверный индекс"
    invalid_version_message = "Неверная версия"

    def __init__(self, max_size=None, depth=5, bits_for_level=4):
        """
        Инициализирует список с указанными параметрами.
        :param max_size: Максимальный размер списка (если не указан,
        используется размер по умолчанию).
        :param depth: Глубина структуры (по умолчанию 5).
        :param bits_for_level: Число бит на один элемент (по умолчанию 4).
        """
        self.depth = depth
        self.bits_for_level = bits_for_level
        self.max_size = max_size or 2 ** (depth * bits_for_level)
        self.history = []  # История состояний списка

    def _get_current_state(self):
        """
        Возвращает текущее состояние списка (последнюю версию).
        :return: Текущее состояние списка.
        """
        if not self.history:
            return []
        return self.history[-1]

    def _check_index(self, index):
        """
        Проверяет, является ли индекс допустимым.
        :param index: Индекс для проверки.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        if index < 0 or index >= len(self._get_current_state()):
            raise IndexError(self.invalid_index_message)

    def _check_version(self, version):
        """
        Проверяет, является ли версия допустимой.
        :param version: Номер версии.
        :raises ValueError: Если версия недопустима.
        """
        if version < 0 or version >= len(self.history):
            raise ValueError(f"Неверная версия: {version}")

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
        self.history.append(current_state + [element])

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
        self.history.append(current_state[:index] + [element] + current_state[index:])

    def remove(self, index):
        """
        Удаляет элемент по указанному индексу.
        :param index: Индекс элемента для удаления.
        :raises IndexError: Если индекс недопустим.
        """
        self._check_index(index)
        current_state = self._get_current_state()
        self.history.append(current_state[:index] + current_state[index + 1:])

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
        self.history.append(new_state)
        return current_state[-1]

    def clear(self):
        """
        Очищает список, создавая новое пустое состояние.
        """
        self.history.append([])

    def clone(self):
        """
        Создаёт и возвращает новый список, который является копией текущего.
        :return: Клонированный список.
        """
        new_list = PersistentList(self.max_size, self.depth, self.bits_for_level)
        new_list.history = self.history[:]
        return new_list

    def get_version(self, version):
        """
        Возвращает состояние списка на указанной версии.
        :param version: Номер версии.
        :return: Состояние списка в указанной версии.
        :raises ValueError: Если версия недопустима.
        """
        self._check_version(version)
        return self.history[version]

    def update_version(self, version):
        """
        Обновляет текущую версию списка на указанную.
        :param version: Номер версии, которую нужно сделать текущей.
        :raises ValueError: Если версия недопустима.
        """
        self._check_version(version)
        current_state = self.history[version]
        self.history.append(current_state[:])

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
        self.history.append(current_state[:index] + [value] + current_state[index + 1:])
