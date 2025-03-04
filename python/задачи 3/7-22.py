def bubble_sort(arr):
    n = len(arr)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def binary_search(arr, x):
    low, high = 0, len(arr) - 1
    count = 0

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == x:
            count += 1

            # Ищем дополнительные вхождения влево
            left = mid - 1
            while left >= 0 and arr[left] == x:
                count += 1
                left -= 1

            # Ищем дополнительные вхождения вправо
            right = mid + 1
            while right < len(arr) and arr[right] == x:
                count += 1
                right += 1

            return count
        elif arr[mid] > x:
            low = mid + 1
        else:
            high = mid - 1

    return count

# Пример использования
arr = [5, 3, 8, 2, 5, 7, 1, 4, 5, 6]
x = 5

bubble_sort(arr)
result = binary_search(arr, x)

print("Отсортированный массив:", arr)
print(f"Количество вхождений {x}: {result}")
