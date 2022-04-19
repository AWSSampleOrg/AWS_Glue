# -*- encoding:utf-8 -*-
import boto3
import sys
import uuid
from awsglue.utils import getResolvedOptions
from logging import getLogger, StreamHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL
import os

#logger setting
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(os.getenv("LOG_LEVEL", DEBUG))
logger.addHandler(handler)
logger.propagate = False


args = getResolvedOptions(sys.argv, ['BUCKET_NAME', 'SRC_OBJECT_KEY', 'SRC_FILE_ENCODING', 'DEST_OBJECT_PREFIX'])


s3 = boto3.resource('s3')

def main():
    src_obj = s3.Object(args['BUCKET_NAME'], args['SRC_OBJECT_KEY'])
    body = src_obj.get()['Body'].read().decode(args['SRC_FILE_ENCODING'])


    dest_obj_file_name = str(uuid.uuid4())
    dest_obj = s3.Object(args['BUCKET_NAME'], args['DEST_OBJECT_PREFIX'] + '/' + dest_obj_file_name)
    dest_obj.put(Body = body)


    src_obj.delete()



if __name__ == "__main__":
    main()
