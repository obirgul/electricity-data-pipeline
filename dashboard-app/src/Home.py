import streamlit as st

st.set_page_config(page_title="Electicity Dashboard", page_icon="⚡️", layout="centered")


def home():
    st.title("Insight Engine")

    st.write("""Welcome to this sample dashboard! This dashboard serves as an example and is suitable for 
    introductory purposes. The primary focus of this project is to highlight good practices in data pipeline 
    development. As a result, advanced functionalities were intentionally taken out, and only basic graphs were 
    incorporated.

Feel free to explore and use this dashboard as a starting point for understanding data pipeline structures and best 
practices.""")


if __name__ == '__main__':
    home()
