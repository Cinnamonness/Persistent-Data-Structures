import pytest
from persistent_map import PersistentMap


# Тестирование методов класса PersistentMap
@pytest.fixture
def persistent_map():
    """Фикстура для создания PersistentMap"""
    return PersistentMap({'a': 1, 'b': 2})


def test_get_version(persistent_map):
    """Тест 1. Проверка получения состояния на определенной версии"""
    persistent_map['c'] = 3
    persistent_map.set_version(1)
    assert persistent_map['c'] == 3

    persistent_map.set_version(0)
    with pytest.raises(KeyError, match='Key "c" does not exist'):
        persistent_map.get(0, 'c')


def test_set_version(persistent_map):
    """Тест 2. Проверка обновления версии"""
    persistent_map['c'] = 3
    persistent_map.set_version(1)
    assert persistent_map['c'] == 3


def test_invalid_version_get(persistent_map):
    """Тест 3. Проверка на исключение для недопустимой версии при получении"""
    with pytest.raises(ValueError, match='Version "2" does not exist'):
        persistent_map.get(2, 'a')


def test_invalid_key_get(persistent_map):
    """Тест 4. Проверка на исключение для недопустимого ключа при получении"""
    with pytest.raises(KeyError, match='Key "c" does not exist'):
        persistent_map.get(0, 'c')


def test_setitem(persistent_map):
    """Тест 5. Проверка обновления элемента с использованием __setitem__"""
    persistent_map['c'] = 3
    assert persistent_map['c'] == 3


def test_getitem(persistent_map):
    """Тест 6. Проверка получения элемента с использованием __getitem__"""
    assert persistent_map['a'] == 1
    assert persistent_map['b'] == 2


def test_pop(persistent_map):
    """Тест 7. Проверка удаления элемента с использованием pop"""
    value = persistent_map.pop('a')
    assert value == 1
    assert 'a' not in persistent_map._version_map[persistent_map._current_version].state


def test_remove(persistent_map):
    """Тест 8. Проверка удаления элемента с использованием remove"""
    persistent_map.remove('a')
    assert 'a' not in persistent_map._version_map[persistent_map._current_version].state


def test_clear(persistent_map):
    """Тест 9. Проверка очистки структуры данных"""
    persistent_map.clear()
    assert persistent_map._version_map[persistent_map._current_version].state == {}


def test_version_history(persistent_map):
    """Тест 10. Проверка истории версий"""
    persistent_map['c'] = 3
    persistent_map.set_version(1)
    persistent_map['d'] = 4
    persistent_map.set_version(2)

    assert persistent_map.get_version(0) == {'a': 1, 'b': 2}
    assert persistent_map.get_version(1) == {'a': 1, 'b': 2, 'c': 3}
    assert persistent_map.get_version(2) == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_create_new_state(persistent_map):
    """Тест 11. Проверка создания новой версии с минимальным дублированием данных"""
    initial_state = persistent_map._version_map[persistent_map._current_version].state.copy()
    persistent_map['c'] = 3
    assert persistent_map._version_map[persistent_map._current_version].state != initial_state
    assert initial_state == {'a': 1, 'b': 2}


def test_multiple_versions(persistent_map):
    """Тест 12. Проверка изменения на несколько версий"""
    persistent_map['c'] = 3
    persistent_map.set_version(1)
    persistent_map['d'] = 4
    persistent_map.set_version(2)

    persistent_map['e'] = 5
    persistent_map.set_version(3)

    assert persistent_map.get_version(1) == {'a': 1, 'b': 2, 'c': 3}
    assert persistent_map.get_version(2) == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    assert persistent_map.get_version(3) == {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}


def test_setitem_overwrite(persistent_map):
    """Тест 13. Проверка перезаписи существующего элемента"""
    persistent_map['a'] = 10
    assert persistent_map['a'] == 10

    persistent_map['a'] = 20
    assert persistent_map['a'] == 20


def test_persistent_state_integrity(persistent_map):
    """Тест 14. Проверка целостности состояния после последовательных изменений"""
    persistent_map['c'] = 3
    version_1 = persistent_map.get_version(1)

    persistent_map['d'] = 4
    version_2 = persistent_map.get_version(2)

    assert version_1 == {'a': 1, 'b': 2, 'c': 3}
    assert version_2 == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    assert version_1 != version_2


def test_get_non_existing_key_version(persistent_map):
    """Тест 15. Проверка получения несуществующего ключа в существующей версии"""
    persistent_map.set_version(0)
    with pytest.raises(KeyError, match='Key "c" does not exist'):
        persistent_map.get(0, 'c')
