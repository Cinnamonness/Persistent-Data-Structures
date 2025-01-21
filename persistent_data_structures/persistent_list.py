from copy import deepcopy

from base_persistent import BasePersistent


class Node:
    """
    Класс для узлов двусвязного списка.
    """

    def __init__(self, value: any = None, prev: 'Node' = None, next_node: 'Node' = None) -> None:
        """
        Инициализирует новый узел.

        :param value: Значение для хранения в узле (по умолчанию None).
        :param prev: Ссылка на предыдущий узел (по умолчанию None).
        :param next_node: Ссылка на следующий узел (по умолчанию None).
        """
        self.value = value
        self.prev = prev
        self.next_node = next_node


class PersistentLinkedList(BasePersistent):
    """Персистентный двусвязный список.
    Класс PersistentLinkedList реализует неизменяемый двусвязный список
    с возможностью хранения нескольких версий, где каждая
    версия является изменением предыдущей.
    """

    def __init__(self, initial_state: list = None) -> None:
        """
        Инициализирует персистентный двусвязный список.

        :param initial_state: Начальное состояние списка, если оно передано.
        :return: None
        """
        super().__init__(None)
        self.size = 0
        head = tail = None
        if initial_state:
            for data in initial_state:
                node = Node(data)
                if head is None:
                    head = tail = node
                else:
                    tail.next_node = node
                    node.prev = tail
                    tail = node
            self.size = len(initial_state)
        self._history[0] = (head, tail)

    def add(self, data: any) -> None:
        """
        Добавляет элемент в конец списка в новой версии.

        :param data: Данные, которые нужно добавить в список.
        :return: None
        """
        self._create_new_state()
        head, tail = self._history[self._last_state]
        if isinstance(data, BasePersistent):
            data._container = self
            data._location = self.size
        new_node = Node(data)
        if tail is None:
            head = tail = new_node
        else:
            tail.next_node = new_node
            new_node.prev = tail
            tail = new_node
        self.size += 1
        self._history[self._last_state] = (head, tail)

    def add_first(self, data: any) -> None:
        """
        Добавляет элемент в начало списка в новой версии.

        :param data: Данные, которые нужно добавить в начало списка.
        :return: None
        """
        self._create_new_state()
        head, tail = self._history[self._last_state]
        if isinstance(data, BasePersistent):
            data._container = self
            data._location = 0
        new_node = Node(data, next_node=head)
        if head:
            head.prev = new_node
        head = new_node
        if tail is None:
            tail = new_node
        self.size += 1
        # сдвигаем индексы персистентных элементов
        current = head
        while current.next_node:
            current = current.next_node
            if isinstance(current.value, BasePersistent):
                current.value._location += 1

        self._history[self._last_state] = (head, tail)

    def insert(self, index: int, data: any) -> None:
        """
        Вставляет элемент в список по указанному индексу.

        :param index: Индекс, на котором нужно вставить элемент.
        :param data: Данные, которые нужно вставить.
        :return: None
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        self._create_new_state()
        head, tail = self._history[self._last_state]
        if isinstance(data, BasePersistent):
            data._container = self
            data._location = index

        current = head
        count = 0
        while current:
            if count == index:
                new_node = Node(data, prev=current.prev, next_node=current)
                if current.prev:
                    current.prev.next_node = new_node
                current.prev = new_node
                if current == head:
                    head = new_node
                self.size += 1
                count += 1

            if isinstance(current.value, BasePersistent) and count > index:
                current.value._location += 1
            count += 1
            current = current.next_node
        self._history[self._last_state] = (head, tail)

    def pop(self, index: int) -> any:
        """
        Удаление элемента в новой версии списка и возвращение его значения.

        :param index: Индекс элемента для удаления.
        :return: Значение удаленного элемента.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        self._create_new_state()
        head, tail = self._history[self._last_state]
        popped_value = self.__getitem__(index)
        current = head
        count = 0
        while current:
            if count == index:
                if current.prev:
                    current.prev.next_node = current.next_node
                if current.next_node:
                    current.next_node.prev = current.prev
                if current == head:
                    head = current.next_node
                if current == tail:
                    tail = current.prev

                self.size -= 1
                self._history[self._last_state] = (head, tail)

            if isinstance(current.value, BasePersistent) and count > index:
                current.value._location -= 1
            count += 1
            current = current.next_node
        return popped_value

    def remove(self, index: int) -> None:
        """
        Удаляет элемент по индексу из списка в новой версии.

        :param index: Индекс элемента для удаления.
        :return: None
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        self.pop(index)

    def get(self, version: int = None, index: int = None) -> any:
        """
        Возвращает элемент по индексу из указанной версии.

        :param version: Номер версии (по умолчанию текущая версия).
        :param index: Индекс элемента для получения.
        :return: Значение элемента на указанной версии и индексе.
        :raises ValueError: Если указанная версия не существует.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        if version is None:
            version = self._current_state
        if version > self._current_state or version < 0:
            raise ValueError(f"Version {version} does not exist")
        head, tail = self._history[version]
        if head is None:
            raise IndexError("Index out of range")
        current = head
        count = 0
        while current:
            if count == index:
                return current.value
            count += 1
            current = current.next_node
        raise IndexError("Index out of range")

    def clear(self) -> None:
        """
        Очищает список, создавая новую версию.

        :return: None
        """
        self._create_new_state()
        self.size = 0
        self._history[self._last_state] = (None, None)

    def __getitem__(self, index: int) -> any:
        """
        Получение значения элемента из текущей версии списка по индексу.

        :param index: Индекс элемента в текущей версии списка.
        :return: Значение элемента в текущей версии списка по заданному индексу.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        head, tail = self._history[self._current_state]
        current = head
        count = 0
        while current:
            if count == index:
                return current.value
            count += 1
            current = current.next_node
        raise IndexError("Index out of range")

    def __setitem__(self, index: int, value: any) -> None:
        """
        Обновление значения элемента в новой версии списка по индексу.

        :param index: Индекс элемента, который необходимо обновить.
        :param value: Новое значение для обновляемого элемента.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        self._create_new_state()
        if isinstance(value, BasePersistent):
            value._container = self
            value._location = index
        head, tail = self._history[self._last_state]
        current = head
        count = 0
        while current:
            if count == index:
                current.value = value
                break
            count += 1
            current = current.next_node
        else:
            raise IndexError("Index out of range")
        self._history[self._last_state] = (head, tail)

    def get_size(self) -> int:
        """
        Получение текущего размера списка.

        :return: Количество элементов в текущей версии списка.
        """
        return self.size

    def calc_size(self) -> int:
        """
        Расчет текущего размера списка.

        :return: Количество элементов в текущей версии списка.
        """
        size = 0
        head, tail = self._history[self._current_state]
        current = head
        while current:
            size += 1
            current = current.next_node
        return size

    def check_is_empty(self) -> bool:
        """
        Проверяет, пуст ли список.

        :return: True, если список пуст, иначе False.
        """
        head, tail = self._history[self._current_state]
        return head is None
    
    def update_version(self, version) -> None:
        """Обновляет текущую версию персистентной структуры данных до указанной.

        :param version: Номер версии.
        :raises ValueError: Если указанная версия не существует.
        """
        if version < 0 or version >= len(self._history):
            raise ValueError(f'Version "{version}" does not exist')
        self._current_state = version
        self.size = self.calc_size()

    def undo(self) -> None:
        """Отменяет последнее изменение."""
        if self._container is not None:
            raise NotImplementedError(f'Cannot undo inside container "{self._container}"')
        if self._current_state == 0:
            raise ValueError("No actions to undo")
        if self._current_state > 0:
            self._current_state -= 1
            self.size = self.calc_size()

    def redo(self) -> None:
        """Повторяет последнее отмененное изменение.

        :raises ValueError: Если нет операций."""
        if self._container is not None:
            raise NotImplementedError(f'Cannot redo inside container "{self._container}"')
        if self._current_state >= self._last_state:
            raise ValueError("No operations to redo")
        self._current_state += 1
        self.size = self.calc_size()

    def _create_new_state(self) -> None:
        """Создает новую версию."""
        # Персистентные структуры могут быть вложенными,
        # поэтому нужно сохранять историю изменений в родительской персистентной структуре
        if self._container is not None:
            # В текущей версии родительской структуры подменяем имеющуюся вложенную структуру
            # на ее копию, таким образом изменения во вложенной структуре не будут отражаться на
            # прощлых версиях родительской структуры
            head, tail = self._container._history[self._container._current_state]
            current = head
            while current:
                if current.value is self:
                    current.value = deepcopy(self)
                    break
                current = current.next_node
        self._last_state += 1
        self._history[self._last_state] = deepcopy(self._history[self._current_state])
        self._current_state = self._last_state
        if self._container is not None:
            self._container[self._location] = self
