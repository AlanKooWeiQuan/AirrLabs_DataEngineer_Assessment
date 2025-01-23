


Procedure:
1) Setup MYSQL server, create a new database and configure all those necessary table and view. (may refer to all the SQL scripts in path "github_ETL_pipeline\sql")

2) Setup Dagster which used to peroform full data refresh which perform github data extraction using github API, data load into staging layer of database, data transformation which go through SRI layer and T2 layer then finally creating meanningful data in T3 layer. Meanwhile, Dagster enable user to monitor the data pipeline refresh status.

3)  input, credential, 
