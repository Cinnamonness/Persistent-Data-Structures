from base_persistent import BasePersistent, Node
from typing import Any, Optional


class ListNode:
    """Класс узла для хранения состояния в двусвязном списке."""

    def __init__(self, value: Any = None, prev: Optional['ListNode'] = None,
                 next_node: Optional['ListNode'] = None) -> None:
        """
        Инициализация узла списка.

        :param value: Значение, которое будет храниться в узле.
        :param prev: Ссылка на предыдущий узел (по умолчанию None).
        :param next_node: Ссылка на следующий узел (по умолчанию None).
        """
        self.value = value
        self.prev = prev
        self.next_node = next_node
        self.children = {}


class PersistentLinkedList(BasePersistent):
    """Персистентный двусвязный список, использующий базовый класс для версионирования."""

    def __init__(self, initial_state: Optional[list[Any]] = None) -> None:
        """
        Инициализация персистентного списка.

        :param initial_state: Начальный список данных для создания состояния (по умолчанию None).
        """
        super().__init__(initial_state)
        self.size = 0
        head = tail = None

        if initial_state:
            for data in initial_state:
                node = ListNode(data)
                if head is None:
                    head = tail = node
                else:
                    tail.next_node = node
                    node.prev = tail
                    tail = node
            self.size = len(initial_state)

        self._version_map[0] = Node(head)

    def add(self, data: Any) -> None:
        """Добавляет элемент в конец списка в новой версии."""
        self._create_new_state_doubly_linked_list()
        head = self._version_map[self._current_version].state
        tail = self._get_tail(head)
        new_node = ListNode(data)

        if tail:
            tail.next_node = new_node
            new_node.prev = tail
        else:
            head = new_node

        self._version_map[self._current_version].state = head
        self.size += 1

    def add_first(self, data: Any) -> None:
        """
        Добавляет элемент в начало списка в новой версии.

        :param data: Данные, которые нужно добавить в начало списка.
        :return: None
        """
        self._create_new_state_doubly_linked_list()
        head = self._version_map[self._current_version].state
        new_node = ListNode(data, next_node=head)

        if head:
            head.prev = new_node

        head = new_node
        self._version_map[self._current_version].state = head
        self.size += 1

    def insert(self, index: int, data: Any) -> None:
        """Вставляет элемент в список по указанному индексу."""
        self._create_new_state_doubly_linked_list()
        head = self._version_map[self._current_version].state
        current = head
        count = 0

        if index == 0:
            new_node = ListNode(data, next_node=head)
            if head:
                head.prev = new_node
            head = new_node
            self._version_map[self._current_version].state = head
            self.size += 1
            return

        while current:
            if count == index:
                new_node = ListNode(data, prev=current.prev, next_node=current)
                if current.prev:
                    current.prev.next_node = new_node
                current.prev = new_node
                if current == head:
                    head = new_node
                self.size += 1
                break
            count += 1
            current = current.next_node
        else:
            raise IndexError("Index out of range")

        self._version_map[self._current_version].state = head

    def pop(self, index: int) -> Any:
        """
        Удаление элемента в новой версии списка и возвращение его значения.

        :param index: Индекс элемента для удаления.
        :return: Значение удаленного элемента.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        self._create_new_state_doubly_linked_list()
        head = self._version_map[self._current_version].state
        current = head
        count = 0

        while current:
            if count == index:
                value = current.value
                if current.prev:
                    current.prev.next_node = current.next_node
                if current.next_node:
                    current.next_node.prev = current.prev
                if current == head:
                    head = current.next_node
                self.size -= 1
                break
            count += 1
            current = current.next_node
        else:
            raise IndexError("Index out of range")

        self._version_map[self._current_version].state = head
        return value

    def remove(self, value: Any) -> None:
        """
        Удаляет элемент из списка в новой версии.

        :param value: Данные элемента для удаления.
        :return: None
        :raises ValueError: Если элемент не найден в списке.
        """
        self._create_new_state_doubly_linked_list()
        head = self._version_map[self._current_version].state
        current = head

        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next_node = current.next_node
                if current.next_node:
                    current.next_node.prev = current.prev
                if current == head:
                    head = current.next_node
                self.size -= 1
                break
            current = current.next_node
        else:
            raise ValueError(f"Value {value} not found in the list")

        self._version_map[self._current_version].state = head

    def get(self, version: int = None, index: int = None) -> Any:
        """
        Возвращает элемент по индексу из указанной версии.

        :param version: Номер версии (по умолчанию текущая версия).
        :param index: Индекс элемента для получения.
        :return: Значение элемента на указанной версии и индексе.
        :raises ValueError: Если указанная версия не существует.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        if version is None:
            version = self._current_version

        if version not in self._version_map:
            raise ValueError(f"Version {version} does not exist")
        head = self._version_map[version].state
        current = head
        count = 0

        while current:
            if count == index:
                return current.value
            count += 1
            current = current.next_node

        raise IndexError("Index out of range")

    def _get_tail(self, head: ListNode) -> Optional[ListNode]:
        """Возвращает последний узел в списке."""
        current = head
        while current and current.next_node:
            current = current.next_node
        return current

    def clear(self) -> None:
        """Очищает список, создавая новую версию."""
        self._create_new_state_doubly_linked_list()
        self._version_map[self._current_version].state = None
        self.size = 0

    def __getitem__(self, index: int) -> Any:
        """
        Получение значения элемента из текущей версии списка по индексу.

        :param index: Индекс элемента в текущей версии списка.
        :return: Значение элемента в текущей версии списка по заданному индексу.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        head = self._version_map[self._current_version].state
        current = head
        count = 0
        while current:
            if count == index:
                return current.value
            count += 1
            current = current.next_node
        raise IndexError("Index out of range")

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Обновление значения элемента в новой версии списка по индексу.

        :param index: Индекс элемента, который необходимо обновить.
        :param value: Новое значение для обновляемого элемента.
        :raises IndexError: Если индекс выходит за пределы списка.
        """
        self._create_new_state()
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
        self._version_map[self._last_state] = (head, tail)

    def _deep_copy_list(self, head: ListNode) -> Optional[ListNode]:
        """Глубокое копирование списка с его узлами."""
        if not head:
            return None

        new_head = ListNode(head.value)
        current = head.next_node
        new_current = new_head

        while current:
            new_node = ListNode(current.value)
            new_current.next_node = new_node
            new_node.prev = new_current
            new_current = new_node
            current = current.next_node

        return new_head

    def get_size(self) -> int:
        """
        Получение текущего размера списка.

        :return: Количество элементов в текущей версии списка.
        """
        return self.size

    def check_is_empty(self) -> bool:
        """
        Проверяет, пуст ли список.

        :return: True, если список пуст, иначе False.
        """
        head = self._version_map[self._current_version].state
        return head is None

    def __str__(self) -> str:
        """Отображение списка для вывода."""
        head = self._version_map[self._current_version].state
        result = []
        current = head
        while current:
            result.append(current.value)
            current = current.next_node
        return '->'.join(map(str, result))
