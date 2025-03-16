class Strategy:
    def execute(self, a, b):
        pass

class AddStrategy(Strategy):
    def execute(self, a, b):
        return a + b

class SubtractStrategy(Strategy):
    def execute(self, a, b):
        return a - b

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, a, b):
        return self.strategy.execute(a, b)

# Использование:
context = Context(AddStrategy())
print(context.execute_strategy(5, 3))  # 8

context = Context(SubtractStrategy())
print(context.execute_strategy(5, 3))  # 2
