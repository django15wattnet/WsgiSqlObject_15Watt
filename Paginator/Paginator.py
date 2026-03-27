from sqlobject.main import SelectResults


class Paginator(object):
	"""
		Für ein SQLObject.SelectResults die Infos für eine Paginierung bereitstellen
	"""
	def __init__(
			self,
			res: SelectResults,
			dictParams: dict = {},
			page: int|None = None,
			pageSize: int|None = None
	):
		self.__res = res

		if page is None and 'page' in dictParams:
			self.__page = int(dictParams['page'][0])
		elif page is not None:
			self.__page = page
		elif page is None:
			self.__page = 1
		else:
			# Safety first
			self.__page = 1

		if pageSize is None and 'pageSize' in dictParams:
			self.__pageSize = int(dictParams['pageSize'][0])
		elif pageSize is not None:
			self.__pageSize = pageSize
		elif pageSize is None:
			self.__pageSize = 25
		else:
			# Safety first
			self.__pageSize = 25


	@property
	def items(self) -> list:
		"""
			Items der aktuellen Seite
		"""
		return self.__res[(self.__page - 1) * self.__pageSize:self.__page * self.__pageSize]


	@property
	def prevPage(self) -> int|None:
		"""
			Vorherige Seite
		"""
		if self.__page == 1:
			return None

		return self.__page - 1


	@property
	def nextPage(self) -> int|None:
		"""
			Nächste Seite
		"""
		if self.__page * self.__pageSize >= self.__res.count():
			return None

		return self.__page + 1


	@property
	def pageCount(self) -> int:
		"""
			Anzahl der Seiten
		"""
		return self.__res.count() // self.__pageSize + 1


	@property
	def lastPage(self) -> int:
		"""
			Letzte Seite
		"""
		return self.__res.count() // self.__pageSize + 1


	@property
	def firstPage(self) -> int:
		"""
			Erste Seite
		"""
		return 1


	@property
	def currentPage(self) -> int:
		"""
			Aktuelle Seite
		"""
		return self.__page


	def __str__(self):
		return f'Paginator: {self.__res.count()} items, {self.__pageSize} items per page, {self.__page} page'
