import streamlit as st
from src.common import *
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
                    type="primary"
                )
    save_params(params)

# Check if the script is run in local mode (e.g., "streamlit run app.py local")
if "local" in sys.argv:
    # In local mode, run the main function without applying captcha
    main()

# If not in local mode, assume it's hosted/online mode
else:
           
    # WORK LIKE MULTIPAGE APP
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:

        # Apply captcha control to verify the user
        captcha_control()

    else:     
        # Run the main function
        main()
        

