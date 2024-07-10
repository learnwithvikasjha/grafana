# High level steps to create Grafana Dashboard using Amazon Timestream Database
- Create a database in Timestream
- Create a table in Timestream
- Insert some data to the table. Data should have **Dimensions** and **Measures**
- Create a user in AWS IAM and give that user access to read and write to timestream database. You can attach below inline policy in the newly created user:
-
```
  {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"timestream:DescribeEndpoints",
				"timestream:WriteRecords",
				"timestream:CreateTable",
				"timestream:DescribeTable",
				"timestream:ListTables",
				"timestream:UpdateTable",
				"timestream:DeleteTable",
				"timestream:DescribeDatabase",
				"timestream:ListDatabases",
				"timestream:CreateDatabase",
				"timestream:DeleteDatabase"
			],
			"Resource": "*"
		}
	]
}

```

### Python program to insert random weather data to timestream

```
import boto3
import time
import random

# Replace with your actual AWS access key and secret key
AWS_ACCESS_KEY_ID = 'aws-access-key'
AWS_SECRET_ACCESS_KEY = 'aws-secret'
AWS_REGION = 'us-east-1'

# Initialize Timestream write client with explicit credentials
client = boto3.client(
    'timestream-write',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


# Function to create a record
def create_record(country, temperature, timestamp):
    return {
        'Dimensions': [
            {'Name': 'country', 'Value': country}
        ],
        'MeasureName': 'temperature',
        'MeasureValue': str(temperature),
        'MeasureValueType': 'DOUBLE',
        'Time': timestamp
    }

# List of countries for generating random data
countries = ['USA', 'Canada', 'India', 'UK', 'Germany']

# Function to generate random temperature
def generate_random_temperature():
    return round(random.uniform(-10, 40), 2)

# Continuously insert data every second
while True:
    # Prepare data
    records = []
    timestamp = str(int(time.time() * 1000))
    for country in countries:
        temperature = generate_random_temperature()
        records.append(create_record(country, temperature, timestamp))
    
    # Write records to Timestream
    try:
        response = client.write_records(
            DatabaseName='weatherDB',
            TableName='tempratureq2',
            Records=records
        )
        print(f"Inserted records at {time.ctime()}")
    except Exception as e:
        print(f"Error inserting records: {e}")
    
    # Sleep for 1 second
    time.sleep(1)
```
