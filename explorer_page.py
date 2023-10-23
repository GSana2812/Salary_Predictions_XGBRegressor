import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from descriptions import COMPANY_LOCATION, EMPLOYMENT_TYPE, EXPERIENCE_LEVEL, COMPANY_SIZE
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots


@st.cache_resource
def load_data():

    df = pd.read_csv('salaries.csv')

    df['company_location'] = df['company_location'].map(COMPANY_LOCATION)
    df['employment_type'] = df['employment_type'].map(EMPLOYMENT_TYPE)
    df['experience_level'] = df['experience_level'].map(EXPERIENCE_LEVEL)
    df['company_size'] = df['company_size'].map(COMPANY_SIZE)


    return df


def show_explore_page():

    df = load_data()

    st.title("Visualizing Data Professionals Charts")

    st.write(
        """#### Distribution of Data Entries throughout years"""
    )

    data_values = df['work_year'].value_counts()

    fig = go.Figure(data=go.Pie(
        labels=data_values.index,
        values=data_values.values,
        hole=0.4,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(
            colors=px.colors.sequential.Jet_r,
            line=dict(
                color='honeydew',
                width=2
            )
        ),
    ))

    # Update layout
    fig.update_layout(
        title="Distribution of Data Entries across Years",
        annotations=[dict(text="Year Overview", showarrow=False, font_size=20)],
        height=600
    )

    st.plotly_chart(fig)

    st.write( """#### Examining Mean Salary by Year""")

    # Salary Distribution getting the mean salary by year
    mean_salary_by_year = df.groupby('work_year')['salary_in_usd'].mean()

    # Visualizing Salary Distributions
    fig = make_subplots()

    barchart_trace = go.Bar(
        x=mean_salary_by_year.index,
        y=mean_salary_by_year.values,
        name="Mean Salary",
        marker=dict(color='blue')
    )

    fig.add_trace(barchart_trace)

    scatter_trace = go.Scatter(
        x=mean_salary_by_year.index,
        y=mean_salary_by_year.values,
        name="Mean Salary",
        mode="lines+markers",
        line=dict(color="orange"),
        marker=dict(symbol="circle-open", size=13)
    )

    fig.add_trace(scatter_trace)

    fig.update_layout(
        title="Examining Mean Salary by Year",
        xaxis_title="Working Year",
        yaxis_title="Mean Salary",
        height=600
    )

    st.plotly_chart(fig)

    st.write(""""### Distribution of Experience over Years""")

    fig = px.histogram(
        data_frame=df,
        x='experience_level',
        facet_col='work_year',
        nbins=7,
        text_auto=True,
        labels={'experience_level': 'Experience Level', 'count': 'Count'},
        title='Distribution of Experience Levels across Work Years'
    )

    # Configure histogram aesthetics
    fig.update_traces(
        textposition='auto',
        marker_color='brown',
    )

    # Update layout
    fig.update_layout(yaxis_title='Count')

    # Show the histogram
    st.plotly_chart(fig)

    st.write(""""### Salary (US$) vs Country""")

    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    df.boxplot('salary_in_usd', 'company_location', ax=ax)
    plt.suptitle('Salary (US$) v Country')
    plt.title('')
    plt.ylabel('Salary')
    plt.xticks(rotation=90)

    st.pyplot(fig)

    st.write(
        """
    #### Distribution of experience levels
    """
    )
    exp_values = df['experience_level'].value_counts()

    colors = sns.color_palette("Set2")
    plt.pie(exp_values, labels=exp_values.index, colors=colors, autopct='%.0f%%')
    plt.title('Distribution of Experience Levels')
    plt.show()

    st.write(
        """
    #### Distribution of experience levels
    """
    )

    # Remote Ratio per work year
    fig, ax = plt.subplots(4, 1, figsize=(5, 10))

    for i, year in enumerate([2020, 2021, 2022, 2023]):
        year_df = df[df['work_year'] == year]
        remote_ratio = year_df['remote_ratio'].value_counts(normalize=True)
        colors = sns.color_palette("Set2")
        sns.barplot(x=remote_ratio.index, y=remote_ratio.values * 100, ax=ax[i], palette=colors)
        ax[i].set_title(f'Remote Ratio in {year}')
        ax[i].set_ylabel('Percentage')
        if year == 2023:
            ax[i].set_xticklabels(['Not Remote', 'Partially Remote', 'Fully Remote'])
        else:
            ax[i].set_xticks([])
        ax[i].set_xlabel('')

    st.pyplot(fig)

    st.write(
        """
    #### Salary Distributions by Experience Level
    """
    )
    # get salary by experience level
    entry_level = df[df['experience_level'] == 'Entry-Level']['salary_in_usd']
    mid_level = df[df['experience_level'] == 'Mid-Level']['salary_in_usd']
    senior_level = df[df['experience_level'] == 'Senior-Level']['salary_in_usd']
    exec_level = df[df['experience_level'] == 'Executive-Level']['salary_in_usd']

    # plot salary distribution by experience level
    fig, ax = plt.subplots(figsize=(7, 3))
    colors = sns.color_palette("Set2")

    sns.kdeplot(entry_level, ax=ax, shade=False, color=colors[0], label='Entry Level', linewidth=2)
    sns.kdeplot(mid_level, ax=ax, shade=False, color=colors[1], label='Mid Level', linewidth=2)
    sns.kdeplot(senior_level, ax=ax, shade=False, color=colors[2], label='Senior Level', linewidth=2)
    sns.kdeplot(exec_level, ax=ax, shade=False, color=colors[3], label='Executive Level', linewidth=2)

    ax.set_title('Salary Distribution by Experience Level')
    ax.set_xticks([0, 100000, 200000, 300000, 400000, 500000])
    ax.set_xticklabels(['$0', '$100K', '$200K', '$300K', '$400K', '$500K'])
    ax.set_xlabel('Salary')
    ax.set_ylabel('Density')
    ax.legend(facecolor='white')

    st.pyplot(fig)

    st.write(
        """
    #### Salary Distributions by Company Size
    """
    )

    # plot salary distributions by company size

    small = df[df['company_size'] == 'Small']['salary_in_usd']
    medium = df[df['company_size'] == 'Medium']['salary_in_usd']
    large = df[df['company_size'] == 'Large']['salary_in_usd']

    fig, ax = plt.subplots(figsize=(7, 3))
    colors = sns.color_palette("Set2")

    sns.kdeplot(small, ax=ax, shade=False, color=colors[0], label='Small', linewidth=2)
    sns.kdeplot(medium, ax=ax, shade=False, color=colors[1], label='Medium', linewidth=2)
    sns.kdeplot(large, ax=ax, shade=False, color=colors[2], label='Large', linewidth=2)

    ax.set_title('Salary Distribution by Company Size')
    ax.set_xticks([0, 100000, 200000, 300000, 400000, 500000])
    ax.set_xticklabels(['$0', '$100K', '$200K', '$300K', '$400K', '$500K'])
    ax.set_xlabel('Salary')
    ax.set_ylabel('Density')
    ax.legend(facecolor='white')

    st.pyplot(fig)

    st.write(
        """
    #### Top 10 jobs with highest salaries
    """
    )

    top_10_jobs = df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)[:10]

    fig, ax = plt.subplots(figsize=(7, 3))
    colors = sns.color_palette("Set2")

    sns.barplot(x=top_10_jobs.values, y=top_10_jobs.index, ax=ax, palette=colors)
    ax.set_title('Top 10 Job Titles with Highest Mean Salary')
    ax.set_xlabel('Mean salary')
    ax.set_ylabel('Job Title')
    ax.set_xticks([0, 100000, 200000, 300000, 400000, 500000])
    ax.set_xticklabels(['$0', '$100K', '$200K', '$300K', '$400K', '$500K'])

    st.pyplot(fig)






