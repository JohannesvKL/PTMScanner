import streamlit as st
from captcha.image import ImageCaptcha
from src.common import *
from streamlit.web import cli
from pathlib import Path
import sys

from src.captcha_ import *

params = page_setup(page="main")

def main():
    st.title("Template App")
    st.markdown("## A template for an OpenMS streamlit app.")
    if Path("OpenMS-App.zip").exists():
        st.markdown("## Installation")
        with open("OpenMS-App.zip", "rb") as file:
            st.download_button(
                    label="Download for Windows",
                    data=file,
                    file_name="OpenMS-App.zip",
                    mime="archive/zip",
                )
    save_params(params)

# Check if the script is run in local mode (e.g., "streamlit run app.py local")
if "local" in sys.argv:
    # In local mode, run the main function without applying captcha
    main()

# If not in local mode, assume it's hosted/online mode
else:
    # If captcha control is not in session state or set to False
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        # hide app pages as long as captcha not solved
        delete_all_pages("app")

        # Apply captcha control to verify the user
        captcha_control()

    else:     
        # Run the main function
        main()

        # Restore all pages (assuming "app" is the main page)
        restore_all_pages("app")
        

