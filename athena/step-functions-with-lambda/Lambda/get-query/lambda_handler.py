# -*- encoding: utf-8 -*-
import os

def lambda_handler(event, context):
    GLUE_DATABASE = os.environ["GLUE_DATABASE"]
    GLUE_TABLE = os.environ["GLUE_TABLE"]
    OUTPUT_LOCATION = os.environ["OUTPUT_LOCATION"]

    with open("./query.sql") as fp:
        sql = fp.read().replace("%DATABASE%", GLUE_DATABASE).replace("%TABLE%", GLUE_TABLE)

    return { "queryString": sql, "outputLocation": OUTPUT_LOCATION }
