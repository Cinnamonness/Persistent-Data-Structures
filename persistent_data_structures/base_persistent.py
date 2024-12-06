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

    def _create_new_state(self) -> None:
        """Создает новую версию."""
        self._last_state += 1
        self._history[self._last_state] = deepcopy(self._history[self._current_state])
        self._current_state = self._last_state
