# -*- coding: utf-8  -*-
import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

with open('issn.tab') as f:
    lines = f.read().splitlines()

for line in lines[1000:]:
  issn=line.split('\t')[0]
  ref=line.split('\t')[1]
  item_Q=line.split('\t')[2]
  print item_Q,
  print ref
  for i in range(1):#try:  
    item = pywikibot.ItemPage(repo, item_Q)
    item.get()
    issns= [claim.toJSON()['mainsnak']['datavalue']['value'] for claim in item.claims['P236']]
    print issns
    if issn not in issns:    
	stringclaim = pywikibot.Claim(repo, u'P236')
        stringclaim.setTarget(issn)

        ref_url = pywikibot.Claim(repo, u'P854')
        ref_url.setTarget(ref)

        retrieved = pywikibot.Claim(repo, u'P813')
        date = pywikibot.WbTime(year=2018, month=3, day=23)
        retrieved.setTarget(date)
        
        item.addClaim(stringclaim)
        stringclaim.addSources([ref_url,retrieved], summary='Adding a source')
        
        #item.addClaim(stringclaim,summary="Adding ISSN")
  #except Exception as e: print(e)

