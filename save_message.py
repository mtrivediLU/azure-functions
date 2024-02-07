import pyodbc
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the JSON data from the request body
        req_body = req.get_json()
        fname = req_body.get('fname')
        lname = req_body.get('lname')
        email = req_body.get('email')
        message = req_body.get('message')

        # Directly use the database credentials in the connection string (for testing purposes only)
        connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:testing-v2.database.windows.net,1433;Database=Database;Uid=Mihir;Pwd=Testing@123?;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert data into the Contacts table
        insert_query = "INSERT INTO Contacts (FirstName, LastName, Email, Message) VALUES (?, ?, ?, ?);"
        cursor.execute(insert_query, (fname, lname, email, message))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return func.HttpResponse("Message sent successfully!", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
