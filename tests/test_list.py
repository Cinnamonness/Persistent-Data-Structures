import pytest
from persistent_list import PersistentLinkedList


# Тестирование методов класса PersistentLinkedList
@pytest.fixture
def persistent_list():
    """Инициализация персистентного двусвязного списка с начальными данными"""
    return PersistentLinkedList([1, 2, 3, 4])


def test_initial_state(persistent_list):
    """Тест 1. Проверка начального состояния списка"""
    assert persistent_list.get_size() == 4
    assert persistent_list.get(version=0, index=0) == 1


def test_add(persistent_list):
    """Тест 2. Проверка добавления элемента в конец списка"""
    persistent_list.add(5)
    assert persistent_list.get_size() == 5
    assert persistent_list.__getitem__(4) == 5


def test_add_first(persistent_list):
    """Тест 3. Проверка добавления элемента в начало списка"""
    persistent_list.add_first(0)
    assert persistent_list.get_size() == 5
    assert persistent_list.__getitem__(0) == 0


def test_insert(persistent_list):
    """Тест 4. Проверка вставки элемента в список по индексу"""
    persistent_list.insert(2, 99)
    assert persistent_list.get_size() == 5
    assert persistent_list.__getitem__(2) == 99
    assert persistent_list.__getitem__(3) == 3


def test_pop(persistent_list):
    """Тест 5. Проверка удаления элемента по индексу"""
    removed_value = persistent_list.pop(1)
    assert removed_value == 2
    assert persistent_list.get_size() == 3
    with pytest.raises(IndexError):
        persistent_list.get(1)


def test_remove(persistent_list):
    """Тест 6. Проверка удаления элемента по значению"""
    persistent_list.remove(3)
    assert persistent_list.get_size() == 3
    with pytest.raises(ValueError):
        persistent_list.remove(10)


def test_add_multiple(persistent_list):
    """Тест 7. Проверка добавления нескольких элементов в конец списка"""
    persistent_list.add(5)
    persistent_list.add(6)
    persistent_list.add(7)
    assert persistent_list.get_size() == 7
    assert persistent_list.__getitem__(4) == 5
    assert persistent_list.__getitem__(5) == 6
    assert persistent_list.__getitem__(6) == 7


def test_insert_at_start(persistent_list):
    """Тест 8. Проверка вставки элемента в начало списка"""
    persistent_list.insert(0, -1)
    assert persistent_list.get_size() == 5
    assert persistent_list.__getitem__(0) == -1


def test_insert_out_of_range(persistent_list):
    """Тест 9. Проверка вставки элемента за пределами допустимого диапазона индексов"""
    with pytest.raises(IndexError):
        persistent_list.insert(10, 100)


def test_remove_non_existing_value(persistent_list):
    """Тест 10. Проверка удаления несуществующего элемента из списка"""
    with pytest.raises(ValueError):
        persistent_list.remove(99)


def test_pop_multiple(persistent_list):
    """Тест 11. Проверка удаления нескольких элементов по индексу"""
    persistent_list.pop(0)
    persistent_list.pop(1)
    assert persistent_list.get_size() == 2
    assert persistent_list.__getitem__(0) == 2
    assert persistent_list.__getitem__(1) == 4


def test_set_version(persistent_list):
    """Тест 12. Проверка переключения между версиями"""
    persistent_list.add(5)
    persistent_list.add(6)
    persistent_list.set_version_doubly_linked_list(0)
    assert persistent_list.get_size() == 4
    persistent_list.set_version_doubly_linked_list(2)
    assert persistent_list.get_size() == 6


def test_get_invalid_index(persistent_list):
    """Тест 12. Проверка ошибки при попытке получить элемент по недопустимому индексу"""
    with pytest.raises(IndexError):
        persistent_list.get(index=100)


def test_get_version(persistent_list):
    """Тест 13. Проверка получения состояния списка на определенной версии"""
    persistent_list.add(5)
    persistent_list.add(6)
    assert persistent_list.get(version=0, index=3) == 4
    assert persistent_list.get(version=2, index=4) == 5


def test_clear(persistent_list):
    """Тест 14. Проверка очистки списка"""
    persistent_list.clear()
    assert persistent_list.get_size() == 0
    with pytest.raises(IndexError):
        persistent_list.get(0)


def test_check_is_empty(persistent_list):
    """Тест 15. Проверка пуст ли список"""
    assert not persistent_list.check_is_empty()
    persistent_list.clear()
    assert persistent_list.check_is_empty()


def test_get_invalid_version(persistent_list):
    """Тест 16. Проверка ошибки при попытке получить версию, которой не существует"""
    with pytest.raises(ValueError):
        persistent_list.get_version(999)
