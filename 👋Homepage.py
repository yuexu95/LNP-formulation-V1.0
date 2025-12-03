"""

This is the main page, that you have to run with "streamlit run" to launch the app locally.
Streamlit automatically create the tabs in the left sidebar from the .py files located in /pages
Here we just have the home page, with a short description of the tabs, and some images

"""


import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.image as mpimg

st.set_page_config(
    page_title="Home page",
    page_icon="👋",
    layout="centered")


# Main Description
st.title("👋 Welcome to LNP formulation calculator, your best tool to calculate lipid nanoparticle formulations!")
st.markdown("Developed by Yue Xu Instructor@YongLiLab@BCM: https://yuexu95.github.io/")
st.markdown("The app is still under development. Please reach me in the homepage by email: yue.xu@bcm.edu if you have any comments or suggestions.")

# Description of the features. 
st.markdown(
    """
    ### Select on the left panel what you want to explore:

    - With General info, you will have a short description of the LNP formulation and calculation principles.
    - With pDNA Formulation, you will explore the LNP formulation calculator for plasmid DNA.
    - With mRNA Formulation, you will explore the LNP formulation calculator for mRNA.
    - with N/P Ratio, you will explore the N/P ratio calculator and its principles.
    \n  
    ### Enjoy the app!
    """
)
