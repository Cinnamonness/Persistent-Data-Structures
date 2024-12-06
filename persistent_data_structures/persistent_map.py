from persistent_data_structures.base_persistent import BasePersistent


class PersistentMap(BasePersistent):
    """Персистентный ассоциативный массив.

    Представляет собой словарь, который сохраняет историю изменений.
    """
    def __init__(self, initial_state: dict = {}) -> None:
        """Инициализирует персистентный ассоциативный массив.

        :param initial_state: Начальное состояние персистентной структуры данных.
        """
        super().__init__(initial_state)

    def __setitem__(self, key: any, value: any) -> None:
        """Обновляет или создает элемент по указанному ключу в новой версии.

        :param key: Ключ
        :param value: Значение
        """
        self._create_new_state()
        self._history[self._last_state][key] = value

    def __getitem__(self, key: any) -> any:
        """Возвращает элемент текущей версии по указанному ключу.

        :param key: Ключ
        :return: Значение сответствующее указанному ключу или None, если ключ не существует."""
        return self._history[self._current_state][key]

    def get(self, version: int, key: any) -> any:
        """Возвращает элемент с указанной версией и ключом.

        :param version: Номер версии
        :param key: Ключ
        :return: Значение сответствующее указанному ключу или None, если ключ не существует.
        :raises ValueError: Если версия не существует
        :raises KeyError: Если ключ не существует
        """
        if version > self._current_state or version < 0:
            raise ValueError(f'Version "{version}" does not exist')
        if key not in self._history[version]:
            raise KeyError(f'Key "{key}" does not exist')
        return self._history[version]

    def pop(self, key: any) -> any:
        """Удаляет элемент по указанному ключу и возвращает его.

        :param key: Ключ
        :return: Удаленный элемент
        """
        self._create_new_state()
        return self._history[self._last_state].pop(key)

    def remove(self, key: any) -> None:
        """Удаляет элемент по указанному ключу в новой версии.

        :param key: Ключ
        """
        self.pop(key)

    def clear(self) -> None:
        """Очищает ассоциативный массив в новой версии."""
        self._create_new_state()
        self._history[self._current_state] = {}
