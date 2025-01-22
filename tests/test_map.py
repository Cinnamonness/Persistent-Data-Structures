import pytest
from persistent_map import PersistentMap
from transaction import transaction
from threading import Thread


# Тестирование методов класса PersistentMap
@pytest.fixture
def persistent_map():
    """Фикстура для создания PersistentMap"""
    return PersistentMap({'a': 1, 'b': 2})


def test_get_version(persistent_map):
    """Тест 1. Проверка получения состояния на определенной версии"""
    persistent_map['c'] = 3
    persistent_map.update_version(1)
    assert persistent_map['c'] == 3

    persistent_map.update_version(0)
    with pytest.raises(KeyError, match='Key "c" does not exist'):
        persistent_map.get(0, 'c')


def test_update_version(persistent_map):
    """Тест 2. Проверка обновления версии"""
    persistent_map['c'] = 3
    persistent_map.update_version(1)
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
    assert 'a' not in persistent_map._history[persistent_map._current_state]


def test_remove(persistent_map):
    """Тест 8. Проверка удаления элемента с использованием remove"""
    persistent_map.remove('a')
    assert 'a' not in persistent_map._history[persistent_map._current_state]


def test_clear(persistent_map):
    """Тест 9. Проверка очистки структуры данных"""
    persistent_map.clear()
    assert persistent_map._history[persistent_map._current_state] == {}


def test_version_history(persistent_map):
    """Тест 10. Проверка истории версий"""
    persistent_map['c'] = 3
    persistent_map.update_version(1)
    persistent_map['d'] = 4
    persistent_map.update_version(2)

    assert persistent_map.get_version(0) == {'a': 1, 'b': 2}
    assert persistent_map.get_version(1) == {'a': 1, 'b': 2, 'c': 3}
    assert persistent_map.get_version(2) == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_transaction_success(persistent_map):
    """Тест 11. Проверка успешного выполнения транзакции"""
    def modify_map():
        persistent_map['c'] = 3
    transaction(modify_map)
    assert persistent_map['c'] == 3


def test_transaction_with_threads(persistent_map):
    """Тест 12. Проверка выполнения транзакции с использованием потоков"""
    def modify_map_in_thread():
        persistent_map['d'] = 4
    thread1 = Thread(target=transaction, args=(modify_map_in_thread,))
    thread2 = Thread(target=transaction, args=(modify_map_in_thread,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    assert persistent_map['d'] == 4


def test_transaction_state_consistency(persistent_map):
    """Тест 13. Проверка консистентности состояния после транзакций"""
    def modify_map_consistently():
        persistent_map['f'] = 6
        persistent_map['g'] = 7
    transaction(modify_map_consistently)
    assert persistent_map['f'] == 6
    assert persistent_map['g'] == 7


def test_mutex_locking(persistent_map):
    """Тест 14. Проверка работы мьютекса"""
    counter = 0

    def modify_shared_resource():
        nonlocal counter
        for _ in range(100):
            with persistent_map._mutex:
                temp = counter
                counter = temp + 1
    threads = [Thread(target=modify_shared_resource) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert counter == 1000


def test_nested_transactions(persistent_map):
    """Тест 15. Проверка корректности работы вложенных транзакций"""
    def outer_transaction():
        persistent_map['outer'] = 1

        def inner_transaction():
            persistent_map['inner'] = 2
        transaction(inner_transaction)
    transaction(outer_transaction)
    assert persistent_map['outer'] == 1
    assert persistent_map['inner'] == 2


def test_transaction_isolation(persistent_map):
    """Тест 16. Проверка изоляции транзакций"""
    def modify_map():
        persistent_map['e'] = 5
    thread1 = Thread(target=transaction, args=(modify_map,))
    thread2 = Thread(target=transaction, args=(modify_map,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    assert persistent_map['e'] == 5


def test_multiple_changes_in_transaction(persistent_map):
    """Тест 17. Проверка транзакции с несколькими изменениями"""
    def modify_multiple_keys():
        persistent_map['x'] = 10
        persistent_map['y'] = 20
    transaction(modify_multiple_keys)
    assert persistent_map['x'] == 10
    assert persistent_map['y'] == 20


def test_transaction_versioning(persistent_map):
    """Тест 18. Проверка корректности версий после транзакции"""
    def modify_map():
        persistent_map['new_key'] = 42
    transaction(modify_map)
    assert persistent_map['new_key'] == 42
    assert persistent_map._current_state == 1
