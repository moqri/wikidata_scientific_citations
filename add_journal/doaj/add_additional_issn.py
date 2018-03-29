# -*- coding: utf-8  -*-
import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

with open('additional_issn.tab') as f:
    lines = f.read().splitlines()

for line in lines:
  issn=line.split('\t')[1]
  ref=line.split('\t')[2]
  item_Q=line.split('\t')[0]
  if item_Q in ["Q15758027","Q27988671","Q7257499","Q15749678","Q15765970","Q15749605","Q27727335","Q20013100","Q15757154","Q26839990","Q26841889","Q15750168","Q26842201","Q15753100","Q20025079","Q15817196","Q15764760","Q5656999","Q3428694","Q15758264","Q15816228","Q15765917","Q26853875","Q15765745","Q15756325","Q26842690","Q26842803","Q15753391","Q50403141","Q5570360","Q15763777","Q21385637","Q26842115","Q5133809","Q1872766","Q15752002","Q26842360","Q4806438","Q15749681","Q15758179","Q15724434","Q15764515","Q28976784","Q19850987","Q26853896","Q26853803","Q1843481","Q11821781","Q50806657","Q50806722","Q6295679","Q24657325","Q50806790","Q15753692","Q13733498","Q15734667","Q15753120","Q24040391","Q15754217","Q2661755","Q15764481","Q15752422","Q15755163","Q15753840","Q15766086","Q11821779","Q9061461","Q26842451","Q26842036","Q26841915","Q15751005","Q26842216","Q26842826","Q26842683","Q15750616","Q26842040","Q50811045","Q15758443","Q15716320","Q27725638","Q15756496","Q50811251","Q50811251","Q11822687","Q15760178","Q15753835","Q15766566","Q15817257","Q15764921","Q2246127","Q6295118","Q15724657","Q26842028","Q27710889","Q15755099","Q15757245","Q24039150","Q15758869","Q15750794","Q27726274","Q24908228","Q11788760","Q15759322","Q50811045","Q19622316","Q27720763","Q50419784"]:
      continue
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

