import re
import pandas as pd

# Define a regular expression pattern to detect rows within the text data
ROW_PATTERN = r'^([^\n]*\n)'

# Define a regular expression pattern to detect columns within each row
COLUMN_PATTERN = r'([^\t\n]*)(\t|\n)'

# Define a function to preprocess the text data
def preprocess_text(text):
    # Remove unwanted characters from the text data
    text = re.sub('\r\n', '\n', text)
    text = re.sub('\r', '\n', text)
    
    return text

# Define a function to detect the table data
def detect_table_data(text):
    # Find the start and end of the table
    start_pattern = re.compile(r'(?P<start>Table|TABLE)\s+\d+')
    end_pattern = re.compile(r'(?P<end>NOTES|Notes)')
    
    start_match = start_pattern.search(text)
    end_match = end_pattern.search(text)
    
    if start_match and end_match:
        table_start = start_match.start()
        table_end = end_match.start()
        return text[table_start:table_end]
    
    return None

# Define a function to extract the table data
def extract_table_data(table_text):
    rows = re.findall(ROW_PATTERN, table_text, re.MULTILINE)
    
    if not rows:
        return None
    
    header_row = rows[0]
    column_matches = re.findall(COLUMN_PATTERN, header_row)
    
    if not column_matches:
        return None
    
    headers = [match[0].strip() for match in column_matches]
    data = []
    
    for row in rows[1:]:
        column_matches = re.findall(COLUMN_PATTERN, row)
        if not column_matches:
            continue
        row_data = [match[0].strip() for match in column_matches]
        data.append(row_data)
    
    return pd.DataFrame(data, columns=headers)

# Define a function to extract the text data
def extract_text_data(text, table_text):
    if table_text is None:
        return text
    
    return text.replace(table_text, '')

# Define a function to organize the text data into a DataFrame
def organize_data(text):
    # Preprocess the text data
    preprocessed_text = preprocess_text(text)
    
    # Detect the table data
    table_text = detect_table_data(preprocessed_text)
    
    # Extract the table data
    table_data = extract_table_data(table_text)
    
    # Extract the text data
    text_data = extract_text_data(preprocessed_text, table_text)
    
    return table_data, text_data
