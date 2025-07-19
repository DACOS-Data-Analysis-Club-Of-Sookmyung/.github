import os
import yaml
import requests

ORG_NAME = "DACOS-Data-Analysis-Club-Of-Sookmyung"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# labels.yml 로드
with open("labels.yml", "r") as file:
    labels = yaml.safe_load(file)

# 모든 repository 가져오기
repos_url = f"https://api.github.com/orgs/{ORG_NAME}/repos"
repos = requests.get(repos_url, headers=HEADERS).json()

for repo in repos:
    repo_name = repo["name"]
    print(f"Syncing labels for: {repo_name}")
    # 기존 라벨 가져오기
    labels_url = f"https://api.github.com/repos/{ORG_NAME}/{repo_name}/labels"
    existing_labels = [l["name"] for l in requests.get(labels_url, headers=HEADERS).json()]
    # 새 라벨 생성
    for label in labels:
        if label["name"] not in existing_labels:
            response = requests.post(labels_url, headers=HEADERS, json=label)
            print(f"  Added {label['name']} - Status: {response.status_code}")
        else:
            print(f"  {label['name']} already exists, skipped.")
