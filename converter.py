import os
import patoolib

def handle_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)

    if file_extension == ".Z":
        # Decompress the file
        patoolib.extract_archive(file_path, outdir=".")
        file_path = file_name
        file_name, file_extension = os.path.splitext(file_path)

    if file_extension == ".tbl":
        # Rename .tbl to .txt
        new_file_path = file_name + ".txt"
        os.rename(file_path, new_file_path)
        file_path = new_file_path

    # If file extension is .txt, do nothing
    return file_path