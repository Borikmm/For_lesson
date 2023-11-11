import urllib.request
import json
import sys
import os.path
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        '''
        Этот метод обеспечивает симметричность графика. Другими словами, если существует путь от узла A к B со значением V, должен быть путь от узла B к узлу A со значением V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Возвращает узлы графа"
        return self.nodes

    def get_outgoing_edges(self, node):
        "Возвращает соседей узла"
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Возвращает значение ребра между двумя узлами."
        return self.graph[node1][node2]


    def dijkstra_algorithm(self, start_node):
        unvisited_nodes = list(self.get_nodes())

        # Мы будем использовать этот словарь, чтобы сэкономить на посещении каждого узла и обновлять его по мере продвижения по графику
        shortest_path = {}

        # Мы будем использовать этот dict, чтобы сохранить кратчайший известный путь к найденному узлу
        previous_nodes = {}

        # Мы будем использовать max_value для инициализации значения "бесконечности" непосещенных узлов
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        # Однако мы инициализируем значение начального узла 0
        shortest_path[start_node] = 0

        # Алгоритм выполняется до тех пор, пока мы не посетим все узлы
        while unvisited_nodes:
            # Приведенный ниже блок кода находит узел с наименьшей оценкой
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния
            neighbors = graph.get_outgoing_edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

            # После посещения его соседей мы отмечаем узел как "посещенный"
            unvisited_nodes.remove(current_min_node)

        self.previous_nodes = previous_nodes
        self.shortest_path = shortest_path


    def print_result(self, start_node, target_node, list_citys):
        path = []
        node = target_node

        while node != start_node:
            path.append(node)
            node = self.previous_nodes[node]

        # Добавить начальный узел вручную
        path.append(start_node)

        print("Найден следующий лучший маршрут с ценностью {} km.".format(self.shortest_path[target_node]))
        print(" -> ".join(reversed(path)))
        print(f"Посещено городов: {int((len(path)*100)/len(list_city))}%")

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69")

def get_courd(place):
    location = geolocator.geocode(place)
    return (location.latitude, location.longitude)

def find_near_city(list_city):
    init_graph = {}
    for node in list_city:
        init_graph[node] = {}


    if (os.path.isfile('data.txt')):
        with open('data.txt') as json_file:
            distance_between_citys = json.load(json_file)
    else:
        distance_between_citys = {}
        for node in list_city:
            distance_between_citys[node] = {}

        for a in list_city:
            for b in list_city:
                if a == b:
                    continue
                try:
                    distance_between_citys[a][b] = find_dist_line(a, b)
                    print("True")

                except:
                    print("..................")
                    try:
                        distance_between_citys[a][b] = find_dist_line(a, b)
                    except: print("Джекпот сучки")

        with open('data.txt', 'w') as outfile:
            json.dump(distance_between_citys, outfile)

    for a in list_city:
        need = []
        for key, value in distance_between_citys[a].items():
            need.append((key, value))
        #print(f"{a}")
        need1 = sorted([(n[1], n[0]) for n in need])
        for b in range(0, 2):
            #print(f"{need1[b][0]} = {need1[b][1]}")


            init_graph[a][need1[b][1]] = need1[b][0]


    return init_graph

API_BANG = "Al75wVKnKol2excS7Cf4HrKi_yhXZVNCDFFfY-7QBOB9EAqUB6PCigzXqchPFdPO"

def find_dist_line(city1, city2):
    distance = geodesic(get_courd(city1), get_courd(city2)).km
    return distance

def find_distance_real(city1:str=None, city2:str=None, long:int=None, lat:int=None) -> int:

    longitude = get_courd(city1)[1] if long == None else long
    latitude = get_courd(city1)[0] if lat == None else lat

    destination = city2

    encodedDest = urllib.parse.quote(destination, safe='')

    routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(
        longitude) + "&wp.1=" + encodedDest + "&key=" + API_BANG

    request = urllib.request.Request(routeUrl)
    response = urllib.request.urlopen(request)

    r = response.read().decode(encoding="utf-8")
    result = json.loads(r)

    need = result["resourceSets"][0]["resources"][0]["travelDistance"]

    return need

if __name__ == "__main__":

    list_city = ['Москва',
                 'Санкт-Петербург',
                 'Казань',
                 'Новосибирск',
                 'Екатеринбург',
                 'Нижний Новгород',
                 'Челябинск',
                 'Омск',
                 'Самара',
                 'Ростов-на-Дону',
                 'Уфа',
                 'Красноярск',
                 'Пермь',
                 'Воронеж',
                 'Волгоград',
                 'Краснодар',
                 'Саратов',
                 'Тюмень',
                 'Тольятти',
                 'Ижевск',
                 'Чита']

    # 17 citys = 80%

    init_graph = find_near_city(list_city)
    graph = Graph(list_city, init_graph)
    graph.dijkstra_algorithm(start_node="Москва")
    graph.print_result(start_node="Москва", target_node="Чита", list_citys=list_city)



