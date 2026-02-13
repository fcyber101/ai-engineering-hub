
### Document Loading units ###


# get a list of all docs

import os

def get_all_files(root_dir="."):
    """get all files in subdirectory"""
    file_list = []

    for entry in os.scandir(root_dir):
        if entry.name.startswith('~$') or entry.name.startswith('.'):
            continue
        if entry.is_file():
            file_list.append(entry.path)
        elif entry.is_dir():
            file_list.extend(get_all_files(entry.path))

    return file_list

all_markdown_files = get_all_files("./data/documents/markdown_docs/")
print(f"All files: {len(all_markdown_files)}")