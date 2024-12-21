from copy import deepcopy


class BasePersistent:
    """Базовый класс для персистентных стркутур данных.

    Каждая персистентная структура будет хранить в себе историю изменений в виде словаря с ключами
    версиями и значениями - состояниями. Также персистентная структура будет хранить номер ткущей
    и номер последней версии.
    """
    def __init__(self, initial_state=None) -> None:
        """Инициализирует персистентную структуру данных.
        :param initial_state: Начальное состояние персистентной структуры данных.
        """
        self._history = {0: initial_state}
        self._current_state = 0
        self._last_state = 0
        self._container = None
        self._location = None

    def get_version(self, version):
        """Возвращает состояние персистентной структуры данных на указанной версии.

        :param version: Номер версии.
        :return: Состояние персистентной структуры данных на указанной версии.
        :raises ValueError: Если указанная версия не существует.
        """
        if version < 0 or version >= len(self._history):
            raise ValueError(f'Version "{version}" does not exist')
        return self._history[version]

    def update_version(self, version):
        """Обновляет текущую версию персистентной структуры данных до указанной.

        :param version: Номер версии.
        :raises ValueError: Если указанная версия не существует.
        """
        if version < 0 or version >= len(self._history):
            raise ValueError(f'Version "{version}" does not exist')
        self._current_state = version

    def undo(self):
        """Отменяет последнее изменение."""
        if self._container is not None:
            raise NotImplementedError(f'Cannot undo inside container "{self._container}"')
        if self._current_state == 0:
            raise ValueError("No actions to undo")
        if self._current_state > 0:
            self._current_state -= 1

    def redo(self):
        """Отменяет отмененное изменение."""
        if self._container is not None:
            raise NotImplementedError(f'Cannot redo inside container "{self._container}"')
        if self._current_state < self._last_state:
            self._current_state += 1

    def _create_new_state(self) -> None:
        """Создает новую версию."""
        # Персистентные структуры могут быть вложенными,
        # поэтому нужно сохранять историю изменений в родительской персистентной структуре
        if self._container is not None:
            # В текущей версии родительской структуры подменяем имеющуюся вложенную структуру
            # на ее копию, таким образом изменения во вложенной структуре не будут отражаться на
            # прощлых версиях родительской структуры
            self._container._history[
                self._container._current_state
            ][self._location] = deepcopy(self)
        self._last_state += 1
        self._history[self._last_state] = deepcopy(self._history[self._current_state])
        self._current_state = self._last_state
        if self._container is not None:
            self._container[self._location] = self
