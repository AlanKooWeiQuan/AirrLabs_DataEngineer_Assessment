
SELECT 
    day_of_week
    ,MAX(CASE WHEN time_block = 0 THEN commit_count ELSE 0 END) AS "00-03"
    ,MAX(CASE WHEN time_block = 3 THEN commit_count ELSE 0 END) AS "03-06"
    ,MAX(CASE WHEN time_block = 6 THEN commit_count ELSE 0 END) AS "06-09"
    ,MAX(CASE WHEN time_block = 9 THEN commit_count ELSE 0 END) AS "09-12"
    ,MAX(CASE WHEN time_block = 12 THEN commit_count ELSE 0 END) AS "12-15"
    ,MAX(CASE WHEN time_block = 15 THEN commit_count ELSE 0 END) AS "15-18"
    ,MAX(CASE WHEN time_block = 18 THEN commit_count ELSE 0 END) AS "18-21"
    ,MAX(CASE WHEN time_block = 21 THEN commit_count ELSE 0 END) AS "21-00"
    
FROM (
    SELECT 
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END AS day_order
    ,day_of_week
    ,time_block
    ,COUNT(*) AS commit_count
    FROM  DB_GITHUB_REPO.T2_COMMITTER_TB
    GROUP BY day_of_week, time_block

) AS ordered_data
GROUP BY day_order, day_of_week
ORDER BY day_order;