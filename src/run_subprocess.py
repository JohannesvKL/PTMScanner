import streamlit as st
import subprocess

def run_subprocess(args, variables, result_dict):
    """
    run subprocess 
    Args:
        args: command with args
        variables: variable if any
        result_dict: contain success (success flag) and log (capture long log)
                     should contain result_dict["success"], result_dict["log"]
    Returns:
        None
    """

    # run subprocess and get every line of executable log in same time
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    stdout_ = []
    stderr_ = []

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            #print every line of exec on page
            st.text(output.strip())
            #append line to store log
            stdout_.append(output.strip())

    while True:
        error = process.stderr.readline()
        if error == '' and process.poll() is not None:
            break
        if error:
            #print every line of exec on page even error
            st.error(error.strip())
            #append line to store log of error
            stderr_.append(error.strip())

    #check if process run successfully
    if process.returncode == 0:
        result_dict["success"] = True
        #save in to log all lines
        result_dict["log"] = " ".join(stdout_)
    else:
        result_dict["success"] = False
        #save in to log all lines even process cause error
        result_dict["log"] = " ".join(stderr_)