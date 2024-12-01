import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from node_list import FatNode, PersistentListFatNode

# Тестирование методов класса PersistentListFatNode

def test_initialization():
    """Тест 1. Проверка на инициализацию пустого списка."""
    persistent_list = PersistentListFatNode(max_size=5)
    assert persistent_list.check_is_empty() == True
    assert persistent_list.size() == 0
    assert persistent_list.check_is_full() == False

def test_add_elements():
    """"Тест 2: Проверка на добавление элементов в список."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    persistent_list.add(3)
    
    assert persistent_list.size() == 3
    assert persistent_list.get(0) == 1
    assert persistent_list.get(1) == 2
    assert persistent_list.get(2) == 3

def test_add_to_full_list():
    """Тест 3: Проверка на добавление элемента в полный список."""
    persistent_list = PersistentListFatNode(max_size=3)
    persistent_list.add(1)
    persistent_list.add(2)
    persistent_list.add(3)
    
    with pytest.raises(ValueError, match="Список полон"):
        persistent_list.add(4)

def test_insert_element():
    """Тест 4: Проверка вставки элемента на конкретную позицию."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    persistent_list.insert(1, 3)  
    
    assert persistent_list.size() == 3
    assert persistent_list.get(0) == 1
    assert persistent_list.get(1) == 3
    assert persistent_list.get(2) == 2

def test_remove_element():
    """Тест 5: Проверка удаления элемента."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    persistent_list.add(3)
    
    persistent_list.remove(1)  
    
    assert persistent_list.size() == 2
    assert persistent_list.get(0) == 1
    assert persistent_list.get(1) == 3

def test_get_element():
    """Тест 6: Проверка получения элемента по индексу."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    
    assert persistent_list.get(0) == 1
    assert persistent_list.get(1) == 2

def test_invalid_index():
    """Тест 7: Проверка индекса, выходящего за пределы списка."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    
    with pytest.raises(IndexError, match="Неверный индекс"):
        persistent_list.get(1)

def test_pop_empty_list():
    """Тест 8: Пустой список, попытка удаления."""
    persistent_list = PersistentListFatNode(max_size=5)
    
    with pytest.raises(ValueError, match="Список пуст"):
        persistent_list.pop()

def test_pop_last_element():
    """Тест 9: Проверка на удаление последнего элемента списка."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    
    assert persistent_list.pop() == 2
    assert persistent_list.size() == 1
    assert persistent_list.get(0) == 1

def test_clone():
    """Тест 10: Проверка клонирования списка."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    
    cloned_list = persistent_list.clone()
    assert cloned_list.size() == persistent_list.size()
    assert cloned_list.get(0) == persistent_list.get(0)
    assert cloned_list.get(1) == persistent_list.get(1)

def test_version_history():
    """Тест 11: Проверка истории версий."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    persistent_list.add(3)
    
    # Проверяем состояние на разных версиях
    assert persistent_list.get_version(0) == [1]
    assert persistent_list.get_version(1) == [1, 2]
    assert persistent_list.get_version(2) == [1, 2, 3]
    
    # Попытка получить несуществующую версию
    with pytest.raises(ValueError, match="Неверная версия"):
        persistent_list.get_version(3)

def test_clear():
    """Тест 12: Проверка очистки списка."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)
    persistent_list.add(2)
    
    persistent_list.clear()
    
    assert persistent_list.check_is_empty() == True
    assert persistent_list.size() == 0

def test_update_version():
    """Тест 13: Проверка корректности обновления версий."""
    persistent_list = PersistentListFatNode(max_size=5)
    persistent_list.add(1)  # Список: [1] -> версия 0
    persistent_list.add(2)  # Список: [1, 2] -> версия 1
    persistent_list.add(3)  # Список: [1, 2, 3] -> версия 2
    persistent_list.add(4)  # Список: [1, 2, 3, 4] -> версия 3
    persistent_list.add(5)  # Список: [1, 2, 3, 4, 5] -> версия 4
    assert persistent_list._get_current_state() == [1, 2, 3, 4, 5]
    persistent_list.update_version(2)
    assert persistent_list._get_current_state() == [1, 2, 3]
    persistent_list.add(6)
    assert persistent_list._get_current_state() == [1, 2, 3, 6]
    assert persistent_list.get_version(2) == [1, 2, 3]
    persistent_list.update_version(0)
    assert persistent_list._get_current_state() == [1]
    assert persistent_list.get_version(4) == [1, 2, 3, 4, 5]