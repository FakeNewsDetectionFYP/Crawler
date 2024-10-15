from tools.db_initializer import initialize_databases  # Import the database initializer
from tools.queryManager import handle_user_queries  # Import query handler

# Set database directory path
db_directory = 'databases'  # Adjust this if needed
csv_file_path = '20241015021500.export.csv'  # Replace with your actual CSV file path

def main():
    # Initialize the databases
    initialize_databases(db_directory)

    # Handle user queries (menu options)
    handle_user_queries(db_directory, csv_file_path)

if __name__ == '__main__':
    main()