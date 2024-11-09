import pandas as pd
import plotly.graph_objects as go
import numpy as np
from rapidfuzz import process
import requests
from bs4 import BeautifulSoup
import time
import streamlit as st
# Load the CSV file
file_path = 'predictions_with_future_years.csv'
data = pd.read_csv(file_path)

# Define the months and view columns for years
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

view_columns_dict = {
    '2019': 'views_2019',
    '2020': 'views_2020',
    '2021': 'views_2021',
    '2022': 'views_2022',
    '2023': 'views_2023',
    '2024': 'views_2024',
    '2025': 'views_2025',
    '2026': 'views_2026',
    '2027': 'views_2027',
    '2028': 'views_2028'
}

addtocart_columns_dict = {
    '2019': 'addtocart_2019',
    '2020': 'addtocart_2020',
    '2021': 'addtocart_2021',
    '2022': 'addtocart_2022',
    '2023': 'addtocart_2023',
    '2024': 'addtocart_2024',
    '2025': 'addtocart_2025',
    '2026': 'addtocart_2026',
    '2027': 'addtocart_2027',
    '2028': 'addtocart_2028'
}

# Function to generate synthetic monthly data based on festive seasons, avoiding zeros
def generate_monthly_data(yearly_data):
    base_data = np.random.normal(loc=yearly_data/12, scale=yearly_data*0.05, size=12)

    festive_boost = {
        'January': 1.1,  # New Year's sales
        'March': 1.3,    # Holi
        'August': 1.2,   # Raksha Bandhan, Independence Day
        'October': 1.5,  # Dussehra
        'November': 1.7, # Diwali
        'December': 1.2  # Christmas, year-end sales
    }

    monthly_data = []
    for i, month in enumerate(months):
        if month in festive_boost:
            monthly_data.append(base_data[i] * festive_boost[month])
        else:
            monthly_data.append(base_data[i])

    min_threshold = yearly_data * 0.01
    monthly_data = np.maximum(monthly_data, min_threshold)

    monthly_data = monthly_data / sum(monthly_data) * yearly_data
    return monthly_data

# Function to calculate the price based on demand and apply Diwali discount for November
def adj_price_demand(base, views, cart, month):
    demand_factor = (views / 1000 * 0.005) + (cart / 100 * 0.02)
    price = base * (1 + demand_factor)

    if month == 'November':
        price = price * 0.4  # 60% discount

    return price

# Function to find the most compatible category using token-based matching
def get_most_compatible_category(category_input):
    category_list = data['Category'].str.lower().unique().tolist()
    category_input = category_input.lower()

    closest_match, similarity, _ = process.extractOne(category_input, category_list, score_cutoff=60)  # Threshold for matching

    if similarity < 60:
        print(f"No close match found for the category '{category_input}'.")
        return None

    return closest_match

# Function to find the most compatible product in the same category using token-based matching
def get_most_compatible_product(category, product_name):
    category_products = data[data['Category'].str.lower() == category]

    if category_products.empty:
        print(f"No products found under the category '{category}'.")
        return None

    product_names = category_products['Product_Name'].str.lower().tolist()
    product_name = product_name.lower()

    closest_match, similarity, _ = process.extractOne(product_name, product_names, score_cutoff=60)

    if similarity < 60:
        print(f"No close match found for the product '{product_name}' in the category '{category}'.")
        return None

    return category_products[category_products['Product_Name'].str.lower() == closest_match].iloc[0]

# Modified function to plot data based on product name, category, and year
def plot_data_for_category_and_product(product_name, category_input, year):
    if year not in view_columns_dict:
        print("Invalid year. Please enter a valid year between 2019 and 2028.")
        return

    # Find the most compatible category
    category = get_most_compatible_category(category_input)

    if category is None:
        return

    # Find the most compatible product in the given category
    product_row = get_most_compatible_product(category, product_name)

    if product_row is None:
        return

    product_name = product_row['Product_Name']
    yearly_views = product_row[view_columns_dict[year]]
    yearly_addtocart = product_row[addtocart_columns_dict[year]]

    # Generate synthetic monthly views and addtocart data
    monthly_views = generate_monthly_data(yearly_views)
    monthly_addtocart = generate_monthly_data(yearly_addtocart)

    base_price = float(product_row['Base_Price'].replace('₹', '').replace(',', ''))

    # Calculate monthly prices using the adjusted price demand logic
    monthly_prices = [adj_price_demand(base_price, views, cart, month)
                      for views, cart, month in zip(monthly_views, monthly_addtocart, months)]

    fig1 = go.Figure()

    # Plot views
    fig1.add_trace(go.Scatter(x=months, y=monthly_views, mode='lines+markers', name='Views', line=dict(color='blue')))
    fig1.add_trace(go.Scatter(x=months, y=monthly_addtocart, mode='lines+markers', name='Add to Cart', line=dict(color='orange')))

    fig1.update_layout(
        title=f'Monthly Views and Add to Cart for {product_name} in {year}',
        xaxis_title='Month',
        yaxis_title='Count',
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickformat=','),
        template='plotly_white'
    )

    fig1.show()

    # Create a second plot for prices
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=months, y=monthly_prices, mode='lines+markers', name='Price', line=dict(color='green')))

    fig2.update_layout(
        title=f'Monthly Prices for {product_name} in {year}',
        xaxis_title='Month',
        yaxis_title='Price (₹)',
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickprefix='₹', tickformat=','),
        template='plotly_white'
    )

    fig2.show()

# Input handling function
def get_valid_input():
    category = input("Enter the product category: ")
    # Get URL input from user
    target_url = input("Enter the Amazon product URL: ")

    headers = {
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    # Retry loop for scraping product details
    product_name = None

    while product_name is None:
        resp = requests.get(target_url, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch the page. Status code: {resp.status_code}")
            break

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Extracting Product Name
        try:
            product_name = soup.find('h1', {'id': 'title'}).text.strip()
        except:
            product_name = None  # Retry if not found


        # Wait for a while before retrying
        if product_name is None :
            print("Retrying to fetch the data...")
            time.sleep(5)

    if product_name :
        print(f"Product_Name: {product_name}")
    else:
        print("Failed to scrape product details.")

    while True:
        year = input("Enter the year (between 2019 and 2028): ")
        if year in view_columns_dict:
            break
        else:
            print("Invalid year. Please enter a valid year between 2019 and 2028.")

    return product_name, category, year

# Get user input
product_name, category, year = get_valid_input()

# Plot data based on the product name, category, and year
plot_data_for_category_and_product(product_name, category, year)