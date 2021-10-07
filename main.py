import json
import numpy as np

STEP = 2e-5

def extrct(filename):
	with open(filename, "r") as f:
		data = json.load(f)

	return data

def clean(data):
	true_data =[data[0],]

	for val in data[1:]:
		if val != true_data[-1]:
			true_data.append(val)
		else:
			continue

	return true_data

class Node:
	'''Node class provides functionality of moving
	   in given direction and comparing node's coordinates.'''
	K = 0
	def __init__(self, lat, lon):
		self.coords = np.array([lon, lat])
		self.idx = 0

	def move(self, dist, vec):
		vec = normalize(vec)
		self.coords += vec * dist

	@staticmethod
	def normalize(vec):
		return vec / (vec**2).sum()**0.5

	def compare(self, other):
		if self.coords == other.coords:
			return True

	def __eq__(self, other):
		if (self.coords == other.coords).all():
			return True
		return False


class Route:
	'''Route class serves as a container for Node objects.'''
	length = 0

	def __init__(self):
		self.storage = np.array([])

	def append(self, node):
		node.idx = self.length
		self.storage = np.append(self.storage, node)
		self.length += 1

	def create(self, data):
		for dot in data:
			node = Node(**dot)
			self.append(node)

		return self


class Triplet:
	'''Triplet object is used to calculate direction in which
	   node should be moved.'''
	def __init__(self, nodes):
		self.nodes = nodes.copy()

	def get_bis(self):
		a = self.nodes[0].coords - self.nodes[1].coords
		b = self.nodes[2].coords - self.nodes[1].coords

		a_norm = Node.normalize(a)
		b_norm = Node.normalize(b)
		bis = Node.normalize(a_norm + b_norm)

		return bis

	def move(self, dist, vec):
		vec = Node.normalize(vec)
		self.nodes[1].coords += vec * dist


def main():
	data = extrct("route.json")
	data = clean(data)

	route = Route()
	route.create(data)

	triplets = np.array([])
	for node in route.storage[1:-1]:
		for oth in route.storage[1:-1]:
			if node == oth and node.idx != oth.idx:
				node_triplet = Triplet(route.storage[node.idx-1:node.idx+2])
				oth_triplet = Triplet(route.storage[oth.idx-1:oth.idx+2])

				node_n = node_triplet.get_bis()
				oth_n = oth_triplet.get_bis()

				node_triplet.move(STEP, node_n)
				oth_triplet.move(STEP, oth_n)

	new_data = route.storage
	
	arr = []
	for el in new_data:
		d = {}
		d["lon"] = el.coords[0]
		d["lat"] = el.coords[1]

		arr.append(d)

	with open("new_route.json", "w") as f:
	 	json.dump(arr, f)


if __name__ == "__main__":
	main()
