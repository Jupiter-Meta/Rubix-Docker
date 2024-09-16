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
        cur.execute(f"SELECT * FROM userattributes LIMIT %s;", (fetchSize,))
        
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

def fetchUserTransactionswithID(userID):
    userid_cleaned = userID.replace("'", "")
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
        cur.execute(f"SELECT * FROM usertransactions WHERE userid = %s;", (userid_cleaned,))
        
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

def fetchUserAttributeswithID(userID):
    userid_cleaned = userID.replace("'", "")
    
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
        cur.execute(f"SELECT * FROM userattributes WHERE userid = %s;", (userid_cleaned,))
        
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

def writeAttributes(data):
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
        insert_query = """INSERT INTO userattributes (did, userid, onboarded, keywords, attributes) VALUES (%s, %s, %s, %s, %s);"""
        # Execute a query
        cur.execute(insert_query, (data["did"], data["userId"], data["onboarded"], data["keywords"], data["attributes"]))
        
        # Fetch all rows from the executed query
        connection.commit()
        
        return 1
        
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    
