import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from streamlit_option_menu import option_menu

# Function to connect to MySQL and fetch data
def fetch_data():
    # Replace these with your MySQL database credentials
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'customer'
    }

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)

    # Fetch data from MySQL into a DataFrame
    query = "SELECT * FROM customer_info;"
    data = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    return data

# Load data from MySQL
data = fetch_data()

# Streamlit app favicon and title
st.set_page_config(page_title="Emotional analysis",
                   page_icon=":bar_chart:",
                   layout="wide")

selected = option_menu(None, ["Home", "Location", "Age Group", "Gender"],
                        icons=['house', 'bi-geo-alt-fill', "bi-diagram-2-fill", 'bi-gender-ambiguous'], key='menu_5', orientation="horizontal")

if selected=='Home':
    # st.write("home")

    # Streamlit App
    st.title('Emotion Analysis Dashboard')

    # Sidebar for selecting emotion
    st.sidebar.title('Filter Options')
    selected_emotion = st.sidebar.selectbox('Select Emotion', ["Select emotion"] + list(data['emotion'].unique()))

    if st.sidebar.button('Visualize'):
        # Filter data based on selected emotion
        if selected_emotion=="Select emotion":
            st.warning('Please select a valid emotion and click the button to start visualizing.')
        else:
            filtered_data = data[data['emotion'] == selected_emotion]

            # Display filtered data
            st.subheader(f'Emotions Distribution for {selected_emotion} across Products')
            st.write(filtered_data)

            # Create a Plotly chart (bar chart for emotions distribution across products)
            # st.subheader(f'Emotions Distribution Across Products for {selected_emotion}')
            products_chart = px.bar(filtered_data, x='product_name', title=f'Emotions Distribution Across Products for {selected_emotion}')
            st.plotly_chart(products_chart)        
    else:
        st.info('Click the button to start visualizing.')

elif selected=='Location':
    # st.write("Loc")

    # App
    st.title('Emotion Analysis Dashboard')

    # Sidebar for selecting emotion and product
    st.sidebar.title('Filter Options')
    selected_emotion = st.sidebar.selectbox('Select Emotion', ["Select emotion"] + list(data['emotion'].unique()))
    selected_product = st.sidebar.selectbox('Select Product', ["Select product"] + list(data['product_name'].unique()))

    if st.sidebar.button('Visualize'):
        if selected_emotion=="Select emotion" or selected_product=="Select product":
            st.warning('Please select a valid emotion and product then click the button to start visualizing.')
        else:
            # Filter data based on selected emotion and product
            filtered_data = data[(data['emotion'] == selected_emotion) & (data['product_name'] == selected_product)]

            # Display filtered data
            st.subheader(f'Emotions for {selected_product} with {selected_emotion} emotion')
            st.write(filtered_data)

            # Create a Plotly chart (bar chart for emotions distribution across locations)
            # st.subheader(f'Emotions Distribution Across Locations for {selected_product}')
            emotions_chart = px.bar(filtered_data, x='location', color='emotion', title=f'Emotions Distribution Across Locations for {selected_product}')
            st.plotly_chart(emotions_chart)
    else:
        st.info("Click the button to start visualizing.")

elif selected=="Age Group":
    # st.write("age")

    # App
    st.title('Emotion Analysis Dashboard')

    # Sidebar for selecting emotion and product
    st.sidebar.title('Filter Options')
    selected_emotion = st.sidebar.selectbox('Select Emotion', ["Select emotion"] + list(data['emotion'].unique()))
    selected_product = st.sidebar.selectbox('Select Product', ["Select product"] + list(data['product_name'].unique()))

    if st.sidebar.button('Visualize'):
        if selected_emotion=="Select emotion" or selected_product=="Select product":
            st.warning('Please select a valid emotion and product then click the button to start visualizing.')
        else:
            # Filter data based on selected emotion and product
            filtered_data = data[(data['emotion'] == selected_emotion) & (data['product_name'] == selected_product)]

            # Display filtered data
            st.subheader(f'Emotions for {selected_product} with {selected_emotion} emotion')
            st.write(filtered_data)

            # Create a Plotly chart (bar chart for emotions distribution across locations)
            # st.subheader(f'Emotions Distribution Across age-group for {selected_product}')
            emotions_chart = px.bar(filtered_data, x='age', color='emotion', title=f'Emotions Distribution Across Age Groups for {selected_product}')
            st.plotly_chart(emotions_chart)
    else:
        st.info("Click the button to start visualizing.")
        
elif selected=="Gender":
    # st.write("gender")

    # App
    st.title('Emotion Analysis Dashboard')

    # Sidebar for selecting emotion and product
    st.sidebar.title('Filter Options')
    selected_emotion = st.sidebar.selectbox('Select Emotion', ["Select emotion"] + list(data['emotion'].unique()))
    selected_product = st.sidebar.selectbox('Select Product', ["Select product"] + list(data['product_name'].unique()))

    if st.sidebar.button('Visualize'):
        if selected_emotion=="Select emotion" or selected_product=="Select product":
            st.warning('Please select a valid emotion and product then click the button to start visualizing.')
        else:
            # Filter data based on selected emotion and product
            filtered_data = data[(data['emotion'] == selected_emotion) & (data['product_name'] == selected_product)]

            # Display filtered data
            st.subheader(f'Emotions for {selected_product} with {selected_emotion} emotion')
            st.write(filtered_data)

            # Create a Plotly chart (bar chart for emotions distribution across locations)
            # st.subheader(f'Emotions Distribution Across Genders for {selected_product}')
            emotions_chart = px.bar(filtered_data, x='gender', color='emotion', title=f'Emotions Distribution Across genders for {selected_product}')
            st.plotly_chart(emotions_chart)
    else:
        st.info("Click the button to start visualizing.")