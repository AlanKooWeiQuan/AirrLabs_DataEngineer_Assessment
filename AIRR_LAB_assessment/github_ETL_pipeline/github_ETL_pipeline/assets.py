
from dagster import asset
import pandas as pd
import mysql.connector
import requests
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import json


# Define global DATABASE_CREDENTIAL variables
with open('credential/database_crd.json', 'r') as file:
        DATABASE_CREDENTIAL = json.load(file)


# JOB 1 : Start of Dummy
@asset(description="Start of Dummy")
def start():
    pass


# JOB 2 : data extraction from github repo using github API 
@asset(description="fetch commits data from source github api", deps=[start])
def data_extraction():

    # get the required credential
    with open('input/input.json', 'r') as file:
        input = json.load(file)
        REPO_OWNER = input.get("REPO_OWNER")
        REPO_NAME = input.get("REPO_NAME")
        month_of_data =  input.get("month_of_data")
    
    with open('credential/github_crd.json', 'r') as file:
        github_credential = json.load(file)
        PERSONAL_ACCESS_TOKEN = github_credential.get("PERSONAL_ACCESS_TOKEN")

    # configure the request parameter
    BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"

    HEADERS = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {PERSONAL_ACCESS_TOKEN}"
    }

    six_months_ago = datetime.now() - timedelta(days=month_of_data*30)  
    params = {"since": six_months_ago.isoformat(), "per_page": 100, "page": 1}
    all_commits = []

    # api request to fetch github data 
    while True:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print("Error fetching data from GitHub API:", response.json())
            break

        data = response.json()
        if not data:
            break

        all_commits.extend(data)
        params["page"] += 1

    return all_commits


# JOB 3 : load the extraced github repo commit data into database staging layer
@asset(description="load source data into database STG layer", deps=[data_extraction])
def data_load(data_extraction):
    # extract required data from raw commit data
    rows = []
    for commit in data_extraction:
        committer = commit.get("author")
        if committer:
            committer_name = committer.get("login")
            committer_date = commit.get("commit", {}).get("committer", {}).get("date")
            commit_hash = commit.get("sha")

            if committer_name and committer_date:
                rows.append((committer_name, committer_date, commit_hash))

    # convert as pandas data frame
    df = pd.DataFrame(rows, columns=["committer_name", "commit_date", "commit_hash"])
    df["commit_date"] = pd.to_datetime(df["commit_date"])

    # Connect to database and load data
    connection = mysql.connector.connect(**DATABASE_CREDENTIAL)
    cursor = connection.cursor()
    cursor.execute(f""" delete from db_github_repo.T1_STG_committer_TB """)
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO T1_STG_committer_TB (committer_name, commit_date, commit_hash)
            VALUES (%s, %s, %s)
        """, tuple(row))

    connection.commit()
    cursor.close()
    connection.close()


# JOB 4 : T1 job which load data from T1 staging layer into T1 SRI layer
@asset(description="load from STG layer into SRI layer", deps=[data_load])
def T1_COMMITTER_TXF():
    # Connect to MySQL and load data
    connection = mysql.connector.connect(**DATABASE_CREDENTIAL)
    cursor = connection.cursor()

    with open('sql/T1/STG/TXF/T1_COMMITTER_TXF.SQL', 'r') as file:
        sql_script = file.read()
        sql_script_list = sql_script.split(";")
    
    for sql in sql_script_list:
        cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


# JOB 5 : T2 job which load data from T1 SRI layer into T2 layer
@asset(description="load from SRI layer into T2 layer", deps=[T1_COMMITTER_TXF])
def T2_COMMITTER_TXF():
    # Connect to MySQL and load data
    connection = mysql.connector.connect(**DATABASE_CREDENTIAL)
    cursor = connection.cursor()

    with open('sql/T2/TXF/T2_COMMITTER_TXF.SQL', 'r') as file:
        sql_script = file.read()
        sql_script_list = sql_script.split(";")
    
    for sql in sql_script_list:
        cursor.execute(sql)

    connection.commit()
    cursor.close()
    connection.close()


# JOB 6 : End of Dummy
@asset(description="End of Dummy", deps=[T2_COMMITTER_TXF])
def end():
    pass