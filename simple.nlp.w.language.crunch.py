#Simple Example of Enriching Items with an external NLP system - LanguageCrunch

import sys
import os
import re
import datetime

sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
import requests

def cleanEntPERSON (entPerson):
	if entPerson.isdigit():
		entPersonClean = 'bogusPersonValue'
	elif len(entPerson.split(' ')) > 5:
		entPersonClean = 'bogusPersonValue'
	else:
		entPersonClean = entPerson
	return entPersonClean

print datetime.datetime.now()
for item in current_selected_items:
	print item.getName()
	itemText = item.getTextObject().toString().replace('\n',' ')
	itemText = re.sub('[^0-9a-zA-Z.,;:=+?!@#$%^&]+', ' ', itemText)

	payload = {'sentence': itemText}
	# https://github.com/artpar/languagecrunch/
	response = requests.get('http://localhost:8080/nlp/parse', params=payload)
	data = response.json()

	# Entity Definitions
	#https://spacy.io/api/annotation#named-entities
	
	allEntPERSON = []
	
	for entity in data['entities']:
		if entity['label'] == 'PERSON':
			#print entity['label'] + " | " + entity['text']
			if entity['label'] == 'PERSON':
				personEntity = cleanEntPERSON(entity['text'])
				if personEntity != 'bogusPersonValue':
					allEntPERSON.append(personEntity)

			item_custom_metadata = item.getCustomMetadata()
			if len(set(allEntPERSON)) >=1:
				item_custom_metadata['nuix_blog_person_entities'] = ';'.join(set(allEntPERSON))
