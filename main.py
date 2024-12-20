import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

map_image_path = "map.png"

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
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=8, font_weight='bold', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)
    plt.title("Cities and Travel Costs (All Regions)")
    plt.show(block=False)

def plot_final_subgraph(cities, positions, full_path, map_image_path, distances, include_return):
    img = mpimg.imread(map_image_path)
    G = nx.DiGraph()
    for i in range(len(full_path) - 1):
        G.add_edge(full_path[i], full_path[i + 1], weight=distances[cities.index(full_path[i])][cities.index(full_path[i + 1])])
    if include_return and distances[cities.index(full_path[-1])][cities.index(full_path[0])] > 0:
        G.add_edge(full_path[-1], full_path[0], weight=distances[cities.index(full_path[-1])][cities.index(full_path[0])])
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(img, extent=[0, 10, 0, 12], aspect='auto')
    pos = {city: positions[cities.index(city)] for city in cities}
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1000, font_size=10, font_weight='bold', edge_color='blue', ax=ax)
    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red', ax=ax)
    plt.title("Optimal Route")
    plt.show(block=True)

def compute_all_pairs_shortest_paths(cities, distances):
    G = nx.Graph()
    for i, city_from in enumerate(cities):
        for j, city_to in enumerate(cities):
            if distances[i][j] > 0:
                G.add_edge(city_from, city_to, weight=distances[i][j])
    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))
    full_paths = dict(nx.all_pairs_dijkstra_path(G, weight='weight'))
    return shortest_paths, full_paths

def traveling_salesman(mandatory_stops, shortest_paths, include_return):
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
        cost = dp[(1 << n) - 1][u]
        if include_return and shortest_paths[mandatory_stops[u]][mandatory_stops[0]] > 0:
            cost += shortest_paths[mandatory_stops[u]][mandatory_stops[0]]
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
    cities = [
        "Brittany", "Normandy", "Île-de-France", "Hauts-de-France", "Grand Est",
        "Pays de la Loire", "Centre-Val de Loire", "Bourgogne-Franche-Comté",
        "Nouvelle-Aquitaine", "Occitanie", "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur", "Corsica"
    ]

    base_distances = [
        [0, 300, 400, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0],  # Brittany
        [300, 0, 200, 400, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Normandy
        [400, 200, 0, 300, 400, 0, 200, 0, 0, 0, 0, 0, 0],  # Île-de-France
        [0, 400, 300, 0, 300, 0, 0, 0, 0, 0, 0, 0, 0],  # Hauts-de-France
        [0, 0, 400, 300, 0, 0, 0, 600, 0, 0, 0, 0, 0],  # Grand Est
        [200, 0, 0, 0, 0, 0, 300, 0, 500, 0, 0, 0, 0],  # Pays de la Loire
        [0, 0, 200, 0, 0, 300, 0, 400, 0, 0, 0, 0, 0],  # Centre-Val de Loire
        [0, 0, 0, 0, 600, 0, 400, 0, 600, 0, 800, 0, 0],  # Bourgogne-Franche-Comté
        [0, 0, 0, 0, 0, 500, 0, 600, 0, 500, 600, 0, 0],  # Nouvelle-Aquitaine
        [0, 0, 0, 0, 0, 0, 0, 0, 500, 0, 200, 600, 0],  # Occitanie
        [0, 0, 0, 0, 0, 0, 0, 800, 600, 200, 0, 100, 0],  # Auvergne-Rhône-Alpes
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 100, 0, 700],  # Provence-Alpes-Côte d'Azur
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 700, 0],  # Corsica
    ]

    positions = [
        (1.8, 8.3), (3.5, 9), (5, 8.8), (5, 10.5), (7, 9),
        (2.8, 7.3), (4.5, 7.5), (6.5, 7), (3.5, 4.8),
        (5, 3), (6.5, 5), (7.3, 3.2), (9.5, 1.5)
    ]

    optimal_road_trip(cities, base_distances, positions)
