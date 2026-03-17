import pandas as pd
import sqlite3

df = pd.read_csv('superstore_cleaned.csv')

# Load into SQLite
conn = sqlite3.connect('superstore.db')
df.to_sql('orders', conn, if_exists='replace', index=False)

queries = {
    "Total Sales & Profit by Category": """
        SELECT Category,
               ROUND(SUM(Sales), 2)  AS Total_Sales,
               ROUND(SUM(Profit), 2) AS Total_Profit,
               ROUND(SUM(Profit)*100.0/SUM(Sales), 2) AS Margin_Pct
        FROM orders
        GROUP BY Category
        ORDER BY Total_Sales DESC
    """,
    "Top 10 Customers by Revenue": """
        SELECT [Customer Name],
               ROUND(SUM(Sales), 2) AS Revenue,
               COUNT(DISTINCT [Order ID]) AS Orders
        FROM orders
        GROUP BY [Customer Name]
        ORDER BY Revenue DESC
        LIMIT 10
    """,
    "Sales by Region & Segment": """
        SELECT Region, Segment,
               ROUND(SUM(Sales), 2)  AS Sales,
               ROUND(SUM(Profit), 2) AS Profit
        FROM orders
        GROUP BY Region, Segment
        ORDER BY Sales DESC
    """,
    "Loss-Making Products": """
        SELECT [Product Name],
               ROUND(SUM(Profit), 2) AS Total_Profit
        FROM orders
        GROUP BY [Product Name]
        HAVING Total_Profit < 0
        ORDER BY Total_Profit ASC
        LIMIT 10
    """,
    "Yearly Growth": """
        SELECT Year,
               ROUND(SUM(Sales), 2)  AS Total_Sales,
               ROUND(SUM(Profit), 2) AS Total_Profit
        FROM orders
        GROUP BY Year
        ORDER BY Year
    """
}

for title, query in queries.items():
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)
    print(pd.read_sql_query(query, conn).to_string(index=False))

conn.close()