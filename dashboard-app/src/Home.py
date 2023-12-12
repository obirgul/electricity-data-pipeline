import streamlit as st

st.set_page_config(page_title="Electicity Dashboard", page_icon="⚡️", layout="centered")


def home():
    st.title("Insight Engine")

    st.write("""This is a sample dashboard for Electricity Data.""")


if __name__ == '__main__':
    home()
