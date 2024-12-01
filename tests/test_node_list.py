import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from node_list import FatNode, PersistentLinkedListFatNode

# Тестирование методов класса PersistentLinkedListFatNode

@pytest.fixture
def fat_node_list():
    """Создает новый экземпляр PersistentLinkedListFatNode для использования в тестах."""
    return PersistentLinkedListFatNode(max_size=5)

def test_add(fat_node_list):
    """Тест 1. Добавление элементов в список."""
    fat_node_list.add(1)
    fat_node_list.add(2)
    fat_node_list.add(3)
    assert fat_node_list.get(0) == 1
    assert fat_node_list.get(1) == 2
    assert fat_node_list.get(2) == 3
    assert fat_node_list.size() == 3

def test_insert(fat_node_list):
    """Тест 2. Вставка элементов в список."""
    fat_node_list.add(1)
    fat_node_list.add(3)
    fat_node_list.insert(1, 2)  
    assert fat_node_list.get(0) == 1
    assert fat_node_list.get(1) == 2
    assert fat_node_list.get(2) == 3

def test_remove(fat_node_list):
    """Тест 3. Удаление элементов из списка."""
    fat_node_list.add(1)
    fat_node_list.add(2)
    fat_node_list.add(3)
    fat_node_list.remove(1) 
    assert fat_node_list.get(0) == 1
    assert fat_node_list.get(1) == 3
    assert fat_node_list.size() == 2

def test_get(fat_node_list):
    """Тест 4. Получения элемента по индексу."""
    fat_node_list.add(10)
    fat_node_list.add(20)
    fat_node_list.add(30)
    assert fat_node_list.get(0) == 10
    assert fat_node_list.get(1) == 20
    assert fat_node_list.get(2) == 30

def test_versioning(fat_node_list):
    """Тест 5. Проверка версионности списка."""
    fat_node_list.add(1)  # Версия 0
    fat_node_list.add(2)  # Версия 1
    fat_node_list.remove(0)  # Версия 2
    assert fat_node_list.get_version(0) == [1]
    assert fat_node_list.get_version(1) == [1, 2]
    assert fat_node_list.get_version(2) == [2]

def test_full_list(fat_node_list):
    """Тест 6. Проверка ограничений по максимальному размеру."""
    fat_node_list.add(1)
    fat_node_list.add(2)
    fat_node_list.add(3)
    fat_node_list.add(4)
    fat_node_list.add(5)
    with pytest.raises(ValueError, match=fat_node_list.full_array_message):
        fat_node_list.add(6) 

def test_empty_list(fat_node_list):
    """Тест 7. Проверка удаления из пустого списка."""
    with pytest.raises(ValueError, match=fat_node_list.empty_array_message):
        fat_node_list.remove(0)

def test_invalid_index(fat_node_list):
    """Тест 8. Проверка доступа к несуществующему индексу."""
    fat_node_list.add(1)
    with pytest.raises(IndexError, match=fat_node_list.invalid_index_message):
        fat_node_list.get(10)

def test_invalid_version(fat_node_list):
    """Тест 9. Проверка доступа к несуществующей версии."""
    fat_node_list.add(1)  # Версия 0
    with pytest.raises(ValueError, match=fat_node_list.invalid_version_message):
        fat_node_list.get_version(10)