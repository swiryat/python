class Node:
    def __init__(self, data, color="RED"):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        # Вставка нового узла в дерево
        node = Node(data)
        if not self.root:
            # Если дерево пустое, устанавливаем корень новым узлом
            self.root = node
            self.root.color = "BLACK"
            return
        
        current = self.root
        parent = None
        while current:
            # Ищем место для вставки нового узла
            parent = current
            if node.data < current.data:
                current = current.left
            else:
                current = current.right
        
        # Устанавливаем родителя для нового узла
        node.parent = parent
        if node.data < parent.data:
            parent.left = node
        else:
            parent.right = node

        # Балансировка после вставки
        self.fix_insert(node)

    def fix_insert(self, node):
        # Балансировка дерева после вставки нового узла
        while node != self.root and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                # Если родитель узла - левый потомок своего родителя
                uncle = node.parent.parent.right
                if uncle and uncle.color == "RED":
                    # Случай 1: дядя красный
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Случай 2: дядя черный и узел - правый потомок
                        node = node.parent
                        self.left_rotate(node)
                    # Случай 3: дядя черный и узел - левый потомок
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent)
            else:
                # Если родитель узла - правый потомок своего родителя
                uncle = node.parent.parent.left
                if uncle and uncle.color == "RED":
                    # Случай 1: дядя красный
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        # Случай 2: дядя черный и узел - левый потомок
                        node = node.parent
                        self.right_rotate(node)
                    # Случай 3: дядя черный и узел - правый потомок
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.left_rotate(node.parent.parent)

        self.root.color = "BLACK"

    def left_rotate(self, x):
        # Левый поворот узла
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        # Правый поворот узла
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def inorder_traversal(self, node):
        # Обход дерева в порядке возрастания значений
        if node:
            self.inorder_traversal(node.left)
            print(node.data, node.color)
            self.inorder_traversal(node.right)

# Пример использования:
tree = RedBlackTree()
tree.insert(10)
tree.insert(20)
tree.insert(30)
tree.insert(15)
tree.insert(25)
tree.inorder_traversal(tree.root)
