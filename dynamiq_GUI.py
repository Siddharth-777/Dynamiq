import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from rapidfuzz import process
import requests
from bs4 import BeautifulSoup
import time

# Load the CSV file
file_path = 'G:/Dynamiq/Dynamiq/predictions_with_future_years.csv'
data = pd.read_csv(file_path)

# Define columns and months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
view_columns_dict = {str(year): f'views_{year}' for year in range(2019, 2029)}
addtocart_columns_dict = {str(year): f'addtocart_{year}' for year in range(2019, 2029)}

# Styling
st.set_page_config(page_title="Dynamiq: A Price Prediction Model", layout="wide", page_icon="🛒")
st.markdown(
    """
    <style>
        body { background-color: #040404; color: #ffffff; }
        .title { font-size: 30px; font-style: italic; text-align: left; margin-top: 50px; margin-bottom: 30px; }
        .results { font-size: 18px; font-weight: bold; text-align: center; margin-top: 40px; }
        .input-container { display: flex; justify-content: center; gap: 10px; margin-top: 20px; }
        .input-container > div { flex: 1; }
        .analyse-btn { display: flex; justify-content: center; margin-top: 20px; }
        input, textarea { font-size: 16px; color: #ffffff; background-color: #333; border: 1px solid #ffffff; }
        button { background-color: #63d38b; color: white; padding: 10px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<div class='title'>Dynamiq : A price prediction model</div>", unsafe_allow_html=True)

# Input fields
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([6, 2, 2])
categories = [
    "Computers&accessories > accessories&peripherals > keyboards",
    "Computers&accessories > accessories&peripherals > mice",
    "Computers&accessories > accessories&peripherals > webcams",
    "Computers&accessories > accessories&peripherals > cables&accessories > cables > USBcables",
    "Computers&accessories > externaldevices&datastorage > externalharddrives",
    "Computers&accessories > externaldevices&datastorage > usbdrives",
    "Computers&accessories > externaldevices&datastorage > memorycards",
    "Computers&accessories > networkingdevices > routers",
    "Computers&accessories > networkingdevices > switches",
    "Computers&accessories > networkingdevices > modems",
    "Computers&accessories > networkingdevices > extenders",
    "Computers&accessories > networkingdevices > wifiadapters",
    "Computers&accessories > printersinks&accessories > printers",
    "Computers&accessories > printersinks&accessories > inks",
    "Computers&accessories > printersinks&accessories > toner",
    "Computers&accessories > components > motherboards",
    "Computers&accessories > components > graphiccards",
    "Computers&accessories > components > processors",
    "Computers&accessories > components > ram",
    "Computers&accessories > components > powersupplies",
    "Computers&accessories > laptops&tablets > laptops",
    "Computers&accessories > laptops&tablets > tablets",
    "Computers&accessories > monitors > monitors",
    "Electronics > homeaudio > speakers",
    "Electronics > homeaudio > soundbars",
    "Electronics > hometheater > projectors",
    "Electronics > hometheater > avreceivers",
    "Electronics > tv&video > televisions",
    "Electronics > tv&video > streamingdevices",
    "Electronics > mobileaccessories > chargers",
    "Electronics > mobileaccessories > powerbanks",
    "Electronics > mobileaccessories > phonecases",
    "Electronics > headphones&earbuds&accessories > headphones",
    "Electronics > headphones&earbuds&accessories > earbuds",
    "Electronics > headphones&earbuds&accessories > headset",
    "Electronics > cameras&photography > cameras",
    "Electronics > cameras&photography > lenses",
    "Electronics > cameras&photography > tripods",
    "Electronics > wearabletechnology > smartwatches",
    "Electronics > wearabletechnology > fitnesstrackers",
    "Electronics > poweraccessories > batteries",
    "Electronics > poweraccessories > chargers",
    "Electronics > generalpurposebatteries&chargers > batteries",
    "Electronics > generalpurposebatteries&chargers > chargers",
    "Officeproducts > officeelectronics > computers",
    "Officeproducts > officeelectronics > printers",
    "Officeproducts > officeelectronics > scanners",
    "Officeproducts > officepaperproducts > notebooks",
    "Officeproducts > officepaperproducts > pens",
    "Officeproducts > stationery&writingsupplies > pens",
    "Officeproducts > stationery&writingsupplies > pencils",
    "Home&kitchen > kitchenappliances > mixers",
    "Home&kitchen > kitchenappliances > microwaves",
    "Home&kitchen > kitchenappliances > refrigerators",
    "Home&kitchen > kitchenappliances > blenders",
    "Home&kitchen > homeappliances > heaters",
    "Home&kitchen > homeappliances > fans",
    "Home&kitchen > homestorage&organization > baskets",
    "Home&kitchen > homestorage&organization > drawers",
    "Home&kitchen > smallkitchenappliances > toasters",
    "Home&kitchen > smallkitchenappliances > coffee_makers",
    "Home&kitchen > craftmaterials > artsupplies",
    "Home&kitchen > craftmaterials > paintingtools",
    "Health&personalcare > homemedicalsupplies&equipments > thermometers",
    "Health&personalcare > homemedicalsupplies&equipments > bloodpressuremonitors",
    "Health&personalcare > healthmonitors > fitnesstrackers",
    "Health&personalcare > healthmonitors > heart_rate_monitors",
    "Car&motorbike > caraccessories > car_audio",
    "Car&motorbike > caraccessories > car_covers",
    "Musicalinstruments > microphones > wired_microphones",
    "Musicalinstruments > microphones > wireless_microphones",
    "Toys&games > art&crafts > craft_kits",
    "Toys&games > art&crafts > painting_sets",
    "Homeimprovement > electrical&adapters > outlet_adapters",
    "Homeimprovement > electrical&adapters > extension_cords",
    "Homeimprovement > cordmanagement > cord_clips",
    "Homeimprovement > cordmanagement > cable_trays",
    "Miscellaneous > pens&writing > ballpoint_pens",
    "Miscellaneous > pens&writing > gel_pens",
    "Miscellaneous > pens&writing > fountain_pens"
]

with col1:
    category_input = st.selectbox("Choose the category", categories)

with col2:
    product_url = st.text_input("URL")
with col3:
    year = st.selectbox("Year", [str(y) for y in range(2019, 2029)])
st.markdown("</div>", unsafe_allow_html=True)

# Helper functions
def generate_monthly_data(yearly_data):
    base_data = np.random.normal(loc=yearly_data / 12, scale=yearly_data * 0.05, size=12)
    festive_boost = {'January': 1.1, 'March': 1.3, 'August': 1.2, 'October': 1.5, 'November': 1.7, 'December': 1.2}
    monthly_data = [base_data[i] * festive_boost.get(month, 1) for i, month in enumerate(months)]
    monthly_data = np.maximum(monthly_data, yearly_data * 0.01)
    return monthly_data / sum(monthly_data) * yearly_data

def adj_price_demand(base, views, cart, month):
    demand_factor = (views / 1000 * 0.005) + (cart / 100 * 0.02)
    price = base * (1 + demand_factor)
    if month == 'November':
        price *= 0.4
    return price

def get_most_compatible_category(category_input):
    category_list = data['Category'].str.lower().unique().tolist()
    match, similarity, _ = process.extractOne(category_input.lower(), category_list, score_cutoff=60)
    return match if similarity >= 60 else None

def get_most_compatible_product(category, product_name):
    products = data[data['Category'].str.lower() == category]
    match, similarity, _ = process.extractOne(product_name.lower(), products['Product_Name'].str.lower().tolist(), score_cutoff=60)
    return products[products['Product_Name'].str.lower() == match].iloc[0] if similarity >= 60 else None

def get_product_name_from_url(url, max_retries=25, delay=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    retries = 0
    product_name = None

    # Create a placeholder for the "Processing..." message with loading dots
    loading_message = st.empty()
    dots = 0

    while retries < max_retries and not product_name:
        try:
            # Update "Processing..." message with loading dots
            dots_text = "." * dots
            loading_message.write(f"Processing{dots_text}")
            dots = (dots + 1) % 4  # Cycle dots from 0 to 3

            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Attempt to locate the product name
            product_name = soup.find('h1', {'id': 'title'}).text.strip()
        except AttributeError:
            product_name = None  # Ensure product_name is None if not found

        time.sleep(delay)
        retries += 1

    # Clear the loading message once done
    loading_message.empty()
    return product_name

# Plot data function
def plot_data(product_name, category_input, year):
    category = get_most_compatible_category(category_input)
    if category is None:
        st.write("Category not found. Please enter a valid category.")
        return

    product = get_most_compatible_product(category, product_name)
    if product is None:
        st.write("Product not found in the category.")
        return

    yearly_views = product[view_columns_dict[year]]
    yearly_addtocart = product[addtocart_columns_dict[year]]
    base_price = float(product['Base_Price'].replace('₹', '').replace(',', ''))

    monthly_views = generate_monthly_data(yearly_views)
    monthly_addtocart = generate_monthly_data(yearly_addtocart)
    monthly_prices = [adj_price_demand(base_price, v, c, m) for v, c, m in zip(monthly_views, monthly_addtocart, months)]

    # Determine the best time to buy and sell
    best_sell_month = months[np.argmax(monthly_prices)]
    best_buy_month = months[np.argmin(monthly_prices)]

    # Graph 1: Views and Add to Cart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=months, y=monthly_views, mode='lines+markers', name='Views', line=dict(color='blue')))
    fig1.add_trace(go.Scatter(x=months, y=monthly_addtocart, mode='lines+markers', name='Add to Cart', line=dict(color='orange')))
    fig1.update_layout(title=f'Monthly Views and Add to Cart for {product_name} in {year}', xaxis_title='Month', yaxis_title='Count')

    # Graph 2: Prices
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=months, y=monthly_prices, mode='lines+markers', name='Price', line=dict(color='green')))
    fig2.update_layout(title=f'Monthly Prices for {product_name} in {year}', xaxis_title='Month', yaxis_title='Price (₹)')

    # Display the best months to buy and sell
    st.write(f"**The best time to sell the product:** {best_sell_month}")
    st.write(f"**The best time to buy the product:** {best_buy_month}")

    return fig1, fig2

# Main button
st.markdown("<div class='analyse-btn'>", unsafe_allow_html=True)
if st.button("Analyse"):
    if product_url and year.isdigit() and 2019 <= int(year) <= 2028:
        year = str(year)
        product_name = get_product_name_from_url(product_url)
        if product_name:
            fig1, fig2 = plot_data(product_name, category_input, year)
            if fig1 and fig2:
                st.markdown("<div class='results'>RESULTS</div>", unsafe_allow_html=True)
                st.plotly_chart(fig1)
                st.plotly_chart(fig2)
    else:
        st.write("Please enter a valid URL and a year between 2019 and 2028.")
