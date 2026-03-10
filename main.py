import pyodbc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to SQL Server LocalDB
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=CustomerDB;"
    "Trusted_Connection=yes;"
)

# Read data from SQL Server
query = "SELECT * FROM customers"
df = pd.read_sql(query, conn)

# Behaviour Change Detection
df = df.sort_values(["Customer_ID", "Month"])
df["Previous_Spend"] = df.groupby("Customer_ID")["Amount_Spent"].shift(1)
df["Percent_Change"] = ((df["Amount_Spent"] - df["Previous_Spend"]) / df["Previous_Spend"]) * 100
df["Behaviour_Changed"] = df["Percent_Change"].apply(lambda x: "Yes" if abs(x) > 50 else "No")

print(df)

# Seaborn Visualization
sns.lineplot(data=df, x="Month", y="Amount_Spent", hue="Customer_ID")
plt.title("Customer Behaviour Analysis using SQL Server")
plt.show()

conn.close()