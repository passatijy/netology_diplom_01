import requests
import json
import time


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
	repeat = True
	while repeat:
		print('.', end = '')
		response = requests.get(full_url).json()
		if 'error' in response :
			if response['error']['error_code'] == 6 :
				time.sleep(5)
		else:
			repeat = False
	return response

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

	def friends_id(self):
		api_response = make_request('users.get', self.user_id,self.token)
		result_list = []
		if 'error' not in api_response.keys():
			for one_friend in self.friends['response']['items']:
				result_list.append(one_friend['id'])
		else:
			result_list.append('error found')
		return result_list

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

	def group_list(self):
		full_url = 'https://api.vk.com/method/users.getSubscriptions' + '?user_id=' + self.user_id + '&v=5.52' + '&access_token=' + self.token
		return requests.get(full_url).json()['response']['groups']['items']


#token = input('Введите токен: ')


def get_all_fr_groups(user):
	result_list = []
	for friend in user.friends_id():
		result_list.append(VkUser(str(friend), token).friends_id())


#testuser = VkUser('171691064',token)
testuser = VkUser('552934290', token)
print('Testuser:', testuser)

# декомпозиция
# надо получить списки всех групп всех пользователей - основного и его друзей
# надо сделать исключение множеств групп пользователя и групп его друзей
# user1(g1,g2,g3,g4)
# user1(fr1,fr2)
# fr1(g1,g2)
# fr2(g2,g3)
# res g4
# то есть можно получить список всех групп у друзей, можно выкинуть не уникальные, и по оставшемуся сматчивать. Совпавшее выкидывать типа pop?


# 


