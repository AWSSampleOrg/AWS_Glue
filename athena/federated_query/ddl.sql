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
  `partition_year` int,
  `partition_month` int,
  `partition_date` int)
ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET_NAME>/input'
TBLPROPERTIES (
  'classification'='csv',
  'serialization.encoding'='UTF8',
  'skip.header.line.count'='1')
