# -*- coding: utf-8  -*-
import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

with open('pages.txt') as f:
    items_Q = f.read().splitlines()
for item_Q in items_Q:
    item = pywikibot.ItemPage(repo, item_Q)
    item.get()
    print item.labels['en']
    if item.labels['en'][-1]=='.' or item.labels['en'][-1]=='*': 
        new_labels=item.labels
        new_labels['en']=new_labels['en'][:-1]
        item.editLabels(labels=new_labels, summary="Fixing the label imported by Fatameh.")

#claim.setTarget(target)
#item.addClaim(claim, summary=u'Adding claim')
