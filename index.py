from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json

with open('./data-seasons.json') as f:
	data = json.load(f)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

driver = webdriver.Chrome(chrome_options=chrome_options)

def main(set):
	output = []

	for s in set:
		driver.get(s['src'])

		ls = driver.find_element_by_class_name('pgs-seaslist')
		lsa = ls.find_elements_by_tag_name('a')
		LS = []

		for listItem in lsa:
			href = listItem.get_attribute('href')
			LS.append(href)

		for href in LS:
			i = LS.index(href)
			ID = 's{}'.format(set.index(s)+1)
			output.extend(openSeason(href, i+1, s['name'], ID))

	writeToFile(output)

	driver.close()

def openSeason(href, index, name, ID):
	driver.get(href)

	playlist = None
	output = []

	try:
		playlist = driver.find_element_by_id('htmlPlayer_playlist')
	except NoSuchElementException as e:
		print('[E] NoSuchElementException - #htmlPlayer_playlist not found, wait for it.')
		driver.implicitly_wait(3)
		playlist = driver.find_element_by_id('htmlPlayer_playlist')

	playlistContent = playlist.find_elements_by_xpath('./pjsdiv')

	player = driver.find_element_by_id('htmlPlayer')
	video = player.find_element_by_tag_name('video')

	for pl in playlistContent:
		i = playlistContent.index(pl)

		driver.execute_script('arguments[0].click();', pl)
		driver.implicitly_wait(20)

		print('[%s][%s:%s] %s - %s' % (ID, index, i+1, name, video.get_attribute('src')))
		output.append({
			'id': ID,
			'name': name,
			'season': index,
			'epizode': i+1,
			'src': video.get_attribute('src')
		})

	return output

def writeToFile(data):
	with open('./data.js', 'w') as file:
		file.write('const data = %s' % (json.dumps(data, ensure_ascii=False, sort_keys=True)))
		file.close()

main(data)
