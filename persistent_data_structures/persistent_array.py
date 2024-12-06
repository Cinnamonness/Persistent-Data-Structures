import numpy as np

from persistent_data_structures.base_persistent import BasePersistent


class PersistentArray(BasePersistent):
    """Персистентный массив.
    Класс PersistentArray реализует неизменяемый массив с
    возможностью хранения нескольких версий, где каждая
    версия является изменением предыдущей.
    """

    def __init__(self, size: int = 1024, default_value: int = 0) -> None:
        """Инициализирует новый массив с несколькими версиями.

        Создается первая версия массива, которая состоит из элементов,
        равных default_value.
        :param size: Начальный размер массива (по умолчанию 1024).
        :param default_value: Значение по умолчанию для элементов массива (по умолчанию 0).
        """
        self.size = size
        self.default_value = default_value
        initial_state = np.full(size, default_value)
        super().__init__(initial_state)

    def __getitem__(self, index: int) -> any:
        """Получение значения из текущей версии массива по индексу.

        :param index: Индекс элемента в текущей версии массива.
        :return: Значение элемента в текущей версии массива по заданному индексу.
        :raises ValueError: Если индекс выходит за пределы допустимого диапазона.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        return self._history[self._current_state][index]

    def get(self, version: int, index: int) -> any:
        """Получение значения элемента для определенной версии массива по индексу.

        :param version: Номер версии, из которой нужно получить элемент.
        :param index: Индекс элемента в указанной версии массива.
        :return: Значение элемента в указанной версии массива по заданному индексу.
        :raises ValueError: Если версия или индекс выходят за пределы допустимого диапазона.
        """
        if version > self._current_state or version < 0:
            raise ValueError(f'Version "{version}" does not exist')
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        return self._history[version][index]

    def add(self, value: any) -> None:
        """Добавление нового элемента в конец массива в новую версию.

        :param value (int): Значение нового элемента, который добавляется в массив.
        """
        self._create_new_state()
        self._history[self._last_state] = np.append(self._history[self._last_state], value)
        self.size += 1

    def pop(self, index: int) -> any:
        """Удаление элемента в новой версии массива и возвращение его значения.

        :param index (int): Индекс элемента, который необходимо удалить.
        :return int: Значение удаленного элемента.
        :raises ValueError: Если индекс выходит за пределы допустимого диапазона.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        removed_element = self._history[self._current_state][index]
        self._create_new_state()
        self._history[self._last_state] = np.delete(self._history[self._last_state], index)
        self.size -= 1
        return removed_element

    def __setitem__(self, index: int, value: any) -> None:
        """Обновление значения элемента в новую версии массива.

        Обновляет значение элемента из текущей версии массива по индексу
        и помещает получившийся массив в новую версию.
        :param index: Индекс элемента, который необходимо обновить.
        :param value: Новое значение для обновляемого элемента.
        :raises ValueError: Если индекс выходит за пределы допустимого диапазона.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        self._create_new_state()
        self._history[self._last_state][index] = value

    def insert(self, index: int, value: any) -> None:
        """Вставка нового элемента в массив в указанную позицию в новой версии.

        Вставляет новый элемент в указанную позицию в текущей версии массива и помещает
        получившийся массив в новую версию.
        :param index: Позиция, в которую нужно вставить новый элемент.
        :param value: Значение нового элемента, который нужно вставить.
        :raises ValueError: Если индекс выходит за пределы допустимого диапазона.
        """
        if index < 0 or index > self.size:
            raise ValueError("Invalid index")
        self._create_new_state()
        self._history[self._last_state] = np.insert(self._history[self._last_state], index, value)
        self.size += 1

    def remove(self, index: int) -> None:
        """Удаление элемента в новой версии массива по индексу.

        Удаляет элемент из текущей версии массива по индексу и помещает результат в новую версию.
        :param index: Индекс элемента, который необходимо удалить.
        :raises ValueError: Если индекс выходит за пределы допустимого диапазона.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        self.pop(index)

    def get_size(self) -> int:
        """Получение текущего размера массива.

        :return: Количество элементов в текущей версии массива.
        """
        return self.size

    def check_is_empty(self):
        """Проверка, является ли массив пустым в текущей версии.

        :return: True, если массив пуст, иначе False.
        """
        return self.size == 0
