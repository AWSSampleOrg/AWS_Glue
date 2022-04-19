CREATE EXTERNAL TABLE `sample_table`(
  `device_id` string,
  `uuid` bigint,
  `appid` bigint,
  `country` string,
  `year` int,
  `month` int,
  `date` int,
  `hour` int)
PARTITIONED BY (
  `partition_year` string)
ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET_NAME>/'
TBLPROPERTIES (
  'classification'='csv',
  'serialization.encoding'='UTF8',
  'skip.header.line.count'='1')
