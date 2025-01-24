
SELECT 
committer_name
,streak_length
,streak_start
,streak_end

FROM (
    SELECT
    committer_name
    ,COUNT(*) AS streak_length
    ,MIN(commit_date) AS streak_start
    ,MAX(commit_date) AS streak_end

    FROM (
        SELECT 
        committer_name
        ,commit_date
        ,DATE(commit_date) - INTERVAL ROW_NUMBER() OVER (PARTITION BY committer_name ORDER BY commit_date) DAY AS streak_group

        FROM (
			SELECT DISTINCT 
            committer_name
            , commit_date
            FROM DB_GITHUB_REPO.T2_COMMITTER_TB
            ) distinct_data

    ) AS Streaks
    GROUP BY committer_name, streak_group

) AS Streak_Lengths
ORDER BY streak_length DESC
LIMIT 1;