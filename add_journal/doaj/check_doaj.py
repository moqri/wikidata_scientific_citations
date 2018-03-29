# -*- coding: utf-8  -*-
import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

with open('check_doaj.tab') as f:
    lines = f.read().splitlines()

for line in lines:
  issn1=line.split('\t')[2]
  issn2=line.split('\t')[3]
  item_Q=line.split('\t')[0]
  for i in range(1):#try:  
    item = pywikibot.ItemPage(repo, item_Q)
    item.get()
    issns= [claim.toJSON()['mainsnak']['datavalue']['value'] for claim in item.claims['P236']]
    len_issns=str(len(issns))
    issns=[x for x in issns if (x != issn1 and x != issn2)]
    with open('check_doaj.csv','a') as file:
        file.write(item_Q+','+len_issns+','+str(len(issns))+'\n')
