# Optimal Road Trip Planning

## Overview
This project provides a dynamic programming-based solution for planning an optimal road trip. It calculates the most efficient travel route visiting mandatory stops within a specified budget, with optional integration of non-mandatory stops. The solution employs graph theory for route optimization and visualizes the results on a map.

## Features
- Calculates shortest paths between cities using Dijkstra's algorithm.
- Implements a Traveling Salesman Problem (TSP) solver for mandatory stops.
- Option to include non-mandatory stops in the route.
- Visualizes the graph of cities and travel routes on a map.
- Supports budget constraints and optional return to the starting city.

## Prerequisites
- Python 3.8 or later
- Required libraries:
  - `networkx`
  - `matplotlib`
  - `pillow` (for image support, if needed)

Install the libraries using:
```bash
pip install networkx matplotlib
```

## Files
- `main.py`: Contains the implementation of the optimal road trip algorithm and visualization.
- `map.png`: A background map image used for visualization.

## Input Data
- **Cities**: A list of city names.
- **Distances**: A matrix representing the travel costs between cities.
- **Positions**: Coordinates for each city to place them on the map.

## How to Run
1. Save the city data, distances, and positions in the `main.py` file.
2. Ensure `map.png` is present in the same directory as the script.
3. Run the script:
   ```bash
   python main.py
   ```
4. Follow the on-screen instructions to input budget, mandatory stops, and optional non-mandatory stops.

## Example Cities
This project includes a predefined list of 13 French regions with their distances and positions. Modify these lists as needed to adapt the project to your scenario.

## Key Functions
### `plot_graph_with_background`
Plots all cities and their connections on the background map.

### `plot_final_subgraph`
Visualizes the optimal travel route overlaid on the background map.

### `compute_all_pairs_shortest_paths`
Computes shortest paths and distances between all city pairs using Dijkstra's algorithm.

### `traveling_salesman`
Solves the TSP for a set of mandatory stops, optionally including a return to the start.

### `reconstruct_full_path`
Expands the TSP solution to show the full route sequence.

### `optimal_road_trip`
Coordinates user input, route computation, and visualization.

## Customization
- **Cities and Distances**: Modify the `cities`, `base_distances`, and `positions` lists.
- **Map**: Replace `map.png` with your own map image (ensure it matches the coordinate system used).
- **Budget and Constraints**: Customize the input prompts or hardcode values as needed.

## Visualization
The project provides two visualizations:
1. **All Regions**: Displays all cities and their connections.
2. **Optimal Route**: Highlights the computed optimal route with cost annotations.

## Example Workflow
1. Enter your trip budget.
2. Select mandatory stops by their indices.
3. Optionally add non-mandatory stops.
4. Decide whether to include a return route.
5. View the computed route and cost.

## Output
- **Mandatory Route**: Displays the cities and total cost.
- **Combined Route** (if feasible): Shows the route including non-mandatory stops and its cost.
- Visual graphs showing the connections and optimal routes.

## Limitations
- The project assumes non-negative travel costs.
- Limited to static map visualization.
- Performance may degrade with a large number of cities.

## Future Enhancements
- Incorporate real-world map data for geolocation.
- Use more advanced optimization algorithms for larger datasets.
- Add GUI for user-friendly interaction.

## License
This project is released under the MIT License. Feel free to use and modify it as needed.

