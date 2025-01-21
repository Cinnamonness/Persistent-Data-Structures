import pytest

from persistent_list import PersistentLinkedList


# Тестирование методов класса PersistentLinkedList
@pytest.fixture
def persistent_list():
    """Создает фикстуру для тестирования PersistentLinkedList."""
    initial_data = [1, 2, 3]
    return PersistentLinkedList(initial_data)


def test_initial_state(persistent_list):
    """Тест 1. Проверка, что начальное состояние списка корректно"""
    assert persistent_list.get(version=0, index=0) == 1
    assert persistent_list.get(version=0, index=1) == 2
    assert persistent_list.get(version=0, index=2) == 3
    assert persistent_list.size == 3


def test_add_element(persistent_list):
    """Тест 2. Проверка на добавление нового элемента в конец списка"""
    persistent_list.add(4)
    assert persistent_list.get(version=1, index=3) == 4
    assert persistent_list.size == 4


def test_add_first_element(persistent_list):
    """Тест 3. Проверка на добавление элемента в начало списка"""
    persistent_list.add_first(0)
    assert persistent_list.get(version=1, index=0) == 0
    assert persistent_list.get(version=1, index=1) == 1
    assert persistent_list.size == 4


def test_insert_element(persistent_list):
    """Тест 4. Проверка на вставку элемента на заданный индекс"""
    persistent_list.insert(1, 10)
    assert persistent_list.get(version=1, index=1) == 10
    assert persistent_list.get(version=1, index=2) == 2
    assert persistent_list.size == 4


def test_pop_element(persistent_list):
    """Тест 5. Проверка на удаление элемента по индексу"""
    value = persistent_list.pop(1)
    assert value == 2
    assert persistent_list.get(version=1, index=1) == 3
    assert persistent_list.size == 2


def test_remove_element(persistent_list):
    """Тест 6. Проверка на удаление элемента с использованием remove()"""
    persistent_list.remove(0)
    assert persistent_list.get(version=1, index=0) == 2
    assert persistent_list.size == 2


def test_undo_operation(persistent_list):
    """Тест 7. Проверка на возможность отмены последней операции"""
    persistent_list.add(4)
    persistent_list.undo()
    assert persistent_list.size == 3
    assert persistent_list.get(version=0, index=2) == 3


def test_redo_operation(persistent_list):
    """Тест 8. Проверка на возможность повторения отмененной операции"""
    persistent_list.add(4)
    persistent_list.undo()
    persistent_list.redo()
    assert persistent_list.get(version=1, index=3) == 4
    assert persistent_list.size == 4


def test_version_retrieval(persistent_list):
    """Тест 9. Проверка на восстановление предыдущей версии списка"""
    persistent_list.add(4)
    persistent_list.add(5)
    persistent_list.update_version(0)
    assert persistent_list.size == 3
    assert persistent_list.get(version=0, index=2) == 3


def test_invalid_version(persistent_list):
    """Тест 10. Проверка на обработку неверного номера версии"""
    with pytest.raises(ValueError):
        persistent_list.get_version(10)


def test_index_out_of_range(persistent_list):
    """Тест 11. Проверка на обработку индекса за пределами диапазона"""
    with pytest.raises(IndexError):
        persistent_list.get(version=0, index=10)


@pytest.fixture
def setup_nested_persistent_list():
    """Фикстура для создания вложенной персистентной структуры"""
    inner_list = PersistentLinkedList([4, 5])
    outer_list = PersistentLinkedList([1, inner_list, 3])
    return outer_list, inner_list


def test_nested_persistence(setup_nested_persistent_list):
    """Тест 12. Проверка на вложенность и персистентность вложенных структур"""
    outer_list, inner_list = setup_nested_persistent_list
    assert outer_list.get(index=0) == 1
    assert isinstance(outer_list.get(index=1), PersistentLinkedList)
    assert outer_list.get(index=2) == 3
    nested_list = outer_list.get(index=1)
    assert nested_list.get(index=0) == 4
    assert nested_list.get(index=1) == 5
    nested_list.add(6)
    assert nested_list.get(version=1, index=2) == 6
    updated_nested = outer_list.get(index=1)
    assert updated_nested.get(version=1, index=2) == 6
    assert outer_list.get(version=0, index=1).get(index=1) == 5


def test_nested_undo_redo(setup_nested_persistent_list):
    """Тест 13. Проверка работы undo и redo для вложенных структур"""
    outer_list, inner_list = setup_nested_persistent_list
    inner_list.add(7)
    assert inner_list.get(version=1, index=2) == 7
    inner_list.undo()
    assert inner_list.get(index=1) == 5
    with pytest.raises(IndexError):
        inner_list.get(index=2)
    inner_list.redo()
    assert inner_list.get(index=2) == 7


def test_deep_nested_persistence():
    """Тест 14. Проверка на многослойную вложенность персистентных структур"""
    inner_list = PersistentLinkedList([1, 2])
    middle_list = PersistentLinkedList([inner_list])
    outer_list = PersistentLinkedList([middle_list])
    inner_list.add(3)
    assert inner_list.get(index=2) == 3
    assert middle_list.get(index=0).get(index=2) == 3
    assert outer_list.get(index=0).get(index=0).get(index=2) == 3
    assert inner_list.get(version=0, index=1) == 2
    assert middle_list.get(version=0, index=0).get(version=0, index=1) == 2
    assert outer_list.get(version=0, index=0).get(version=0, index=0).get(version=0, index=1) == 2


def test_cascade_undo_redo():
    """Тест 15. Проверка каскадную вложенность"""
    list1 = PersistentLinkedList([1, 2, 3])
    list2 = PersistentLinkedList([4, 5])
    list3 = PersistentLinkedList([6, 7])
    list1.add(list2)
    list2.add(list3)
    assert list1.get() == [list2]
    list1.undo()
    assert list1.get() == [1, 2, 3]
    list1.redo()
    assert list1.get() == [list2]


def test_triple_nested_undo_redo():
    """Тест 16. Проверка undo-redo с тройной вложенностью"""
    list1 = PersistentLinkedList([1, 2, 3])
    list2 = PersistentLinkedList([4, 5])
    list3 = PersistentLinkedList([6, 7])
    list1.add(list2)
    list2.add(list3)
    assert list1.get() == [list2]
    assert list2.get() == [list3]
    list3.add(8)
    assert list3.get() == [6, 7, 8]
    list1.undo()
    assert list1.get() == [1, 2, 3]
    list2.undo()
    assert list2.get() == [4, 5]
    list3.undo()
    assert list3.get() == [6, 7]
    list1.redo()
    assert list1.get() == [list2]
    list2.redo()
    assert list2.get() == [list3]
    list3.redo()
    assert list3.get() == [6, 7, 8]
