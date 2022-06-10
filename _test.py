from utils import tileMultiple

def test_tileMultiple():
    assert tileMultiple(2048, 10000, 10000) == (4,4)
