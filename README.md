# A Simple ETL Data Pipeline for Github Porject's Commit History  
> _A project built with [Python], [SQL] & [Local MySQL Database]_.
> <br/>
> _Data Pipeline monitor with Dagster_.

## Tech Stack
| Subject                                              | Description                                                          |
|------------------------------------------------------|----------------------------------------------------------------------|
| Data Pipeline ETL Porcess Logic and Question Query   | Python, MySQL                                                        |
| Database                                             | MySQL                                                                |
| Data Pipeline Orchestrator                           | Dagster with Python                                                  |

## Data Pipeline Architecture
![Snipaste_2025-01-24_10-08-05](https://github.com/user-attachments/assets/7447323a-7e05-44ba-857f-887f5577f3de)


## Data Pipeline Orchestrator : Dagster
- Overview: Dagster is an open-source orchestrator designed for ETL pipelines, offering an easy-to-use Python API.
- Features:
  - Direct integration with MySQL and other databases.
  - Supports logging, monitoring, and error handling.
  - Comes with a user-friendly web UI for monitoring pipelines.


Procedure:
1) Setup MYSQL server, create a new database and configure all those necessary table and view. (may refer to all the SQL scripts in path "github_ETL_pipeline\sql")

2) Setup Dagster which used to peroform full data refresh which perform github data extraction using github API, data load into staging layer of database, data transformation which go through SRI layer and T2 layer then finally creating meanningful data in T3 layer. Meanwhile, Dagster enable user to monitor the data pipeline refresh status.

3)  input, credential, 
