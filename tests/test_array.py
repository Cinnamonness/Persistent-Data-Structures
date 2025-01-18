import pytest
from persistent_array import PersistentArray


@pytest.fixture
def persistent_array():
    """Фикстура для создания персистентного массива с размером 5 и значением по умолчанию 0."""
    return PersistentArray(size=5, default_value=0)


def test_initial_state(persistent_array):
    """Тест 1. Проверка начального состояния массива"""
    assert persistent_array.get_size() == 5
    for i in range(5):
        assert persistent_array[i] == 0


def test_get_item(persistent_array):
    """Тест 2. Проверка метода получения элемента массива"""
    persistent_array[1] = 10
    assert persistent_array[1] == 10


def test_set_item(persistent_array):
    """Тест 3. Проверка метода установки элемента массива"""
    persistent_array[2] = 20
    assert persistent_array[2] == 20
    assert persistent_array.get_version(0)[2] == 0


def test_add(persistent_array):
    """Тест 4. Проверка добавления нового элемента в массив"""
    persistent_array.add(42)
    assert persistent_array.get_size() == 6
    assert persistent_array[5] == 42


def test_pop(persistent_array):
    """Тест 5. Проверка удаления элемента из массива"""
    persistent_array[2] = 30
    removed = persistent_array.pop(2)
    assert removed == 30
    assert persistent_array.get_size() == 4


def test_insert(persistent_array):
    """Тест 6. Проверка вставки элемента в массив по индексу"""
    persistent_array.insert(2, 50)
    assert persistent_array[2] == 50
    assert persistent_array.get_size() == 6


def test_remove(persistent_array):
    """Тест 7. Проверка удаления элемента массива по индексу"""
    persistent_array.remove(3)
    assert persistent_array.get_size() == 4


def test_undo_redo(persistent_array):
    """Тест 8. Проверка функционала отмены и повторения изменений"""
    persistent_array[1] = 10
    persistent_array.undo()
    assert persistent_array[1] == 0
    persistent_array.redo()
    assert persistent_array[1] == 10


def test_check_is_empty():
    """Тест 9. Проверка метода проверки пустоты массива"""
    array = PersistentArray(size=0)
    assert array.check_is_empty()
    array.add(5)
    assert not array.check_is_empty()


def test_get_version(persistent_array):
    """Тест 10. Проверка получения версии массива"""
    persistent_array[1] = 10
    assert persistent_array.get_version(0)[1] == 0
    assert persistent_array.get_version(1)[1] == 10
    with pytest.raises(ValueError):
        persistent_array.get_version(3)


def test_update_version(persistent_array):
    """Тест 11. Проверка метода обновления версии массива"""
    persistent_array[1] = 10
    persistent_array.update_version(1)
    assert persistent_array[1] == 10
    with pytest.raises(ValueError):
        persistent_array.update_version(2)


def test_undo(persistent_array):
    """Тест 12. Проверка отмены изменений (undo)"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    state_after_add = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_add == [0, 0, 0, 0, 0, 10, 20, 30]
    persistent_array.undo()
    state_after_undo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_undo == [0, 0, 0, 0, 0, 10, 20]
    persistent_array.undo()
    state_after_second_undo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_second_undo == [0, 0, 0, 0, 0, 10]


def test_redo(persistent_array):
    """Тест 13. Проверка возврата изменений после undo (redo)"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    persistent_array.undo()
    persistent_array.undo()
    state_after_undo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_undo == [0, 0, 0, 0, 0, 10]
    persistent_array.redo()
    state_after_redo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_redo == [0, 0, 0, 0, 0, 10, 20]
    persistent_array.redo()
    state_after_second_redo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_second_redo == [0, 0, 0, 0, 0, 10, 20, 30]


def test_undo_redo_integrity(persistent_array):
    """Тест 14. Проверка целостности данных при использовании undo и redo"""
    persistent_array.add(10)
    persistent_array.add(20)
    state_after_add = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_add == [0, 0, 0, 0, 0, 10, 20]
    persistent_array.undo()
    state_after_undo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_undo == [0, 0, 0, 0, 0, 10]
    persistent_array.redo()
    state_after_redo = persistent_array._history[persistent_array._current_state].tolist()
    assert state_after_redo == [0, 0, 0, 0, 0, 10, 20]


def test_remove_nested_persistent_array(persistent_array):
    """Тест 15. Проверка удаления вложенной структуры из массива"""
    nested_array = PersistentArray(size=3, default_value=5)
    persistent_array.add(nested_array)
    persistent_array.remove(5)
    assert persistent_array.get_size() == 5
    with pytest.raises(ValueError):
        persistent_array[5]


def test_nested_persistent_array_get(persistent_array):
    """Тест 16. Проверка получения элемента вложенной структуры"""
    nested_array = PersistentArray(size=3, default_value=5)
    persistent_array.add(nested_array)
    assert persistent_array[5][1] == 5


def test_size_after_pop(persistent_array):
    """Тест 17. Проверка размера после удаления элемента"""
    persistent_array.add(10)
    persistent_array.add(20)
    assert persistent_array.get_size() == 7
    persistent_array.pop(1)
    assert persistent_array.get_size() == 6


def test_multiple_versions(persistent_array):
    """Тест 18. Проверка сохранения нескольких версий"""
    persistent_array.add(10)
    persistent_array.add(20)
    persistent_array.add(30)
    assert persistent_array.get(0, 0) == 0
    assert persistent_array.get(1, 5) == 10
    assert persistent_array.get(2, 6) == 20
    assert persistent_array.get(3, 7) == 30


def test_invalid_index_get(persistent_array):
    """Тест 20. Проверка на исключение для недопустимого индекса при получении"""
    with pytest.raises(ValueError):
        persistent_array[10]


def test_invalid_index_set(persistent_array):
    """Тест 21. Проверка на исключение для недопустимого индекса при обновлении"""
    with pytest.raises(ValueError):
        persistent_array[10] = 5


def test_invalid_version_get(persistent_array):
    """Тест 22. Проверка на исключение для недопустимой версии при получении"""
    persistent_array.add(1)
    persistent_array.add(2)
    with pytest.raises(ValueError):
        persistent_array.get(10, 0)


def test_invalid_version_update(persistent_array):
    """Тест 23. Проверка на исключение для недопустимой версии при обновлении"""
    persistent_array.add(1)
    persistent_array.add(2)
    with pytest.raises(ValueError):
        persistent_array.update_version(10)


def test_nested_array(persistent_array):
    """Тест 24. Проверка вложенности персистентных массивов"""
    nested_array = PersistentArray(size=3, default_value=1)
    persistent_array.add(nested_array)
    assert persistent_array.get_size() == 6
    assert persistent_array[5] == nested_array
    assert persistent_array[5][1] == 1


def test_nested_array_undo_redo(persistent_array):
    """Тест 25. Проверка отмены и повторения изменений во вложенных массивах"""
    nested_array = PersistentArray(size=3, default_value=1)
    persistent_array.add(nested_array)
    persistent_array[5][0] = 42
    persistent_array.undo()
    assert persistent_array[5][0] == 1
    persistent_array.redo()
    assert persistent_array[5][0] == 42


def test_nested_array_deepcopy(persistent_array):
    """Тест 26. Проверка правильности работы deepcopy для вложенных массивов"""
    nested_array = PersistentArray(size=3, default_value=1)
    persistent_array.add(nested_array)
    persistent_array[5][0] = 42
    nested_array_copy = persistent_array.get_version(1)[5]
    assert nested_array_copy[0] == 1
    assert persistent_array[5][0] == 42


def test_remove_nested_array(persistent_array):
    """Тест 27. Проверка удаления вложенного массива"""
    nested_array = PersistentArray(size=3, default_value=1)
    persistent_array.add(nested_array)
    persistent_array.remove(5)
    assert persistent_array.get_size() == 5
    with pytest.raises(ValueError):
        persistent_array[5]
