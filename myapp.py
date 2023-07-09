import sys

import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import tempfile
from questions import landing, q1, q2, q3, q4, q5
from utils import remove_cold_rent_outliers
import numpy as np

# data = 'immo_data.csv'
# df = pd.read_csv(data)
# df = remove_cold_rent_outliers(df)


def main():
    # Define the options for the menu
    menu_options = {
        "Welcome": "",
        "Q1": "",
        "Q2": "",
        "Q3": "",
        "Q4": "",
        "Q5": "",
    }

    st.title("Apartment Rental Data Analysis")


    # Create the sidebar menu
    selected_option = st.sidebar.selectbox("Questions", list(menu_options.keys()))

    # Display the selected option's content on the main screen
    if selected_option == 'Welcome':
        landing()


    if selected_option == 'Q1':
        q1()
    elif selected_option == 'Q2':
        q2()
    elif selected_option == 'Q3':
        q3()
    elif selected_option == 'Q4':
        q4()
    elif selected_option == 'Q5':
        q5()


if __name__ == '__main__':
    main()
