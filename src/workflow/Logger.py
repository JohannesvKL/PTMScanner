from pathlib import Path
import streamlit as st


class Logger:
    # Methods for logging messages
    def __init__(self):
        self.log_file = Path(st.session_state["workflow-dir"], "log.txt")

    def log(self, message: str) -> None:
        # Write the message to the log file.
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{message}\n\n")
