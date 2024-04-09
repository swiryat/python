def binary_search(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == x:
            return mid  # Найден элемент, возвращаем его индекс
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return -1  # Элемент не найден

def intersection(arr1, arr2):
    result = []

    for x in arr1:
        if binary_search(arr2, x) != -1:
            result.append(x)

    return result

# Пример использования
arr1 = [1, 2, 3, 4, 5]
arr2 = [3, 4, 5, 6, 7]

result = intersection(arr1, arr2)

print("Отсортированный массив, содержащий только общие значения:", result)
