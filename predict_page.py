import streamlit as st
import pickle
import pandas as pd
import numpy as np
from descriptions import COMPANY_SIZE_MAPPER, EXPERIENCE_LEVEL_MAPPER


def load_data():
    with open("saved_steps.pkl", "rb") as file:
        df = pickle.load(file)
    return df

data = load_data()
xgb = data['model']
encoded_columns = data['encoded_columns']
EXPERIENCE = data['experience_level']
COMPANY_SIZE = data['company_size']
EMPLOYMENT_TYPE = data['employment_type']
JOB_TITLE = data['job_title']
COMPANY_LOCATION = data['company_location']



def show_predict_page():
    st.title("Data Professionals Salary Prediction")
    #st.write("""### We need some information to predict the salary""")


    experience = st.selectbox("Experience Level", EXPERIENCE)
    size = st.selectbox("Company Size", COMPANY_SIZE)
    employment = st.selectbox("Employment Type", EMPLOYMENT_TYPE)
    job = st.selectbox("Job Title", JOB_TITLE)    
    country = st.selectbox("Country", COMPANY_LOCATION)

    confirm_button = st.button("Calculate salary")


    if confirm_button:
        X = {'experience_level': experience,
         'company_size': size,
         'employment_type': employment,
         'job_title': job,
         'company_location': country
         }
         
        encoded_row = [1 if col == X['company_location'] or col == X['job_title'] or col == X['employment_type'] else 0 for col in encoded_columns]

        # Create a new dataframe for prediction with the same column names
        df_prediction = pd.DataFrame([encoded_row], columns=[encoded_columns])

        # The df_prediction dataframe now contains one-hot encoding for the specified features
        df_prediction['experience_level'] = X['experience_level']
        df_prediction['company_size'] = X['company_size']


        df_prediction['experience_level'] = df_prediction['experience_level'].map(lambda x: EXPERIENCE_LEVEL_MAPPER.get(x, x)).astype('float64')
        df_prediction['company_size'] = df_prediction['company_size'].map(lambda x: COMPANY_SIZE_MAPPER.get(x,x)).astype('float64')
    

        salary = xgb.predict(df_prediction)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")


