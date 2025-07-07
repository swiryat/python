import random
import time
import cProfile
import pstats
import io
import matplotlib.pyplot as plt

class BellmanFord:
    def __init__(self, vertices, edges, source):
        self.V = vertices
        self.edges = edges
        self.source = source
        self.dist = [float('inf')] * vertices
        self.predecessor = [-1] * vertices
        self.history = []

    def run(self):
        self.dist[self.source] = 0

        # Основной цикл
        for i in range(self.V - 1):
            changed = False
            for u, v, weight in self.edges:
                if self.dist[u] != float('inf') and self.dist[u] + weight < self.dist[v]:
                    self.dist[v] = self.dist[u] + weight
                    self.predecessor[v] = u
                    changed = True
            self.history.append(self.dist.copy())
            if not changed:
                break

        # Проверка на отрицательный цикл
        for u, v, weight in self.edges:
            if self.dist[u] != float('inf') and self.dist[u] + weight < self.dist[v]:
                raise ValueError("Обнаружен отрицательный цикл")

        return self.dist

    def get_path(self, target):
        path = []
        while target != -1:
            path.append(target)
            target = self.predecessor[target]
        return path[::-1]

    def visualize_iterations(self):
        for i, distances in enumerate(self.history):
            plt.plot(distances, label=f'Итерация {i+1}')
        plt.xlabel('Вершина')
        plt.ylabel('Дистанция')
        plt.title('Эволюция расстояний')
        plt.legend()
        plt.grid()
        plt.show()

# === Тестовая демонстрация ===

def demo():
    V = 5
    E = [
        (0, 1, -1),
        (0, 2,  4),
        (1, 2,  3),
        (1, 3,  2),
        (1, 4,  2),
        (3, 2,  5),
        (3, 1,  1),
        (4, 3, -3)
    ]
    bf = BellmanFord(V, E, 0)
    distances = bf.run()
    print("Кратчайшие расстояния:", distances)
    print("Путь до 3-й вершины:", bf.get_path(3))
    bf.visualize_iterations()

# === Профилирование ===

def profile_demo():
    pr = cProfile.Profile()
    pr.enable()
    demo()
    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

# === Запуск ===
if __name__ == "__main__":
    profile_demo()
