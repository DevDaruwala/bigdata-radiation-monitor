import pandas as pd

# Define the unwanted columns as a list for easier removal later
UNWANTED_COLUMNS = ['Location Name', 'MD5Sum', 'Height', 'Surface', 'Radiation', 'Loader ID']

# Now, I am defining the cleaning function that will process each record (dictionary)
def clean_record(record):
    """
    This function will:
    1. Skip records where Unit is not 'cpm'
    2. Remove all unwanted columns from the record
    3. Return the cleaned record (or None if skipped)
    """
    # 1. Filter by 'Unit'
    unit = record.get('Unit')
    if unit != 'cpm':
        return None

    # 2. Remove unwanted columns
    cleaned_record = {k: v for k, v in record.items() if k not in UNWANTED_COLUMNS}

    # 3. Return the cleaned record
    return cleaned_record