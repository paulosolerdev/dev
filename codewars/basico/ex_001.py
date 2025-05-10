import urllib.parse

def generate_link(username):
    encoded_username = urllib.parse.quote(username)
    return f"http://www.codewars.com/users/{encoded_username}"
