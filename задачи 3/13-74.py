class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def evaluate_expression_tree(root):
    if root is None:
        return 0

    if root.left is None and root.right is None:
        return root.value

    left_value = evaluate_expression_tree(root.left)
    right_value = evaluate_expression_tree(root.right)

    if root.value == '+':
        return left_value + right_value
    elif root.value == '-':
        return left_value - right_value
    elif root.value == '*':
        return left_value * right_value
    elif root.value == '/':
        return left_value / right_value

    return 0

def build_expression_tree(expression):
    stack = []

    operators = {'+', '-', '*', '/'}

    for char in expression.split():
        if char.isdigit() or (char[0] == '-' and char[1:].isdigit()):
            stack.append(TreeNode(int(char)))
        elif char in operators:
            root = TreeNode(char)
            if stack:
                root.right = stack.pop()
            if stack:
                root.left = stack.pop()
            stack.append(root)

    return stack.pop()

# Остальной код остается без изменений

def main():
    expression = input("Введите арифметическое выражение: ")
    expression_tree = build_expression_tree(expression)
    
    result = evaluate_expression_tree(expression_tree)
    
    print(f"Результат выражения {expression}: {result}")

if __name__ == "__main__":
    main()
