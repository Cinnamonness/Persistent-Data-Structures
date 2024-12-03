import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from node_array import PersistentArray


def test_initialization():
    """Тест 1. Проверка создания и начального состояния массива."""
    arr = PersistentArray(max_size=5)
    assert arr.get_size() == 0
    assert arr.check_is_empty() is True
    assert arr.check_is_full() is False


def test_add_elements():
    """Тест 2. Проверка добавления элементов."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    assert arr.get_size() == 3
    assert arr[0] == 10
    assert arr[1] == 20
    assert arr[2] == 30


def test_add_elements_with_versions():
    """Тест 3. Проверка добавления элементов с проверкой версий."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    assert arr.get_version(0) == []
    assert arr.get_version(1) == [10]
    assert arr.get_version(2) == [10, 20]
    assert arr.get_version(3) == [10, 20, 30]


def test_pop():
    """Тест 4. Проверка метода pop."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    removed_value = arr.pop(1)
    assert removed_value == 20
    assert arr.get_size() == 2
    assert arr[0] == 10
    assert arr[1] == 30


def test_insert():
    """Тест 5. Проверка метода insert."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    arr.insert(1, 15)
    assert arr.get_size() == 4
    assert arr[0] == 10
    assert arr[1] == 15
    assert arr[2] == 20
    assert arr[3] == 30


def test_remove():
    """Тест 6. Проверка метода remove."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    arr.remove(1)
    assert arr.get_size() == 2
    assert arr[0] == 10
    assert arr[1] == 30


def test_get_version():
    """Тест 7. Проверка метода get для разных версий."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    assert arr.get_version(1) == [10]
    assert arr.get_version(2) == [10, 20]
    assert arr.get_version(3) == [10, 20, 30]


def test_out_of_bounds():
    """Тест 8. Проверка на выход за границы массива."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)

    with pytest.raises(ValueError):
        arr[2]

    with pytest.raises(ValueError):
        arr.get(1, 2)


def test_max_size():
    """Тест 9. Проверка на максимальный размер."""
    arr = PersistentArray(max_size=3)

    arr.add(10)
    arr.add(20)
    arr.add(30)

    with pytest.raises(ValueError):
        arr.add(40)


def test_update_version():
    """Тест 10. Проверка метода update_version."""
    arr = PersistentArray(max_size=5)
    arr.add(10)
    arr.add(20)
    arr.add(30)

    arr.update_version(1)
    assert arr.get_version(1) == [10]
    assert arr.get_size() == 1
