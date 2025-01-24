DELETE FROM DB_GITHUB_REPO.T2_committer_TB;

INSERT INTO DB_GITHUB_REPO.T2_committer_TB
SELECT 
committer_name
,DATE(commit_date) AS commit_date
,DAYNAME(commit_date) AS day_of_week
,FLOOR(HOUR(commit_date) / 3) * 3 AS time_block
FROM  DB_GITHUB_REPO.T1_SRI_COMMITTER_TB