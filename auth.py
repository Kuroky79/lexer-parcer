from requests.auth import HTTPBasicAuth
import requests
import ast


def get_session():
    session = requests.Session()
    return session


def auth(username, password):
    endpoint= "http://26.190.19.174:8000/auth/sign-in/"
    request_body = {
        "username": username,
        "password": password
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(endpoint, data=request_body, headers=headers)
    return response


def lala():
    endpoint= "http://26.190.19.174:8000/auth/user/"
    headers= "Authorization: Bearer {access_token}}"
    response = requests.get(endpoint, headers=headers)
    return response

    session = requests.Session()
    session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    r =session.post("http://26.190.19.174:8000/auth/sign-in/", {
         'username': 'John_Doe123',
         'password': '123',
    })

    access_token = ast.literal_eval(r.text)
    session.headers.update({'Authorization': 'Bearer ' + access_token['access_token']})
    r = session.get("http://26.190.19.174:8000/auth/user/")
