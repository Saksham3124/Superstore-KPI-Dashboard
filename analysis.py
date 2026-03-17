import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ────────────────────────────────────────────
df = pd.read_csv('Sample - Superstore.csv', encoding='latin-1')

# ── Basic Info ───────────────────────────────────────────
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing Values:\n", df.isnull().sum())
print("\nData Types:\n", df.dtypes)

# ── Data Cleaning ────────────────────────────────────────
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])
df['Year']       = df['Order Date'].dt.year
df['Month']      = df['Order Date'].dt.month

# ── KPI Summary ──────────────────────────────────────────
total_sales   = df['Sales'].sum()
total_profit  = df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100
total_orders  = df['Order ID'].nunique()

print("\n========== KPI SUMMARY ==========")
print(f"Total Sales:    ${total_sales:,.2f}")
print(f"Total Profit:   ${total_profit:,.2f}")
print(f"Profit Margin:  {profit_margin:.2f}%")
print(f"Total Orders:   {total_orders}")

# ── Sales by Category ────────────────────────────────────
print("\n--- Sales by Category ---")
print(df.groupby('Category')['Sales'].sum().sort_values(ascending=False))

# ── Sales by Region ──────────────────────────────────────
print("\n--- Sales by Region ---")
print(df.groupby('Region')['Sales'].sum().sort_values(ascending=False))

# ── Top 5 Sub-Categories by Profit ───────────────────────
print("\n--- Top 5 Sub-Categories by Profit ---")
print(df.groupby('Sub-Category')['Profit'].sum()
        .sort_values(ascending=False).head(5))

# ── Loss-Making Sub-Categories ───────────────────────────
print("\n--- Loss-Making Sub-Categories ---")
print(df.groupby('Sub-Category')['Profit'].sum()
        .sort_values().head(3))

# ── Monthly Sales Trend ──────────────────────────────────
monthly = df.groupby(['Year','Month'])['Sales'].sum().reset_index()

plt.figure(figsize=(12, 4))
for year in monthly['Year'].unique():
    data = monthly[monthly['Year'] == year]
    plt.plot(data['Month'], data['Sales'], marker='o', label=str(year))
plt.title('Monthly Sales Trend by Year')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.legend()
plt.tight_layout()
plt.savefig('monthly_trend.png')
plt.show()
print("\nChart saved as monthly_trend.png")

# ── Save Cleaned Data for Power BI ──────────────────────
df.to_csv('superstore_cleaned.csv', index=False)
print("\nCleaned data saved as superstore_cleaned.csv")