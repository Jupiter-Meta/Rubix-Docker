import psycopg2

def fetchUserTransactions(fetchSize):
    
    connection_params = {
    'host': 'udchalo-preprod-db.cluster-cnhilnddjsql.ap-south-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'rubix_dev',
    'user': 'superj_rubix',      # Replace with your actual username
    'password': 'superj_rubix'   # Replace with your actual password
    }
    conn = None
    cur = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**connection_params)
        
        # Create a cursor object
        cur = conn.cursor()
        
        # Execute a query
        cur.execute(f"SELECT * FROM usertransactions LIMIT %s;", (fetchSize,))
        
        # Fetch all rows from the executed query
        records = cur.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cur.description]
        
        # Map each row to a dictionary with field names as keys
        results = []
        for row in records:
            row_dict = dict(zip(column_names, row))
            results.append(row_dict)
        
        return results
        
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

def fetchUserAttributes(fetchSize):
    
    connection_params = {
    'host': 'udchalo-preprod-db.cluster-cnhilnddjsql.ap-south-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'rubix_dev',
    'user': 'superj_rubix',      # Replace with your actual username
    'password': 'superj_rubix'   # Replace with your actual password
    }
    conn = None
    cur = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**connection_params)
        
        # Create a cursor object
        cur = conn.cursor()
        
        # Execute a query
        cur.execute(f"SELECT * FROM usertransactions LIMIT %s;", (fetchSize,))
        
        # Fetch all rows from the executed query
        records = cur.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cur.description]
        
        # Map each row to a dictionary with field names as keys
        results = []
        for row in records:
            row_dict = dict(zip(column_names, row))
            results.append(row_dict)
        
        return results
        
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()