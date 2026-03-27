from sqlobject import *


class KernelSqlObject:
	
	def __init__(self, nameConfig: str = 'config', nameRoutes: str = 'routes'):
		super().__init__(nameConfig=nameConfig, nameRoutes=nameRoutes)
		self.__connectToDatabase()
	
	
	def __connectToDatabase(self):
		"""
			If the key uriDb is present in the project root config.py, a SqlObject
			database connection will be established.
		:return:
		"""
		if 'uriDb' not in self._config:
			self._config['dbConnection'] = None
			return

		self._config['dbConnection'] = connectionForURI(uri=self._config['uriDb'])
		sqlhub.processConnection = self._config['dbConnection']
