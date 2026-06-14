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

no_of_queries = 1000
queries = []
list_of_patches = ["length","average_time","speed_profile","road_type"]
list_of_queries = ["remove_edge","modify_edge","knn","shortest_path"]
for query_id in range(1,no_of_queries+1):
    type = random.randint(0,3)
    edge_idx = -1+(type<2)*random.randint(1,edge_id-1)
    if_patch = (type==1)*random.random()>0.5
    source = -1+(type==3)*random.randint(0,node_id)
    target = -1+(type==3)*random.randint(0,node_id)
    mode = 0-(type!=3)+(random.random()>0.5)*(type==3)
    forbidden_nodes = (type==3)*[random.randint(0,node_id-1) for i in range(random.randint(0,int(random.random()/20*(node_id-1))))]
    forbidden_road_types = (type==3)*list_of_road_types[random.randint(0,4):random.randint(0,4)]
    poi = (type==2)*list_of_pois[random.randint(0,5)]
    lat = -1 + (type==2)*(random.randint(int(minlat),int(maxlat))+random.random())
    lon = -1 + (type==2)*(random.randint(int(minlon),int(maxlon))+random.random())
    k = -1+(type==2)*(1+random.randint(1,node_id))
    metric = 0-(type!=2)+(random.random()>0.5)*(type==2)
    queries.append({
        "type":list_of_queries[type],
        "id":query_id
    })
    if (edge_idx!=-1):
        queries[-1].update({"edge_id":edge_idx})
    if (if_patch):
        patch = {}
        if (random.random()<0.5):
            patch["length"] = random.randint(100,5000)+random.random()
        if (random.random()<0.5):
            patch["average_time"] = max(0,50+random.randint(-10,10)*random.random())
        if (random.random()<0.5):
            patch["speed_profile"] = [random.randint(1,101)*random.random()+0.5 for i in range(96)]
        if (random.random()<0.5):
            patch["road_type"] = list_of_road_types[random.randint(0,4)]
        
        queries[-1].update({"patch":patch})
    if forbidden_nodes or forbidden_road_types:
        if not forbidden_road_types:
            queries[-1].update({"constraints":{"forbidden_nodes":forbidden_nodes}})
        elif not forbidden_nodes:
            queries[-1].update({"constraints":{"forbidden_road_types":forbidden_road_types}})
        else:
            queries[-1].update({"constraints":{"forbidden_nodes":forbidden_nodes,"forbidden_road_types":forbidden_road_types}})
    if poi:
        queries[-1].update({"poi":poi})
    if source!=-1:
        queries[-1].update({"source":source})
    if target!=-1:
        queries[-1].update({"target":target})
    if mode!=-1:
        queries[-1].update({"mode":mode*"time"+(1-mode)*"distance"})
    if lat!=-1 and lon!=-1:
        queries[-1].update({"query_point":{"lat":lat, "lon":lon}})
    if k!=-1:
        queries[-1].update({"k":k})
    if metric!=-1:
        queries[-1].update({"metric":metric*"euclidean"+(1-metric)*"shortest_path"})
        
output1 = {"meta":{"id":"sample1"} ,"events":queries}
with open("queries.json", "w") as f:
    json.dump(output1, f, indent=2)

print(f"Queries added to queries.json")

