from copy import deepcopy


class PersistentMap:
    """Персистентный ассоциативный массив.

    Представляет собой словарь, который сохраняет историю изменений.

    Примеры использования:
    >>> map = PersistentMap({'foo': 'bar'}) # Создаем пустой ассоциативный массив
    >>> map['key'] = 'value' # Добавляем элемент
    >>> map['key'] = 'value2' # Изменяем элемент в следующей версии
    >>> map['key'] # Получаем элемент последней версии
    'value2'
    >>> map.get(1, 'key')
    {'key': 'value'}
    >>> map.remove('key') # Удаляем элемент в новой версии
    >>> map.clear() # Очищаем ассоциативный массив в новой версии
    >>> map.get(0, 'key') # Пытаемся получить элемент отсутствующий в переданной версии
    Traceback (most recent call last):
        ...
    KeyError: Key "key" does not exist

    """
    def __init__(self, dictionary: dict = {}):
        self._history = {0: dictionary}
        self._current_state = 0

    def __setitem__(self, key, value):
        """Обновляет или создает элемент по указанному ключу в новой версии."""
        self._update_version()
        self.history[self.current_state][key] = value

    def __getitem__(self, key):
        """Возвращает элемент последней версии по указанному ключу."""
        return self.history[self.current_state][key]

    def get(self, version: int, key: int):
        """Возвращает элемент с указанной версией и ключом."""
        if version > self.current_state or version < 0:
            raise ValueError(f'Version "{version}" does not exist')
        if key not in self.history[version]:
            raise KeyError(f'Key "{key}" does not exist')
        return self.history[version]

    def remove(self, key):
        """Удаляет элемент по указанному ключу в новой версии."""
        self._update_version()
        self.history[self.current_state].pop(key)

    def clear(self):
        """Очищает ассоциативный массив в новой версии."""
        self._update_version()
        self.history[self.current_state] = {}

    def _update_version(self):
        """Обновляет текущую версию и сохраняет копию предыдущей версии."""
        self.current_state += 1
        self.history[self.current_state] = deepcopy(self.history[self.current_state-1])
