import heapq

def dijkstra(graph, start):
    # Инициализация расстояний до всех вершин как бесконечность
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0  # Расстояние до начальной вершины равно 0
    # Инициализация приоритетной очереди с начальной вершиной
    queue = [(0, start)]

    while queue:
        # Извлечение вершины с наименьшим известным расстоянием
        current_distance, current_vertex = heapq.heappop(queue)

        # Если текущее расстояние до текущей вершины больше уже известного,
        # то игнорируем эту вершину
        if current_distance > distances[current_vertex]:
            continue

        # Обновление расстояний до соседей текущей вершины
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            # Если новое расстояние меньше уже известного, обновляем его
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

# Пример графа в виде списка смежности
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_vertex = 'A'
shortest_distances = dijkstra(graph, start_vertex)
print("Кратчайшие расстояния от вершины", start_vertex, ":")
for vertex, distance in shortest_distances.items():
    print("До вершины", vertex, ":", distance)
