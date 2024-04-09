import heapq

def read_weighted_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        matrix = [list(map(int, line.strip().split())) for line in lines]
    return matrix

def prim_minimum_spanning_tree(graph):
    num_vertices = len(graph)
    visited = [False] * num_vertices
    min_spanning_tree = []

    # Используем кучу для хранения ребер графа
    heap = [(0, 0, 0)]  # (вес, начальная вершина, конечная вершина)

    while heap:
        weight, start, end = heapq.heappop(heap)

        if visited[end]:
            continue

        visited[end] = True
        min_spanning_tree.append((start, end, weight))

        for neighbor, neighbor_weight in enumerate(graph[end]):
            if not visited[neighbor] and neighbor_weight > 0:
                heapq.heappush(heap, (neighbor_weight, end, neighbor))

    return min_spanning_tree

def main():
    file_path = input("Введите путь к файлу с весовой матрицей графа: ")
    
    try:
        graph = read_weighted_matrix(file_path)
        min_spanning_tree = prim_minimum_spanning_tree(graph)

        print("Минимальное остовное дерево:")
        for edge in min_spanning_tree:
            print(f"Ребро: {edge[0]} - {edge[1]}, Вес: {edge[2]}")

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
