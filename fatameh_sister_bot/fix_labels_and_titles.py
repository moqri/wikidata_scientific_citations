# -*- coding: utf-8  -*-
import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

with open('pages.txt') as f:
    items_Q = f.read().splitlines()
for item_Q in items_Q[1345:]:
    print item_Q,
    item = pywikibot.ItemPage(repo, item_Q)
    item.get()
    if 'en' not in item.labels:
        continue
    if item.labels['en'][-1]=='.' or item.labels['en'][-1]=='*': 
        new_labels=item.labels
	fixed_label=item.labels['en'][:-1].strip()
        while fixed_label[-1] =='.' or fixed_label[-1]=='*':
		fixed_label=fixed_label[:-1]
	new_labels['en']=fixed_label
        item.editLabels(labels=new_labels, summary="Removing trailing dots or astrisks from the label")
    
    title_claim=item.claims['P1476']
    title_json= title_claim[0].toJSON()
    title= title_json['mainsnak']['datavalue']['value']['text']
    if title[-1]=='.' or title[-1]=='*':
        fixed_title=title[:-1].strip()
        while fixed_title[-1]=='.' or fixed_title[-1]=='*':
		fixed_title=fixed_title[:-1]
	title_json['mainsnak']['datavalue']['value']['text']=fixed_title
        corrected_claim=pywikibot.Claim.fromJSON(site,title_json)     
        item.claims['P1476']=[corrected_claim]
        item.editEntity(summary="Removing trailing dots or astrisks from the title")


