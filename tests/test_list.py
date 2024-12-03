import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_list import PersistentLinkedList

# Тестирование методов класса PersistentLinkedList

@pytest.fixture
def persistent_list():
    """Инициализация списка с максимальным размером 5."""
    return PersistentLinkedList(max_size=5)


def test_initialization(persistent_list):
    """Тест 1. Проверка инициализации списка."""
    assert persistent_list.max_size == 5
    assert persistent_list.head is None
    assert persistent_list.tail is None
    assert persistent_list.size() == 0
    assert len(persistent_list.history) == 1


def test_add_element(persistent_list):
    """Тест 2. Проверка добавления элемента в список."""
    persistent_list.add(10)
    assert persistent_list.size() == 1
    assert persistent_list.head.value == 10
    assert persistent_list.tail.value == 10
    assert len(persistent_list.history) == 2


def test_add_element_to_full_list():
    """Тест 3. Проверка добавления элемента в полный список,
    должно вызвать исключение ValueError."""
    plist = PersistentLinkedList(max_size=2)
    plist.add(10)
    plist.add(20)
    with pytest.raises(ValueError):
        plist.add(30)


def test_insert_element(persistent_list):
    """Тест 4. Проверка вставки элемента по индексу."""
    persistent_list.add(10)
    persistent_list.add(20)
    persistent_list.insert(1, 15)
    assert persistent_list.size() == 2
    assert persistent_list.head.next_node.value == 15
    assert persistent_list.tail.value == 20
    assert len(persistent_list.history) == 4


def test_insert_at_first_position(persistent_list):
    """Тест 5. Проверка вставки элемента в начало списка."""
    persistent_list.add(10)
    persistent_list.insert(0, 5)
    assert persistent_list.size() == 2
    assert persistent_list.head.value == 5
    assert persistent_list.head.next_node.value == 10
    assert len(persistent_list.history) == 3


def test_remove_element(persistent_list):
    """Тест 6. Проверка удаления элемента по индексу."""
    persistent_list.add(10)
    persistent_list.add(20)
    removed_value = persistent_list.remove(0)
    assert removed_value == 10
    assert persistent_list.size() == 1
    assert persistent_list.head.value == 20
    assert len(persistent_list.history) == 4


def test_get_element(persistent_list):
    """Тест 7. Проверка получения элемента по индексу и версии."""
    persistent_list.add(10)
    persistent_list.add(20)
    assert persistent_list.get(1, 0) == 10
    assert persistent_list.get(2, 1) == 20


def test_get_version(persistent_list):
    """Тест 8. Провекра получения версии списка."""
    persistent_list.add(10)
    persistent_list.add(20)
    persistent_list.add(30)
    version_1 = persistent_list.get_version(1)
    assert version_1 == [10]
    version_2 = persistent_list.get_version(2)
    assert version_2 == [10, 20]
    version_3 = persistent_list.get_version(3)
    assert version_3 == [10, 20, 30]


def test_update_version(persistent_list):
    """Тест 9. Проверка обновления версии списка."""
    persistent_list.add(10)
    persistent_list.add(20)
    persistent_list.add(30)
    persistent_list.update_version(2)
    assert persistent_list.size() == 2
    assert persistent_list.head.value == 10
    assert persistent_list.tail.value == 20


def test_clear_list(persistent_list):
    """Тест 10. Проверка очистки списка."""
    persistent_list.add(10)
    persistent_list.add(20)
    persistent_list.clear()
    assert persistent_list.size() == 0
    assert persistent_list.head is None
    assert persistent_list.tail is None
    assert len(persistent_list.history) == 4


def test_check_is_empty(persistent_list):
    """Тест 11. Проверка метода check_is_empty."""
    assert persistent_list.check_is_empty() is True
    persistent_list.add(10)
    assert persistent_list.check_is_empty() is False


def test_check_is_full(persistent_list):
    """Тест 12. Проверка метода check_is_full."""
    assert not persistent_list.check_is_full()
    persistent_list.add(10)
    persistent_list.add(20)
    persistent_list.add(30)
    persistent_list.add(40)
    persistent_list.add(50)
    assert persistent_list.check_is_full()


def test_size_of_empty_list(persistent_list):
    """Тест 13. Проверка метода size для пустого списка."""
    assert persistent_list.size() == 0


def test_size_after_operations(persistent_list):
    """Тест 14. Проверка метода size после нескольких операций."""
    persistent_list.add(10)
    persistent_list.add(20)
    persistent_list.add(30)
    assert persistent_list.size() == 3
    persistent_list.remove(0)
    assert persistent_list.size() == 2
