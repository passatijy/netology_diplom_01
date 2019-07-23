import requests
import time
from tqdm import tqdm

base_url = 'https://api.vk.com/method/'
def make_config(base_url,**kvargs):
	full_url = base_url
	make_request_config_error = False
	if 'access_token' in kvargs.keys():
		access_token = kvargs['access_token']
		if 'method' in kvargs.keys():
			method = kvargs['method']
			full_url = full_url + method
			if 'user_id' in kvargs.keys():
				user_id = kvargs['user_id']
				full_url = full_url + '?user_id=' + user_id
			elif 'users_ids' in kvargs.keys():
				users_ids = kvargs['users_ids']
				full_url = full_url + '?users_ids=' + users_ids
			if 'target_uid' in kvargs.keys():
				target_uid = kvargs['target_uid']
				full_url = full_url + '&target_uid=' + target_uid
			if 'version' in kvargs.keys():
				version = kvargs['version']
				full_url = full_url + '&v=' + version
			if 'fields' in kvargs.keys():
				fields = kvargs['fields']
				full_url = full_url + '&fields=' + fields
			full_url = full_url + '&access_token=' + access_token
			#print('3 full_url = ', full_url)
		else:
			make_request_config_error = True
			full_url = 'Error, no vk api method given'
	else:
		make_request_config_error = True
		full_url = 'Error, no access_token given'
	return full_url



def make_request(full_url):
	try:
		response = requests.get(full_url).json()
		return response
	except Exception as e:
		print('Some error occured', e)

def make_pretty_request(full_url):
	try:
		repeat = True
		while repeat:
			response = requests.get(full_url).json()
			if 'error' in response.keys():
				if response['error']['error_code'] == 6 :
					print('..to many req..',end='')
					time.sleep(2)
				else:
					repeat = False
			else:
				repeat = False
		return response
	except Exception as e:
		print('Some error occured', e)

def make_pretty_request_v2(base_url,config):
	try:
		repeat = True
		while repeat:
			response = requests.get(base_url, params = config).json()
			if 'error' in response.keys():
				if response['error']['error_code'] == 6 :
					print('..to many req..',end='')
					time.sleep(2)
				else:
					repeat = False
			else:
				repeat = False
		return response
	except Exception as e:
		print('Some error occured', e)


config = {
	'access_token': '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1',
	'method': 'users.get',
	'user_id': '552934290',
	'version': '5.52',
	'fields': "city"
}
'''
print('request config is: ', make_config(base_url, **config))
user1 = make_pretty_request(make_config(base_url, **config))
user2 = make_pretty_request(make_config("https://ya.ru/", **config))
print('user1=',user1)
print('user2=',user2)

k = 0
while k < 15:
	print(make_pretty_request(make_config(base_url, **config)))
	k = k + 1
'''