# supermarket-datapipeline-s3-to-psql - developed with Docker

This data pipeline app shows a simple user profile app set up using 
- s3 as data lake
- load.py for etl to move the data to RDMS
- pgdatabase for data storage
- test.py for confirming the loading process was successful


All components are docker-based

### With Docker

#### To start the application

Step 1: start up the application in detached mode

    docker-compose -f docker-compose.yaml up -d

Step 2: open pgadmin and connect to the pgdatabase to see the content

Step 3: run test.py to confirm other python application can access the database content

    python3 test.py