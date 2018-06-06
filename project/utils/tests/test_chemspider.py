from utils.chemspider import fetch_chemspider


def test_success():
    cs = fetch_chemspider('1836-75-5')
    assert cs == {
        'CommonName': 'nitrofen',
        'SMILES': 'c1cc(ccc1[N+](=O)[O-])Oc2ccc(cc2Cl)Cl',
        'MW': '284.0949',
        'image': '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',   # noqa
        'status': 'success'
    }
