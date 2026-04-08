import os
import datetime
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
load_dotenv()

# Initialize Google Cloud SQL Connector
connector = Connector()

# Function to return the database connection string
def getconn():
    conn = connector.connect(
        f"{os.getenv('DB_PROJECT_ID')}:{os.getenv('DB_REGION')}:{os.getenv('DB_INSTANCE_NAME')}",
        "pg8000",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME"),
        ip_type=IPTypes.PUBLIC  # Uses public IP for hackathon speed
    )
    return conn

# Create the SQLAlchemy Engine
engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Define the Database Schema ---
class PatientIncident(Base):
    __tablename__ = "patient_incidents"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    patient_details = Column(String, nullable=False)
    eta_minutes = Column(Integer, nullable=False)
    priority_level = Column(String, nullable=False)
    assigned_resources = Column(String, nullable=False)

# Function to initialize the database tables
def init_db():
    print("Connecting to Google Cloud SQL...")
    Base.metadata.create_all(bind=engine)
    print("Success! Database tables created.")

if __name__ == "__main__":
    init_db()