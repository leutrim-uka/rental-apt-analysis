import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from utils import plot_germany, remove_outliers_in_column
from PIL import Image

question1 = 'Which German states have the highest cold rent in average?'
question2 = 'Which parts of Berlin have the highest cold rent in average?'
question3 = 'Which type of heating is most common throughout Germany?'
question4 = 'Which states have newer/older buildings?'
question5 = 'What is the average size of apartments in sqm in each state?'


def landing():
    st.subheader("Please select a research question from the dropdown on the left")
    st.text(f'''
        Question 1: {question1}
        Question 2: {question2}
        Question 3: {question3}
        Question 4: {question4}
    ''')

def q1():
    df = pd.read_csv('data/q1.csv')
    question = f'Q1: {question1}'

    st.subheader(question)

    labels = ['Cold rent']
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    plt.suptitle('Comparison of cold rent among all 16 states\n(Outliers removed on a state-by-state basis)')
    df[['baseRent_mean']].sort_values(by='baseRent_mean').plot(ax=ax[0], kind='bar')
    ax[0].legend(labels=labels)
    ax[0].set_title('Mean rent prices')
    ax[0].set_xlabel('State')
    ax[0].set_ylabel('Rent (EUR)')
    df[['baseRent_median']].sort_values(by='baseRent_median').plot(ax=ax[1], kind='bar')
    ax[1].legend(labels=labels)
    ax[1].set_title('Median rent prices')
    ax[1].set_xlabel('State')
    st.pyplot(fig)

    sns.set_style('whitegrid')

    plot_germany(df[['regio1', 'baseRent_mean']], 'baseRent_mean', "Mean Rent Prices (in EUR)\nOutliers removed")

    st.text('Click on the column header to change sorting')
    st.dataframe(df, use_container_width=True)

def q2():
    question = f'Q2: {question2}'

    st.subheader(question)

    df = pd.read_csv('data/q2.csv')[['note', 'baseRent']]

    st.write(df.head(10))

    image = Image.open('data/q2_berlin.png')
    st.image(image)

    st.subheader("Bonus: Which parts of Berlin have the lowest rent?")
    st.write(df.tail(10))

def q3():
    question = f'Q3: {question3}'

    # Print the question on screen
    st.subheader(question)

    # Read and group data
    df = pd.read_csv('data/immo_data.csv', usecols=['regio1', 'heatingType'])
    df = df.groupby('heatingType').count()[['regio1']].sort_values(by='regio1', ascending=False)
    df.rename(columns={'regio1': 'count'}, inplace=True)

    # Remove underscore withing yticks for better readability
    ticks = df.index
    labels = [tick.replace('_', ' ') for tick in ticks]

    # Plot
    fig, ax = plt.subplots()
    df.plot(ax=ax, kind='barh', )
    plt.ylabel('Heating type\n')
    plt.xlabel('\nCount of apartments with the corresponding heating type')
    ax.set_yticklabels(labels)
    st.pyplot(fig)

    # Show dataframe on screen
    st.text('The exact count of apartments with a specific heating type is shown below:')
    st.write(df)

def q4():
    question = f'Q4: {question4}'

    # Print the question on screen
    st.subheader(question)

    # Read and group data
    df = pd.read_csv('data/immo_data.csv', usecols=['regio1', 'yearConstructed'])

    # Median
    median_age = df.groupby('regio1')[['yearConstructed']].median().sort_values(by='yearConstructed', ascending=True)
    median_age.rename(columns={'yearConstructed': 'yearConstructed_median'}, inplace=True)

    # Mean
    mean_age = df.groupby('regio1')[['yearConstructed']].mean().sort_values(by='yearConstructed', ascending=True)
    mean_age.rename(columns={'yearConstructed': 'yearConstructed_mean'}, inplace=True)
    mean_age.yearConstructed_mean = mean_age.yearConstructed_mean.apply(lambda x: round(x, 2))

    st.markdown('**Median of construction year**')

    col1, col2 = st.columns(2)

    with col1:
        st.write(median_age)

        st.markdown('**Median of construction year**')
        st.write(mean_age)



    with col2:
        plot_germany(median_age, 'yearConstructed_median', 'Median Age of Buildings')
        st.text('\n')
        plot_germany(mean_age, 'yearConstructed_mean', 'Mean Age of Buildings')
        st.markdown('**Mean of construction year**')


def q5():
    question = f'Q5: {question5}'

    # Print the question on screen
    st.subheader(question)

    st.text('Unit in the livingSpace column is square meters (sqm)')

    # Read and group data
    df = pd.read_csv('data/immo_data.csv', usecols=['regio1', 'yearConstructed'])
    df = remove_outliers_in_column(df, 'yearConstructed')
    df = pd.read_csv('data/immo_data.csv', usecols=['regio1', 'livingSpace'])
    df = df.groupby('regio1')[['livingSpace']].mean().reset_index().sort_values(by='livingSpace', ascending=True)

    df.livingSpace = df.livingSpace.apply(lambda x: round(x, 2))

    st.dataframe(df, use_container_width=True)

    plot_germany(df, 'livingSpace', 'Median of the apartment size in square meters')