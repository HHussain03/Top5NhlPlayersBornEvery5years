import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

# Configure logging
logging.basicConfig(filename='nhl_analysis.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define column names as variables
COLUMN_NAMES = [
    'Rk', 'Name', 'Born', 'GP', 'G', 'A', 'P', 'ESG', 'PPG', 'GWG', 'ESA',
    'PPA', 'ESP', 'PPP', 'G/GP', 'A/GP', 'P/GP', 'SHOTS', 'SH%', 'HITS', 'BS'
]

# Path to your Excel file
EXCEL_FILE = "/Users/sha/Desktop/untitled folder/Data Projects/NHL/Best Player born every 5 years.xlsx"   # Update this to your file path

# Check if the file exists
if not os.path.exists(EXCEL_FILE):
    raise FileNotFoundError(f"Excel file not found at: {EXCEL_FILE}")


def convert_to_numeric(df, columns):
    """Converts specified columns in a DataFrame to numeric, handling errors."""
    for col in columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except KeyError as e:
            logging.error(f"Column '{col}' not found in DataFrame: {e}")
            raise
        except Exception as e:
            logging.error(f"Error converting column '{col}' to numeric: {e}")
            raise
    return df


def load_data_from_excel(file_path, column_names):
    """Loads NHL data from an Excel file, handling potential errors."""
    try:
        print("Loading data from Excel...")
        df = pd.read_excel(file_path)
        print("\nColumns in the Excel file:")
        print(df.columns)
        print("\nFirst few rows of the raw data:")
        print(df.head())  # Print the first few rows
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def clean_data(df, start_year, end_year):
    """Cleans and preprocesses the NHL player data."""
    # Rename columns
    df.columns = COLUMN_NAMES

    # Drop unnecessary columns
    cols_to_drop = ['Rk', 'ESG', 'GWG', 'ESA',
    'PPA', 'ESP', 'PPP', 'G/GP', 'A/GP', 'P/GP', 'SHOTS', 'SH%', 'HITS', 'BS']
    df = df.drop(columns=cols_to_drop, errors='ignore')

    # Convert columns to numeric
    numeric_cols = ['GP', 'G', 'A', 'P', ]
    df = convert_to_numeric(df, numeric_cols)
    print("\nAfter convert_to_numeric:")
    print(df.head())

    # Extract birth year and clean player name
    #df['Born'] = df['Name'].str.extract(r'\((\d{4})\)')
    #print("\nAfter Born - name extract:")
    #print(df.head())

    
    df['Name'] = df['Name'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()
    print("\nAfter Name replace:")
    print(df.head())

    # Convert Born to numeric
    df['Born'] = pd.to_numeric(df['Born'], errors='coerce')
    print("\nAfter Born to numeric:")
    print(df.head())

    # Calculate points per game
    #df['Points'] = df['G'] + df['A']
    #print("\nAfter Points calculation:")
    #print(df.head())

    # Filter for Born
    print("Shape before filtering born: ", df.shape)
    df = df[(df['Born'] >= start_year) & (df['Born'] <= end_year)]
    print("Shape after filtering born: ", df.shape)
    print("\nAfter Filter for Born:")
    print(df.head())

    # Filter for GP
    print("Shape before filtering GP: ", df.shape)
    df = df[df['GP'] >= 200]
    print("Shape after filtering GP: ", df.shape)
    print("\nAfter Filter for GP:")
    print(df.head())


    #df = df.dropna() #Comment this line out for debugging
    print("Shape after dropna: ", df.shape)

    df = df.reset_index(drop=True)

    print("\nCleaned data:")
    print(df.head())  # Print the first few rows of cleaned data

    return df


def analyze_data(df, bins, labels, metric):
    """Analyzes the cleaned data to find top players by birth year group."""
    df['BornGroup'] = pd.cut(df['Born'], bins=bins, labels=labels)

    print(df.groupby('BornGroup').count()) #Debugging to check if there are items to group by

    df = df.sort_values(by=metric, ascending=False)
    print(df.head())
    top_players = df.groupby('BornGroup').head(5)
    print(df.head())

    print("\nTop players:")
    print(top_players)  # Print the top players
    print(top_players.columns) #debugging

    return top_players


def main(df,file_path, column_names, start_year, end_year, bins, labels, metric):
    # ... (rest of the code)
    top_players = analyze_data(df, bins, labels, metric)

    print("Shape of df: ", df.shape) # add this line
    print("Shape of top players", top_players.shape) # add this line
    print("columns of top players: ", top_players.columns) #add this line
    visualize_data(top_players, metric)
    # ...



def visualize_data(top_players, metric):
    """Visualizes the top players data."""
    if top_players.empty:
        print("No data to visualize.")
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_players, x='Name', y=metric)
    plt.xticks(rotation=45, ha='right')  # rotated and aligned
    plt.xlabel('Name')
    plt.ylabel(metric)
    plt.title('Top NHL Players')
    plt.tight_layout()
    plt.show()


def export_data(df, top_players):
    """Exports the data to CSV files."""
    df = pd.DataFrame(top_players)
    df.to_csv('nhl_analysis_debug.csv', index=False)
    top_players.to_csv('nhl_analysis_debug.csv', index=False)
    print("CSV file exported successfully!")
    print("Current Working Directory:", os.getcwd())


def main(file_path, column_names, start_year, end_year, bins, labels, metric):
    """Main function to run the NHL data analysis."""
    try:
        df = load_data_from_excel(file_path, column_names)
        df = clean_data(df, start_year, end_year)
        top_players = analyze_data(df, bins, labels, metric)
        visualize_data(top_players, metric)
        export_data(df, top_players)

    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        raise


if __name__ == "__main__":
    START_YEAR = 1985
    END_YEAR = 2000
    BINS = [1984, 1990, 1995, 2001]
    LABELS = ['1985-1990', '1991-1995', '1996-2000']
    METRIC =  'P'

    main(EXCEL_FILE, COLUMN_NAMES, START_YEAR, END_YEAR, BINS, LABELS, METRIC)
    print("Done! Check the CSV files and visualizations.")


df_check = pd.read_csv("nhl_analysis_debug.csv")
print(df_check.head())  # Verify the content