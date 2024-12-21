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


def test_invalid_index_access(persistent_array):
    """Тест 21. Проверка обращения к недопустимому индексу"""
    with pytest.raises(ValueError, match="Invalid index"):
        persistent_array[-1]
    with pytest.raises(ValueError, match="Invalid index"):
        persistent_array[100]


def test_invalid_index_update(persistent_array):
    """Тест 22. Проверка обновления недопустимого индекса"""
    with pytest.raises(ValueError, match="Invalid index"):
        persistent_array[-1] = 5
    with pytest.raises(ValueError, match="Invalid index"):
        persistent_array[100] = 5


def test_pop_from_empty_array():
    """Тест 23. Проверка удаления элемента из пустого массива"""
    empty_array = PersistentArray(size=0)
    with pytest.raises(ValueError, match="Invalid index"):
        empty_array.pop(0)


def test_set_invalid_version(persistent_array):
    """Тест 24. Проверка установки несуществующей версии"""
    with pytest.raises(ValueError, match='Version "10" does not exist'):
        persistent_array.set_version(10)


def test_boundary_indices(persistent_array):
    """Тест 25. Проверка граничных индексов"""
    persistent_array[0] = 100
    persistent_array[4] = 200
    assert persistent_array[0] == 100
    assert persistent_array[4] == 200


def test_insert_boundary(persistent_array):
    """Тест 26. Проверка вставки в начало и конец массива"""
    persistent_array.insert(0, 50)
    persistent_array.insert(persistent_array.get_size(), 60)
    assert persistent_array[0] == 50
    assert persistent_array[persistent_array.get_size() - 1] == 60


def test_check_is_empty_array():
    """Тест 27. Проверка пустого массива"""
    empty_array = PersistentArray(size=0)
    assert empty_array.check_is_empty() is True

    empty_array.add(10)
    assert empty_array.check_is_empty() is False


def test_get_version_state(persistent_array):
    """Тест 28. Проверка получения состояния версии"""
    persistent_array.add(100)
    state = persistent_array.get_version_state(1)
    assert state[-1] == 100


def test_large_array_operations():
    """Тест 29. Проверка работы с большим массивом"""
    large_array = PersistentArray(size=10000, default_value=1)
    large_array.add(2)
    assert large_array.get_size() == 10001
    assert large_array[10000] == 2


def test_get_version_invalid(persistent_array):
    """Тест 30. Проверка получения состояния для несуществующей версии"""
    with pytest.raises(ValueError):
        persistent_array.get(100, 0)


def test_remove_invalid_index(persistent_array):
    """Тест 31. Проверка удаления элемента с недопустимым индексом"""
    with pytest.raises(ValueError):
        persistent_array.remove(-1)
    with pytest.raises(ValueError):
        persistent_array.remove(10)


def test_set_invalid_index(persistent_array):
    """Тест 32. Проверка обновления элемента с недопустимым индексом"""
    with pytest.raises(ValueError):
        persistent_array[-1] = 5
    with pytest.raises(ValueError):
        persistent_array[10] = 5


def test_get_invalid_index(persistent_array):
    """Тест 33. Проверка получения элемента с недопустимым индексом"""
    with pytest.raises(ValueError):
        persistent_array[-1]
    with pytest.raises(ValueError):
        persistent_array[10]


def test_empty_array():
    """Тест 34. Проверка работы с пустым массивом"""
    empty_array = PersistentArray(size=0)
    assert empty_array.get_size() == 0
    assert empty_array.check_is_empty() is True
    with pytest.raises(ValueError, match="Invalid index"):
        _ = empty_array[0]


def test_combination_operations(persistent_array):
    """Тест 35. Проверка сложной последовательности операций"""
    persistent_array.add(10)
    persistent_array.insert(1, 20)
    persistent_array.pop(0)
    persistent_array[2] = 30
    assert persistent_array.get_size() == 6


def test_version_consistency(persistent_array):
    """Тест 36. Проверка консистентности версий"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.set_version(1)
    assert persistent_array.get_size() == 7
    assert persistent_array[5] == 10

    persistent_array.set_version(2)
    assert persistent_array.get_size() == 7
    assert persistent_array[6] == 20


def test_remove_last_element(persistent_array):
    """Тест 37. Проверка удаления последнего элемента"""
    persistent_array.add(10)
    removed_value = persistent_array.pop(persistent_array.get_size() - 1)
    assert removed_value == 10
    assert persistent_array.get_size() == 5


def test_add_and_pop_multiple(persistent_array):
    """Тест 38. Проверка добавления и удаления нескольких элементов"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    persistent_array.pop(1)
    persistent_array.add(40)
    persistent_array.pop(2)
    assert persistent_array.get_size() == 7


def test_large_index_access(persistent_array):
    """Тест 39. Проверка доступа по большому индексу"""
    persistent_array.add(10)
    persistent_array.add(20)
    with pytest.raises(ValueError):
        persistent_array[10]


def test_invalid_index_insertion(persistent_array):
    """Тест 40. Проверка вставки по недопустимому индексу"""
    persistent_array.add(10)
    persistent_array.add(20)
    with pytest.raises(ValueError):
        persistent_array.insert(10, 15)


def test_set_version_invalid(persistent_array):
    """Тест 41. Проверка установки несуществующей версии"""
    persistent_array.add(10)
    persistent_array.add(20)
    with pytest.raises(ValueError):
        persistent_array.set_version(3)


def test_update_element_in_existing_version(persistent_array):
    """Тест 42. Проверка обновления элемента при добавлении в существующую версию"""
    persistent_array.add(10)
    persistent_array.set_version(1)
    persistent_array.add(20)
    assert persistent_array[5] == 10
    assert persistent_array[6] == 20


def test_set_element_in_empty_array():
    """Тест 43. Проверка обновления элемента в пустом массиве"""
    empty_array = PersistentArray(size=0)
    with pytest.raises(ValueError):
        empty_array[0] = 5


def test_insert_after_remove(persistent_array):
    """Тест 44. Проверка повторной вставки после удаления элемента"""
    persistent_array.add(10)
    persistent_array.remove(0)
    persistent_array.insert(0, 20)
    assert persistent_array[0] == 20


def test_multiple_additions(persistent_array):
    """Тест 45. Проверка добавления нескольких элементов"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    assert persistent_array.get_size() == 8
    assert persistent_array[5] == 10
    assert persistent_array[6] == 20
    assert persistent_array[7] == 30


def test_size_after_operations(persistent_array):
    """Тест 46. Проверка размера после последовательных операций"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.remove(1)
    persistent_array.insert(0, 30)
    assert persistent_array.get_size() == 7


def test_version_does_not_modify_current_state(persistent_array):
    """Тест 47. Проверка того, что версия не изменяет текущие данные"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.set_version(1)
    persistent_array.add(30)
    persistent_array.set_version(2)
    assert persistent_array[0] == 0


def test_add_after_remove_all_elements(persistent_array):
    """Тест 48. Проверка добавления элемента после удаления всех элементов"""
    persistent_array.remove(0)
    persistent_array.remove(0)
    persistent_array.remove(0)
    persistent_array.remove(0)
    persistent_array.remove(0)
    persistent_array.add(100)
    assert persistent_array.get_size() == 1
    assert persistent_array[0] == 100


def test_index_after_operations(persistent_array):
    """Тест 49. Проверка правильности индекса после множества операций"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    persistent_array.remove(1)
    persistent_array.insert(1, 25)
    persistent_array[2] = 40
    assert persistent_array[1] == 25
    assert persistent_array[2] == 40


def test_large_index_add_remove(persistent_array):
    """Тест 50. Проверка добавления и удаления на больших индексах"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    persistent_array.remove(2)
    persistent_array.insert(1, 40)
    persistent_array[2] = 50
    assert persistent_array[1] == 40
    assert persistent_array[2] == 50
