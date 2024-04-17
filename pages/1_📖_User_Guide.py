import streamlit as st
from src.common import page_setup

page_setup()

st.markdown("""
# User Guide

Welcome to the OpenMS Streamlit Web Application! This guide will help you understand how to use our tools effectively.

## Advantages of OpenMS Web Apps

OpenMS web applications provide a user-friendly interface for accessing the powerful features of OpenMS. Here are a few advantages:
- **Accessibility**: Access powerful OpenMS algorithms and TOPP tools from any device with a web browser.
- **Ease of Use**: Simplified user interface makes it easy for both beginners and experts to perform complex analyses.
- **No Installation Required**: Use the tools without the need to install OpenMS locally, saving time and system resources.

## Workspaces

In the OpenMS web application, workspaces are designed to keep your analysis organized:
- **Workspace Specific Parameters and Files**: Each workspace stores parameters and files (uploaded input files and results from workflows).
- **Persistence**: Your workspaces and parameters are saved, so you can return to your analysis anytime and pick up where you left off.

## Online and Local Mode Differences

There are a few key differences between operating in online and local modes:
- **File Uploads**:
  - *Online Mode*: You can upload only one file at a time. This helps manage server load and optimizes performance.
  - *Local Mode*: Multiple file uploads are supported, giving you flexibility when working with large datasets.
- **Workspace Access**:
  - In online mode, workspaces are stored temporarily and might be cleared after your session ends.
  - In local mode, workspaces are saved on your local machine, allowing for persistent storage.

## Downloading Results

You can download the results of your analyses, including figures and tables, directly from the application:
- **Figures**: Click the download button on the figure display area.
- **Tables**: Use the download button next to displayed tables to save them as CSV files.

## Getting Started

To get started:
1. Select or create a new workspace.
2. Upload your data file.
3. Set the necessary parameters for your analysis.
4. Run the analysis.
5. View and download your results.

For more detailed information on each step, refer to the specific sections of this guide.
""")


