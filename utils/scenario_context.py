class ScenarioContext:
    """
    A container class to store and share arbitrary test data across different BDD steps.
    This satisfies the container class requirement.
    """
    def __init__(self):
        self._data = {}

    def set(self, key: str, value: any):
        """Store a value with a specific key."""
        self._data[key] = value

    def get(self, key: str, default: any = None) -> any:
        """Retrieve a value by its key. Returns default if not found."""
        return self._data.get(key, default)

    def clear(self):
        """Clear all stored data."""
        self._data.clear()
