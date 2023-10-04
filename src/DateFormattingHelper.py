from datetime import datetime


def parse_date(date_string):
    """
    Parse a date string with multiple possible formats.

    Parameters:
    date_string (str): The date string to parse.

    Returns:
    datetime: The parsed date as a datetime object, or None if parsing fails.
    """
    # Define a list of possible date formats
    date_formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%b %d, %Y",  # Example: Jan 01, 2021
        "%B %d, %Y",  # Example: January 01, 2021
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        # Add more formats as needed
    ]

    # Try parsing the date string with each format
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue  # If parsing fails, try the next format

    # If all parsing attempts fail, return None or handle the error as needed
    print(f"Could not parse date: {date_string}")
    return None


# # Example usage:
# date_strings = ["2021-09-28", "28-09-2021", "09/28/2021", "2021/09/28", "Sep 28, 2021", "September 28, 2021"]
# for date_str in date_strings:
#     parsed_date = parse_date(date_str)
#     print(f"Original: {date_str}, Parsed: {parsed_date}")
