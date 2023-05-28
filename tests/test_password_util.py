from utils import get_password_hash, verify_password

def test_get_password_hash():
    h = get_password_hash('123')
    assert len(h) > 0
    assert isinstance(h, str)


def test_verify_password():
    h = get_password_hash('123')
    assert verify_password('123', h) == True
    assert verify_password('321', h) == False