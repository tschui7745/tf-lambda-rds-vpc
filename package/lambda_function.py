import sys
import logging
import pymysql
import json
import os

# rds settings
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
rds_endpoint = os.environ['RDS_ENDPOINT']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=rds_endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    logger.info(f"Event data: {event}")
    data = json.loads(event)
    Name = data['Name']

    item_count = 0
    sql_string = f"insert into Movie (Name) values(%s)"

    with conn.cursor() as cur:
        cur.execute("create table if not exists Movie ( MovieID  int NOT NULL AUTO_INCREMENT, Name varchar(255) NOT NULL, PRIMARY KEY (MovieID))")
        cur.execute(sql_string, (Name))
        conn.commit()
        cur.execute("select * from Movie")
        logger.info("The following items have been added to the database:")
        for row in cur:
            item_count += 1
            logger.info(row)
    conn.commit()

    return "Added %d items to RDS for MySQL table" %(item_count)
    