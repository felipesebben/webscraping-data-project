import glob

import pandas as pd

pd.set_option("display.max_columns", None)


class Transformer:
    """
    Class to transform the data. Performs a series of transformations such as:
    - concatenating the data
    - removing duplicates
    - resetting the index
    - extracting categories from urls
    """

    def concatenate_csv_files(self, raw_data):
        """
        Concatenate csv files. Set the working directory to the data directory to map the csv files.
        """
        # Set the pattern to match all CSV files
        pattern = f"{raw_data}/*.csv"
        # Get a list of all CSV files in the working directory
        csv_files = glob.glob(pattern)

        # Create a list to store the DataFrames
        df_list = []

        # Loop through the list of CSV files
        for csv_file in csv_files:
            # Read each CSV into a DataFrame and append to the list
            df = pd.read_csv(csv_file)
            df_list.append(df)

        concatenated_df = pd.concat(df_list, ignore_index=True)

        return concatenated_df

    def get_category_names_from_url(self, df, url_column):
        """
        Extract the category names from the URL and create a new column in the DataFrame
        """
        # Check if the URL is empty or None
        mask = df[url_column].notnull()

        # Split the URL into parts based on the "/" character
        parts = df.loc[mask, url_column].str.split("/", expand=True)

        # Get the last part of the URL (after the last "/")
        last_part = parts.iloc[:, -1]
        # Split the last part of the URL on the "." character
        last_part_parts = last_part.str.split(".", expand=True)

        # Get the first part of the last part of the URL
        category_name = last_part_parts.loc[:, 0]

        # Create a new column in the DataFrame and assign the category names
        df.loc[mask, "category_name"] = category_name

        return df

    def format_categorical_values(self, df, column, replacements):
        """
        Replace column values with new values.
        """
        df[column] = df[column].replace(replacements)
        print(f"\nUnique values in the column '{column}' after formatting:")
        # Return rows with the replaced values.
        replaced_rows = df.loc[
            df[column].isin(replacements.values()),
            ["name", "hall", "stand", "category_name"],
        ]
        print(f"Rows with the replaced values: {replaced_rows}")
        return df

    def remove_duplicates(self, df):
        """
        Remove duplicates from the DataFrame
        """
        # Check for duplicates
        print(f"Number of duplicates: {df.duplicated().sum()}")
        # Print rows with duplicates
        print(df[df.duplicated()])
        df.drop_duplicates(inplace=True)
        # Reset the index
        df.reset_index(drop=True, inplace=True)
        # Check for duplicates again
        print(f"Number of duplicates after removing: {df.duplicated().sum()}")
        return df

    def split_and_explode(self, df, columns, separator):
        """
        Split columns using a separator and explode the resulting lists.
        """
        # Check if the values for the columns have values with the separator. Print if True and return the rows with the values.
        print(f"Are there any values with the separator '{separator}' in the columns?")
        for column in columns:
            if df[column].str.contains(separator).any():
                print(
                    f"\nYes, there are values with the separator '{separator}' in the column '{column}'. The rows are:/n"
                )
                print(
                    df[["name", "hall", "stand"]].loc[
                        df[column].str.contains(separator, na=False)
                    ]
                )

                # Apply split to the specified column
                print(
                    f"\nSplitting the values in the column '{column}' using the separator '{separator}'."
                )
                df[column] = df[column].str.split(separator)

                # Explode the DataFrame on the specified column
                print(
                    f"\nExploding the DataFrame on the column '{column}'. Then, stripping leading and trailing whitespace from the values."
                )
                df_exploded = df.explode(column)

                # Strip leading and trailing whitespace from the values
                df_exploded[column] = df_exploded[column].str.strip()

                # Print the column values to check if the split and explode operations were successful.
                print(f"\nColumn '{column}' values after splitting and exploding:")
                print(df_exploded[column].unique())

                # Assign the exploded DataFrame back to df
                df = df_exploded

            else:
                print(
                    f"\nNo, there are no values with the separator '{separator}' in the columns."
                )
                pass

        return df

    def select_rearrange_columns(self, df, columns):
        """
        Reorder the columns in the DataFrame.
        """
        columns = ["name", "category_name", "country", "hall", "stand"]
        df = df[columns]

        return df
