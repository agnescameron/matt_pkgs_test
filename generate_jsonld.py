from pubmed_lookup import PubMedLookup, Publication
import pandas
import json
import datetime
from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.peds.document import UsptoPatentExaminationDataSystemDocument
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
client = UsptoPatentExaminationDataSystemClient()

context = {
	"@vocab": "http://purl.org/dc/terms/",
	"prov": "http://www.w3.org/ns/prov#",
}


def makePatentGraph(resultJson):
	global patentNum
	now = datetime.datetime.now()
	patentGraph = {
		"@context": context,
		"prov:wasDerivedFrom": {
			"@id": "https://zenodo.org/record/3755799"
		},
		"prov:wasGeneratedBy": {
			"prov:startedAtTime": {
				"@value": now.strftime('%Y-%m-%dT%H:%M:%S'),
				"@type": "http://www.w3.org/2001/XMLSchema#dateTime"
			},
			"prov:used": {
				"@id": remote_repo
			}
		},
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
	print(now.strftime('%Y-%m-%dT%H:%M:%S'), "generated patent graph", patentNum)
	with open("graphs/patent(%d).jsonld" %patentNum, "w") as file:
		file.write(json.dumps(patentGraph))
		patentNum+=1
	return


def makeArticleGraph(publication):
	global articleNum
	now = datetime.datetime.now()
	articleGraph = {
		"@context": context,
		"prov:wasDerivedFrom": {
			"@id": "https://zenodo.org/record/3755799"
		},
		"prov:wasGeneratedBy": {
			"prov:startedAtTime": {
				"@value": now.strftime('%Y-%m-%dT%H:%M:%S'),
				"@type": "http://www.w3.org/2001/XMLSchema#dateTime"
			},
			"prov:used": {
				"@id": remote_repo
			}
		},
		"@graph": {
			"@type": "BibliographicResource",
			"title": publication.title,
			"identifier": publication.url,
			"contributor": publication.authors
		}
	}
	# print(articleGraph)
	print(now.strftime('%Y-%m-%dT%H:%M:%S'), "generated article graph", articleNum)
	with open("graphs/article(%d).jsonld" %articleNum, "w") as file:
		file.write(json.dumps(articleGraph))
		articleNum+=1
	return

if __name__ == "__main__":
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
