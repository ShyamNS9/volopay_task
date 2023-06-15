import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import SoftwareDetails


def migrate_data():
    session: Session = SessionLocal()

    # Read the CSV file using pandas
    df = pd.read_csv('data.csv')

    # Loop through each row in the DataFrame
    for _, row in df.iterrows():
        # Create an instance of your model and populate it with the data from the row
        # Replace YourModel with your actual model
        model_instance = SoftwareDetails(**row)

        # Add the instance to the session and commit the changes
        session.add(model_instance)
        session.commit()

    session.close()


if __name__ == "__main__":
    migrate_data()
