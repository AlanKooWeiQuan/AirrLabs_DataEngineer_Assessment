DELETE FROM DB_GITHUB_REPO.T1_SRI_committer_TB;

INSERT INTO DB_GITHUB_REPO.T1_SRI_committer_TB
SELECT committer_name, commit_date, commit_hash
FROM DB_GITHUB_REPO.T1_STG_committer_TB