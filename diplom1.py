import requests
import json
import time
from mkreq import make_config, make_pretty_request, make_pretty_request_v2
from tqdm import tqdm

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
base_url = 'https://api.vk.com/method/'
base_config = {
	'access_token': '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1',
	'method': 'users.get',
	'user_id': '552934290',
	'version': '5.52'
}

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
'''

class VkUser():
	def __init__(self, token, req_conf):
		self.token = token
		#self.user_id = req_conf['user_id']
		self.req_conf = req_conf
		self.req_conf['method'] = 'users.get'
		self.req_conf['fields'] = 'city,photo_50'
		self.api_response = make_pretty_request(make_config(base_url,**self.req_conf))
		#api_response = make_request('users.get', self.user_id,self.token)
		#print('response: ', self.api_response)
		if 'error' not in self.api_response.keys():
			self.first_name = self.api_response['response'][0]['first_name']
			self.last_name = self.api_response['response'][0]['last_name']
			self.req_conf['method'] = 'friends.get'
			#self.friends = make_request('friends.get', self.user_id, self.token)
			self.friends = make_pretty_request(make_config(base_url,**self.req_conf))
			if 'photo_50' in self.api_response['response'][0]:
				self.ava_url = self.api_response['response'][0]['photo_50']
		else:
			self.first_name = self.api_response
			self.last_name = self.api_response
			self.friends = self.api_response

	def friends_id(self):
		result_list = []
		if 'error' not in self.friends.keys():
			for one_friend in self.friends['response']['items']:
				result_list.append(one_friend['id'])
		else:
			result_list.append('error found')
		return result_list

	def __and__(self, target_user):
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

	def get_group(self):
		self.req_conf['method'] = 'groups.get'
		self.req_conf['fields'] = 'city,photo_50'
		groups = []
		api_response = make_pretty_request(make_config(base_url,**self.req_conf))
		if 'response' in api_response.keys():
			groups = api_response['response']['items']
		else:
			groups = 'Error found'
		#full_url = 'https://api.vk.com/method/users.getSubscriptions' + '?user_id=' + self.user_id + '&v=5.52' + '&access_token=' + self.token
		#return requests.get(full_url).json()['response']['groups']['items']
		return groups


#token = input('Введите токен: ')


def get_all_fr_groups(user):
	result_list = []
	k = 0
	for friend in tqdm(user.friends_id()):
	#while k < 10 :
		#k = k + 1
		friend = user.friends_id()[k]
		#print('friend:',friend)
		#print('type friend:', type(friend))
		tmp_config = base_config.copy()
		tmp_config['user_id'] = str(friend)
		tmp_user = VkUser(token, tmp_config)
		#print('tmp_user:', tmp_user.last_name)
		#print('tmp_user.friends_id(): ', tmp_user.friends_id())
		result_list.append(tmp_user.get_group())
	return result_list

def uniq_list(seq):
	res = []
	counter_1 = 0
	for k in seq:
		res = res + k
		counter_1 = counter_1 + 1
	keys = {}
	for e in res:
		keys[e] = 1
	return keys.keys()

def find_uniq_group(list_a, list_b):
	counter = 0
	result = []
	for k in list_a:
		if k not in list_b:
			result.append(k)
			counter = counter + 1
	return {'counter':counter,'result':result}

def json_result(list):
	tmp_config = base_config.copy()
	if 'user_id' in tmp_config :
		tmp_config.pop('user_id')
	tmp_config['method'] = 'groups.getById'
	tmp_config['feilds'] = 'members_count,'
	tmp_config['group_ids'] = list
	result = make_pretty_request(make_config(base_url,**tmp_config))


token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

#testuser = VkUser('171691064',token, base_config)
#testuser = VkUser('552934290', token, base_config)
#print('Testuser:', testuser)

'''
tmp_config = base_config.copy()
tmp_config['user_id']='547233513'
tmp_user = VkUser('547233513', token, tmp_config)
'''
tmp_cfg = base_config.copy()
tmp_cfg['user_id']='171691064'
tmp_usr = VkUser(token, tmp_cfg)


#uniq_friend_list = uniq_list(get_all_fr_groups(tmp_usr))
#final_result = find_uniq_group(tmp_usr.friends_id(),uniq_friend_list)
#print('Result is: ', final_result)


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


