import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    database='blockchain',
    user='user',
    password='password'
)

# Read list of Biconomy bundler addresses from file
def read_bundlers_from_file(file_path):
    with open(file_path, 'r') as file:
        bundlers = [line.strip() for line in file if line.strip()]
    return bundlers

bundlers_file_path = 'bundlers.txt'
biconomy_bundlers = read_bundlers_from_file(bundlers_file_path)

def mark_biconomy_bundlers():
    cursor = connection.cursor()
    for bundler in biconomy_bundlers:
        update_query = ("UPDATE user_operations "
                        "SET is_biconomy = TRUE "
                        "WHERE sender = %s")
        cursor.execute(update_query, (bundler,))
    connection.commit()
    cursor.close()

mark_biconomy_bundlers()
