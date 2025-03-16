class OldPrinter:
    def old_print(self, text):
        return f"Печатаю: {text}"

class NewPrinter:
    def print(self, text):
        return f"Печать: {text}"

class PrinterAdapter:
    def __init__(self, old_printer):
        self.old_printer = old_printer

    def print(self, text):
        return self.old_printer.old_print(text)

# Использование:
old_printer = OldPrinter()
adapter = PrinterAdapter(old_printer)
print(adapter.print("Привет"))  # "Печатаю: Привет"
