import pywikibot
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
academic_journal='Q737498'
issn_property='P236'
instance_of='P31'
url_property='P854'
retrieved_property='P813'
#academic_journal='Q10'
#instance_of='P82'
#url_property='P73312'
#retrieved_property='P388'
with open('missing_journals.tsv') as f:
    journals=f.read().splitlines()
for j in journals[17:20]:
    jl=j.split('\t')
    title=jl[0]
    publisher=jl[1]
    issn=jl[2]
    print(issn)
    if jl[3]=='':
        issns=[jl[2]]
    else:
        issns=[jl[2],jl[3]]
    label_dict = {"en": title}
    item = pywikibot.ItemPage(site)
    item.editLabels(labels=label_dict, summary="adding a journal from Crossref")
    desc={"en":"An academic journal published by "+ publisher + " and listed on Crossref"}
    item.editDescriptions(desc, summary=u'Setting journal description based on Crossref')
    stringclaim = pywikibot.Claim(repo, issn_property)
    claim = pywikibot.Claim(repo, instance_of)
    target = pywikibot.ItemPage(repo, academic_journal)
    claim.setTarget(target)
    item.addClaim(claim, summary=u'listed on Crossref')
    
    url = pywikibot.Claim(repo, url_property)
    url.setTarget('https://api.crossref.org/journals/'+issn)
    retrieved = pywikibot.Claim(repo, retrieved_property)
    date = pywikibot.WbTime(year=2018, month=4, day=18)
    retrieved.setTarget(date)
    claim.addSources([url, retrieved], summary=u'adding a reference from Crossref')

    for issn in issns:
        stringclaim.setTarget(issn)
        item.addClaim(stringclaim, summary=u'adding issn from Crossref')
        url = pywikibot.Claim(repo, url_property)
        url.setTarget('https://api.crossref.org/journals/'+issn)
        retrieved = pywikibot.Claim(repo, retrieved_property)
        date = pywikibot.WbTime(year=2018, month=4, day=18)
        retrieved.setTarget(date)
        stringclaim.addSources([url, retrieved], summary=u'adding reference from Crossref')


