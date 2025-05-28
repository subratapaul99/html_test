import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose 
from statsmodels.tsa.holtwinters import ExponentialSmoothing


import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.colors as colors
pio.templates.default = "plotly_white"
data = pd.read_csv("Sample - Superstore.csv", encoding='latin-1') 
data.head(5)
data.describe()
data.info()
Data of order date and ship date:--
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Ship Date'] = pd.to_datetime(data['Ship Date'])
data.info()
data.head(5)
print(data.isnull().sum())  

data = data.dropna()  
data.fillna(0, inplace=True)  

data['Order month'] = data['Order Date'].dt.month
data['Order year'] = data['Order Date'].dt.year
data['Order Day of Week'] = data['Order Date'].dt.dayofweek
data.head(5)

Heatmap Graph :--
corr_matrix = data.select_dtypes(include=[np.number]).corr()
plt.figure(figsize=(10, 6))
corr_matrix = data.select_dtypes(include=[np.number]).corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()
Monthly Sales analysis:--
sales_by_month = data.groupby('Order month')['Sales'].sum().reset_index()
sales_by_month
fig = px.line(sales_by_month,
              x='Order month',
              y='Sales',
              title='Monthly Sales Analysis')
fig.show()


sales Forcasting for next six month:-
data['Order Date'] = pd.to_datetime(data['Order Date'])

data.set_index('Order Date', inplace=True)
numeric_data = data.select_dtypes(include=['number'])
monthly_sales = numeric_data.resample('ME').sum().reset_index()
monthly_sales['Order month'] = monthly_sales['Order Date'].dt.strftime('%Y-%m')
if len(monthly_sales) < 12:
    print("Not enough data for seasonal forecasting. Using trend-based model instead.")
    model = ExponentialSmoothing(monthly_sales['Sales'], trend='add')
else:
    model = ExponentialSmoothing(monthly_sales['Sales'], trend='add', seasonal='add', seasonal_periods=12)


fit = model.fit()

future_dates = pd.date_range(start=monthly_sales['Order Date'].max(), periods=7, freq='ME')[1:]
forecasted_sales = fit.forecast(steps=6)
forecast_df = pd.DataFrame({'Order Date': future_dates, 'Sales': forecasted_sales})

monthly_sales['Type'] = 'Actual'
forecast_df['Type'] = 'Forecasted'
combined_sales = pd.concat([monthly_sales[['Order Date', 'Sales', 'Type']], forecast_df])

fig = px.line(combined_sales, x='Order Date', y='Sales', color='Type', 
              title="📈 Sales Forecasting for Next 6 Months",
              labels={'Sales': 'Total Sales ($)', 'Order Date': 'Month'})

fig.show()
Sales by Category:--
sales_by_category = data.groupby('Category')['Sales'].sum().reset_index()
sales_by_category
fig = px.pie(sales_by_category,
             values='Sales',
             names='Category',
             hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Pastel)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title_text='Sales Analysis by Category', title_font=dict(size=24))

fig.show()


Sales Analysis by SubCategory:--
data.head(10)
sales_by_subcategory = data.groupby('Sub-Category')['Sales'].sum().reset_index()
sales_by_subcategory
fig = px.bar(sales_by_subcategory, x= 'Sub-Category', y = 'Sales', title ="Sales analysis by Sub Category")

fig.show()

Monthly profit analysis:--
data.head(5)
Profit_by_month = data.groupby('Order month')['Profit'].sum().reset_index()
Profit_by_month
fig = px.bar(Profit_by_month, x = 'Order month', y = 'Profit', title = 'monthly Profit analysis')

fig.show()



profit by Category:--
Profit_by_Category = data.groupby('Category')['Profit'].sum().reset_index()
Profit_by_Category
fig = px.pie(Profit_by_Category,
             values='Profit',
             names='Category',
             hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Pastel)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title_text='Profit Analysis by Category', title_font=dict(size=24))

fig.show()
Profit by SubCategory:--
Profit_by_SubCategory = data.groupby('Sub-Category')['Profit'].sum().reset_index()
fig = px.bar(Profit_by_SubCategory, x= 'Sub-Category', y = 'Profit', title ="Profit Analysis bny Sub Category")

fig.show()
Sales and Profit by segment :--
data.head(3)
Sales_Profit_by_segment = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
color_palatte = colors.qualitative.Pastel1

fig = go.Figure()

fig.add_trace(go.Bar(x=Sales_Profit_by_segment['Segment'],
                     y=Sales_Profit_by_segment['Sales'],
                     name='sales',
                     marker_color=color_palatte[0]))

fig.add_trace(go.Bar(x=Sales_Profit_by_segment['Segment'],
                     y=Sales_Profit_by_segment['Profit'],
                     name='Profit',
                     marker_color=color_palatte[1]))

fig.update_layout(title='Sales and Profit Analyis by Customer Segment',
                  xaxis_title='Customer Segment', yaxis_title='Amount')

fig.show()

              
Sales to Profit Ratio:--
Sales_Profit_by_Segment = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
Sales_Profit_by_Segment['Sales_to_Profit_Ratio'] = Sales_Profit_by_Segment['Sales'] / Sales_Profit_by_Segment['Profit']
print(Sales_Profit_by_Segment[['Segment', 'Sales_to_Profit_Ratio']])

data.info()
data.shape
data.head(4)
sales_by_City = data.groupby('City')['Sales'].sum().reset_index()
sales_by_City
fig = px.line(sales_by_City, x = 'City', y = 'Sales', title = 'City sales Analysis')

fig.show()

Top Customers by sales:--
top_customers = data.groupby('Customer Name')['Sales'].sum().reset_index()

top_customers = top_customers.sort_values(by='Sales', ascending=False).head(10)
fig = px.bar(top_customers, 
             x='Customer Name', 
             y='Sales', 
             title="Top 10 Customers by Sales",
             color='Sales',
             text_auto=True)

fig.update_layout(xaxis_title="Customer Name", yaxis_title="Total Sales")
fig.show()
sales_by_Region = data.groupby('Region')['Sales'].sum().reset_index()
sales_by_Region
fig = px.pie(sales_by_Region,
             values='Sales',
             names='Region',
             hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Pastel)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title_text='Sales analysis by Region', title_font=dict(size=24))

fig.show()
data.head(5)
sales_by_Quantity = data.groupby('Quantity')['Sales'].sum().reset_index()
sales_by_Quantity
fig = px.line(sales_by_Quantity, x= 'Quantity', y = 'Sales', title ="Sales and Quantity analysis")

fig.show()
Time Series analysis:--
numeric_data = data.select_dtypes(include=['number'])
monthly_sales = data['Sales'].resample('ME').sum()
decomposition = seasonal_decompose(monthly_sales, model='multiplicative', period=12)
plt.figure(figsize=(14, 8))

plt.subplot(411)
plt.plot(decomposition.observed, label='Observed')
plt.legend(loc='upper left')

plt.subplot(412)
plt.plot(decomposition.trend, label='Trend')
plt.legend(loc='upper left')

plt.subplot(413)
plt.plot(decomposition.seasonal, label='Seasonal')
plt.legend(loc='upper left')

plt.subplot(414)
plt.plot(decomposition.resid, label='Residual')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()
data.columns = data.columns.str.strip()  # Remove any extra spaces from column names
print(data.columns)  # Check column names

print(data.head())