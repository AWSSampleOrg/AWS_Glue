# -*- encoding: utf-8 -*-
from datetime import datetime,timedelta
import os
from athena import get_query_results, query, wait_for_query
from logger import logger

OUTPUT_LOCATION = os.environ["OUTPUT_LOCATION"]
GLUE_DATABASE = os.environ["GLUE_DATABASE"]
GLUE_TABLE = os.environ["GLUE_TABLE"]
GLUE_TABLE_LOCATION = os.environ["GLUE_TABLE_LOCATION"]



def to_partition(year):
    return f'PARTITION (partition_year="{year}")'


def show_partitions():
    query_execution_id = query(f"SHOW PARTITIONS {GLUE_DATABASE}.{GLUE_TABLE};")
    wait_for_query(query_execution_id)
    rows = get_query_results(
        query_execution_id
    )["ResultSet"]["Rows"]
    return [ to_partition(r["Data"][0]["VarCharValue"].split("=")[1] ) for r in rows ]

def drop_partitions(partitions):
    if not len(partitions): return
    wait_for_query(
        query(
            f"ALTER TABLE {GLUE_DATABASE}.{GLUE_TABLE} DROP IF EXISTS {', '.join(partitions) };"
        )
    )

def add_partitions(partitions):
    if not len(partitions): return
    wait_for_query(
        query(
        	f"""ALTER TABLE {GLUE_DATABASE}.{GLUE_TABLE} ADD IF NOT EXISTS {' '.join(
            	partitions
        	)} LOCATION '{GLUE_TABLE_LOCATION}';"""
    	)
    )

def revalidate_partition():
    now = datetime.now()

    current_partitions = set(show_partitions())
    logger.debug({"current_partitions": current_partitions})
    added_partitions = set([ to_partition( (now - timedelta(days=d)).strftime("%Y") ) for d in range(30)])

    drop_partitions(list(current_partitions - added_partitions))
    add_partitions(list(added_partitions))


def lambda_handler(event, context):
    revalidate_partition()
