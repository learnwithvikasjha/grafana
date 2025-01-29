# Run Grafana and Postgresql
Create a file called `docker-compose.yaml` and add the below content to run Grafana and PostgreSQL

```
services:
  postgres:
    image: postgres:16
    container_name: postgres
    environment:
      POSTGRES_USER: grafana
      POSTGRES_PASSWORD: grafana123
      POSTGRES_DB: grafana
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - grafana-net

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_DATABASE_TYPE=postgres
      - GF_DATABASE_HOST=postgres:5432
      - GF_DATABASE_NAME=grafana
      - GF_DATABASE_USER=grafana
      - GF_DATABASE_PASSWORD=grafana123
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - postgres
    networks:
      - grafana-net

volumes:
  postgres_data:
  grafana_data:

networks:
  grafana-net:
```

## Commands to manage Grafana and Postgresql
To start the services:
```
docker-compose up -d
```
To stop the services:
```
docker-compose down
```

## Grafana will be accessible at

```
http://localhost:3000/login
```


# Creating python program to generate fake data and insert in the database

- Create a python virtual environment
```
python3 -m venv venv
```
- Activate the environment by running this command
```
source venv/bin/activate
```

- Install required library by running below command

```
pip install -r requirements.txt
```

- create a file called `requirements.txt`
```
psycopg2==2.9.8
faker==18.9.0
```

- create a file called `generate_data.py`
# Python program to generate the fake data and insert in the postgredsql

```
import psycopg2
import random
import logging
from faker import Faker
from datetime import datetime, timedelta

# Database connection details
DB_HOST = "localhost"
DB_NAME = "grafana"
DB_USER = "grafana"
DB_PASSWORD = "grafana123"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fixed list of 50 participants
PARTICIPANT_NAMES = [
    "Tony Campbell", "Jennifer Humphrey", "Michelle Flores PhD", "Alyssa Ramos", "Jeanette Davis",
    "David Campbell", "Jaclyn Castillo", "Craig Craig", "Mrs. Joyce Diaz", "Wendy Anderson", "Ronald Hamilton",
    "Donald Kidd", "Todd Hale", "Lisa Smith", "John Doe", "Jane Doe", "Michael Brown", "Sarah Johnson",
    "William Harris", "Emily Clark", "Chris Lewis", "Patricia Walker", "Linda Hall", "Joseph Allen",
    "Nancy Young", "Steven Martinez", "Carol King", "Daniel Lee", "Barbara Walker", "Matthew Adams",
    "Richard Scott", "Helen Baker", "Andrew Gonzalez", "Laura Perez", "Brian Young", "Rachel Hill",
    "Gary White", "Deborah Moore", "George King", "Jessica Walker", "Steven Lee", "Mark Hall",
    "Susan Adams", "Charles Harris", "Marie Gonzalez", "Tom Perez", "Elizabeth Evans", "James Lee",
    "David Nelson", "Alice Carter", "Mark Martinez", "Helen Clark", "John King"
]

# States for pending and final states
PENDING_STATES = ["RECEIVED", "VALIDATED", "RESERVED", "ACKNOWLEDGED", "CONFIRMED"]
FINAL_STATES = ["INVALID", "COMMITTED", "ABORTED"]

# Initialize Faker instance
fake = Faker()

# Function to create a connection to the database
def create_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("Database connection established.")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return None

# Function to create tables if they don't exist
def create_tables():
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Create participants table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                balance INT NOT NULL
            );
        """)

        # Create transfers table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transfers (
                id SERIAL PRIMARY KEY,
                participant_id INT NOT NULL,
                state VARCHAR(50) NOT NULL,
                amount INT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                FOREIGN KEY (participant_id) REFERENCES participants(id)
            );
        """)

        connection.commit()
        logger.info("Tables created (if they didn't exist).")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Function to insert a new participant into the participants table
def insert_participant(name, balance):
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Check if participant already exists
        cursor.execute("SELECT id FROM participants WHERE name = %s", (name,))
        existing_participant = cursor.fetchone()
        if existing_participant:
            logger.info(f"Participant {name} already exists, skipping insert.")
            return  # Skip insertion if participant already exists

        query = "INSERT INTO participants (name, balance) VALUES (%s, %s)"
        cursor.execute(query, (name, balance))
        connection.commit()
        logger.info(f"Participant {name} inserted with balance {balance}.")
    except Exception as e:
        logger.error(f"Error inserting participant {name}: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Function to insert a new transfer into the transfers table
def insert_transfer(participant_id, state, amount, created_at, updated_at):
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO transfers (participant_id, state, amount, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (participant_id, state, amount, created_at, updated_at))
        connection.commit()
        logger.info(f"Transfer inserted for participant {participant_id} with state {state} and amount {amount}.")
    except Exception as e:
        logger.error(f"Error inserting transfer for participant {participant_id}: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Function to generate transfer data for existing participants
def generate_transfer_data():
    # Fetch participant ids from the database
    connection = create_connection()
    if not connection:
        return []

    cursor = connection.cursor()
    cursor.execute("SELECT id FROM participants;")
    participant_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    # Generate fake transfer data for each participant
    transfers = []
    for participant_id in participant_ids:
        state = random.choice(PENDING_STATES)
        amount = random.randint(50, 1000)  # Random transfer amount
        created_at = fake.date_this_decade()  # Random creation date
        updated_at = created_at + timedelta(days=random.randint(1, 30))  # Random updated date
        transfers.append((participant_id, state, amount, created_at, updated_at))

    return transfers

# Function to generate fake data for participants and transfers
def generate_fake_data():
    # Insert fixed participants (only if they don't already exist)
    for name in PARTICIPANT_NAMES:
        balance = random.randint(1000, 10000)  # Random initial balance
        insert_participant(name, balance)

    # Generate and insert transfer data for existing participants
    transfers = generate_transfer_data()
    for transfer in transfers:
        insert_transfer(*transfer)

    logger.info("Fake data generation complete.")

# Main function to start the data generation
def main():
    # Ensure tables exist before inserting data
    create_tables()
    # Generate and insert fake data
    generate_fake_data()

if __name__ == "__main__":
    main()
```

# Scheduling the python program to generate data and insert in the database every 5 minutes
- schedule the file to run every 5 minutes by scheduling it in the cronjob
```
*/5 * * * * /root/grafana/venv/bin/python /root/grafana/generate_data.py >> /root/grafana/data_generator.log 2>&1
```
