class PersistentArray:
    """
    Класс PersistentArray реализует неизменяемый массив с
    возможностью хранения нескольких версий, где каждая
    версия является изменением предыдущей.

    Включает методы для добавления, удаления, обновления и
    извлечения элементов из различных версий массива, а
    также для проверки его состояния (пустой, полный).
    """

    def __init__(self, max_size=1024, default_value=0):
        """
        Инициализирует новый массив с несколькими версиями.

        Аргументы:
            max_size (int): Максимальный размер массива. По умолчанию 1024.
            default_value (int): Значение по умолчанию для всех элементов
            массива. По умолчанию 0.

        Создается первая версия массива, которая состоит из элементов,
        равных default_value.
        """
        self.max_size = max_size
        self.default_value = default_value
        # Массивы для каждой версии, в каждой версии хранится массив значений
        self.versions = [[default_value] * max_size]
        self.size = 0

    def __getitem__(self, index):
        """
        Получение значения из текущей версии массива по индексу.

        Аргументы:
            index (int): Индекс элемента в текущей версии массива.

        Возвращает:
            int: Значение элемента в текущей версии массива по заданному индексу.

        Исключения:
            ValueError: Если индекс выходит за пределы допустимого диапазона.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        return self.versions[-1][index]

    def get(self, version, index):
        """
        Получение значения элемента для определенной версии массива по индексу.

        Аргументы:
            version (int): Номер версии, из которой нужно получить элемент.
            index (int): Индекс элемента в указанной версии массива.

        Возвращает:
            int: Значение элемента в указанной версии массива по заданному индексу.

        Исключения:
            ValueError: Если версия или индекс выходят за пределы допустимого диапазона.
        """
        if version < 0 or version >= len(self.versions):
            raise ValueError("Invalid version")
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        return self.versions[version][index]

    def add(self, value):
        """
        Добавление нового элемента в текущую версию массива.

        Аргументы:
            value (int): Значение нового элемента, который добавляется в массив.

        Исключения:
            ValueError: Если размер массива превышает максимальный размер.

        Создает новую версию массива с добавлением элемента в конец.
        """
        if self.size >= self.max_size:
            raise ValueError("Exceeded max size")
        # Создание новой версии с копированием старой версии
        new_version = self.versions[-1][:]  # Копирование старой версии
        new_version[self.size] = value
        self.versions.append(new_version)
        self.size += 1

    def pop(self, index):
        """
        Удаление элемента из текущей версии массива и возвращение его значения.

        Аргументы:
            index (int): Индекс элемента, который необходимо удалить.

        Возвращает:
            int: Значение удаленного элемента.

        Исключения:
            ValueError: Если индекс выходит за пределы допустимого диапазона.

        Создает новую версию массива с удалением указанного элемента.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        new_version = self.versions[-1][:]
        removed_element = new_version[index]
        del new_version[index]
        self.versions.append(new_version)
        self.size -= 1
        return removed_element

    def __setitem__(self, index, value):
        """
        Обновление значения элемента в текущей версии массива.

        Аргументы:
            index (int): Индекс элемента, который необходимо обновить.
            value (int): Новое значение для обновляемого элемента.

        Исключения:
            ValueError: Если индекс выходит за пределы допустимого диапазона.

        Создает новую версию массива с обновленным значением элемента по индексу.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        # Создание новой версии с изменением элемента по индексу
        new_version = self.versions[-1][:]  # Копирование старой версии
        new_version[index] = value
        self.versions.append(new_version)

    def insert(self, index, value):
        """
        Вставка нового элемента в массив в указанную позицию.

        Аргументы:
            index (int): Индекс, в который будет вставлен новый элемент.
            value (int): Значение нового элемента.

        Исключения:
            ValueError: Если размер массива превышает максимальный размер
            или индекс некорректен.

        Создает новую версию массива с вставленным элементом.
        """
        if self.size >= self.max_size:
            raise ValueError("Exceeded max size")
        if index < 0 or index > self.size:
            raise ValueError("Invalid index")
        new_version = self.versions[-1][:]
        new_version.insert(index, value)
        self.versions.append(new_version)
        self.size += 1

    def remove(self, index):
        """
        Удаление элемента в текущей версии массива по индексу и
        возвращение его значения.

        Аргументы:
            index (int): Индекс элемента, который необходимо удалить.

        Возвращает:
            int: Значение удаленного элемента.

        Исключения:
            ValueError: Если индекс выходит за пределы допустимого диапазона.

        Создает новую версию массива с удалением указанного элемента.
        """
        if index < 0 or index >= self.size:
            raise ValueError("Invalid index")
        # Создание новой версии с копированием старой версии
        new_version = self.versions[-1][:]  # Копирование старой версии
        removed_element = new_version.pop(index)
        self.versions.append(new_version)
        self.size -= 1
        return removed_element

    def get_size(self):
        """
        Получение текущего размера массива.

        Возвращает:
            int: Количество элементов в текущей версии массива.
        """
        return self.size

    def check_is_empty(self):
        """
        Проверка, является ли массив пустым в текущей версии.

        Возвращает:
            bool: True, если массив пуст, иначе False.
        """
        return self.size == 0

    def check_is_full(self):
        """
        Проверка, является ли массив полным (достиг максимального размера).

        Возвращает:
            bool: True, если массив полный, иначе False.
        """
        return self.size == self.max_size

    def get_version(self, version):
        """
        Получение состояния массива для определенной версии.

        Аргументы:
            version (int): Номер версии, для которой нужно получить состояние.

        Возвращает:
            list: Состояние массива для указанной версии.

        Исключения:
            ValueError: Если версия выходит за пределы допустимого диапазона.
        """
        if version < 0 or version >= len(self.versions):
            raise ValueError("Invalid version")
        return self.versions[version][:self.size]

    def update_version(self, version):
        """
        Обновление текущей версии массива до указанной.

        Аргументы:
            version (int): Номер версии, до которой нужно обновить текущий массив.

        Исключения:
            ValueError: Если версия выходит за пределы допустимого диапазона.

        Изменяет текущий массив на указанный в версии.
        """
        if version < 0 or version >= len(self.versions):
            raise ValueError("Invalid version")
        # Просто возвращаем состояние в указанную версию
        self.versions = self.versions[:version + 1]
        self.size = len(self.versions[-1])
