import streamlit as st
import threading

from src.common import *
from src.workflow import *
from src.run_subprocess import *
from src.captcha_ import *

# Page name "workflow" will show mzML file selector in sidebar also the run_subprocess example
params = page_setup(page="workflow")

# check captcha locally and in hosted mode
check_captcha(params)

st.title("Workflow")

# Define tabs for navigation
tabs = ["Table example", "Run Subprocess example"]
tabs = st.tabs(tabs)

# Example to show table
with tabs[0]:

    # Define two widgets with values from parameter file 
    # To save them as parameters use the same key as in the json file

    # Access the x-dimension via a local variable
    xdimension = st.number_input(
        label="x dimension", min_value=1, max_value=20, value=params["example-x-dimension"], step=1, key="example-x-dimension")

    st.number_input(label="y dimension", min_value=1, max_value=20,
                    value=params["example-y-dimension"], step=1, key="example-y-dimension")

    # Get a dataframe with x and y dimensions via time consuming (sleep) cached function
    # If the input has been given before, the function does not run again
    # Input x from local variable, input y from session state via key
    df = generate_random_table(xdimension, st.session_state["example-y-dimension"])

    # Display dataframe via custom show_table function, which will render a download button as well
    show_table(df, download_name="random-table")    

# Example for running a subprocess
with tabs[1]:
     
    # This example demonstrates how to run an external process (here the Linux command "grep") as a subprocess
    # display the process output. Also works with longer running process like e.g., calling an OpenMS TOPP tool 

    # here can be make form to take all user parameters for OpenMS TOPP tools
    # for make more simple already write function; please see src/ini2dic.py 

    # Define the directory where mzML files are located
    mzML_dir: Path = Path(st.session_state.workspace, "mzML-files")

    # Create two columns for the Streamlit app layout
    col1, col2 = st.columns(2)

    # Create a text area for the user to enter the mzML file name
    mzML_file = col1.text_area('Enter mzML file name', height=10, placeholder="mzML file name", help="Provide the mzML file name without .mzML extension")
    mzML_file_path = os.path.join(mzML_dir, mzML_file+'.mzML')

    # Create a dictionary to capture the output and status of the subprocess
    result_dict = {}
    result_dict["success"] = False
    result_dict["log"] = " "

    # Create a flag to terminate the subprocess
    terminate_flag = threading.Event()
    terminate_flag.set()

    # Function to terminate the subprocess
    def terminate_subprocess():
        global terminate_flag
        terminate_flag.set()

    # Check if the "Extract ids" button is clicked
    if st.button("Extract ids"):

        # Check if the "Terminate/Clear" button is clicked to stop the subprocess and clear the form
        if st.button("Terminate/Clear"):
            # Terminate the subprocess
            terminate_subprocess()
            st.warning("Process terminated. The analysis may not be complete.")
            # Reset the page
            st.experimental_rerun() 

        # Display a status message while running the analysis
        with st.status("Please wait until fetching all ids from mzML 😑"):

            # Define the command to run as a subprocess (example: grep)
            args = ["grep", "idRef", mzML_file_path]

            # Add any additional variables needed for the subprocess (if any)
            variables = []  

            # Display the command that will be executed
            message = f"Running command: {' '.join(args)}"
            st.code(message)

            # Run the subprocess command
            run_subprocess(args, variables, result_dict)

        # Check if the subprocess was successful
        if result_dict["success"]:
            # Here can add code here to handle the results, e.g., display them to the user
            
            pass  # Placeholder for result handling


# At the end of each page, always save parameters (including any changes via widgets with key)
save_params(params)
