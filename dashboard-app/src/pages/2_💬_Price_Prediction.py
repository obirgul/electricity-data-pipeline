import os
import streamlit as st
import pandas as pd
# import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine

# db_uri = "postgresql+psycopg2://myuser:mypassword@localhost:1234/mydatabase"
db_uri = os.getenv("LOCAL_POSTGRES_URI")
engine = create_engine(db_uri)


@st.cache(ttl=60*5, allow_output_mutation=True)
def get_all_price_data(start_date, end_date):
    query = """Select * from tr_electricity_price where date between %(start_date)s and %(end_date)s"""
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={'start_date': start_date, 'end_date': end_date})
    return df


def get_last_pred_data():
    # get the latest prediction scenario id
    query = """select max(id) from prediction_scenario"""
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    max_id = df.iloc[0, 0]

    # get the prediction result for the latest prediction scenario
    query = """select * from prediction_result where "predictionScenarioId" = %(max_id)s"""
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={'max_id': int(max_id)})
    return df


def main():
    st.title("Electricity Price Prediction")

    st.write("We have a regression model that predicts the electricity price for the next 24 hours. This page allows "
             "you to check the model's performance.")

    if 'pred_df' not in st.session_state:
        st.session_state.pred_df = get_last_pred_data()

    st.session_state.pred_df['date'] = pd.to_datetime(st.session_state.pred_df['date'])
    pred_df = st.session_state.pred_df.copy()

    # get min date from prediction result, this will be end date. start date will be 48 hours before end date. make them string
    end_date = st.session_state.pred_df['date'].min()
    start_date = end_date - pd.Timedelta(hours=48)
    start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

    if 'price_df' not in st.session_state:
        st.session_state.price_df = get_all_price_data(start_date, end_date)

    price_df = st.session_state.price_df.copy()
    price_df['date'] = pd.to_datetime(price_df['date'])

    # visualize the prediction result and actual price together in one chart with plotly line chart
    st.subheader("Prediction Result")

    # Line chart için veriyi hazırlama
    fig = go.Figure()

    # İlk DataFrame'i grafiğe ekleme
    fig.add_trace(go.Scatter(x=price_df['date'], y=price_df['price'], mode='lines', name='Hourly Data'))

    # İkinci DataFrame'i grafiğe ekleme
    fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['price'], mode='lines', name='Next Day Data'))

    # Grafiği görselleştirme
    st.plotly_chart(fig)


if __name__ == '__main__':
    main()
