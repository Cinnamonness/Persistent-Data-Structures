from persistent_data_structures.base_persistent import BasePersistent
from time import sleep


class PersistentMap(BasePersistent):
    """Персистентный ассоциативный массив.

    Представляет собой словарь, который сохраняет историю изменений.
    """

    def __setitem__(self, key: any, value: any) -> None:
        """Обновляет или создает элемент по указанному ключу в новой версии.

        :param key: Ключ
        :param value: Значение
        """
        self._mutex.acquire()
        self._create_new_state()
        self._history[self._last_state][key] = value
        sleep(1.0)
        self._mutex.release()

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
        if key not in self._history[self._current_state]:
            raise KeyError(f'Key "{key}" does not exist')
        self._mutex.acquire()
        self._create_new_state()
        popped_item = self._history[self._last_state].pop(key)
        self._mutex.release()
        return popped_item

    def remove(self, key: any) -> None:
        """Удаляет элемент по указанному ключу в новой версии.

        :param key: Ключ
        """
        self.pop(key)

    def clear(self) -> None:
        """Очищает ассоциативный массив в новой версии."""
        self._mutex.acquire()
        self._create_new_state()
        self._history[self._current_state] = {}
        self._mutex.release()
