import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.colors as mcolors
import geopandas as gpd
import streamlit as st

def load_data(src):
    pass


def plot_germany(df, column_to_plot, title):
    df = df.reset_index()
    df.regio1 = df.regio1.map(lambda x: x.replace("_", "-"))

    # Load the GeoJSON file
    geojson_path = "data/2_hoch.geo.json"
    gdf = gpd.read_file(geojson_path)

    # Merge the median rent prices with the GeoDataFrame
    gdf_merged = gdf.merge(df, left_on='name', right_on='regio1')

    colors = ["#D6EAF8", "#21618C"]  # Light teal to dark teal
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_colormap", colors)

    # Plot the map with a gradient based on median rent prices
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_merged.plot(column=column_to_plot, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    # Set the title and adjust the plot appearance
    plt.title(title)
    ax.set_axis_off()

    # Show the plot
    st.pyplot(fig)


def remove_cold_rent_outliers(df):
    df.regio1 = df.regio1.map(lambda x: x.replace("_", "-"))
    states = df.regio1.unique()
    filtered_df = pd.DataFrame()

    for state in states:
        state_base_rent = df[df.regio1 == state]
        q1 = np.percentile(state_base_rent.baseRent, 25)
        q3 = np.percentile(state_base_rent.baseRent, 75)
        iqr = q3 - q1
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr
        state_base_rent = df[(df.regio1 == state) & (df.baseRent >= lower_limit) & (df.baseRent <= upper_limit)]
        filtered_df = pd.concat([filtered_df, state_base_rent])

    return filtered_df


def remove_outliers_in_column(df, column):
    q1 = np.percentile(df[column], 25)
    q3 = np.percentile(df[column], 75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    filtered_df = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]

    return filtered_df
