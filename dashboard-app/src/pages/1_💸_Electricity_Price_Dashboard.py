import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# db_uri = "postgresql+psycopg2://myuser:mypassword@localhost:1234/mydatabase"
db_uri = os.getenv("LOCAL_POSTGRES_URI")
engine = create_engine(db_uri)


@st.cache(ttl=60*5, allow_output_mutation=True)
def get_all_price_data():
    query = """Select * from tr_electricity_price"""
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df


def main():
    st.title("Electricity Price Dashboard")

    st.write("This is a sample dashboard.")

    if 'df' not in st.session_state:
        st.session_state.df = get_all_price_data()

    df = st.session_state.df.copy()
    df['date'] = pd.to_datetime(df['date'])

    st.subheader("Price Data")
    st.write(df)

    st.subheader("Last 24 Hours")
    t1 = df.sort_values(by='date', ascending=False).head(24)
    st.write(t1)
    st.line_chart(t1['price'], use_container_width=True)

    st.subheader("Hourly Electricity Price Trend")
    df['Hour'] = df['date'].dt.hour
    hourly_avg = df.groupby('Hour', as_index=False)['price'].mean()

    line_chart_hourly = px.line(hourly_avg, x='Hour', y='price', title='Hourly Electricity Price Trend')
    st.plotly_chart(line_chart_hourly)


if __name__ == '__main__':
    main()
