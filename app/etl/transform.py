from scripts.transformer import Transformer


def transform():
    """
    Main function to perform the transformation step. Calls the transformer class to perform the transformation.
    """
    transformer = Transformer()
    concatenated_data = transformer.concatenate_csv_files("data/raw/")
    transformed_data = transformer.get_category_names_from_url(
        concatenated_data, "category_icon_url"
    )

    category_replacements = {
        "worldfood": "World Food",
        "pulsesgrainscereals": "Pulses, Grains & Cereals",
        "dairy": "Dairy",
        "beverages": "Beverages",
        "meatpoultry": "Meat & Poultry",
        "fatsoils": "Fats & Oils",
        "powerbrands": "Power Brands",
    }
    formatted_data = transformer.format_categorical_values(
        transformed_data, "category_name", replacements=category_replacements
    )
    removed_duplicates = transformer.remove_duplicates(formatted_data)

    exploded_data = transformer.split_and_explode(
        removed_duplicates, ["hall", "stand"], ","
    )

    hall_replacements = {
        "Trade Center Arena": "Trade Centre Arena",
        "Skh Rashid Hall": "Shk Rashid Hall",
        "Hall2": "Hall 2",
    }
    formatted_col_value = transformer.format_categorical_values(
        exploded_data, "hall", replacements=hall_replacements
    )

    cols = ["name", "category_name", "hall", "stand"]
    selected_cols = transformer.select_rearrange_columns(formatted_col_value, cols)
    return selected_cols
