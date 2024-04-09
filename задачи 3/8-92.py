def read_weighted_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        matrix = [list(map(int, line.strip().split())) for line in lines]
    return matrix

def floyd_warshall(graph):
    num_vertices = len(graph)

    # Инициализация матрицы расстояний
    dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            dist[i][j] = graph[i][j]

    # Алгоритм Флойда-Уоршелла
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

def main():
    file_path = input("Введите путь к файлу с весовой матрицей графа: ")
    
    try:
        graph = read_weighted_matrix(file_path)
        shortest_distances = floyd_warshall(graph)

        print("Матрица кратчайших расстояний:")
        for row in shortest_distances:
            print(row)

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
