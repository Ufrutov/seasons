from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json
import time
import datetime

with open('./data-seasons.json') as f:
	data = json.load(f)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--mute-audio')

# Use proxy for the VPN connection
# --proxy-server=host:port
# PROXY = 'supercars.Apadana.xyz:443'
# chrome_options.add_argument('--proxy-server=%s' % (PROXY))

driver = webdriver.Chrome(chrome_options=chrome_options)

def main(set):
	print('%s [START] selenium.py main start' % (datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
	start = time.time()

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

	print('%s [STOP] selenium.py main stop, worked for %.2gs' % (datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'), time.time() - start))

def openSeason(href, index, name, ID):
	driver.get(href)

	playlist = None
	previous = None
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
		src = video.get_attribute('src')

		if( previous == src ):
			print('[E] Video is not updated, wait for it!')
			time.sleep(2)
			src = video.get_attribute('src')

		print('[%s][%s:%s] %s - %s' % (ID, index, i+1, name, src))
		output.append({
			'id': ID,
			'name': name,
			'season': index,
			'epizode': i+1,
			'src': src
		})

		previous = src

	return output

def writeToFile(data):
	print('Found %s epizodes, write to data.js file' % (len(data)))

	with open('./data.js', 'w') as file:
		file.write('const data = %s' % (json.dumps(data, ensure_ascii=False, sort_keys=True)))
		file.close()

main(data)
