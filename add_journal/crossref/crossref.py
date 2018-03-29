import sys
sys.path.append('../../')
from wikidataintegrator import wdi_core, wdi_login
from wikidataintegrator import wdi_property_store
wdi_property_store.valid_instances['scientific_journal']=['Q5633421']
wdi_property_store.wd_properties['P236']={'core_id': True,
  'datatype': 'string',
  'domain': ['scientific_journal'],
  'name': 'ISSN'}
login_instance = wdi_login.WDLogin(user='mahdimoqri', pwd='')
data='journals.tab'
with open(data) as f:
    journals = f.read().splitlines()
journals=[journal.split('\t') for journal in journals if len(journal.split('\t'))==3]
print len(journals) 
journals_2=[journal for journal in journals if len(journal[2].split(','))==2]
print len(journals_2)
with open('crossref_items.tab','a') as f:
    for journal in journals_2[10000:]: 
        journal_item=journal
        for issn in journal[2].split(','):
            item = wdi_core.WDString(value=issn, prop_nr='P236')
            try:
                wd_item = wdi_core.WDItemEngine(item_name='_', domain='_', data=[item],search_only=True)
                meta=wd_item.entity_metadata
                if 'id' in meta:
                    journal_item=journal_item+[issn, meta['id'][1:]]
            except:
                    journal_item=journal_item+['error']
        f.write('\t'.join(journal_item)+'\n')
