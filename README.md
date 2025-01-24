# A Simple ETL Data Pipeline for Github Porject's Commit History  
> _A project built with [Python], [SQL] & [Local MySQL Database]_.
> <br/>
> _Data Pipeline monitor with Dagster_.
<br/>

## Tech Stack
| Subject                                              | Description                                                          |
|------------------------------------------------------|----------------------------------------------------------------------|
| Data Pipeline ETL Porcess Logic and Question Query   | Python, SQL                                                        |
| Database                                             | MySQL                                                                |
| Data Pipeline Orchestrator                           | Dagster with Python                                                  |
<br/>

## Data Pipeline Architecture
![Snipaste_2025-01-24_10-09-04](https://github.com/user-attachments/assets/042d38d9-8091-4b0d-91dd-0c955b185fcc)
1. Source data : GitHub commits related data from GitHub API
2. T1 layer - STG : staging layer which store the exact original data extract from source
3. T1 layer - SRI : standardized raw integration layer which loaded from staging layer with different loading logic
     - full dump    : replaces the entire dataset with fresh data from the source during each load
     - delta        : appends only new data to the existing dataset without modifying previous data
     - incremental  : processes only the changes (inserts, updates, and deletes) since the last load
5. T2 layer : data which go though data integration, data transformation and logic mapping
6. T3 layer : semantic data which go through certain logic for specific use case query
7. From layer T1 until T3, each instance can have up to 3 diffrent object
     - table     : a table which store the data
     - vr view   : a view which direct view all column from table
     - txf view  : a procedure view which perform data processing and load into table
<br/>

## Data Pipeline Orchestrator : Dagster
- Overview: Dagster is an open-source orchestrator designed for ETL pipelines, offering an easy-to-use Python API.
- Features:
  - Direct integration with MySQL and other databases.
  - Supports logging, monitoring, and error handling.
  - Comes with a user-friendly web UI for monitoring pipelines.
![image](https://github.com/user-attachments/assets/3b6661bb-e04c-4a20-b760-a63284698790)
![image](https://github.com/user-attachments/assets/770b0fb2-e501-4be4-b434-ffc3e8ac198e)

<br/>

Procedure:
1) Setup MYSQL server, create a new database and configure all those necessary table and view. (may refer to all the SQL scripts in path "github_ETL_pipeline\sql")

2) Setup Dagster which used to peroform full data refresh which perform github data extraction using github API, data load into staging layer of database, data transformation which go through SRI layer and T2 layer then finally creating meanningful data in T3 layer. Meanwhile, Dagster enable user to monitor the data pipeline refresh status.

3)  input, credential, 
