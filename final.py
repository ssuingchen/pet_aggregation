#################################
##### Name:Ssu-Ying Chen
##### Uniqname: cssuing
#################################

import json
import time
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

BASE_URL = "https://www.hshv.org/adopt/"
BIRD_URL = "https://www.adoptapet.com/pet-search?clan_id=5&geo_range=50&location=Ann%20Arbor,%20MI&page=1"
RABBIT_URL = "https://www.adoptapet.com/pet-search?clan_id=3&geo_range=50&location=Ann%20Arbor,%20MI&page=1"
CAT_URL = "https://www.adoptapet.com/pet-search?clan_id=2&geo_range=50&location=Wixom,%20MI&page=1"

CACHE_FILENAME = "cache_final.json"
CACHE_DICT = {}

driver = webdriver.Firefox()


def open_cache():
	''' Opens the cache file if it exists and loads the JSON into
	the CACHE_DICT dictionary.
	if the cache file doesn't exist, creates a new cache dictionary
	
	Parameters
	----------
	None
	
	Returns
	-------
	The opened cache: dict
	'''
	try:
		cache_file = open(CACHE_FILENAME, 'r')
		cache_contents = cache_file.read()
		cache_dict = json.loads(cache_contents)
		cache_file.close()
	except:
		cache_dict = {}
	return cache_dict


def save_cache(cache_dict):
	''' Saves the current state of the cache to disk
	
	Parameters
	----------
	cache_dict: dict
		The dictionary to save
	
	Returns
	-------
	None
	'''
	dumped_json_cache = json.dumps(cache_dict)
	fw = open(CACHE_FILENAME,"w")
	fw.write(dumped_json_cache)
	fw.close()


def make_request_with_cache(url):
	'''Check the cache for a saved result for this unique_key
	combo. If the result is found, return it. Otherwise send a new 
	request, save it, then return it. Wait until the data to be retrieved
	before moving to the next line of code.
   
   Params
   _______
	params: url
	
	Returns
	-------
	dict
		the results of the query as a dictionary loaded from cache
		JSON
	'''
	#TODO Implement function	
	if url in CACHE_DICT.keys():
		print("Using Cache", url)
		return CACHE_DICT[url]
	else:
		print("Fetching", url)
		driver.get(url)
		time.sleep(8.0)
		response = driver.page_source
		CACHE_DICT[url] = response
		save_cache(CACHE_DICT)
		return CACHE_DICT[url]


def make_request_with_cache_non_sleep(url):
	'''Check the cache for a saved result for this unique_key
	combo. If the result is found, return it. Otherwise send a new 
	request, save it, then return it.
   
   Params
   _______
	params: url
	
	Returns
	-------
	dict
		the results of the query as a dictionary loaded from cache
		JSON
	'''
	#TODO Implement function	
	if url in CACHE_DICT.keys():
		print("Using Cache", url)
		return CACHE_DICT[url]
	else:
		print("Fetching", url)
		driver.get(url)
		response = driver.page_source
		CACHE_DICT[url] = response
		save_cache(CACHE_DICT)
		return CACHE_DICT[url]

class PetData:
	'''create a pet instance

	Instance Attributes
	-------------------
	breed: string
	
	name: string

	sex: string

	color: string

	age: string

	pet_id: int
	'''

	def __init__(self, breed = None, name = None, sex = None,\
					color = None, age = None, pet_id = None, species = None):
		self.breed = breed
		self.name = name
		self.sex = sex
		self.color = color
		self.age = age
		self.pet_id = pet_id
		self.species = species

	def info(self):
		'''
		return the information of the object
		'''

		return self.name + " " + "(" + self.species + "|" + self.breed + ")" + ": " + self.sex\
		 + " " + self.color + " " + self.age + " " + self.pet_id


def build_first_site_pet_url_list():
	''' Make a list that contains all pet urls on the page

	Parameters
	----------
	None

	Returns
	-------
	list
		pet urls
	'''

	soup = BeautifulSoup(make_request_with_cache_non_sleep(BASE_URL), 'html.parser')

	pet_url_list = []
	all_pets_div = soup.find_all("div", class_="animal_list_box")
	for pet_div in all_pets_div:
		pet_url_list.append(pet_div.find("a", class_="results_animal_link")['href'])

	return pet_url_list


def build_second_site_url_list(site_url):
	''' Make a list that contains all pet urls on the page

	Parameters
	----------
	None

	Returns
	-------
	list
		pet urls
	'''
	PET_BASE_URL = "https://www.adoptapet.com"
	soupPet = BeautifulSoup(make_request_with_cache(site_url), 'html.parser')
	pet_url_list = []
	all_pet_div = soupPet.find_all("div", class_="search__result")
	for pet_div in all_pet_div:
		pet_url_list.append(PET_BASE_URL+pet_div.find("a", class_="pet__item__link")['href'])

	return pet_url_list


def get_first_site_pet_instance(pet_url):
	'''Make an instances from a pet URL.
	
	Parameters
	----------
	pet_url: string
		The URL for a pet page
	
	Returns
	-------
	instance
		a pet instance
	'''
	soupPet = BeautifulSoup(make_request_with_cache(pet_url), 'html.parser')
	name = soupPet.find("div", class_="details_animal_header_right").text.strip()[5:]
	pet_full_data = soupPet.find("div", class_="details_animal_left_details").findChildren("span")
	species = "No Species"
	breed = "No Breed"
	sex = "No Sex"
	color = "No Color"
	age = "No Age"
	pet_id = "No Pet ID"
	for data in pet_full_data:
		if data.text == "Species:":
			species = data.next_sibling.strip()
		elif data.text == "Breed:":
			breed = data.next_sibling.strip()
		elif data.text == "Gender:":
			sex = data.next_sibling.strip()
		elif data.text == "Color:":
			color = data.next_sibling.strip()
		elif data.text == "Age:":
			age = data.next_sibling.strip()
		elif data.text == "Animal ID:":
			pet_id = data.next_sibling.strip()
		
	pet_instance = PetData(breed = breed, name = name, sex = sex,\
					color = color, age = age, pet_id = pet_id, species = species)

	return pet_instance


def get_second_site_pet_instance(pet_url, species="None"):
	'''Make an instances from a pet URL.
	
	Parameters
	----------
	pet_url: string
		The URL for a pet page
	
	Returns
	-------
	instance
		a pet instance
	'''

	species = species
	breed = "No Breed"
	sex = "No Sex"
	color = "No Color"
	age = "No Age"
	pet_id = "No Pet ID"

	soupPet = BeautifulSoup(make_request_with_cache(pet_url), 'html.parser')
	name = soupPet.find("div", class_="pet-header__pet-name").find("span").text
	pet_full_data = soupPet.find_all("div", class_="pet-facts__content--section")
	for pet_data in pet_full_data:
		pet_info = pet_data.findChildren("div")
		for item in pet_info:
			if item.text.strip() == "Breed":
				breed = item.find_next_sibling("div").text
				print("Breed of pet: ", breed)
			elif item.text.strip() == "Sex":
				sex = item.find_next_sibling("div").text
				print("Sex of pet: ", sex)
			elif item.text.strip() == "Color":
				color = item.find_next_sibling("div").text
				print("Color of pet: ", color)
			elif item.text.strip() == "Age":
				age = item.find_next_sibling("div").text
				print("Age of pet: ", age)
			elif item.text.strip() == "Pet ID":
				pet_id = item.find_next_sibling("div").text
				print("ID of pet: ", pet_id)

	pet_instance = PetData(breed = breed, name = name, sex = sex,\
					color = color, age = age, pet_id = pet_id, species = species)

	return pet_instance


def start_app():
	'''
	combine all the functions above and run the interface in terminal
	'''
	CACHE_DICT = open_cache()
	pet_first_site_url_list = build_first_site_pet_url_list()

	second_site_base_urls = [(BIRD_URL, "Bird"), (RABBIT_URL, "Rabbit"), (CAT_URL, "Cat")]
	pet_second_site_url_list = []
	# search for pet urls on each site page
	for second_site_base_url, species in second_site_base_urls:
		second_site_url_list = build_second_site_url_list(second_site_base_url)
		# append all the pets on the page to pet_second_site_url_list, and add a species to each pet url
		for pet_url in second_site_url_list:
			pet_second_site_url_list.append((pet_url, species))

	pet_instance_list = []
	for pet_url in pet_first_site_url_list:
		try:
			pet_instance = get_first_site_pet_instance(pet_url)
			pet_instance_list.append(pet_instance)
		
		except:
			pass

	for pet_url, species in pet_second_site_url_list:
		try:
			pet_instance = get_second_site_pet_instance(pet_url, species)
			pet_instance_list.append(pet_instance)
		
		except:
			pass

	return pet_instance_list

if __name__ == "__main__":
	pet_instance_list = start_app()
	
	driver.close()
	driver.quit()

	print(len(pet_instance_list))
	for pet in pet_instance_list:
		print(pet.info())

	pet_df = pd.DataFrame(columns=["name", "species", "breed", "sex", "color", "age", "pet_id"])
	name = [ pet.name for pet in pet_instance_list ]
	species = [pet.species for pet in pet_instance_list ]
	breed = [pet.breed for pet in pet_instance_list ]
	sex = [pet.sex for pet in pet_instance_list ]
	color = [pet.color for pet in pet_instance_list ]
	age = [pet.age for pet in pet_instance_list ]
	pet_id = [pet.pet_id for pet in pet_instance_list ]

	pet_df["name"] = name
	pet_df["species"] = species 
	pet_df["breed"] = breed 
	pet_df["sex"] = sex
	pet_df["color"] = color
	pet_df["age"] = age
	pet_df["pet_id"] = pet_id

	pet_df.to_csv("pet.csv")
