import psycopg2

# Define your connection parameters
connection_params = {
    'host': 'udchalo-preprod-db.cluster-cnhilnddjsql.ap-south-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'rubix_dev',
    'user': 'superj_rubix',      # Replace with your actual username
    'password': 'superj_rubix'   # Replace with your actual password
}

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**connection_params)
    
    # Create a cursor object
    cur = conn.cursor()
    
    # Execute a query
    cur.execute("SELECT * FROM usertransactions;")
    
    # Fetch all rows from the executed query
    records = cur.fetchall()
    
    # Print the results
    for row in records:
        print(row)
    
except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()