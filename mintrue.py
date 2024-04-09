class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def build_tree_from_array(arr, start, end):
    if start > end:
        return None
    mid = (start + end) // 2
    node = TreeNode(arr[mid])
    node.left = build_tree_from_array(arr, start, mid - 1)
    node.right = build_tree_from_array(arr, mid + 1, end)
    return node

def find_min(root):
    if root is None:
        return float('inf')
    if root.left is None:
        return root.val
    return find_min(root.left)

# Чтение ввода из файла
with open(r'C:\Users\swer\Documents\GitHub\python\input.txt', 'r') as file:
    n = int(file.readline())
    arr = list(map(int, file.readline().split()))

# Построение дерева из массива
root = build_tree_from_array(arr, 0, n - 1)

# Нахождение минимального элемента в дереве
min_val = find_min(root)

# Запись результата в файл
with open('C:\\Users\\swer\\Documents\\GitHub\\python\\input.txt', 'r') as file:
    file.write(str(min_val))
