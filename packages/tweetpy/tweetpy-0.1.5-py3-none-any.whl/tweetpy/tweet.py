import requests
class Tweet:
	def __init__(self, id):
		self.id = id
		self.__data= requests.get("https://cdn.syndication.twimg.com/tweet-result?id="+str(id)).json()
		self.full_text = self.__data['text']
		self.text = self.__data['text'][self.__data['display_text_range'][0]:self.__data['display_text_range'][1]]
		self.created_at = self.__data['created_at']
		self.lang = self.__data['lang']
		self.id_str = self.__data['id_str']
	def __str__(self):
		return f"tweet id: {self.id}"
