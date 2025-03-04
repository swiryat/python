def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

def main():
    # Пример графа заданного списком смежности
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
        'G': ['C']
    }

    start_vertex = input("Введите начальную вершину: ")
    end_vertex = input("Введите конечную вершину: ")

    paths = find_all_paths(graph, start_vertex, end_vertex)

    if paths:
        print(f"Все маршруты из {start_vertex} в {end_vertex}:")
        for path in paths:
            print(" -> ".join(path))
    else:
        print(f"Маршруты из {start_vertex} в {end_vertex} не найдены.")

if __name__ == "__main__":
    main()
