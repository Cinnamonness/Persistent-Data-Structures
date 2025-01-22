import pytest
from persistent_list import PersistentLinkedList
from transaction import transaction
from threading import Thread


# Тестирование методов класса PersistentLinkedList
@pytest.fixture
def linked_list():
    """
    Фикстура для создания экземпляра персистентного двусвязного списка.
    """
    return PersistentLinkedList([1, 2, 3, 4, 5])


def test_add(linked_list):
    """Тест 1. Проверка добавления элемента в конец списка"""
    linked_list.add(6)
    assert linked_list.get(index=5) == 6


def test_add_first(linked_list):
    """Тест 2. Проверка добавления элемента в начало списка"""
    linked_list.add_first(0)
    assert linked_list.get(index=0) == 0


def test_insert(linked_list):
    """Тест 3. Проверка вставки элемента по индексу"""
    linked_list.insert(2, 10)
    assert linked_list.get(index=2) == 10
    assert linked_list.get(index=3) == 3


def test_pop(linked_list):
    """Тест 4. Проверка удаления элемента по индексу"""
    removed_value = linked_list.pop(2)
    assert removed_value == 3
    assert linked_list.get(index=2) == 4


def test_remove(linked_list):
    """Тест 5. Проверка удаления элемента по значению"""
    linked_list.remove(4)
    with pytest.raises(ValueError):
        linked_list.remove(4)


def test_get(linked_list):
    """Тест 6. Проверка получения элемента по индексу"""
    assert linked_list.get(index=0) == 1
    assert linked_list.get(index=4) == 5


def test_get_version(linked_list):
    """Тест 7. Проверка получения версии списка"""
    linked_list.add(6)
    linked_list.add(7)
    version_1 = linked_list.get_version(1)
    assert version_1[0] is not None
    version_0_values = []
    current = version_1[0]
    while current:
        version_0_values.append(current.value)
        current = current.next_node
    assert version_0_values == [1, 2, 3, 4, 5, 6]


def test_update_version(linked_list):
    """Тест 8. Проверка обновления версии списка"""
    linked_list.add(6)
    linked_list.add(7)
    linked_list.update_version(1)
    assert linked_list.get(index=5) == 6
    linked_list.update_version(0)
    assert linked_list.get(index=4) == 5


def test_clear(linked_list):
    """Тест 9. Проверка очистки списка"""
    linked_list.clear()
    assert linked_list.get_size() == 0
    assert linked_list.check_is_empty()


def test_get_size(linked_list):
    """Тест 10. Проверка получения размера списка"""
    assert linked_list.get_size() == 5
    linked_list.add(6)
    assert linked_list.get_size() == 6


def test_check_is_empty(linked_list):
    """Тест 11. Проверка метода для проверки пустоты списка"""
    linked_list.clear()
    assert linked_list.check_is_empty() is True
    linked_list.add(10)
    assert linked_list.check_is_empty() is False


def test_transaction_success(linked_list):
    """Тест 12. Проверка успешного выполнения транзакции"""
    def modify_list():
        linked_list.add_first(3)
    transaction(modify_list)
    assert linked_list[0] == 3


def test_transaction_with_threads(linked_list):
    """Тест 13. Проверка выполнения транзакции с использованием потоков"""
    def modify_list_in_thread():
        linked_list.add(4)
    thread1 = Thread(target=transaction, args=(modify_list_in_thread,))
    thread2 = Thread(target=transaction, args=(modify_list_in_thread,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    assert linked_list.get_size() == 7
    assert linked_list.get(index=5) == 4
    assert linked_list.get(index=6) == 4


def test_transaction_state_consistency(linked_list):
    """Тест 14. Проверка консистентности состояния после транзакций"""
    def modify_list_consistently():
        linked_list.add(6)
        linked_list.add(7)
    transaction(modify_list_consistently)
    assert linked_list.get(index=5) == 6
    assert linked_list.get(index=6) == 7


def test_mutex_locking(linked_list):
    """Тест 15. Проверка работы мьютекса"""
    counter = 0

    def modify_shared_resource():
        nonlocal counter
        for _ in range(100):
            with linked_list._mutex:
                temp = counter
                counter = temp + 1
    threads = [Thread(target=modify_shared_resource) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert counter == 1000


def test_nested_transactions(linked_list):
    """Тест 16. Проверка корректности работы вложенных транзакций"""
    def outer_transaction():
        linked_list.add(1)

        def inner_transaction():
            linked_list.add(2)
        transaction(inner_transaction)
    transaction(outer_transaction)
    assert linked_list.get(index=0) == 1
    assert linked_list.get(index=1) == 2


def test_multiple_changes_in_transaction(linked_list):
    """Тест 17. Проверка транзакции с несколькими изменениями"""
    def modify_multiple_elements():
        linked_list.add_first(10)
        linked_list.add_first(20)
    transaction(modify_multiple_elements)
    assert linked_list.get(index=1) == 10
    assert linked_list.get(index=0) == 20


def test_transaction_versioning(linked_list):
    """Тест 18. Проверка корректности версий после транзакции"""
    def modify_list():
        linked_list.add_first(42)
    transaction(modify_list)
    assert linked_list.get(index=0) == 42
    assert linked_list._current_state == 1
