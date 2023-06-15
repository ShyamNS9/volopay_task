# Volopay Assignment

To provide a step-by-step guide in your README file for someone who has cloned your project and wants to perform the migration using the data in the `data.csv` file, you can include the following instructions:

1. Clone the Project:
   ```
   git clone https://github.com/ShyamNS9/volopay_task.git
   ```

2. create .env file in the root dir.
   
   - The variables in env will be:
   ```
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=******* (unique field)
   DATABASE_USERNAME=user_name (unique field)
   DATABASE_NAME=database_name (unique field)
   ```

3. Set Up the Database:
   - Ensure PostgreSQL is installed and running on your local machine.
   - Create a new PostgreSQL database.
   - Update the database connection details in the `.env` file, you have created in step 2.

4. Install Dependencies:
   - Navigate to the project's root directory.
   - Create and activate a virtual environment (optional but recommended).
   - Install the project's dependencies:
     ```
     pip install -r requirements.txt
     ```

5. Run Initial Migration:
   - Apply the migration to create the necessary tables in the database:
     ```
     alembic upgrade head
     ```

6. Migrate the Data:
   - Ensure the `data.csv` file is located in the project's root directory.
   - Run the migration script to move the data from `data.csv` to the database:
     ```
     python migrate.py
     ```

7. Verify the Migration:
   - Connect to your PostgreSQL database using a client tool or command-line interface.
   - Verify that the data from `data.csv` has been successfully migrated into the corresponding table.


  NOTE: Postman file is added to the project itself.