import osmnx as ox
import json
import random
# Choose an area 
place_name = "Mumbai, India"

# Download drivable road network 
G = ox.graph_from_place(place_name, network_type='drive')


# Build exportable structures 
nodes = {}
edges = []
edge_id = 1

list_of_pois = ["restaurant","hospital","petrol station","pharmacy","hotel","atm"]
list_of_road_types = ["primary","secondary","tertiary","local","expressway"]
node_id = 0
map = {}
maxlat = -1
minlat = 360
maxlon = -1
minlon = 360
for node, data in G.nodes(data=True):
    nodes[node] = {
        "id": node_id,
        "lat": data["x"],
        "lon": data["y"],
        "pois": list_of_pois[random.randint(0,5):random.randint(0,5):random.randint(1,2)]
    }
    maxlat = max(maxlat,data["x"])
    minlat = min(minlat,data["x"])
    maxlon = max(maxlon,data["y"])
    minlon = min(minlon,data["y"])
    map[node] = node_id
    node_id += 1
done = []
for u, v, data in G.edges(data=True):
    print(data)
    dist = data.get("length", 0.0)
    road_type = data.get("highway", "local")
    maxspeed = data.get("maxspeed", 50)  # default 50 km/h
    if road_type not in list_of_road_types:
        road_type = list_of_road_types[random.randint(0,4)]
    if isinstance(maxspeed, list):
        maxspeed = maxspeed[0]
    try:
        maxspeed = float(maxspeed)
    except:
        maxspeed = 50.0
    speed_profile = [random.randint(1,101)*random.random()+0.5 for i in range(96)]
    if_speed = random.random() > 0.5
    oneway = data.get("oneway")
    if ((map[u],map[v]) in done or map[u]==map[v]):
        continue
    edges.append({
        "id": edge_id,
        "u": map[u],
        "v": map[v],
        "length": dist,
        "average_time": max(0,maxspeed+random.randint(-10,10)*random.random()),
        "road_type": road_type,
        "oneway":bool(oneway)
    })
    done.append((map[u],map[v]))
    if (oneway==False):
        done.append((map[v],map[u]))
    
    if (if_speed):
        edges[-1].update({"speed_profile":speed_profile})
    edge_id += 1

#  Export JSON 
output = {"nodes": list(nodes.values()), "meta":{"id":"sample1","nodes":node_id,"description":"DoraMapMakers"} ,"edges": edges}
with open("graph.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Exported {len(nodes)} nodes and {len(edges)} edges to graph.json")

no_of_queries = 20
queries = []
list_of_queries = ["k_shortest_paths","k_shortest_paths_heuristic","approx_shortest_path"]
for query_id in range(1,no_of_queries+1):
    type = random.randint(0,2)
    num_queries = 1
    if (type==2):
        num_queries*=random.randrange(10,1000,10)
    
    queries.append({
        "type":list_of_queries[type],
        "id":query_id
    })
    if (type==0):
        s = random.randint(1,node_id)
        t = random.randint(1,node_id)
        k = random.randint(2,20)
        queries[-1].update({"source":s,"target":t,"k":k,"mode":"distance"})
    elif (type==1):
        s = random.randint(1,node_id)
        t = random.randint(1,node_id)
        k = random.randint(2,7)
        overlap = random.randint(20,80)
        queries[-1].update({"source":s,"target":t,"k":k,"overlap_threshold":overlap})
    elif (type==2):
        sub_queries = []
        for j in range(num_queries):
            s = random.randint(1,node_id)
            t = random.randint(1,node_id)
            sub_queries.append({"source":s,"target":t})
        time = random.randint(5,15)
        error = random.randint(5,15)
        queries[-1].update({"queries":sub_queries,"time_budget_ms":time,"acceptable_error_pct":error})
    
output1 = {"meta":{"id":"sample1"} ,"events":queries}
with open("queries.json", "w") as f:
    json.dump(output1, f, indent=2)

print(f"Queries added to queries.json")

