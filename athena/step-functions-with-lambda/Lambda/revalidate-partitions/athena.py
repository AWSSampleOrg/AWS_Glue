# -*- encoding:utf-8 -*-
import os
import time
from logger import logger
import boto3

athena = boto3.client("athena")

OUTPUT_LOCATION = os.environ["OUTPUT_LOCATION"]
GLUE_DATABASE = os.environ["GLUE_DATABASE"]

class QueryFailedException(Exception):
    """
    when The Query fails to finish , This Exception class called
    """
    pass


def wait_for_query(query_execution_id):
    while True:
        query_execution_status = get_query_execution(query_execution_id)
        logger.debug({ "query_execution_status":  query_execution_status })
        if query_execution_status == "SUCCEEDED":
            break
        elif query_execution_status == "FAILED" or query_execution_status == "CANCELLED":
            raise QueryFailedException(f"query_execution_status = {query_execution_status}")
        else:
            time.sleep(10)

def get_query_execution(query_execution_id):
    return athena.get_query_execution(
        QueryExecutionId = query_execution_id
    )['QueryExecution']['Status']['State']


def query(sql):
    logger.debug({"sql": sql})
    query_execution_id = athena.start_query_execution(
        QueryString = sql,
        QueryExecutionContext={
            "Database": GLUE_DATABASE
        },
        ResultConfiguration={
            "OutputLocation" : OUTPUT_LOCATION
        }
    )["QueryExecutionId"]
    logger.debug({"query_execution_id": query_execution_id})
    return query_execution_id

def get_query_results(query_execution_id):
    return athena.get_query_results(
        QueryExecutionId = query_execution_id
    )
