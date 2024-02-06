import shutil
from pathlib import Path
import streamlit as st
import zipfile
from io import BytesIO


class DirectoryManager:
    # Methods related to directory management
    def __init__(self):
        pass

    def ensure_directory_exists(self, directory: str, reset: bool = False) -> str:
        """
        Ensures that the specified directory exists, creating it if necessary.
        Optionally resets the directory, removing all contents if it already exists.
        
        Parameters:
            directory (str): The directory to check or create.
            reset (bool): If True, the directory will be emptied if it already exists.
        
        Returns:
            str: The path to the directory.
        """
        if reset:
            shutil.rmtree(directory, ignore_errors=True)
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def zip_and_download_files(self, directory: str):
        """
        Creates a zip archive of all files within a specified directory,
        including files in subdirectories, and offers it as a download
        button in a Streamlit application.

        Args:
            directory (str): The directory whose files are to be zipped.
        """
       # Ensure directory is a Path object and check if directory is empty
        directory = Path(directory)
        if not any(directory.iterdir()):
            st.error("No files to compress.")
            return

        bytes_io = BytesIO()
        files = list(directory.rglob("*"))  # Use list comprehension to find all files

        # Check if there are any files to zip
        if not files:
            st.error("Directory is empty or contains no files.")
            return

        n_files = len(files)

        # Initialize Streamlit progress bar
        my_bar = st.progress(0)

        with zipfile.ZipFile(bytes_io, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, file_path in enumerate(files):
                if file_path.is_file():  # Ensure we're only adding files, not directories
                    # Preserve directory structure relative to the original directory
                    zip_file.write(file_path, file_path.relative_to(directory.parent))
                    my_bar.progress((i + 1) / n_files)  # Update progress bar

        my_bar.empty()  # Clear progress bar after operation is complete
        bytes_io.seek(0)  # Reset buffer pointer to the beginning

        # Display a download button for the zip file in Streamlit
        st.columns(2)[1].download_button(
            label="⬇️ Download Now",
            data=bytes_io,
            file_name="input-files.zip",
            mime="application/zip",
            use_container_width=True
        )
