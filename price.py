from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def apply_discount(self, price):
        pass

class TenPercentDiscount(Discount):
    def apply_discount(self, price):
        return price * 0.9  # 10% скидка

class TwentyPercentDiscount(Discount):
    def apply_discount(self, price):
        return price * 0.8  # 20% скидка

def calculate_price(price, discount: Discount):
    return discount.apply_discount(price)

# Использование:
print(calculate_price(100, TenPercentDiscount()))  # 90.0
print(calculate_price(100, TwentyPercentDiscount()))  # 80.0
