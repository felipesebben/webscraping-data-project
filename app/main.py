from etl import extract, load, transform


def main():
    """
    Main function to perform the ETL process.
    """
    # Extract data
    data = extract.extract()

    # Transform data
    data = transform.transform()

    # Load data
    load.load(
        data, "data/processed", "csv", "gulfood_2024_processed.csv"
    )  # Comment this line if you want to save the file as xlsx
    load.load(
        data, "data/processed", "xlsx", "gulfood_2024_processed.xlsx"
    )  # Comment this line if you want to save the file as csv


if __name__ == "__main__":
    main()
