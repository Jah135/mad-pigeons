from typing import Callable, Any


class EventSignal:
    """An object used to store callback functions that can then all be invoked at once at a later time."""

    callbacks: list[Callable[..., None]]

    def __init__(self) -> None:
        self.callbacks = []

    def connect(self, callback: Callable[..., None]):
        """Adds a callback function"""
        self.callbacks.append(callback)

    def disconnect_all(self):
        """Disconnects all connected callback functions"""

        self.callbacks.clear()

    def fire(self, *args: Any):
        """Invokes all connected callback functions"""

        for callback in self.callbacks:
            callback(*args)
