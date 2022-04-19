# -*- encoding:utf-8 -*-
from asyncio.log import logger
from datetime import datetime, timedelta
import os
from logging import getLogger, StreamHandler, DEBUG
# third party
import athena

# logger setting
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(os.getenv("LOG_LEVEL", DEBUG))
logger.addHandler(handler)
logger.propagate = False

GLUE_DATABASE = os.environ["GLUE_DATABASE"]
GLUE_TABLE = os.environ["GLUE_TABLE"]
GLUE_TABLE_LOCATION = os.environ["GLUE_TABLE_LOCATION"]

def to_partition(year, month, date):
    return f'PARTITION (partition_year={f"{year:04}"}, partition_month={f"{month:02}"}, partition_date={f"{date:02}"})'

def chunk_list(l: list, step: int):
    return [l[i:i + step] for i in range(0, len(l), step)]

def revalidate_partitions():
    now = datetime.now()

    added_infos = {
        "partition": [],
        "location": [],
    }
    for d in range(30):
        n_dates_ago = (now - timedelta(days=d))
        added_infos["location"].append(f"{GLUE_TABLE_LOCATION}/{f'{n_dates_ago.year:04}'}/{f'{n_dates_ago.month:02}'}/{f'{n_dates_ago.day:02}'}")
        added_infos["partition"].append(to_partition(
            n_dates_ago.year, n_dates_ago.month, n_dates_ago.day
        ))
    added_partitions = set(added_infos["partition"])

    for records in athena.sync_query(athena.show_partitions_sql()):
        current_partitions = set([
            to_partition(
                *[ int(i.split("=")[1]) for i in record["partition"].split("/") ]
            ) for record in records
        ])
        need_to_be_dropped_partitions = list(current_partitions - added_partitions)
        if len(need_to_be_dropped_partitions):
            # This is a workaround to avoid the following error,
            # which should be an implicit specification of Athena from the Apache Hive,
            # divide the partition length shortly. Less than 20 would be almost successful.
            # FAILED: SemanticException [Error 10006]: Partition not found
            for partition in chunk_list(need_to_be_dropped_partitions, 20):
                athena.sync_execute_query(
                	athena.drop_partitions_sql(partition)
            	)

    if len(added_partitions):
        athena.sync_execute_query(
            athena.add_partitions_sql(list(added_partitions), added_infos["location"])
        )

def lambda_handler(event, context):
    revalidate_partitions()

    for records in athena.sync_query(f"SELECT * FROM {GLUE_DATABASE}.{GLUE_TABLE};"):
        logger.debug(records)
