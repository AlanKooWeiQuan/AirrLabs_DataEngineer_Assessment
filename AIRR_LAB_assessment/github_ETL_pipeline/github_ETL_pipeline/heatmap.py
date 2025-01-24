import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Define global DATABASE_CREDENTIAL variable
with open('../credential/database_crd.json', 'r') as file:
        DATABASE_CREDENTIAL = json.load(file)

# heat map generation fucntion
def generate_heatmap():
    connection = mysql.connector.connect(**DATABASE_CREDENTIAL)
    QUERY_HEATMAP = f"""
        SELECT 
        day_of_week
        ,CASE time_block
            WHEN 0 THEN "00-03"
            WHEN 3 THEN "03-06"
            WHEN 6 THEN "06-09"
            WHEN 9 THEN "09-12"
            WHEN 12 THEN "12-15"
            WHEN 15 THEN "15-18"
            WHEN 18 THEN "18-21"
            WHEN 21 THEN "21-00"
        END AS time_block
        , COUNT(*) AS commit_count
        FROM DB_GITHUB_REPO.T2_COMMITTER_TB
        GROUP BY day_of_week, time_block;
        """
    heatmap_data = pd.read_sql(QUERY_HEATMAP, connection)
    connection.close()

    pivot_table = heatmap_data.pivot(index="day_of_week", columns="time_block", values="commit_count")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot_table = pivot_table.reindex(day_order)

    sns.heatmap(pivot_table, annot=True, fmt="g", cmap="coolwarm")
    plt.title("Commits Heatmap by Day and Time Block")
    plt.ylabel("Day of Week")
    plt.xlabel("3-hour Blocks")
    plt.show()


# main process
if __name__ == "__main__":
    print("Generating heatmap...")
    generate_heatmap()