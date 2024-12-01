import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_list import PersistentLinkedList, Node

# Тестирование методов класса PersistentLinkedList

@pytest.fixture
def linked_list():
    """Создает новый экземпляр PersistentLinkedList для использования в тестах."""
    return PersistentLinkedList(max_size=5)

def test_add_and_size(linked_list):
    """Тест 1. Добавлние элементов и получение размера списка."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    assert linked_list.size() == 3

def test_add_first(linked_list):
    """Тест 2. Добавление элемента в начало списка."""
    linked_list.add(1)
    linked_list.add_first(0)
    assert linked_list.get(0) == 0
    assert linked_list.get(1) == 1

def test_insert(linked_list):
    """Тест 3. Вставка элемента по индексу."""
    linked_list.add(1)
    linked_list.add(3)
    linked_list.insert(1, 2)
    assert linked_list.get(1) == 2
    assert linked_list.get(2) == 3

def test_remove(linked_list):
    """Тест 4. Удаление элемента по индексу."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    linked_list.remove(1)
    assert linked_list.size() == 2
    assert linked_list.get(0) == 1
    assert linked_list.get(1) == 3

def test_remove_first(linked_list):
    """Тест 5. Удаление первого элемента списка."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.remove_first()
    assert linked_list.size() == 1
    assert linked_list.get(0) == 2

def test_remove_last(linked_list):
    """Тест 6. Удаление последнего элемента списка."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.remove_last()
    assert linked_list.size() == 1
    assert linked_list.get(0) == 1

def test_get(linked_list):
    """Тест 7. Доступ к элементу по индексу."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    assert linked_list.get(0) == 1
    assert linked_list.get(1) == 2
    assert linked_list.get(2) == 3

def test_clear(linked_list):
    """Тест 8. Очистка списка."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.clear()
    assert linked_list.size() == 0

def test_history(linked_list):
    """Тест 9. Сохранение состояния списка в историю."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    assert linked_list.get_version(0) == [1]
    assert linked_list.get_version(1) == [1, 2]
    assert linked_list.get_version(2) == [1, 2, 3]

def test_update_version(linked_list):
    """Тест 10. Обновление версии списка."""
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    linked_list.update_version(1)
    assert linked_list.size() == 2
    assert linked_list.get(0) == 1
    assert linked_list.get(1) == 2

def test_clone(linked_list):
    """Тест 11. Клонирование списка."""
    linked_list.add(1)
    linked_list.add(2)
    cloned_list = linked_list.clone()
    assert cloned_list.size() == 2
    assert cloned_list.get(0) == 1
    assert cloned_list.get(1) == 2

def test_invalid_index(linked_list):
    """Тест 12. Обработка некорректного индекса."""
    linked_list.add(1)
    with pytest.raises(IndexError):
        linked_list.get(1)

def test_invalid_version(linked_list):
    """Тест 13. Обработка некорректной версии."""
    linked_list.add(1)
    with pytest.raises(ValueError):
        linked_list.get_version(1)