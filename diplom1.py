import requests
import json


#(eshmargunov) и id (171691064)
'''
[
    {
    “name”: “Название группы”, 
    “gid”: “идентификатор группы”, 
    “members_count”: количество_участников_сообщества
    },
    {
    …
    }
]
'''




def make_request(method, user_id, access_token):
	full_url = 'https://api.vk.com/method/' + method + '?user_id=' + user_id + '&v=5.52' + '&access_token=' + access_token + '&fields=city,photo_50'
	return requests.get(full_url).json()

class VkUser():
	def __init__(self, user_id, token):
		self.token = token
		self.user_id = user_id
		api_response = make_request('users.get', self.user_id,self.token)
		print('response: ', api_response)
		if 'error' not in api_response.keys():
			self.first_name = api_response['response'][0]['first_name']
			self.last_name = api_response['response'][0]['last_name']
			self.friends = make_request('friends.get', self.user_id, self.token)
			if 'photo_200' in api_response['response'][0]:
				self.ava_url = api_response['response'][0]['photo_200']
		else:
			self.first_name = api_response
			self.last_name = api_response
			self.friends = api_response

	def __and__(self, target_user):
		#self.target_user = target_user
		full_url = 'https://api.vk.com/method/friends.getMutual' + '?source_uid=' + self.user_id + '&target_uid=' + target_user.user_id + '&v=5.52' + '&access_token=' + self.token
		return requests.get(full_url).json()

	def get_photo(self):
		r = requests.get(self.ava_url, stream=True)
		self.photo_filename = self.first_name + '_' + self.last_name + '.jpg'
		if r.status_code == 200:
			with open(self.photo_filename, 'wb') as f:
				for chunk in r:
					f.write(chunk)
		return self.photo_filename
#	def __str__(self):

	def friend_list_table(self):
		if 'response' in self.friends.keys():
				fr_list = []
				for user in self.friends['response']['items']:
					if 'deactivated' in user:
						print('Id: ', user['id'],'last_name: ', user['last_name'],'deactivated: ',user['deactivated'])
					else:
						print('Id: ', user['id'],'last_name: ', user['last_name'],'deactivated: no')
					
		else :
			print('Error get friends:', self.friends)

	def get_mutual(self, target_user):
		self.target_user = target_user
		full_url = 'https://api.vk.com/method/friends.getMutual' + '?source_uid=' + self.user_id + '&target_uid=' + self.target_user + '&v=5.52' + '&access_token=' + self.token
		return requests.get(full_url).json()

	def friend_list(self):
		fr_list = []
		if 'response' in self.friends.keys():
				for user in self.friends['response']['items']:
					fr_list.append(user['first_name'] + '_' + user['last_name'])
		else :
			fr_list.append(self.friends)
		return fr_list

#token = input('Введите токен: ')
token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'



testuser = VkUser('171691064',token)

print('Testuser:', testuser)


