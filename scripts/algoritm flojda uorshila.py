def floyd_warshall(graph):
    n = len(graph)
    # Инициализация матрицы расстояний
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    # Заполнение матрицы изначальными значениями расстояний
    for u in graph:
        for v in graph[u]:
            dist[u][v] = graph[u][v]

    # Поиск кратчайших расстояний между всеми парами вершин через промежуточные вершины
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# Пример графа в виде словаря смежности
graph = {
    0: {0: 0, 1: 3, 2: 6},
    1: {0: float('inf'), 1: 0, 2: -2},
    2: {0: float('inf'), 1: float('inf'), 2: 0}
}

# Вызов алгоритма и вывод результатов
result = floyd_warshall(graph)
print("Матрица кратчайших расстояний:")
for row in result:
    print(row)
