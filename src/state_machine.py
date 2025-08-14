from contextlib import contextmanager
import threading
from typing import TypeVar

T = TypeVar("T")


class State[T]:
    def transition(self, inputs: T) -> "State[T] | None": ...


class StateMachine[T]:
    """Thread safe state machine abstraction"""

    _current_state: State[T]
    _machine_mutex: threading.Semaphore

    def __init__(self) -> None:
        self._machine_mutex = threading.Semaphore()

    @contextmanager
    def get_state(self):
        with self._machine_mutex:
            yield self._current_state

    def transition(self, inputs: T):
        with self._machine_mutex:
            self._current_state = self._current_state.transition(inputs) or self._current_state
