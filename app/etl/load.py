import os

from etl import transform


def load(transformed_data, file_path, file_type, file_name):
    """
    Perform the load step. Save the transformed data to a defined format file.
    Parameters:
    - transformed_data: The transformed data to load
    - file_path: The path to save the file
    - file_type: The file type to save the file as (csv or xlsx)
    - file_name: The name of the file to save
    """
    transformed_data = transform.transform()
    # Create the directory if it doesn't exist
    os.makedirs(file_path, exist_ok=True)
    if file_type == "csv":
        transformed_data.to_csv(f"{file_path}/{file_name}", index=False, header=True)
    elif file_type == "xlsx":
        transformed_data.to_excel(f"{file_path}/{file_name}", index=False, header=True)
    else:
        raise ValueError("File type not supported")
