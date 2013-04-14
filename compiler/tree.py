#!/usr/bin/python

class Tree:
	def __init__(self, t, v):
		self.ntype = t
		self.val = v
		self.childs = []
	
	def add_child(self, child):
		self.childs.append(child)
	
	def print_tree(self, level):
		print((' '*level)+':'+self.ntype+' '+self.val)
		if self.childs:
			for child in self.childs:
				child.print_tree(level+1)

if __name__ == '__main__':
	root = Tree('root', '0')
	child1 = Tree('child1', '1')
	child2 = Tree('child2', '2')
	child3 = Tree('child3', '3')
	grand_child1 = Tree('grand_child1', '4')
	grand_child2 = Tree('grand_child2', '5')

	root.add_child(child1)
	root.add_child(child2)
	root.add_child(child3)

	child1.add_child(grand_child1)
	child3.add_child(grand_child2)

	root.print_tree(0)
