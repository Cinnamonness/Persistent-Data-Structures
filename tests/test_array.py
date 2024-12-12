import pytest
from persistent_array import PersistentArray


# Тестирование методов класса PersistentArray
@pytest.fixture
def persistent_array():
    """Фикстура для создания PersistentArray"""
    return PersistentArray(size=5, default_value=0)


def test_initial_state(persistent_array):
    """Тест 1. Проверка начального состояния массива"""
    assert persistent_array.get_size() == 5
    assert persistent_array[0] == 0
    assert persistent_array[4] == 0


def test_initial_size(persistent_array):
    """Тест 2. Проверка начального размера массива"""
    assert persistent_array.get_size() == 5


def test_get_version(persistent_array):
    """Тест 3. Проверка извлечения элемента по версии"""
    persistent_array.add(1)
    persistent_array.add(2)

    assert persistent_array.get(0, 0) == 0
    assert persistent_array.get(1, 5) == 1
    assert persistent_array.get(2, 6) == 2


def test_set_version(persistent_array):
    """Тест 4. Проверка обновления текущей версии"""
    persistent_array.add(1)
    persistent_array.add(2)
    persistent_array.set_version(1)

    assert persistent_array[5] == 1
    persistent_array.set_version(2)
    assert persistent_array[6] == 2


def test_add_element(persistent_array):
    """Тест 5. Проверка добавления элемента в массив"""
    persistent_array.add(10)
    assert persistent_array.get_size() == 6
    assert persistent_array[5] == 10


def test_multiple_add_elements(persistent_array):
    """Тест 6. Проверка добавления нескольких элементов"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    assert persistent_array.get_size() == 8
    assert persistent_array[5] == 10
    assert persistent_array[6] == 20
    assert persistent_array[7] == 30


def test_pop_element(persistent_array):
    """Тест 7. Проверка удаления элемента из массива"""
    persistent_array.add(10)
    persistent_array.add(20)
    removed_value = persistent_array.pop(1)
    assert removed_value == 0
    assert persistent_array.get_size() == 6
    assert persistent_array[1] == 0


def test_insert_element(persistent_array):
    """Тест 8. Проверка вставки элемента по указанному индексу"""
    persistent_array.add(10)
    persistent_array.insert(2, 15)
    assert persistent_array.get_size() == 7
    assert persistent_array[2] == 15


def test_remove_element(persistent_array):
    """Тест 9. Проверка удаления элемента из массива по индексу"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.remove(1)
    assert persistent_array.get_size() == 6
    assert persistent_array[1] == 0


def test_add_and_remove_elements(persistent_array):
    """Тест 10. Проверка добавления и удаления элементов"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    assert persistent_array.get_size() == 8
    persistent_array.remove(5)
    assert persistent_array.get_size() == 7


def test_versioning(persistent_array):
    """Тест 11. Проверка работы с версиями массива"""
    persistent_array.add(10)
    persistent_array.add(20)
    assert persistent_array.get_version_state(1)[5] == 10
    assert persistent_array.get_version_state(2)[6] == 20
    persistent_array.set_version(1)
    assert persistent_array[5] == 10
    persistent_array.set_version(2)
    assert persistent_array[6] == 20


def test_invalid_index_in_version(persistent_array):
    """Тест 12. Проверка недействительного индекса для версии"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    with pytest.raises(ValueError):
        persistent_array.get(1, 10)


def test_get_size(persistent_array):
    """Тест 13. Проверка размерности массива"""
    assert persistent_array.get_size() == 5
    persistent_array.add(10)
    assert persistent_array.get_size() == 6


def test_check_is_empty(persistent_array):
    """Тест 14. Проверка на пустоту"""
    assert not persistent_array.check_is_empty()
    persistent_array.remove(4)
    persistent_array.remove(3)
    persistent_array.remove(2)
    persistent_array.remove(1)
    persistent_array.remove(0)
    assert persistent_array.check_is_empty()


def test_single_element_operations(persistent_array):
    """Тест 15. Проверка операций с массивом из одного элемента"""
    persistent_array.add(10)
    persistent_array.remove(0)
    assert persistent_array.get_size() == 5
    assert persistent_array[0] == 0


def test_invalid_index_getitem(persistent_array):
    """Тест 16. Проверка недействительного доступа по индексу для getitem"""
    with pytest.raises(ValueError):
        persistent_array[10]


def test_invalid_index_setitem(persistent_array):
    """Тест 17. Проверка недействительного доступа по индексу для setitem"""
    with pytest.raises(ValueError):
        persistent_array[10] = 10


def test_invalid_index_pop(persistent_array):
    """Тест 18. Проверка недействительного доступа по индексу для pop"""
    with pytest.raises(ValueError):
        persistent_array.pop(10)


def test_invalid_index_insert(persistent_array):
    """Тест 19. Проверка недействительного доступа по индексу для insert"""
    with pytest.raises(ValueError):
        persistent_array.insert(10, 10)


def test_invalid_version_get(persistent_array):
    """Тест 20. Проверка недействительного доступа по индексу для get"""
    persistent_array.add(10)
    with pytest.raises(ValueError):
        persistent_array.get(10, 0)
