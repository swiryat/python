def binary_search_recursive(arr, target, left, right):
    if left > right:
        return False

    mid = (left + right) // 2

    if arr[mid] == target:
        return True
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# Пример использования
arr = [100, 450, 730, 800, 950, 999, 1000, 3000, 3300, 8000, 9990, 10000]
target = 999
result = binary_search_recursive(arr, target, 0, len(arr) - 1)
print(result)  # Выведет: True