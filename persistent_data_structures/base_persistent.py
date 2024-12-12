from copy import deepcopy
from typing import Optional, Dict


class NodeState:
    """Класс, представляющий состояние узла. Он может быть определен
      в зависимости от структуры данных."""
    def __init__(self, data: Optional['NodeState'] = None):
        self.data = data
        self.next_node: Optional['NodeState'] = None


class Node:
    """Класс узла для хранения состояния в B-дереве."""
    def __init__(self, state: Optional[NodeState]) -> None:
        """
        Инициализирует узел с заданным состоянием.

        :param state: Состояние узла.
        """
        self.state: Optional[NodeState] = state
        self.children: Dict[int, 'Node'] = {}


class BasePersistent:
    """Базовый класс для персистентных структур данных с использованием B-дерева."""

    def __init__(self, initial_state: Optional[NodeState] = None) -> None:
        """
        Инициализирует персистентную структуру данных.

        :param initial_state: Начальное состояние персистентной структуры данных.
        """
        self.root: Node = Node(initial_state)
        self._current_version: int = 0
        self._last_version: int = 0
        self._version_map: Dict[int, Node] = {0: self.root}

    def get_version(self, version: int) -> NodeState:
        """
        Возвращает состояние персистентной структуры данных на указанной версии.

        :param version: Номер версии.
        :return: Состояние персистентной структуры данных на указанной версии.
        :raises ValueError: Если указанная версия не существует.
        """
        if version not in self._version_map:
            raise ValueError(f'Version "{version}" does not exist')
        return self._version_map[version].state

    def set_version(self, version: int) -> None:
        """
        Обновляет текущую версию персистентной структуры данных до указанной.

        :param version: Номер версии.
        :raises ValueError: Если указанная версия не существует.
        """
        if version not in self._version_map:
            raise ValueError(f'Version "{version}" does not exist')
        self._current_version = version
        self.root = self._version_map[version]

    def set_version_doubly_linked_list(self, version: int) -> None:
        """
        Обновляет текущую версию персистентной структуры данных до
        указанной для двусвязного списка.

        :param version: Номер версии.
        :raises ValueError: Если указанная версия не существует.
        """
        if version not in self._version_map:
            raise ValueError(f'Version "{version}" does not exist')
        self._current_version = version
        self.root = self._version_map[version]
        head = self._version_map[self._current_version].state
        self.size: int = 0
        current = head
        while current:
            self.size += 1
            current = current.next_node
        self._version_map[self._current_version].state = head

    def _create_new_state(self) -> None:
        """
        Создает новую версию персистентной структуры данных с
        минимальным дублированием данных.

        Этот метод копирует текущее состояние структуры данных и создает
        новую версию, добавляя ее в карту версий.
        Дублирование данных минимизируется путем использования глубокого
        копирования состояния узла.

        :raises ValueError: Если текущая версия не существует в карте версий.
        """
        self._last_version += 1
        parent_node = self._version_map[self._current_version]
        new_state = deepcopy(parent_node.state)
        new_node = Node(new_state)
        parent_node.children[self._last_version] = new_node
        self._version_map[self._last_version] = new_node
        self._current_version = self._last_version
        self.root = new_node

    def _create_new_state_doubly_linked_list(self) -> None:
        """
        Создает новую версию состояния для двусвязного списка,
        минимизируя дублирование данных.

        Этот метод копирует состояние двусвязного списка, создавая
        новый узел с минимальным дублированием
        данных, чтобы сохранить версионность структуры данных.

        :raises ValueError: Если текущая версия не существует в карте версий.
        """
        self._current_version += 1
        head = self._version_map[self._current_version - 1].state
        new_head = self._deep_copy_list(head)
        self._version_map[self._current_version] = Node(new_head)
