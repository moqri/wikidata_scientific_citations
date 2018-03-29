from wikidataintegrator.wdi_helpers import PubmedItem, Release, id_mapper


def test_get_pubmed_item():
    # this one exists
    qid = PubmedItem(27528457).get_or_create()
    assert qid == "Q27098545"
    qid = PubmedItem("4986259", id_type="PMC").get_or_create()
    assert qid == "Q27098545"
    qid = PubmedItem("10.1186/S12864-016-2855-3", id_type="DOI").get_or_create()
    assert qid == "Q27098545"


def test_get_pmc_item():
    # only has a pmc id
    qid = PubmedItem("PMC3425984", id_type='PMC').get_or_create()
    assert qid == "Q42758027"


def test_get_pubmed_item_cache():
    # this one exists
    wdid = PubmedItem(1234).get_or_create()
    assert ('1234', 'MED') in PubmedItem._cache
    assert PubmedItem._cache[('1234', 'MED')] == "Q27442302"


def test_pubmedstub_bad_pmid():
    # invalid pubmed id
    wdid = PubmedItem(999999999).get_or_create(login='fake login')
    assert wdid is None


def test_release_lookup_database():
    r = Release("Ensembl Release 85", "Release 85 of Ensembl", "85", edition_of="Ensembl")
    assert r.edition_of_wdid == 'Q1344256'


def test_release_lookup_release():
    r = Release("Ensembl Release 85", "Release 85 of Ensembl", "85", edition_of="Ensembl")
    assert r.get_or_create() == 'Q27666311'
    assert 'Q1344256' in Release._release_cache
    assert '85' in Release._release_cache['Q1344256']


def test_release_new_item_no_write():
    r = Release("Ensembl Release 85", "Release 85 of Ensembl", "XXX", edition_of_wdid='Q1344256')
    try:
        r.get_or_create()
    except ValueError as e:
        assert "login required to create item" == str(e)


def test_id_mapper():
    # get all uniprot to wdid, where taxon is human
    d = id_mapper("P352", (("P703", "Q15978631"),))
    assert 100000 > len(d) > 20000

    d = id_mapper("P683", raise_on_duplicate=False, return_as_set=True)
    assert '3978' in d
    assert type(d['3978']) == set

    # should raise error
    raised = False
    try:
        d = id_mapper("P492", raise_on_duplicate=True)
    except ValueError:
        raised = True
    assert raised


def test_id_mapper_mrt():
    # this may break if it changes in wikidata ....
    d = id_mapper("P486", prefer_exact_match=True)
    assert d['D000998'] == 'Q40207875'
    assert d['D000037'] == 'Q388113'
    assert 'D000033' not in d

    d = id_mapper("P486", prefer_exact_match=True, return_as_set=True)
    assert d['D000998'] == {'Q40207875'}
    assert d['D000037'] == {'Q388113'}
    assert 'D000033' not in d

    d = id_mapper("P486", prefer_exact_match=False, return_as_set=True)
    # unique value constraint
    assert d['D000998'] == {'Q40207875', 'Q846227'}
    # single value constraint
    assert d['D000037'] == d['D000033'] == {'Q388113'}
