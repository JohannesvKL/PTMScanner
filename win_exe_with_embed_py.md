## 💻 Create a window executable of a Streamlit App with embeddable Python

To create an executable for Streamlit app on Windows, we'll use an embeddable version of Python.</br>
Here's a step-by-step guide:

### Download and Extract Python Embeddable Version

1. Download a suitable Python embeddable version. For example, let's download Python 3.11.9:

    ```bash
    wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
    ```

2. Extract the downloaded zip file:

    ```bash
    unzip python-3.11.9-embed-amd64.zip
    ```

### Install pip

1. Download `get-pip.py`:

    ```bash
    wget https://bootstrap.pypa.io/get-pip.py
    ```

2. Install pip:

    ```bash
    ./python-3.11.9-embed-amd64/python <path_to_get-pip.py> --no-warn-script-location
    ```

### Configure Python Environment

1. Uncomment 'import site' in the `python311._pth` file:

    ```bash
    # Uncomment to run site.main() automatically
    # Remove hash from python-3.11.9-embed-amd64/python311._pth file
    import site 

    # Or use command
    sed -i 's/^# import site/import site/' python-3.11.9-embed-amd64/python311._pth
    ```

### Install Required Packages

Install all required packages from `requirements.txt`:

```bash
./python-3.11.9-embed-amd64/python -m pip install -r requirements.txt --no-warn-script-location
```

### Copy App Files and Create `run_app.bat` File

1. Create a folder for your Streamlit app:

    ```bash
    mkdir ../streamlit_exe
    ```

2. Copy Python environment and app files:

    ```bash
    # Copy Python environment and app files
    cp -r python-3.11.9-embed-amd64 streamlit_exe
    cp -r src pages .streamlit example_data app.py ../streamlit_exe
    ```
   
3. Create a Clickable Shortcut

    Create a `run_app.bat` file to make running the app easier:
    
    ```batch
    @echo off
    .\python-3.11.9-embed-amd64\python -m streamlit run app.py local
    ```
#### 🚀 <code> After successfully completing all these steps, the Streamlit app will be available by running the run_app.bat file.</code>

> [!NOTE]
You can still change the configuration of Streamlit app with .streamlit/config.toml file, e.g., provide a different port, change upload size, etc.

