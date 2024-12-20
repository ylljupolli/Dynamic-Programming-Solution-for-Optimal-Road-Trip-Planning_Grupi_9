import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

def plot_graph_with_background(cities, distances, positions, map_image_path):
    img = mpimg.imread(map_image_path)
    G = nx.Graph()
    for i, city in enumerate(cities):
        for j, cost in enumerate(distances[i]):
            if cost > 0:
                G.add_edge(cities[i], cities[j], weight=cost)
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(img, extent=[0, 10, 0, 12], aspect='auto')
    pos = {city: positions[i] for i, city in enumerate(cities)}

def plot_final_subgraph(cities, positions, full_path):
    G = nx.DiGraph()
    for i in range(len(full_path) - 1):
        G.add_edge(full_path[i], full_path[i + 1])
    pos = {city: positions[cities.index(city)] for city in cities}
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=3000, font_size=10, font_weight='bold')
    plt.title("Optimal Route with Intermediate Stops")
    plt.show()

def compute_all_pairs_shortest_paths(cities, distances):
    G = nx.Graph()
    for i, city_from in enumerate(cities):
        for j, city_to in enumerate(cities):
            if distances[i][j] > 0:
                G.add_edge(city_from, city_to, weight=distances[i][j])
    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))
    full_paths = dict(nx.all_pairs_dijkstra_path(G, weight='weight'))
    return shortest_paths, full_paths

def traveling_salesman_with_indirect_routes(cities, mandatory_stops, shortest_paths):
    n = len(mandatory_stops)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for u in range(n):
            if mask & (1 << u):
                for v in range(n):
                    if not (mask & (1 << v)):
                        dp[mask | (1 << v)][v] = min(dp[mask | (1 << v)][v], dp[mask][u] + shortest_paths[mandatory_stops[u]][mandatory_stops[v]])
    min_cost = float('inf')
    last_city = -1
    for u in range(1, n):
        cost = dp[(1 << n) - 1][u] + shortest_paths[mandatory_stops[u]][mandatory_stops[0]]
        if cost < min_cost:
            min_cost = cost
            last_city = u
    path = []
    mask = (1 << n) - 1
    current_city = last_city
    while current_city != -1:
        path.append(mandatory_stops[current_city])
        next_mask = mask ^ (1 << current_city)
        next_city = -1
        for u in range(n):
            if dp[mask][current_city] == dp[next_mask][u] + shortest_paths[mandatory_stops[u]][mandatory_stops[current_city]]:
                next_city = u
                break
        mask = next_mask
        current_city = next_city
    path.append(mandatory_stops[0])
    path.reverse()
    return path, min_cost

def reconstruct_full_path(path, full_paths):
    full_path = []
    for i in range(len(path) - 1):
        segment = full_paths[path[i]][path[i + 1]]
        if i > 0:
            segment = segment[1:]
        full_path.extend(segment)
    return full_path

def optimal_road_trip(cities, distances, positions):
    plot_graph_with_background(cities, distances, positions, map_image_path)
    budget = float(input("Enter your budget for the trip: "))
    print("Cities:")
    for i, city in enumerate(cities):
        print(f"{i}: {city}")
    mandatory_indices = list(map(int, input("Enter the indices of mandatory stops (comma-separated): ").split(',')))
    non_mandatory_input = input("Enter the indices of non-mandatory stops (comma-separated, or press Enter to skip): ").strip()
    non_mandatory_indices = list(map(int, non_mandatory_input.split(','))) if non_mandatory_input else []
    mandatory_stops = [cities[i] for i in mandatory_indices]
    non_mandatory_stops = [cities[i] for i in non_mandatory_indices]
    include_return = input("Do you want to include the returning route to the starting city? (yes/no): ").strip().lower() == 'yes'
    plt.close('all')
    shortest_paths, full_paths = compute_all_pairs_shortest_paths(cities, distances)
    mandatory_path, mandatory_cost = traveling_salesman(mandatory_stops, shortest_paths, include_return)
    if mandatory_cost <= budget:
        print("Mandatory Route:", mandatory_path)
        print("Cost:", mandatory_cost)
        full_path = reconstruct_full_path(mandatory_path, full_paths)
        plot_final_subgraph(cities, positions, full_path, map_image_path, distances, include_return)
        remaining_budget = budget - mandatory_cost
        if non_mandatory_stops:
            all_stops = mandatory_stops + [stop for stop in non_mandatory_stops if stop not in mandatory_stops]
            combined_path, combined_cost = traveling_salesman(all_stops, shortest_paths, include_return)
            if combined_cost <= budget:
                print("Combined Route (Including Non-Mandatory Stops):", combined_path)
                print("Cost:", combined_cost)
                full_combined_path = reconstruct_full_path(combined_path, full_paths)
                plot_final_subgraph(cities, positions, full_combined_path, map_image_path, distances, include_return)
            else:
                print("Not enough budget to include non-mandatory stops.")
        else:
            print("No non-mandatory stops specified.")
    else:
        print("No feasible route within the budget for mandatory stops.")
        plt.close('all')

if __name__ == "__main__":
    cities = ["Paris", "Berlin", "Rome", "Madrid", "Amsterdam", "Vienna"]
    base_distances = [
        [0, 1050, 0, 1260, 100, 0],
        [1050, 0, 1180, 0, 750, 100],
        [0, 1180, 0, 1360, 0, 800],
        [1260, 0, 1360, 0, 1500, 0],
        [100, 750, 0, 1500, 0, 1000],
        [0, 100, 800, 0, 1000, 0]
    ]
    positions = [
        (2.3522, 48.8566),
        (13.4050, 52.5200),
        (12.4964, 41.9028),
        (-3.7038, 40.4168),
        (4.9041, 52.3676),
        (16.3738, 48.2082)
    ]
    optimal_road_trip(cities, base_distances, positions)
