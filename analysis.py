import pandas as pd
from scipy.stats import pearsonr
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np


users = pd.read_csv(r"C:\Users\Abdul Kavi Chaudhary\Downloads\users.csv")
repos = pd.read_csv(r"C:\Users\Abdul Kavi Chaudhary\Downloads\repositories.csv")

top_5_followers = users.nlargest(5, 'followers')['login'].tolist()
print("Top 5 users with highest followers:", ", ".join(top_5_followers))


users['created_at'] = pd.to_datetime(users['created_at'])
earliest_5_users = users.nsmallest(5, 'created_at')['login'].tolist()
print("5 earliest registered users:", ", ".join(earliest_5_users))


top_3_licenses = repos['license_name'].dropna().value_counts().head(3).index.tolist()
print("Top 3 most popular licenses:", ", ".join(top_3_licenses))

#4. Company with the majority of developers
most_common_company = users['company'].mode().iloc[0]
print("Company with most developers:", most_common_company)

#5. Most popular programming language
most_popular_language = repos['language'].mode().iloc[0]
print("Most popular language:", most_popular_language)

#6. Second most popular language among users who joined after 2020
users['created_at'] = pd.to_datetime(users['created_at'])
post_2020_users = users[users['created_at'].dt.year > 2020]
post_2020_repos = repos[repos['login'].isin(post_2020_users['login'])]
second_popular_language = post_2020_repos['language'].value_counts().index[1]
print("Second most popular language for post-2020 users:", second_popular_language)

#7. Language with highest average stars per repository
avg_stars_per_language = repos.groupby('language')['stargazers_count'].mean().idxmax()
print("Language with highest avg stars per repo:", avg_stars_per_language)

#8. Top 5 users by leader strength
users['leader_strength'] = users['followers'] / (1 + users['following'])
top_5_leader_strength = users.nlargest(5, 'leader_strength')['login'].tolist()
print("Top 5 users by leader strength:", ", ".join(top_5_leader_strength))

#9. Correlation between followers and public repositories
followers_repos_corr = users[['followers', 'public_repos']].corr().iloc[0, 1]
print("Correlation between followers and repos:", round(followers_repos_corr, 3))

#10. Additional followers per public repository (regression slope)
X = users[['public_repos']]
y = users['followers']
model = LinearRegression().fit(X, y)
followers_per_repo_slope = model.coef_[0]
print("Followers per additional repo:", round(followers_per_repo_slope, 3))

#11. Correlation between projects and wiki enabled
projects_wiki_corr = repos[['has_projects', 'has_wiki']].corr().iloc[0, 1]
print("Correlation between projects and wiki enabled:", round(projects_wiki_corr, 3))

#12. Do hireable users follow more people?
hireable_following_diff = users[users['hireable'] == True]['following'].mean() - users[users['hireable'] == False]['following'].mean()
print("Following difference (hireable - not hireable):", round(hireable_following_diff, 3))

#13. Correlation of bio length with followers
users_with_bio = users[users['bio'].notna()]
users_with_bio['bio_word_count'] = users_with_bio['bio'].apply(lambda x: len(x.split()))
X = users_with_bio[['bio_word_count']]
y = users_with_bio['followers']
model = LinearRegression().fit(X, y)
slope = model.coef_[0]
print("Regression slope of followers on bio word count:", round(slope, 3))

#14. Top 5 users by weekend repository creation
repos['created_at'] = pd.to_datetime(repos['created_at'])
repos['created_day'] = repos['created_at'].dt.dayofweek
weekend_repos = repos[repos['created_day'] >= 5]
top_5_weekend_creators = weekend_repos['login'].value_counts().head(5).index.tolist()
print("Top 5 users by weekend repo creation:", ", ".join(top_5_weekend_creators))

#16. Most common surname
users['surname'] = users['name'].fillna("").apply(lambda x: x.split()[-1] if len(x.split()) > 1 else None)
most_common_surname = users['surname'].value_counts().idxmax()
print("Most common surname:", most_common_surname)
