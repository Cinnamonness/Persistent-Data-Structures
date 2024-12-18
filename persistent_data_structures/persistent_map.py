from base_persistent import BasePersistent
from typing import Any


class PersistentMap(BasePersistent):
    """Персистентный ассоциативный массив.

    Представляет собой словарь, сохраняющий историю изменений.
    """

    def __init__(self, initial_state: dict[Any, Any] = {}) -> None:
        """Инициализирует персистентный ассоциативный массив.

        :param initial_state: Начальное состояние персистентной структуры данных.
        """
        super().__init__(initial_state)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Обновляет или создаёт элемент по указанному ключу в новой версии.

        :param key: Ключ, который нужно обновить или создать.
        :param value: Значение, связанное с указанным ключом.
        """
        self._create_new_state()
        self._version_map[self._last_version].state[key] = value

    def __getitem__(self, key: Any) -> Any:
        """Возвращает элемент текущей версии по указанному ключу.

        :param key: Ключ элемента, который нужно получить.
        :return: Значение, соответствующее указанному ключу, или None, если ключ не существует.
        """
        return self._version_map[self._current_version].state.get(key)

    def get(self, version: int, key: Any) -> Any:
        """Возвращает элемент из указанной версии по ключу.

        :param version: Номер версии.
        :param key: Ключ элемента, который нужно получить.
        :return: Значение, соответствующее указанному ключу.
        :raises ValueError: Если версия не существует.
        :raises KeyError: Если ключ не существует.
        """
        if version not in self._version_map:
            raise ValueError(f'Version "{version}" does not exist')
        if key not in self._version_map[version].state:
            raise KeyError(f'Key "{key}" does not exist')
        return self._version_map[version].state[key]

    def pop(self, key: Any) -> Any:
        """Удаляет и возвращает элемент по указанному ключу.

        :param key: Ключ элемента, который нужно удалить.
        :return: Удалённый элемент.
        """
        self._create_new_state()
        return self._version_map[self._last_version].state.pop(key)

    def remove(self, key: Any) -> None:
        """Удаляет элемент по указанному ключу в новой версии.

        :param key: Ключ элемента, который нужно удалить.
        """
        self.pop(key)

    def clear(self) -> None:
        """Очищает ассоциативный массив в новой версии."""
        self._create_new_state()
        self._version_map[self._current_version].state.clear()
