import requests
class Tweet:
	def __init__(self, id):
		self.id = id
		try:
			self.__data= requests.get("https://cdn.syndication.twimg.com/tweet-result?id="+str(id)).json()
		except:
			self.__data=dict()
		self.__dict__.update(self.__data)
		self.created_at = datetime.strptime(self.created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
	
	def __str__(self):
		return f"tweet id: {self.id}"
		
