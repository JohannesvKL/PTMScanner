import streamlit as st
import threading

from src.common import *
from src.workflow import *
from src.run_subprocess import *
from src.captcha_ import *

# Page name "workflow" will show mzML file selector in sidebar
params = page_setup(page="workflow")

#if local no need captcha
if st.session_state.location == "local":
    params["controllo"] = True
    st.session_state["controllo"] = True

#if controllo is false means not captcha applied
if 'controllo' not in st.session_state or params["controllo"] == False:
    #apply captcha
    captcha_control()
        
else:
    ### main content of page

    st.title("Workflow")
    
    tabs = ["Table example", "Run Subprocess example"]

    tabs = st.tabs(tabs)

    # Define two widgets with values from paramter file
    # To save them as parameters use the same key as in the json file

    with tabs[0]:
        # We access the x-dimension via local variable
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

    with tabs[1]:
        ###### Here just example for run subprocess 
        mzML_dir: Path = Path(st.session_state.workspace, "mzML-files")
        col1, col2 = st.columns(2)

        ## here can be make form to take all user parameters for OpenMS TOPP tools
        # for make more simple already write function; please see ini2dic.py 

        mzML_file = col1.text_area('Enter mzML file name', height=10, placeholder="mzML file name", help="provide mzML file name without .mzML extension")
        mzML_file_path = os.path.join(mzML_dir, mzML_file+'.mzML')

        #result dictionary to capture output of subprocess
        result_dict = {}
        result_dict["success"] = False
        result_dict["log"] = " "

        #create terminate flag from even function
        terminate_flag = threading.Event()
        terminate_flag.set()

        #terminate subprocess by terminate flag
        def terminate_subprocess():
            global terminate_flag
            terminate_flag.set()

        # run analysis 
        if st.button("Extract ids"):

            # To terminate subprocess and clear form
            if st.button("Terminate/Clear"):
                #terminate subprocess
                terminate_subprocess()
                st.warning("Process terminated. The analysis may not be complete.")
                #reset page
                st.experimental_rerun() 

            #with st.spinner("Running analysis... Please wait until analysis done 😑"): #without status/ just spinner button
            with st.status("Please wait until fetch all ids from mzML 😑"):

                #If session state is local
                if st.session_state.location == "local":

                    #If local the OpenMS executable in bin e-g bin/OpenNuXL 
                    #exec_command = os.path.join(os.getcwd(),'bin', "exec_name")

                    #example of run subprocess
                    args = ["grep", "idRef", mzML_file_path]


                #If session state is online/docker
                else:    

                    #example of run subprocess
                    args = ["grep", "idRef", mzML_file_path]

                # Add any additional variables needed for the subprocess (if any)
                variables = []  

                #want to see the command values and argues
                message = f"Running '{' '.join(args)}'"
                st.code(message)

                #run subprocess command
                run_subprocess(args, variables, result_dict)

            #if run_subprocess success (no need if not success because error will show/display in run_subprocess command)
            if result_dict["success"]:

                # Save the log to a text file in the result_dir
                #log_file_path = result_dir / f"{protocol_name}_log.txt"
                #with open(log_file_path, "w") as log_file:
                    #log_file.write(result_dict["log"])

                #do something probably display results etc
                pass


    # At the end of each page, always save parameters (including any changes via widgets with key)
    save_params(params)
