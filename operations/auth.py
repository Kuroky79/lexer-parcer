import requests
import ast


def auth(username: str, password: str):
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    r = session.post("http://26.190.19.174:8000/auth/sign-in/", {
        'username': username,
        'password': password,
    })
    try:
        (ast.literal_eval(r.text))['access_token']
    except KeyError:
        return '1'
    return (ast.literal_eval(r.text))['access_token']


def get_projects(url: str, token: str):
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token})
    r = session.get(url)
    project_info = ast.literal_eval(r.text)
    return project_info


def get_tasks(url: str, token: str):  # сюда
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token})
    r = session.get(url)
    tasks_info = ast.literal_eval(r.text)
    return tasks_info


def get_users_from_task(url: str, token: str):
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token})
    r = session.get(url)
    users_info = ast.literal_eval(r.text)
    return users_info
