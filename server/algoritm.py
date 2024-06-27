import networkx as nx
import osmnx as ox
import numpy as np
import heapq

# File Project https://github.com/raflihaidar/shortest-path-finding

# Menggunakan cache untuk OSMnx agar mempercepat pemrosesan dan menampilkan log di konsol
ox.config(use_cache=True, log_console=True)

def dijkstra_shortest_path(start_node, end_node, road_graph):
    # Inisialisasi jarak dari node awal ke semua node lain dengan nilai tak hingga
    distances = {node: float('inf') for node in road_graph.nodes}
    # Inisialisasi predecessor untuk melacak jalur
    predecessors = {node: None for node in road_graph.nodes}
    distances[start_node] = 0  # Jarak dari node awal ke dirinya sendiri adalah 0
    visited = set()  # Set untuk melacak node yang sudah dikunjungi

    # Priority queue yang berisi pasangan (jarak, node)
    priority_queue = [(0, start_node)]

    while priority_queue:
        # Mengambil node dengan jarak terpendek dari priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue  # Jika node sudah dikunjungi, lanjutkan ke iterasi berikutnya

        visited.add(current_node)  # Tandai node sebagai sudah dikunjungi

        if current_node == end_node:
            break  # Jika mencapai node tujuan, keluar dari loop

        # Iterasi melalui tetangga-tetangga dari node saat ini
        for neighbor, attr in road_graph[current_node].items():
            edge_weight = attr[0].get('length', 1.0)  # Mendapatkan bobot dari edge (panjang jalan)
            new_distance = current_distance + edge_weight  # Menghitung jarak baru

            # Jika jarak baru lebih kecil, perbarui jarak dan predecessor
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # Mengumpulkan jalur dari node tujuan ke node awal
    path = []
    current_node = end_node
    while current_node is not None:
        path.insert(0, current_node)  # Tambahkan node ke jalur
        current_node = predecessors[current_node]  # Melacak kembali ke node sebelumnya

    return path  # Mengembalikan jalur terpendek

def calculate_nearest_node(graph, latitude, longitude):
    # Mengonversi latitude dan longitude menjadi array 2D
    target_coords = np.array([[longitude, latitude]])
    # Mengekstraksi koordinat semua node dalam graf
    node_coords = np.array([[data['x'], data['y']] for _, data in graph.nodes(data=True)])
    # Menghitung jarak Euclidean antara titik tujuan dan semua node
    distances = np.linalg.norm(target_coords - node_coords, axis=1)
    # Mendapatkan indeks node terdekat
    nearest_node_index = np.argmin(distances)
    # Mengambil identifier node terdekat
    nearest_node = list(graph.nodes())[nearest_node_index]

    return nearest_node  # Mengembalikan node terdekat

def generate_path(origin_point, target_point, perimeter):
    # Mendapatkan batas wilayah berdasarkan titik asal dan titik tujuan
    origin_lat = origin_point[0]
    origin_long = origin_point[1]
    target_lat = target_point[0]
    target_long = target_point[1]
    
    # Menentukan batas utara dan selatan
    if origin_lat > target_lat:
        north = origin_lat 
        south = target_lat
    else:
        north = target_lat
        south = origin_lat

    # Menentukan batas timur dan barat
    if origin_long > target_long:
        east = origin_long 
        west = target_long
    else:
        east = target_long
        west = origin_long

    mode = 'drive'  # Mode 'drive', 'bike', 'walk' (walk biasanya terlalu lambat)

    # Mengambil graf jalan dari wilayah yang ditentukan menggunakan OSMnx
    roadgraph = ox.graph_from_bbox(north+perimeter, south-perimeter, east+perimeter, west-perimeter, network_type=mode, simplify=False)

    # Menghitung node terdekat dari titik asal dan tujuan
    origin_node = calculate_nearest_node(roadgraph, origin_point[0], origin_point[1])
    target_node = calculate_nearest_node(roadgraph, target_point[0], target_point[1])
    
    # Menggunakan algoritma Dijkstra bawaan dari NetworkX untuk menemukan jalur terpendek
    route = nx.shortest_path(roadgraph, origin_node, target_node, weight='length', method='dijkstra')

    # Mengonversi jalur yang ditemukan menjadi koordinat (latitude, longitude)
    route_map = []
    for node in route:
        point = roadgraph.nodes[node]
        route_map.append([point['y'], point['x']])
    
    return route_map  # Mengembalikan jalur sebagai daftar koordinat
