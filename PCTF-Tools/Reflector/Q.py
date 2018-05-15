##
##	CSE 545 - Spring 2018
##	Team 9: Black Shadow (blackshadow@asu.edu)
##

class Queue:
	def __init__ (self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def enQ(self, item):
		self.items.insert(0, item)

	def deQ(self):
		return self.items.pop()
	
	def size(self):
		return len(self.items)

	def getItems(self):
		return self.items

	def getDeepCopy(self):
		q = Queue()
		l = self.items
		l.reverse()
		for item in l:
			q.enQ(item)
		l.reverse()
		return q
