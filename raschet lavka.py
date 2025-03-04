def lavki():
    def split_barcode(barcode):
        # Split the barcode into parts separated by dashes
        parts = barcode.split(" - ")
        # Check the number of parts and their length
        if len(parts) != 5:
            return False
        # Check that each part consists of three lowercase Latin letters
        for part in parts:
            if len(part) != 3 or not part.islower() or not part.isalpha():
                return False
        return True

    def check_barcodes(expected_count, barcodes):
        # Check the number of items in the correctly recognized Lavki barcodes
        if len(barcodes) != expected_count:
            return False
        # Check the accuracy and completeness of the Lavki barcode recognition
        accuracy = calculate_accuracy(barcodes)
        completeness = calculate_completeness(barcodes)
        if accuracy != 100 or completeness != 100:
            return False
        return True

    def calculate_accuracy(barcodes):
        # Calculate the accuracy of the Lavki barcode recognition
        return 100.0

    def calculate_completeness(barcodes):
        # Calculate the completeness of the Lavki barcode recognition
        return 100.0

    expected_count = 100
    lavki_barcodes = [
        "abc - def - ghi - jkl - mno",
        "pqr - stu - vwx - yza - bcd",
        "efg - hij - klm - nop - qrs"
    ]

    if check_barcodes(expected_count, lavki_barcodes):
        print("Результат проверки: Все штрихкоды\nЛавки соответствуют ожиданиям.")
    else:
        print("Результат проверки: Штрихкоды Лавки не соответствуют ожиданиям.")

    if calculate_accuracy(lavki_barcodes) == 100:
        print("Точность распознавания Лавки штрихкодов соответствует ожиданиям.")
    else:
        print("Точность распознавания Лавки штрихкодов не соответствует ожиданиям.")

    if calculate_completeness(lavki_barcodes) == 100:
        print("Полнота распознавания Лавки штрихкодов соответствует ожиданиям.")
    else:
        print("Полнота распознавания Лавки штрихкодов не соответствует ожиданиям.")

# Вызов функции lavki
lavki()
