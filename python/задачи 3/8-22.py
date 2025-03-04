def binary_search(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == x:
            return mid  # Найден элемент, возвращаем его индекс
        elif arr[low] <= arr[mid]:
            # Левая половина отсортирована
            if arr[low] <= x <= arr[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            # Правая половина отсортирована
            if arr[mid] <= x <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1  # Элемент не найден

# Пример использования
arr = [4, 5, 6, 7, 0, 1, 2]
target = 0

result = binary_search(arr, target)

if result != -1:
    print(f"Элемент {target} найден по индексу {result}.")
else:
    print(f"Элемент {target} не найден.")
