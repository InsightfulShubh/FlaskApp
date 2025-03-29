import psycopg2

conn = psycopg2.connect(
    dbname="storedb",
    user="user",
    password="pass",
    host="sdffdcp.ap-south-1.rds.amazonaws.com",
    port="5432"
)

print("Connected to PostgreSQL!")
conn.close()
