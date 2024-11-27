class FatNodeArray:
    """
    Реализация метода Fat Node для персистентных массивов.
    """
    empty_array_message = "Массив пуст"
    full_array_message = "Массив полон"
    invalid_index_message = "Неверный индекс"

    def __init__(self, max_size=None, depth=5, bits_for_level=4):
        """
        Инициализирует массив с указанными параметрами.
        :param max_size: Максимальный размер массива (если не
        указан, используется размер по умолчанию).
        :param depth: Глубина структуры (по умолчанию 5).
        :param bits_for_level: Число бит на один элемент (по умолчанию 4).
        """
        self.depth = depth
        self.bits_for_level = bits_for_level
        self.max_size = max_size or 2 ** (depth * bits_for_level)
        self.history = []  # История состояний массива
        self.add_head()  # Изначальное состояние массива

    def add_head(self):
        """
        Добавляет новое состояние (голову) массива,
        которое изначально пустое.
        """
        self.history.append([])

    def _get_current_state(self):
        """
        Возвращает текущее состояние массива
        (последнюю версию).
        :return: Текущее состояние массива.
        """
        return self.history[-1]

    def _check_index(self, index):
        """
        Проверяет, является ли индекс допустимым.
        :param index: Индекс для проверки.
        :raises IndexError: Если индекс выходит за
        пределы массива.
        """
        if index < 0 or index >= len(self._get_current_state()):
            raise IndexError(self.invalid_index_message)

    def is_empty(self):
        """
        Проверяет, пуст ли массив.
        :return: True, если массив пуст, иначе False.
        """
        return len(self._get_current_state()) == 0

    def size(self):
        """
        Возвращает текущий размер массива.
        :return: Размер массива.
        """
        return len(self._get_current_state())

    def is_full(self):
        """
        Проверяет, полон ли массив.
        :return: True, если массив полон, иначе False.
        """
        return len(self._get_current_state()) >= self.max_size

    def add(self, element):
        """
        Добавляет элемент в конец массива.
        :param element: Элемент, который необходимо добавить.
        :raises ValueError: Если массив полон.
        """
        if self.is_full():
            raise ValueError(self.full_array_message)

        current_state = self._get_current_state()
        # Сохраняем ссылку на предыдущее состояние (fat node)
        new_node = {'value': element, 'prev': current_state}
        self.history.append(current_state + [new_node])

    def insert(self, index, element):
        """
        Вставляет элемент в массив на указанную позицию.
        :param index: Индекс, куда нужно вставить элемент.
        :param element: Элемент, который нужно вставить.
        :raises IndexError: Если индекс недопустим.
        :raises ValueError: Если массив полон.
        """
        self._check_index(index)
        if self.is_full():
            raise ValueError(self.full_array_message)

        current_state = self._get_current_state()
        # Вставляем новый элемент с ссылкой на предыдущее состояние
        new_node = {'value': element, 'prev': current_state}
        self.history.append(current_state[:index] +
                            [new_node] + current_state[index:])

    def remove(self, index):
        """
        Удаляет элемент по указанному индексу.
        :param index: Индекс элемента для удаления.
        :raises IndexError: Если индекс недопустим.
        """
        self._check_index(index)
        current_state = self._get_current_state()
        self.history.append(current_state[:index]
                             + current_state[index + 1:])

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
        Удаляет и возвращает последний элемент массива.
        :return: Удалённый элемент.
        :raises ValueError: Если массив пуст.
        """
        if self.is_empty():
            raise ValueError(self.empty_array_message)

        current_state = self._get_current_state()
        self.history.append(current_state[:-1])
        return current_state[-1]

    def clear(self):
        """
        Очищает массив, создавая новое пустое состояние.
        :return: None
        """
        self.history.append([])

    def clone(self):
        """
        Создаёт и возвращает новый массив, который является копией текущего.
        :return: Клонированный массив.
        """
        new_array = FatNodeArray(self.max_size,
                                 self.depth, self.bits_for_level)
        new_array.history = self.history[:]
        return new_array

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
        current_state = self._get_current_state()
        self.history.append(current_state[:index] +
                            [{'value': value, 'prev': current_state}]
                              + current_state[index + 1:])
