import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from persistent_array import PersistentArray
import unittest


class TestPersistentArray(unittest.TestCase):

    def test_initialization(self):
        """
        Тестирование инициализации массива.
        """
        arr = PersistentArray(max_size=12, depth=4, bits_for_level=8)
        self.assertEqual(arr.size(), 0)  # Массив должен быть пустым при инициализации
        self.assertEqual(arr.max_size, 12)  # Проверяем, что максимальный размер равен 10

    def test_add(self):
        """
        Тестирование добавления элемента в массив.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        self.assertEqual(arr.size(), 1)  # Массив должен содержать один элемент
        self.assertEqual(arr.get(0), 1)  # Проверяем, что добавленный элемент равен 1

    def test_add_full_array(self):
        """
        Тестирование добавления элемента в полный массив.
        """
        arr = PersistentArray(max_size=2)
        arr.add(1)
        arr.add(2)
        with self.assertRaises(ValueError):
            arr.add(3)  # Попытка добавить элемент в полный массив должна вызвать ошибку

    def test_insert(self):
        """
        Тестирование вставки элемента по индексу.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        arr.add(2)
        arr.insert(1, 3)  # Вставляем 3 на индекс 1
        self.assertEqual(arr.get(1), 3)  # Элемент на индексе 1 должен быть 3
        self.assertEqual(arr.size(), 3)  # Размер массива должен быть 3

    def test_insert_invalid_index(self):
        """
        Тестирование вставки элемента с неверным индексом.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        with self.assertRaises(IndexError):
            arr.insert(2, 2)  # Индекс 2 недопустим для массива размером 1

    def test_remove(self):
        """
        Тестирование удаления элемента по индексу.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        arr.add(2)
        arr.remove(0)  # Удаляем элемент по индексу 0
        self.assertEqual(arr.size(), 1)  # Размер массива должен быть 1
        self.assertEqual(arr.get(0), 2)  # Оставшийся элемент на индексе 0 должен быть 2

    def test_remove_invalid_index(self):
        """
        Тестирование удаления элемента с неверным индексом.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        with self.assertRaises(IndexError):
            arr.remove(1)  # Индекс 1 недопустим для массива размером 1

    def test_pop(self):
        """
        Тестирование удаления последнего элемента (pop).
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        arr.add(2)
        popped = arr.pop()  # Удаляем и возвращаем последний элемент
        self.assertEqual(popped, 2)  # Последний элемент должен быть 2
        self.assertEqual(arr.size(), 1)  # Размер массива должен быть 1 после удаления

    def test_pop_empty(self):
        """
        Тестирование pop для пустого массива.
        """
        arr = PersistentArray(max_size=5)
        with self.assertRaises(ValueError):
            arr.pop()  # Попытка удалить элемент из пустого массива должна вызвать ошибку

    def test_clear(self):
        """
        Тестирование очистки массива.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        arr.clear()  # Очищаем массив
        self.assertEqual(arr.size(), 0)  # Массив должен быть пустым после очистки

    def test_clone(self):
        """
        Тестирование клонирования массива.
        """
        arr = PersistentArray(max_size=5)
        arr.add(1)
        arr.add(2)
        cloned_arr = arr.clone()  # Создаем копию массива
        self.assertEqual(arr.size(), cloned_arr.size())  # Размеры должны совпадать
        self.assertEqual(arr.get(0), cloned_arr.get(0))  # Элементы должны совпадать
        self.assertIsNot(arr, cloned_arr)  # Объекты должны быть разными

    def test_indexing(self):
        """
        Тестирование индексации через __getitem__
        """
        arr = PersistentArray(max_size=5)
        arr.add(10)
        arr.add(20)
        self.assertEqual(arr[0], 10)  # Проверка доступа через индексацию (0 -> 10)
        self.assertEqual(arr[1], 20)  # Проверка доступа через индексацию (1 -> 20)

    def test_set_indexing(self):
        """
        Тестирование индексации через __setitem__
        """
        arr = PersistentArray(max_size=5)
        arr.add(10)
        arr[0] = 30  # Меняем элемент на индексе 0
        self.assertEqual(arr[0], 30)  # Элемент на индексе 0 должен быть 30
        self.assertEqual(arr.size(), 1)  # Размер массива не изменился

if __name__ == "__main__":
    unittest.main()