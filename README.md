# A Simple ETL Data Pipeline to Fetch Github Porject's Commit Data  
> _A project built with [Python], [SQL] & [Local MySQL Database]_.
> <br/>
> _Data Pipeline monitor with Dagster_.
<br/>

## Tech Stack
| Subject                                              | Description                                                          |
|------------------------------------------------------|----------------------------------------------------------------------|
| Data Pipeline ETL Porcess  and Question Query        | Python, SQL                                                          |
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

## Guide on Procedure:
1) Setup MYSQL server, create a new database and configure all those necessary table and view. (may refer to all the SQL scripts in path "github_ETL_pipeline\sql")

2) Configure both database and github credential json inside folder credential (for more security on sensitive data, in the future we can change to the method of export the credential into global environment using terminal command)
     - database credential
  
       ![image](https://github.com/user-attachments/assets/04e97fda-d814-44b9-9182-582a6a7e2f46)
     - gihub credential
        
       ![image](https://github.com/user-attachments/assets/3b0e4ba5-8e2b-4b5d-8b6c-e1c40aa5822e)

3) Configure the input json in folder input
     - It allows specifying the GitHub repository owner and repository name from which to extract commit-related data, as well as defining the desired timeframe in months for the data
  
       ![image](https://github.com/user-attachments/assets/7fe66535-fb2b-418a-9404-21dee31ac2ce)


4) Setup Dagster and triger the data pipeline to perform end to end full data refresh
     1. using command line below to install dagster library and corresponding dependencies
        > pip install dagster dagster-webserver pandas dagster-duckdb
     2. configure the dagster cloud ymal file for MySQL connection resource

          ![image](https://github.com/user-attachments/assets/96e1aced-ad4a-4e17-974f-9074d06b56c6)
     3. navigate to folder github_ETL_pipeline and use command below to launch the Dagster local host webserver(http://localhost:3000)
        > dagster dev
     4. In local host dagster UI, navigate to "assets/global asset lineage", after reload definition successfully click button materialize all then monitor the data pipeline refresh. 

          ![image](https://github.com/user-attachments/assets/c5bf0120-23b8-4db6-8a5e-31a17cd07e62)

5) Uisng MySQL workbench

     1. Validate the data sanity of all the refreshed object
  
          ![image](https://github.com/user-attachments/assets/be6c022b-1937-4f59-bdca-4effd8984566)
     2. Run all the T3 view which query the top 5 committer, longest streak committer and number of commits count by all users by day
of the week and by 3 hour blocks

<br/>

## Query result
1. Top 5 Committer

     ![image](https://github.com/user-attachments/assets/f5f319cc-0186-4e49-b4aa-7f4221e47073)

2. Longest Streak Committer

     ![image](https://github.com/user-attachments/assets/03be382a-8775-4331-824d-7b01ca4d98d9)

3. Heat map of number of commits count by all users by day of the week and by 3 hour blocks
   - SQL method
     
     ![image](https://github.com/user-attachments/assets/44626a1e-84cb-489a-a1e2-a1a74361a764)

   - Python method (alternative)
       > navigate to path "github_ETL_pipeline\github_ETL_pipeline" and run the heatmap.py python script
       
     ![image](https://github.com/user-attachments/assets/42fd0ddc-927e-4148-881e-47525c12302b)


