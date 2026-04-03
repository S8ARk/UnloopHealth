import urllib.request
import json

def test_manual():
    print("Testing manual request to /auth/register")
    req = urllib.request.Request('http://localhost:5000/api/auth/register', method='POST', headers={'Content-Type': 'application/json'}, data=json.dumps({"email": "loop_test@example.com", "password": "pass", "full_name": "Test"}).encode('utf-8'))
    try:
        resp = urllib.request.urlopen(req)
        print("Register Success:", resp.status, resp.read().decode())
    except Exception as e:
        print("Register Failed:", e)

if __name__ == "__main__":
    test_manual()
