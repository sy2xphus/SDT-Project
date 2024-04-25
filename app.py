#import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

#creating a header
st.header('Car advertisement exploratory data analysis')

#creating a description
st.write('App shows some dependencies of pricing with different characteristics, utilizing slider for price range')

#reading dataset
df = pd.read_csv('vehicles_us.csv')

#creating a subheader
st.write("""
### Data head
""")

#getting first 10 rows
df.head(10)

#calculating missing values
df.isnull().sum()

#replacing missing values with 'unknown' in 'paint_color' and 'is_4wd' columns
columns_to_replace = ['paint_color','is_4wd']
for column in columns_to_replace:
   df[column] = df[column].fillna('unknown')

#groupping by 'model' column and replacing missing values with median value in 'model_year' column
df['model_year'] = pd.to_numeric(df['model_year'])
df['model_year'] = df['model_year'].astype(float).fillna(df.groupby(['model'])['model_year'].transform('median'))
#checking for missing values
df['model_year'].isnull().sum()

#groupping by 'model' and column and replacing missing values with mode value in 'cylinders' column
df['cylinders'] = pd.to_numeric(df['cylinders'])
df['cylinders'] = df['cylinders'].fillna(df.groupby(['model'])['cylinders'].transform('median'))
#checking for missing values
df['cylinders'].isnull().sum()

#groupping by 'model_year' and 'model' columns and replacing missing values with median value in 'odometer' column
df['odometer'] = pd.to_numeric(df['odometer'])
df['odometer'] = df['odometer'].fillna(df.groupby(['model_year','model'])['odometer'].transform('mean'))
#replacing unfilled values with 0.0
df['odometer'] = df['odometer'].fillna(0.0)
#checking for missing values
df['odometer'].isnull().sum()

#calculating missing values after cleaning
df.isnull().sum()

#checking for duplicates
df.duplicated().sum()

#creating slider for the price range and checkbox for the cars that have less then 10 years since production 
st.caption('Set desirable price')
price_range = st.slider(
     "Write price value",
     value=(1, 37500))

actual_range=list(range(price_range[0],price_range[1]+1))

newer_cars = st.checkbox('Cars less than 10 years old')

if newer_cars:
    filtered_data=df[df.price.isin(actual_range)]
    df.model_year = df.model_year.astype(str)
    filtered_data=filtered_data[df.model_year>='2010']
else:
    filtered_data=df[df.price.isin(actual_range)]

#creating scatterplot showing dependence of price and condition
fig = px.scatter(filtered_data, title="Dependence of car price and car condition", x="price", y="condition")           
st.plotly_chart(fig)

st.write('Key insights from the scatterplot showing dependence of price and condition:')
st.write('1) The vast majority of cars in new, like new, excellent, and good condition exhibit similar price ranges.')
st.write('2) Prices for cars in new, like new, excellent, and good condition predominantly fall below 60000.')
st.write('3) Cars classified as salvage or fair condition typically have prices below 20,000.')

#creating histogram showing average price by model
fig2 = px.histogram(filtered_data, title="Average price by model", x="model", y="price",histfunc="avg")
st.plotly_chart(fig2)

st.write('Key insights from the histogram showing average price by model:')
st.write('1) The majority of models have average prices below 10000.')
st.write('2) The most expensive model is the Mercedes-Benz Sprinter 2500, with an average price of 34900.')

st.header('Following the examination of two hypotheses, we can summarize our findings:')
st.write('1) The prices of cars exhibit a strong correlation with their condition.')
st.write('Notably, vehicles in new, like new, excellent, and good condition generally share a price range of 1 to 60000, whereas cars in salvage or fair condition are considerably lower, often below 20000.')
st.write('Thus, our first hypothesis is supported.')
st.write('2) Contrary to the second hypothesis, the analysis reveals that the average prices of most models are below 10000, with a median price range of 12132.')
st.write('This indicates that the average car price falls below the middle price range.')
st.write('Therefore, the second hypothesis is not validated.')

st.write('In conclusion, while car prices do indeed depend on their condition, the average price tends to be lower than the middle price range, as indicated by our analysis.')





