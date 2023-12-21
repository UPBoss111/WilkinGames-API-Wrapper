import requests

def getPlayer(username: str) -> "Player":

	"""
	Returns a class instance of a Dinogen Online player using the Dinogen Online API. 
	
	Note: In order to retrieve updated data, the function must be called again. Real-time data updates are currently not supported.
	"""

	return Player(username)

def getLeaderboard(type: str) -> "Leaderboard":

	"""
	Returns a class instance of a Dinogen Online survival/stats leaderboard using the Dinogen Online API.
	
	Leaderboards: 'xp', 'kills', 'survival_dino', 'survival_militia', 'survival_chaos', 'survival_chicken', 'survival_zombie', 'survival_pandemonium'
	
	Note: In order to retrieve updated data, the function must be called again. Real-time data updates are currently not supported.
	"""

	return Leaderboard(type)

def getConnectedPlayers() -> int:

	"""
	Retrieves and returns the number of players currently connected to the Dinogen Online account server (US only).
	"""

	response = requests.get("https://dinogen-account-us.wilkingames.net/api/getConnectedPlayers").json()
	
	return len(response)

def playerIsBanned(username: str) -> bool:

	"""
	Returns a boolean value indicating whether the specified player is banned from the Dinogen Online account server and can no longer access it.

	Note: If the player does not exist, it will raise a NameError.
	"""
	
	response = requests.get("https://dinogen-account-us.wilkingames.net/api/isBanned?username=" + username).json()

	if response['bBanned']:
		return True

	else:

		player = requests.get("https://dinogen-account-us.wilkingames.net/api/getPlayer?username=" + username).json()

		if player:
			return False
		else:
			raise NameError("Player not found.") from None

class Player:

	def __init__(self, username: str):

		self.username = username
		response = requests.get("https://dinogen-account-us.wilkingames.net/api/getPlayer?username=" + username).json()
		
		try:
			self.data = response['data']
			data = self.data	
		except KeyError:
			raise NameError("Player not found.") from None

		for key in data:
			setattr(self, key, data[key])

		self.assaultClass = data['classes']['assault']
		self.commandoClass = data['classes']['commando']
		self.supportClass = data['classes']['support']
		self.hunterClass = data['classes']['hunter']
		self.isBanned = playerIsBanned(username)

class Leaderboard:

	def __init__(self, type: str):

		self.type = type
		response = requests.get("https://dinogen-account-us.wilkingames.net/api/getLeaderboard?id=" + type).json()

		self.data = response
		self.topScore = response[0]['score']

		for i in range(10):
			setattr(self, 'n' + str(i + 1), response[i])

	def getLeaderboardPlayer(self, index: int) -> Player:

		"""
		Returns a specific Player object from the leaderboard, given the index of the player as a parameter (int). Index must be from 1-10.
		"""

		if index < 0 or index > 10:
			raise ValueError('Index must be less than or equal to 10.')

		username = self.data[index]['username']

		return Player(username)
