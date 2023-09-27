import requests
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

def get_child_imdb_id(parent_imdb_id):
	url = f"https://www.imdb.com/name/{parent_imdb_id}/bio"
	response = requests.get(url,headers = headers, timeout=20).text
	soup = BeautifulSoup(response, "html.parser")

	# Find all li tag
	datas = soup.find_all('li', class_='ipc-metadata-list__item ipc-metadata-list__item--stacked', id='children')
	
	# Get text from each tag
	children_ids = []

	#check if datas is empty
	if len(datas) == 0:
		return children_ids
	
	data = datas[0].find('ul')
	inner = data.findChildren()
	if inner is not None:
		for el in inner:
			child = el.find('a')
			if child is not None:
				name = child.contents[0]
				link = child.get('href')
				imdb_id = link.split('/')[2]
				children_ids.append(imdb_id)
	return children_ids

def get_parents_imdb_id(parent_imdb_id):
	url = f"https://www.imdb.com/name/{parent_imdb_id}/bio"
	response = requests.get(url,headers = headers, timeout=20).text
	soup = BeautifulSoup(response, "html.parser")

	# Find all li tag
	datas = soup.find_all('li', class_='ipc-metadata-list__item ipc-metadata-list__item--stacked', id='parents')
	
	# Get text from each tag
	parent_ids = []

	#check if datas is empty
	if len(datas) == 0:
		return parent_ids
	
	data = datas[0].find('ul')
	inner = data.findChildren()
	if inner is not None:
		for el in inner:
			parent = el.find('a')
			if parent is not None:
				name = parent.contents[0]
				link = parent.get('href')
				imdb_id = link.split('/')[2]
				parent_ids.append(imdb_id)
	return parent_ids