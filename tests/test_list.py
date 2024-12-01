import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_list import PersistentList

# Тестирование методов класса PersistentList

@pytest.fixture
def p_list():
    """Создание нового списка перед каждым тестом."""
    return PersistentList(max_size=5, depth=2, bits_for_level=3)

def test_add(p_list):
    """Проверка добавления элементов в список."""
    p_list.add(1)
    p_list.add(2)
    assert p_list.get(0) == 1
    assert p_list.get(1) == 2
    assert p_list.size() == 2

def test_add_full(p_list):
    """Проверка добавления элемента в полный список."""
    for i in range(1, 6):  # Добавление 5 элементов
        p_list.add(i)
    
    # Попытка добавить 6-й элемент должна вызвать ошибку
    with pytest.raises(ValueError, match="Список полон"):
        p_list.add(6)

def test_insert(p_list):
    """Проверка вставки элемента по индексу."""
    p_list.add(1)
    p_list.add(2)
    p_list.insert(1, 3)  # Вставка 3 на индекс 1
    assert p_list.get(0) == 1
    assert p_list.get(1) == 3
    assert p_list.get(2) == 2
    assert p_list.size() == 3

def test_remove(p_list):
    """Проверка удаления элемента по индексу."""
    p_list.add(1)
    p_list.add(2)
    p_list.add(3)
    p_list.remove(1)  # Удаление элемента на индексе 1 (2)
    assert p_list.get(0) == 1
    assert p_list.get(1) == 3
    assert p_list.size() == 2

def test_get_version(p_list):
    """"Проверка получения версии списка."""
    p_list.add(1)
    p_list.add(2)
    p_list.add(3)
    version_1 = p_list.get_version(1)  # Получение состояния после 1-й операции
    assert version_1 == [1, 2]  # Версия 1 будет содержать [1, 2]

def test_update_version(p_list):
    """Проверка обновления текущей версии списка."""
    # Шаг 1: Добавляем элементы
    p_list.add(1)  # Версия 0 -> [1]
    p_list.add(2)  # Версия 1 -> [1, 2]
    p_list.add(3)  # Версия 2 -> [1, 2, 3]

    # Шаг 2: Обновляем текущую версию на 1
    p_list.update_version(1)

    # Шаг 3: Проверяем состояние списка на версии 1
    assert p_list.get(0) == 1
    assert p_list.get(1) == 2
    assert p_list.size() == 2  # Размер списка соответствует версии 1

    # Шаг 4: Проверяем добавление элементов после обновления версии
    p_list.add(4)  # После версии 1 -> [1, 2, 4]
    assert p_list.size() == 3
    assert p_list.get(2) == 4

    # Шаг 5: Проверяем переключение на другую версию
    p_list.update_version(0)  # Переключаемся на версию 0
    assert p_list.size() == 1  # Размер соответствует версии 0
    assert p_list.get(0) == 1  # Элемент на версии 0

def test_clone(p_list):
    """Проверка клонирования списка."""
    p_list.add(1)
    p_list.add(2)
    p_list.add(3)
    cloned_list = p_list.clone()

    assert cloned_list.get(0) == 1
    assert cloned_list.get(1) == 2
    assert cloned_list.get(2) == 3
    assert cloned_list.size() == 3

def test_clear(p_list):
    """Проверка очистки списка."""
    p_list.add(1)
    p_list.add(2)
    p_list.clear()

    assert p_list.check_is_empty() is True
    assert p_list.size() == 0

def test_index_error(p_list):
    """Проверка выброса ошибки при неправильном индексе."""
    p_list.add(1)
    p_list.add(2)
    with pytest.raises(IndexError, match="Неверный индекс"):
        p_list.get(2)  # Индекс выходит за пределы списка

def test_invalid_version(p_list):
    """Проверка выброса ошибки при неправильной версии."""
    p_list.add(1)
    p_list.add(2)
    with pytest.raises(ValueError, match="Неверная версия: 3"):
        p_list.get_version(3)  # Версия 3 не существует