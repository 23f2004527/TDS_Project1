import requests
import pandas as pd

headers = {"Authorization": "token YOUR_TOKEN"}
user_data = []
repo_data = []
p = 1
while True:
    users_url = "https://api.github.com/search/users"
    params = {"q": "location:Berlin followers:>200", "per_page": 30, "page": p}
    users_response = requests.get(users_url, headers=headers, params=params).json()
    if 'items' not in users_response or not users_response['items']:
        break
    for user in users_response['items']:
        username = user['login']
        user_details = requests.get(f"https://api.github.com/users/{username}", headers=headers).json()
        company = user_details['company'].lstrip('@').strip().upper() if user_details['company'] else ""
        user_data.append({
            'login': user_details['login'],
            'name': user_details['name'],
            'company': company,
            'location': user_details['location'],
            'email': user_details['email'],
            'hireable': user_details['hireable'],
            'bio': user_details['bio'],
            'public_repos': user_details['public_repos'],
            'followers': user_details['followers'],
            'following': user_details['following'],
            'created_at': user_details['created_at']
        })
        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_params = {"sort": "pushed", "per_page": 500}
        repos_response = requests.get(repos_url, headers=headers, params=repos_params).json()
        for repo in repos_response:
            repo_data.append({
                'login': username,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'],
                'has_projects': repo['has_projects'],
                'has_wiki': repo['has_wiki'],
                'license_name': repo['license']['key'] if repo['license'] else ""
            })
    p += 1

pd.DataFrame(user_data).to_csv("users.csv", index=False)
pd.DataFrame(repo_data).to_csv("repositories.csv", index=False)
