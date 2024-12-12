from base_persistent import BasePersistent
from typing import Any, Dict


class PersistentMap(BasePersistent):
    """A persistent associative array.

    Represents a dictionary that preserves the history of changes.
    """

    def __init__(self, initial_state: Dict[Any, Any] = {}) -> None:
        """Initializes a persistent associative array.

        :param initial_state: The initial state of the persistent data structure.
        """
        super().__init__(initial_state)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Updates or creates an item by the specified key in the new version.

        :param key: The key to be updated or created.
        :param value: The value associated with the key.
        """
        self._create_new_state()
        self._version_map[self._last_version].state[key] = value

    def __getitem__(self, key: Any) -> Any:
        """Returns the item of the current version by the specified key.

        :param key: The key of the item to be fetched.
        :return: The value corresponding to the specified key or None if the key does not exist.
        """
        return self._version_map[self._current_version].state.get(key)

    def get(self, version: int, key: Any) -> Any:
        """Returns the item from the specified version and key.

        :param version: The version number.
        :param key: The key of the item to be fetched.
        :return: The value corresponding to the specified key.
        :raises ValueError: If the version does not exist.
        :raises KeyError: If the key does not exist.
        """
        if version not in self._version_map:
            raise ValueError(f'Version "{version}" does not exist')
        if key not in self._version_map[version].state:
            raise KeyError(f'Key "{key}" does not exist')
        return self._version_map[version].state[key]

    def pop(self, key: Any) -> Any:
        """Removes and returns the item by the specified key.

        :param key: The key of the item to be removed.
        :return: The removed item.
        """
        self._create_new_state()
        return self._version_map[self._last_version].state.pop(key)

    def remove(self, key: Any) -> None:
        """Removes an item by the specified key in the new version.

        :param key: The key of the item to be removed.
        """
        self.pop(key)

    def clear(self) -> None:
        """Clears the associative array in the new version."""
        self._create_new_state()
        self._version_map[self._current_version].state.clear()
