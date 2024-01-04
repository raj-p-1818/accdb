import pyodbc as pyo
import pandas as pd
import pyarrow.parquet as pq
import os


def save_to_parquet(df, file_path):
    # Handle duplicate column names by adding a suffix
    df.columns = pd.Index(df.columns).where(
        ~pd.Index(df.columns).duplicated(), df.columns + "_1"
    )
    df.to_parquet(file_path, index=False)
    print(f"Saved Parquet file: {file_path}")


# Replace with the actual path to your Access database
print(pyo.drivers())
input_path = os.environ["INPUT_BUCKET_PATH"]
out_directory = os.environ["OUTPUT_BUCKET_PATH"]

path = input_path
path_parts = path.split("/")  # Splits the path into a list of parts
filename = path_parts[-1] 
db_name = filename.split('.')[0] # Extracts the last part, which is the filename



if str(input_path) != "":

    connection_string = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" 
        rf"DBQ={input_path}"
    )

    try:
        # trying to connect to the database
        engine = pyo.connect(connection_string)
    except FileNotFoundError:
        print(f"Error: Access database file not found at {connection_string['DBQ']}")
        raise


    cursor = engine.cursor()
    # Output directory for Parquet files
    output_directory = rf"{out_directory}"

    # List to store DataFrames
    dfs = []
    # Iterate through tables
    tables = cursor.tables()
    for i, table_info in enumerate(tables):
        if not str(table_info.table_name).lower().startswith("msys"):
            table_name = table_info.table_name
            print(f"\nProcessing table {i + 1}: {table_name}")
            sql = f"SELECT * FROM `{table_name}`"
            if table_name != "Orders By Date":
                try:
                        df = pd.read_sql(sql, engine)

                        try:
                            # Handle duplicate column names
                            df.columns = pd.Index(df.columns).where(
                                ~pd.Index(df.columns).duplicated(), df.columns + "_1"
                            )

                            # Save the DataFrame to a Parquet file
                            parquet_file_path = os.path.join(
                                output_directory, f"accdb-{db_name}-{table_name}.parquet"
                            )
                            save_to_parquet(df, parquet_file_path)
                        except Exception as e:
                            print(f"Error saving Parquet file for table {table_name}: {e}")
                except Exception as e:
                    print(f"Error reading table {table_name}: {e}")
                # Append the DataFrame to the list
                dfs.append(df)
    cursor.close()
    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)
    # Save the concatenated DataFrame to a single Parquet file
    combined_parquet_file = os.path.join(output_directory, f"accdb-{db_name}-{table_name}.parquet")
    save_to_parquet(final_df, combined_parquet_file)
    print("\nAll Parquet files saved successfully.")
    print(f"Combined Parquet file saved: {combined_parquet_file}") 

else:
    print("accdb file_name is not provided")