# -*- encoding:utf-8 -*-
import sys
from awsglue.transforms import ApplyMapping, SelectFields, ResolveChoice
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from logging import getLogger, StreamHandler, DEBUG
import os

#logger setting
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(os.getenv("LOG_LEVEL", DEBUG))
logger.addHandler(handler)
logger.propagate = False

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'GLUE_DATABASE_NAME', 'SRC_GLUE_TABLE_NAME', 'DEST_GLUE_TABLE_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def main():
    datasource0 = glueContext.create_dynamic_frame.from_catalog(
        database = args['GLUE_DATABASE_NAME'],
        table_name = args['SRC_GLUE_TABLE_NAME'],
        transformation_ctx = "datasource0")

    applymapping1 = ApplyMapping.apply(
        frame = datasource0,
        mappings = [("端末id", "string", "device_id", "string"),
                    ("イベント日時", "bigint", "timestamp", "bigint"),
                    ("状態", "string", "status", "string")],
        transformation_ctx = "applymapping1")

    selectfields2 = SelectFields.apply(
        frame = applymapping1,
        paths = ["device_id", "timestamp", "status"],
        transformation_ctx = "selectfields2")

    resolvechoice3 = ResolveChoice.apply(
        frame = selectfields2,
        choice = "MATCH_CATALOG",
        database = args['GLUE_DATABASE_NAME'],
        table_name = args['DEST_GLUE_TABLE_NAME'],
        transformation_ctx = "resolvechoice3")

    glueContext.write_dynamic_frame.from_catalog(
        frame = resolvechoice3,
        database = args['GLUE_DATABASE_NAME'],
        table_name = args['DEST_GLUE_TABLE_NAME'],
        transformation_ctx = "datasink4")
    job.commit()

if __name__ == "__main__":
    main()
