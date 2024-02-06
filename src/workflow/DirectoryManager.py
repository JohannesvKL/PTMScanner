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
        if reset:
            shutil.rmtree(directory, ignore_errors=True)
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def zip_files(self, directory):
        directory = Path(directory)  # Ensure directory is a Path object

        if not any(directory.iterdir()):
            st.error("No files to compress.")
            return

        bytes_io = BytesIO()

        files = []

        for f in directory.rglob("*"):
            if f.is_file():
                files.append(f)

        n_files = len(files) - 1

        my_bar = st.progress(0, text=f"Compressing files...")

        with zipfile.ZipFile(bytes_io, "w") as zip_file:
            for i, file_path in enumerate(files):
                zip_file.write(
                    file_path, Path(file_path.parents[0].name, file_path.name)
                )
                my_bar.progress(i / n_files)

        my_bar.empty()
        bytes_io.seek(0)
        st.download_button(
            label="⬇️ Download Now",
            data=bytes_io,
            file_name=f"input-files.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True,
        )
