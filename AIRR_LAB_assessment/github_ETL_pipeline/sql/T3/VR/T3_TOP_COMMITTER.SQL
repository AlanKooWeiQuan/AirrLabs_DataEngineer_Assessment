SELECT 
committer_name
,COUNT(*) AS commit_count

FROM DB_GITHUB_REPO.T2_COMMITTER_TB
GROUP BY  committer_name
ORDER BY commit_count DESC
LIMIT 5;