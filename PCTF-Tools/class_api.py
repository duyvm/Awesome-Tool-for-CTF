#!/usr/bin/python

from swpag_client import Team

teamToken = "cn3XA01z3oa8nBBHsUFXtYT01zBXJIk3"
gameIp = "http://52.52.219.26/"

class ProjectCTFAPI():

	# This is just a simple wrapper class
	# See client.py for more methods supported by self.team

	__slots__ = ('team', 'debug')

	"""
		The Team class is your entrypoint into the API
	"""
	def __init__(self):
		self.debug = False
		self.team = Team(gameIp, teamToken)

	"""
		This returns all of the service ids in the game
	"""
	def getServices(self):

		ids = []
		services = self.team.get_service_list()

		if self.debug:
			print("~" * 5 + " Service List " + "~" * 5)
		
		for s in services:
			ids.append(s['service_id'])

			if self.debug:

				print("Service %s: %s\n\t'%s'" % (s['service_id'], s['service_name'], s['description']))

		return ids
					
	"""
		This returns a list of targets (ports, ips, flag ids) for the given service id
	"""
	def getTargets(self, service):
		
		targets = self.team.get_targets(service)
		
		if self.debug:
			print("~" * 5 + " Targets for service %s " % service + "~" * 5)
			
			for t in targets:
				
				for key in ['hostname','port','flag_id', 'team_name']:
			
					print("%10s : %s" % (key, t[key]))
				print("\n")
			
		return targets
	
	"""
		Submit an individual flag "FLGxxxxxxxx" or list of flags ["FLGxxxxxxxxx", "FLGyyyyyyyy", ...]
	"""
	def submitFlag(self, oneOrMoreFlags):
		
		if not isinstance(oneOrMoreFlags, list):
			oneOrMoreFlags = [oneOrMoreFlags]
			
		status = self.team.submit_flag(oneOrMoreFlags)
		
		if self.debug:
			for i, s in enumerate(status):
				print("Flag %s submission status: %s" % (oneOrMoreFlags[i], s))
		
		return status

