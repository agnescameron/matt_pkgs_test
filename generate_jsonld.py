from pubmed_lookup import PubMedLookup, Publication
import pandas
import json
import time
from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.peds.document import UsptoPatentExaminationDataSystemDocument
client = UsptoPatentExaminationDataSystemClient()
import os

#change these if you fork the repo
email = 'agnesfcameron@protonmail.com'
remote_repo = "https://github.com/agnescameron/matt_pkgs_test"

current_pmid = 0
publication = {}
articleNum = 0
patentNum = 0

#url is https://pubmed.ncbi.nlm.nih.gov/ + pmid
url_prefix = 'http://www.ncbi.nlm.nih.gov/pubmed/'

context = {
	"@vocab": "http://purl.org/dc/terms/",
	"script": remote_repo,
	"@prov": "https://zenodo.org/record/3755799"
}

def makePatentGraph(resultJson):
	global patentNum
	patentGraph = {
		"@context": context,
		"@graph": {
			"@type": "BibliographicResource",
			"title": resultJson["inventionTitle"]["content"][0],
			"identifier": row['patent'],
			"references": [
				{
					"@type": "BibliographicResource",
					"title": publication.title,
					"identifier": publication.url,
				}
			],
			"contributor": []
		}
	}
	for record in resultJson["partyBag"]["applicantBagOrInventorBagOrOwnerBag"][1]["inventorOrDeceasedInventor"]:
		name = record["contactOrPublicationContact"][0]["name"]["personNameOrOrganizationNameOrEntityName"][0]["personStructuredName"]
		patentGraph["@graph"]["contributor"].append(name["firstName"] + ' ' + name["middleName"] + " " + name["lastName"])
	# print(patentGraph)
	print(time.asctime(), "successfully generated patent graph", patentNum)
	with open("graphs/patent(%d).jsonld" %patentNum, "w") as file:
		file.write(json.dumps(patentGraph))
		patentNum+=1
	return


def makeArticleGraph(publication):
	global articleNum
	articleGraph = {
		"@context": context,
		"@graph": {
			"@type": "BibliographicResource",
			"title": publication.title,
			"identifier": publication.url,
			"contributor": publication.authors
		}
	}
	# print(articleGraph)
	print(time.asctime(), "successfully generated article graph", articleNum)
	with open("graphs/article(%d).jsonld" %articleNum, "w") as file:
		file.write(json.dumps(articleGraph))
		articleNum+=1
	return

#read in file
tsv = pandas.read_csv('pubmed.tsv', sep='\t', nrows=1000)

#for each new row, append to an existing set of pmid information
for index, row in tsv.iterrows():
	if row['pmid'] != current_pmid:
		current_pmid = row['pmid']
		try:
			publication = Publication(PubMedLookup(url_prefix+str(row['pmid']), email))
			makeArticleGraph(publication)
		except:
			publication = {}
			print('error writing article graph')

	patent = str('US'+row['patent'])+'A'
	try:
		result = client.download_document(number=str(row['patent']), format='json')
		resultJson = json.loads(result["json"])['PatentData'][0]["patentCaseMetadata"]
		makePatentGraph(resultJson)
	except:
		print('error writing patent graph')
