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

def json_result(in_dict):
	result = []
	group_config = {
	'access_token': '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1',
	'method': 'groups.getById',
	'version': '5.52'
	}
	group_id_list = ''
	for k in in_dict['result']:
		group_id_list = group_id_list + str(k) + ','
	group_config['group_ids'] = group_id_list[:-1]
	#print('group_id_list: ', group_id_list, ' group_config: ', group_config)
	groups_dict = make_pretty_request(make_config(base_url,**group_config))
	del group_config['group_ids']
	if 'response' in groups_dict.keys():
		for k in groups_dict['response']:
			res_dict = {}
			res_dict['gid'] = str(k['id'])
			res_dict['name'] = k['name']
			group_config['method'] = 'groups.getMembers'
			group_config['group_id'] = str(k['id'])
			res_dict['count'] = make_pretty_request(make_config(base_url,**group_config))['response']['count'] 
			result.append(res_dict)
	else:
		result = result.append('error in get_group request')
	return result

token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

#################### создаем пользователя
tmp_cfg = base_config.copy()
tmp_cfg['user_id']='171691064'
tmp_usr = VkUser(token, tmp_cfg)

#################### получаем список всех групп всех друзей пользователя:
uniq_friend_list = uniq_list(get_all_fr_groups(tmp_usr))

#out_dict = {'counter': 7, 'result': [8564, 134709480, 125927592, 101522128, 27683540, 4100014, 35486626]}

#################### получаем список уникальных групп у этого пользователя:
final_result = find_uniq_group(tmp_usr.get_group(),uniq_friend_list)


with open('out.json', 'w') as json_file:
	json.dump(json_result(final_result), json_file)
