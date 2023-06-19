import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title='Car Price', page_icon='car.ico', layout="centered", initial_sidebar_state="auto", menu_items=None)

model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
car = pd.read_csv('Cleaned_Car_data.csv')

def main():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()

    companies.insert(0, 'Select Company')
    st.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Old Car Price "
        "Prediction</h1></center>",
        unsafe_allow_html=True)

    company = st.selectbox("Company", companies)
    selected_company_models = car_models if company == 'Select Company' else sorted(
        car[car['company'] == company]['name'].unique())
    car_model = st.selectbox("Car Model", ['Select Car Model'] + selected_company_models,
                             index=0 if len(selected_company_models) > 0 else None)

    selected_year = st.selectbox("Year", ['Please select one'] + list(map(str, year)))

    selected_fuel_type = st.selectbox("Fuel Type", ['Please select one'] + list(fuel_types))
    driven = st.number_input("Kilometers Driven", min_value=0)

    if st.button("Predict"):
        if company == 'Select Company' or car_model == 'Select Car Model' or selected_year == 'Please select one' or selected_fuel_type == 'Please select one':
            st.error("Please fill in all the required fields.")
        else:
            if selected_fuel_type == 'Please select one':
                st.error("Please select a fuel type.")
            else:
                if selected_year == 'Please select one':
                    st.error("Please select a year.")
                else:
                    prediction = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                                            data=np.array([car_model, company, selected_year, driven,
                                                                           selected_fuel_type]).reshape(1, 5)))
                    multiplied_prediction = prediction[0] * 2.9
                    rounded_prediction = round(multiplied_prediction, 2)
                    st.success("Predicted Price: **{:.2f} BDT**".format(rounded_prediction))

if __name__ == "__main__":
    main()
