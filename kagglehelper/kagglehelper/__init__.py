"""This file contains the Python helper functions to
browse and download datasets"""

# IMPORTS
import zipfile
import os
import pandas as pd

# CONSTANTS
ROOT_PATH = "/".join(list(os.getcwd().split("\\")[:3]))
ROOT_LIST = os.listdir(f"{ROOT_PATH}/")
KAGGLE_JSON = "kaggle.json"
KAGGLE_COMPETITION = "kaggle competitions download -c "
KAGGLE_BROWSE = "kaggle datasets list -s "
KAGGLE_DOWNLOAD = "kaggle datasets download -d "


def check_kaggle_cred() -> bool:
    """
    Checks if the required Kaggle API authetication JSON file is present

    Parameters: None

    Returns:
        bool: True if Kaggle user validation is successful else False
    """
    if ".kaggle" in ROOT_LIST:
        kaggle_path = f"{ROOT_PATH}/.kaggle/"
        if KAGGLE_JSON in os.listdir(kaggle_path):
            kaggle_file_path = f"{kaggle_path}/{KAGGLE_JSON}"
            with open(kaggle_file_path, "r", encoding="utf-8") as file:
                kaggle_user_creds = file.readline()

            if ("username" in kaggle_user_creds) & ("key" in kaggle_user_creds):
                return True
    return False


def download_competition_dataset(file_name: str = None, cmd_line: str = None) -> str:
    """
    Downloads and Extracts data from Kaggle

    Parameters:
        * file_name (str): name of the Kaggle Competition file
        * cmd_line (str): command line/shell input

    Returns:
        str: Message whether the Competition Dataset is extracted successfully or not
    """
    if check_kaggle_cred():
        if cmd_line:
            os.popen(cmd_line).read()
            file_name = cmd_line.split()[-1]
        elif file_name:
            os.popen(KAGGLE_COMPETITION + file_name)
        else:
            return "Provide file name or command line"

        try:
            with zipfile.ZipFile(f"{file_name}.zip") as file:
                if "-" in file_name:
                    file_name = file_name.replace("-", "_")
                file.extractall(file_name)
            cwd = str(os.getcwd()).replace("\\", "/")
            return f"Dataset Location: {cwd}/{file_name}"
        except FileNotFoundError:
            return "Zip file not downloaded"
    return (
        'Make sure "~/.kaggle/kaggle.json" file exists and the correct '
        '"username" and "key" is present'
    )


def browse_dataset(subject: str, search_details: bool = False):
    """
    Browse Kaggle datasets based on the input subject

    Parameters:
        * subject (str): criteria for browsing
        * search_details (bool): True if all search details are needed
        else False for limited details

    Returns:
        str: Displays search results
    """
    if check_kaggle_cred():
        browse_list = os.popen(KAGGLE_BROWSE + subject).readlines()

        for line_num, _ in enumerate(browse_list):
            line = browse_list[line_num].replace("  ", "^")
            while "^^" in line:
                line = line.replace("^^", "^")
            line_split = line.split("^")[:-1]
            browse_list[line_num] = line_split
        if len(browse_list) < 2:
            return "No data present"
        # as second line i.e. at index 1 is "----", we remove that
        del browse_list[1]

        # create dataset
        columns = browse_list[0]
        columns = [col_name.strip() for col_name in columns]
        dataset = pd.DataFrame(columns=columns)

        for num in range(len(browse_list) - 1):
            dataset.loc[num] = browse_list[num + 1]
        if not search_details:
            dataset = dataset[["ref", "title", "size", "downloadCount"]]
        return dataset

    return (
        'Make sure "~/.kaggle/kaggle.json" file exists and '
        'the correct "username" and "key" is present'
    )


def download_dataset(reference: str, destination_folder_name: str = None) -> str:
    """
    Downloads a dataset based on the input reference

    Parameters:
        * reference (str): reference from Kaggle which is in format
        'kaggle_username/dataset_name'
        * destination_folder_name (str): name of folder where the
        date will be extracted

    Returns:
        str: Location of the folder where data is extracted.
    """
    if check_kaggle_cred():
        os.popen(KAGGLE_DOWNLOAD + reference).read()
        file_name = reference.split("/")[-1]
        try:
            with zipfile.ZipFile(f"{file_name}.zip") as file:
                if destination_folder_name:
                    file_name = destination_folder_name
                if "-" in file_name:
                    file_name = file_name.replace("-", "_")
                file.extractall(file_name)
            cwd = str(os.getcwd()).replace("\\", "/")
            if destination_folder_name:
                return f"Dataset Location: {cwd}/{destination_folder_name}"
            return f"Dataset Location: {cwd}/{file_name}"
        except FileNotFoundError:
            return (
                "Zip file not downloaded. Make sure the 'reference' "
                "provided is correct. You can check the "
                "reference by browsing the Kaggle datasets using "
                "'browse_dataset' method"
            )
    else:
        return (
            'Make sure "~/.kaggle/kaggle.json" file exists and the '
            'correct "username" and "key" is present'
        )
