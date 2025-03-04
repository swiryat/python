class Observer:
    def update(self, message):
        pass

class ConcreteObserver(Observer):
    def update(self, message):
        print(f"Получено сообщение: {message}")

class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

# Использование:
subject = Subject()
observer1 = ConcreteObserver()
observer2 = ConcreteObserver()

subject.add_observer(observer1)
subject.add_observer(observer2)

subject.notify_observers("Изменение состояния!")
