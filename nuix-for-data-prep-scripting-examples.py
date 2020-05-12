### Data Science 101 #########################
#Return an interable result set.
print len(current_case.search("dog"))

#Return just the number of hits.
print current_case.count("dog")

#Iterate through the results for the search "dog" and print out the item name.
for item in current_case.search("dog"):
	print item.getName()

#Iterate through the current selected items and print out the item name.
for item in current_selected_items:
	print item.getName()

#Iterate through the current selected items and print out the item name and add a Tag.
for item in current_selected_items:
	print item.getName()
	item.addTag("Pets|Dog")

#Iterate through the current selected items and print out the item name and add a Tag, then count the number of items with that tag.
for item in current_selected_items:
	print item.getName()
	item.addTag("Pets|Dog")
print current_case.count("tag:Pets\|Dog")


### Data Science 102 ######################
import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')​
import requests

payload = {'sentence': itemText}
try:
	# https://github.com/artpar/languagecrunch/​	
	response = requests.get('http://localhost:8080/nlp/parse', params=payload)
	data = response.json()
	print data


### Data Science 103 #####################
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

### Data Science 201 #################################
import io
import os

corpus_dir = '/Users/stephenstewart/Documents/Working/Exports/Corpus01/'
os.mkdir('/Users/stephenstewart/Documents/Working/Exports/Corpus01/document')
os.mkdir('/Users/stephenstewart/Documents/Working/Exports/Corpus01/email')
os.mkdir('/Users/stephenstewart/Documents/Working/Exports/Corpus01/spreadsheet')
os.mkdir('/Users/stephenstewart/Documents/Working/Exports/Corpus01/presentation')

def nuixWorkerItemCallback(item):
	md5 = ""
	nuix_Kind = ""
	text_file = ""
	metadata = []

	print("getWorkerGuid =" + str(item.getWorkerGuid()))
	print("getItemGuid = " + str(item.getItemGuid()))
	print("getWorkerStoreDir = " + str(item.getWorkerStoreDir()))
	print("getGuidPath = " + str(item.getGuidPath()))
	print("getDigests.getMd5 = " + str(item.getDigests().getMd5()))
	print("getSourceItem.getName = " + str(item.getSourceItem().getName()))
	#print(dir(item.getSourceItem().getText()))
	md5 = str(item.getDigests().getMd5())

	metadata.append('Nuix_NAME:' + item.getSourceItem().getName())
	#Need to Strip out the -- from GUID.  
	metadata.append('Nuix_GUID:' + str(item.getItemGuid()))
	metadata.append('Nuix_MD5:' + str(item.getDigests().getMd5()))
	
	source_item = item.getSourceItem()
	print(source_item.isKind('document'))
	if source_item.isKind('document') == True:
		nuix_Kind = "document"
		metadata.append("Nuix_KIND:document")		
	elif source_item.isKind('email') == True:
		nuix_Kind = "email"
		metadata.append("Nuix_KIND:email")
	elif source_item.isKind('presentation') == True:
		nuix_Kind = "presentation"
		metadata.append("Nuix_KIND:presentation")
	elif source_item.isKind('spreadsheet') == True:
		nuix_Kind = "spreadsheet"
		metadata.append("Nuix_KIND:spreadsheet")
	else:
		nuix_Kind = 'skip'
	try:
		if nuix_Kind != 'skip':
			text_file = corpus_dir + nuix_Kind + '/' + str(item.getDigests().getMd5()) + '.txt'
			print(text_file)
			metadata.append('##############################\n\n')
			with io.open(text_file, 'w', encoding="utf-8") as outfile:
				outfile.write('\n'.join(metadata))
				outfile.write(item.getSourceItem().getText().toString())
				outfile.flush()
				outfile.close()
	except:
		print("Busted: " + str(item.getName()))
