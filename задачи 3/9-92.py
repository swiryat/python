def read_weighted_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        matrix = [list(map(int, line.strip().split())) for line in lines]
    return matrix

def floyd_warshall(graph):
    num_vertices = len(graph)

    # Инициализация матрицы расстояний и матрицы предшественников
    dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    pred = [[-1] * num_vertices for _ in range(num_vertices)]

    for i in range(num_vertices):
        for j in range(num_vertices):
            dist[i][j] = graph[i][j]
            if i != j and graph[i][j] != float('inf'):
                pred[i][j] = i

    # Алгоритм Флойда-Уоршелла
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]

    return dist, pred

def find_shortest_paths(start, end, pred):
    path = []
    current = end
    while current != start:
        path.insert(0, current)
        current = pred[start][current]
    path.insert(0, start)
    return path

def main():
    file_path = input("Введите путь к файлу с весовой матрицей графа: ")
    
    try:
        graph = read_weighted_matrix(file_path)
        shortest_distances, predecessors = floyd_warshall(graph)

        num_vertices = len(graph)
        print("Матрица кратчайших расстояний:")
        for row in shortest_distances:
            print(row)

        print("\nКратчайшие маршруты:")
        for start in range(num_vertices):
            for end in range(num_vertices):
                if start != end and predecessors[start][end] != -1:
                    path = find_shortest_paths(start, end, predecessors)
                    distance = shortest_distances[start][end]
                    print(f"Маршрут из {start} в {end}: {path}, Длина: {distance}")

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
