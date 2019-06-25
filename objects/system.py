class System(object):
	def __init__(self, manufacturer=None, name=None):
		self.name = name
		self.manufacturer = manufacturer

	def get_name(self):
		return self.name

	def get_manufacturer(self):
		return self.manufacturer

	def create_to_search(self, term):
		return "%s %s %s"%(self.manufacturer, self.name, term)