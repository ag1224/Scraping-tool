from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass

class ConsoleNotifier(Notifier):
    def notify(self, message: str) -> None:
        print(message)