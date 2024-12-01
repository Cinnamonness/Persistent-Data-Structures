import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_array import PersistentArray

# Тестирование методов класса PersistentArray

def test_initialization():
    """"Тест 1. Проверка инициализации массива."""
    arr = PersistentArray(dtype='i', max_size=10)
    assert arr.size() == 0 
    assert arr.dtype == 'i'  
    assert arr.max_size == 10  

def test_add_element():
    """"Тест 2. Проверка добавления элемента в массив."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    assert arr.size() == 1  
    assert arr.get(0) == 5  

def test_insert_element():
    """"Тест 3. Проверка вставки элемента по индексу в массив."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.insert(0, 10)
    assert arr.size() == 2 
    assert arr.get(0) == 10  
    assert arr.get(1) == 5  

def test_remove_element():
    """"Тест 4. Проверка удаления элемента в массиве."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.add(10)
    arr.remove(0)
    assert arr.size() == 1  
    assert arr.get(0) == 10  

def test_get_invalid_index():
    """"Тест 5. Проверка доступа по несуществующему индексу."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    with pytest.raises(IndexError):  
        arr.get(1)

def test_insert_invalid_index():
    """"Тест 6. Проверка вставки по несуществующему индексу."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    with pytest.raises(IndexError):  
        arr.insert(2, 10)

def test_clear():
    """"Тест 7. Проверка очистки массива."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.clear()
    assert arr.size() == 0  
    with pytest.raises(IndexError):  
        arr.get(0)

def test_history():
    """"Тест 8. Проверка корректности получения истории версий."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.add(10)
    assert len(arr.history) == 2  
    arr.remove(0)
    assert len(arr.history) == 3  

def test_get_version():
    """"Тест 9. Проверка обновления версии."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.add(10)
    arr.remove(0)
    arr.add(15)
    assert arr.size() == 2 
    arr.update_version(1)
    assert arr.size() == 1 
    assert arr.get(0) == 5  

def test_clone():
    """"Тест 10. Проверка клонирования массива."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    cloned_arr = arr.clone()
    assert cloned_arr.size() == arr.size()  
    assert cloned_arr.get(0) == arr.get(0)  
    arr.add(10)
    assert cloned_arr.size() != arr.size()  

def test_persistent_changes():
    """"Тест 11. Проверка изменений массива."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.add(10)
    arr.remove(0)
    assert arr.size() == 1  
    assert arr.get(0) == 10  

def test_invalid_version():
    """"Тест 12. Проверка отсутсвия доступа к несуществующей версии."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.add(10)
    with pytest.raises(ValueError):  
        arr.get_version(5)

def test_update_version_invalid():
    """"Тест 12. Проверка отсутсвия обновления по несуществующей версии."""
    arr = PersistentArray(dtype='i', max_size=10)
    arr.add(5)
    arr.add(10)
    with pytest.raises(ValueError):  
        arr.update_version(5)