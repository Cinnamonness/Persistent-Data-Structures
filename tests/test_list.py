import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_list import PersistentLinkedList


# Тестирование методов класса PersistentLinkedList
@pytest.fixture
def linked_list():
    """
    Фикстура для создания экземпляра персистентного двусвязного списка.
    """
    return PersistentLinkedList([1, 2, 3, 4, 5])


def test_add(linked_list):
    """Тест 1. Проверка добавления элемента в конец списка"""
    linked_list.add(6)
    assert linked_list.get(index=5) == 6


def test_add_first(linked_list):
    """Тест 2. Проверка добавления элемента в начало списка"""
    linked_list.add_first(0)
    assert linked_list.get(index=0) == 0


def test_insert(linked_list):
    """Тест 3. Проверка вставки элемента по индексу"""
    linked_list.insert(2, 10)
    assert linked_list.get(index=2) == 10
    assert linked_list.get(index=3) == 3


def test_pop(linked_list):
    """Тест 4. Проверка удаления элемента по индексу"""
    removed_value = linked_list.pop(2)
    assert removed_value == 3
    assert linked_list.get(index=2) == 4


def test_remove(linked_list):
    """Тест 5. Проверка удаления элемента по значению"""
    linked_list.remove(4)
    with pytest.raises(ValueError):
        linked_list.remove(4)


def test_get(linked_list):
    """Тест 6. Проверка получения элемента по индексу"""
    assert linked_list.get(index=0) == 1
    assert linked_list.get(index=4) == 5


def test_get_version(linked_list):
    """Тест 7. Проверка получения версии списка"""
    linked_list.add(6)
    linked_list.add(7)
    version_1 = linked_list.get_version(1)
    assert version_1[0] is not None
    version_0_values = []
    current = version_1[0]
    while current:
        version_0_values.append(current.value)
        current = current.next_node
    assert version_0_values == [1, 2, 3, 4, 5, 6]


def test_update_version(linked_list):
    """Тест 8. Проверка обновления версии списка"""
    linked_list.add(6)
    linked_list.add(7)
    linked_list.update_version(1)
    assert linked_list.get(index=5) == 6
    linked_list.update_version(0)
    assert linked_list.get(index=4) == 5


def test_clear(linked_list):
    """Тест 9. Проверка очистки списка"""
    linked_list.clear()
    assert linked_list.get_size() == 0
    assert linked_list.check_is_empty()


def test_get_size(linked_list):
    """Тест 10. Проверка получения размера списка"""
    assert linked_list.get_size() == 5
    linked_list.add(6)
    assert linked_list.get_size() == 6


def test_check_is_empty(linked_list):
    """Тест 11. Проверка метода для проверки пустоты списка"""
    linked_list.clear()
    assert linked_list.check_is_empty() is True
    linked_list.add(10)
    assert linked_list.check_is_empty() is False
