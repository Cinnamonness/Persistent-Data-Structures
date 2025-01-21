import pytest
from persistent_map import PersistentMap


@pytest.fixture
def setup_persistent_map():
    """Фикстура для создания персистентного ассоциативного массива."""
    return PersistentMap({"a": 1, "b": 2, "c": 3})


def test_get_version(setup_persistent_map):
    """Тест 1. Проверка получения версии персистентного массива"""
    persistent_map = setup_persistent_map
    assert persistent_map.get_version(0) == {"a": 1, "b": 2, "c": 3}


def test_update_version(setup_persistent_map):
    """Тест 2. Проверка обновления версии массива"""
    persistent_map = setup_persistent_map
    persistent_map["d"] = 4
    persistent_map.update_version(0)
    assert persistent_map.get_version(0) == {"a": 1, "b": 2, "c": 3}


def test_setitem_add_new_key(setup_persistent_map):
    """Тест 3. Проверка добавления нового ключа"""
    persistent_map = setup_persistent_map
    persistent_map["d"] = 4
    assert persistent_map["d"] == 4
    assert persistent_map.get_version(1) == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_setitem_update_key(setup_persistent_map):
    """Тест 4. Проверка изменения значения существующего ключа"""
    persistent_map = setup_persistent_map
    persistent_map["a"] = 10
    assert persistent_map["a"] == 10
    assert persistent_map.get_version(1) == {"a": 10, "b": 2, "c": 3}


def test_getitem(setup_persistent_map):
    """Тест 5. Проверка получения значения по ключу"""
    persistent_map = setup_persistent_map
    assert persistent_map["a"] == 1
    assert persistent_map["b"] == 2
    assert persistent_map["c"] == 3


def test_get_existing_version_key(setup_persistent_map):
    """Тест 6. Проверка получения значения существующего ключа из версии"""
    persistent_map = setup_persistent_map
    assert persistent_map.get(0, "a") == 1
    with pytest.raises(KeyError):
        persistent_map.get(0, "d")


def test_get_invalid_version(setup_persistent_map):
    """Тест 7. Проверка ошибки при запросе несуществующей версии"""
    persistent_map = setup_persistent_map
    with pytest.raises(ValueError):
        persistent_map.get(10, "a")


def test_pop_existing_key(setup_persistent_map):
    """Тест 8. Проверка удаления ключа методом pop"""
    persistent_map = setup_persistent_map
    popped_value = persistent_map.pop("a")
    assert popped_value == 1
    assert "a" not in persistent_map.get_version(1)


def test_pop_non_existing_key(setup_persistent_map):
    """Тест 9. Проверка ошибки при pop несуществующего ключа"""
    persistent_map = setup_persistent_map
    with pytest.raises(KeyError):
        persistent_map.pop("d")


def test_remove_existing_key(setup_persistent_map):
    """Тест 10. Проверка удаления ключа методом remove"""
    persistent_map = setup_persistent_map
    persistent_map.remove("b")
    assert "b" not in persistent_map.get_version(1)


def test_remove_non_existing_key(setup_persistent_map):
    """Тест 11. Проверка ошибки при remove несуществующего ключа"""
    persistent_map = setup_persistent_map
    with pytest.raises(KeyError):
        persistent_map.remove("d")


def test_clear(setup_persistent_map):
    """Тест 12. Проверка очистки массива методом clear"""
    persistent_map = setup_persistent_map
    persistent_map.clear()
    assert persistent_map.get_version(1) == {}


def test_undo(setup_persistent_map):
    """Тест 13. Проверка отмены последней операции"""
    persistent_map = setup_persistent_map
    persistent_map["d"] = 4
    persistent_map.undo()
    assert persistent_map.get_version(0) == {"a": 1, "b": 2, "c": 3}


def test_redo(setup_persistent_map):
    """Тест 14. Проверка повторения последней отмененной операции"""
    persistent_map = setup_persistent_map
    persistent_map["d"] = 4
    persistent_map.undo()
    persistent_map.redo()
    assert persistent_map.get_version(1) == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_undo_without_changes(setup_persistent_map):
    """Тест 15. Проверка ошибки отмены операции без изменений"""
    persistent_map = setup_persistent_map
    with pytest.raises(ValueError):
        persistent_map.undo()


def test_redo_without_undo(setup_persistent_map):
    """Тест 16. Проверка ошибки повтора без отмены операции"""
    persistent_map = setup_persistent_map
    persistent_map["d"] = 4
    with pytest.raises(ValueError):
        persistent_map.redo()


def test_setitem_nested_structure(setup_persistent_map):
    """Тест 17. Проверка добавления вложенной структуры в персистентный массив"""
    persistent_map = setup_persistent_map
    nested_map = PersistentMap({"nested_key": 1})
    persistent_map["nested"] = nested_map
    assert persistent_map["nested"].get_version(0) == {"nested_key": 1}
    assert persistent_map.get_version(1) == {"a": 1, "b": 2, "c": 3, "nested": nested_map}


def test_nested_undo(setup_persistent_map):
    """Тест 18. Проверка отмены изменений в вложенной структуре"""
    persistent_map = setup_persistent_map
    nested_map = PersistentMap({"nested_key": 1})
    persistent_map["nested"] = nested_map
    nested_map["nested_key"] = 2
    persistent_map.undo()
    assert persistent_map.get_version(0) == {"a": 1, "b": 2, "c": 3}
    assert persistent_map.get_version(1)["nested"]["nested_key"] == 1


def test_nested_redo(setup_persistent_map):
    """Тест 19. Проверка повтора изменений в вложенной структуре"""
    persistent_map = setup_persistent_map
    nested_map = PersistentMap({"nested_key": 1})
    persistent_map["nested"] = nested_map
    nested_map["nested_key"] = 2
    persistent_map.undo()
    persistent_map.redo()
    assert persistent_map.get_version(2)["nested"]["nested_key"] == 2


def test_remove_nested_structure(setup_persistent_map):
    """Тест 20. Проверка удаления вложенной структуры методом remove"""
    persistent_map = setup_persistent_map
    nested_map = PersistentMap({"nested_key": 1})
    persistent_map["nested"] = nested_map
    persistent_map.remove("nested")
    with pytest.raises(KeyError):
        persistent_map["nested"]


def test_cascade_undo_redo_nested():
    """Тест 13. Проверка каскадного undo/redo с вложенными структурами"""
    persistent_map = PersistentMap({
        "level1": PersistentMap({
            "level2": PersistentMap({
                "level3": 42
            })
        })
    })
    persistent_map["level1"]["level2"]["level3"] = 100
    assert persistent_map["level1"]["level2"]["level3"] == 100
    persistent_map["level1"]["level2"].undo()
    assert persistent_map["level1"]["level2"]["level3"] == 42
    persistent_map["level1"]["level2"].redo()
    assert persistent_map["level1"]["level2"]["level3"] == 100


def test_triple_nested_undo_redo():
    """Тест 14. Проверка undo/redo с тройной вложенностью"""
    persistent_map = PersistentMap({
        "level1": PersistentMap({
            "level2": PersistentMap({
                "level3": PersistentMap({"key": 333})
            })
        })
    })
    persistent_map["level1"]["level2"]["level3"]["key"] = 200
    assert persistent_map["level1"]["level2"]["level3"]["key"] == 200
    persistent_map["level1"]["level2"]["level3"].undo()
    assert persistent_map["level1"]["level2"]["level3"]["key"] == 333
    persistent_map["level1"]["level2"]["level3"].redo()
    assert persistent_map["level1"]["level2"]["level3"]["key"] == 200
