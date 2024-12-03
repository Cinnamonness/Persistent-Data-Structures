import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_array import PersistentArray

# Тестирование методов класса PersistentArray

@pytest.fixture
def persistent_array():
    """Создание объекта PersistentArray с максимальным размером 10."""
    obj = PersistentArray(max_size=10)
    return obj


def test_add_elements(persistent_array):
    """Тест 1: Добавление элементов."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)

    assert persistent_array[0] == 1
    assert persistent_array[1] == 2
    assert persistent_array[2] == 3


def test_get_element_from_version(persistent_array):
    """Тест 2: Получение элемента из версии 3 (до изменений)."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)

    assert persistent_array.get(3, 1) == 2


def test_update_element(persistent_array):
    """Тест 3: Обновление элемента в текущей версии."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)

    persistent_array[1] = 99
    assert persistent_array[1] == 99
    assert persistent_array.get(4, 1) == 99


def test_insert_element(persistent_array):
    """Тест 4: Вставка элемента в новую версию."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)

    persistent_array.insert(1, 100)
    assert persistent_array[1] == 100
    assert persistent_array.get(4, 1) == 100


def test_pop_element(persistent_array):
    """Тест 5: Удаление элемента и возвращение удаленного элемента."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)
    persistent_array.insert(1, 99)

    assert persistent_array.get(4, 1) == 99


def test_get_version_state(persistent_array):
    """Тест 6: Получение состояния для указанной версии."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)
    persistent_array[1] = 99
    persistent_array.insert(1, 100)
    persistent_array.pop(1)

    assert persistent_array.get_version(6) == [1, 99, 3]
    assert persistent_array.get_version(3) == [1, 2, 3]


def test_check_is_empty(persistent_array):
    """Тест 7: Проверка на пустоту."""
    assert persistent_array.check_is_empty()

    persistent_array.add(1)
    assert not persistent_array.check_is_empty()


def test_check_is_full(persistent_array):
    """Тест 8: Проверка на полноту."""
    assert not persistent_array.check_is_full()

    for i in range(10):
        persistent_array.add(i)
    assert persistent_array.check_is_full()


def test_update_version(persistent_array):
    """Тест 9: Обновление текущей версии до указанной."""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.add(3)

    persistent_array[1] = 99
    persistent_array.insert(1, 100)

    persistent_array.update_version(4)
    assert persistent_array[1] == 99
