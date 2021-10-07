import json
from random import uniform as rnd

with open("route.json", "r") as f:
	data = json.load(f)


for idx, node in enumerate(data):
	data[idx]["idx"] = idx

print("Solutons:\n1)Randomized\n2)Non-randomized")
s = int(input(">>"))

# Solution 1
if s == 1:
	for idx, node in enumerate(data):
		data[idx]["lat"] += rnd(-0.000005, 0.000005)
		data[idx]["lon"] += rnd(-0.000005, 0.000005)

# Solution 2
if s == 2:
	for idx, node in enumerate(data):
		for other_node in data:
			if other_node["idx"] != node["idx"]:
				if node["lat"] == other_node["lat"] and node["lon"] == other_node["lon"]:
					data[idx]["lat"] += 0.00001
					data[idx]["lon"] += 0.00001
				elif node["lat"] == other_node["lat"]:
					data[idx]["lat"] += 0.00001
				elif node["lon"] == other_node["lon"]:
					data[idx]["lon"] += 0.00001

	for idx, node in enumerate(data):
		for other_node in data:
			if other_node["idx"] != node["idx"]:
				if node["lat"] == other_node["lat"] and node["lon"] == other_node["lon"]:
					data[idx]["lat"] += 0.00001
					data[idx]["lon"] += 0.00001
				elif node["lat"] == other_node["lat"]:
					data[idx]["lon"] += 0.00001
				elif node["lon"] == other_node["lon"]:
					data[idx]["lat"] += 0.00001


with open("new_route.json", "w") as f:
	json.dump(data, f)