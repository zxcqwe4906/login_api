import subprocess
from fastapi.testclient import TestClient

class DbUrlHandler:
    def __enter__(self):
        with open('db_url.txt', 'w') as f:
            f.write('sqlite:///test.db')
        return self

    def __exit__(self, *args):
        with open('db_url.txt', 'w') as f:
            f.write('sqlite:///user.db')

        subprocess.run(['rm', 'test.db'])

def test_register():
    with DbUrlHandler():
        from main import app
        client = TestClient(app)

        # signup
        response = client.post(
            '/signup',
            json={
                'username': "jack321",
                'email': "jack321@gmail.com",
                'password': "5566"
            }
        )
        assert response.status_code == 200
        assert 'token' in response.json()

        token = response.json()['token']

        # test signin not verified
        response = client.post(
            '/signin',
            json={
                'username': "jack321",
                'email': "jack321@gmail.com",
                'password': "5566"
            }
        )
        assert response.status_code == 403
        assert response.json()['detail'] == 'user not verified'

        # verify token
        response = client.post(f'/verify/{token}')
        assert response.status_code == 200

        # signin again
        response = client.post(
            '/signin',
            json={
                'username': "jack321",
                'email': "jack321@gmail.com",
                'password': "5566"
            }
        )
        assert response.status_code == 200