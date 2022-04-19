CREATE EXTERNAL TABLE `sample_table`(
  `device_id` string COMMENT 'from deserializer',
  `uuid` bigint COMMENT 'from deserializer',
  `appid` bigint COMMENT 'from deserializer',
  `country` string COMMENT 'from deserializer',
  `year` int COMMENT 'from deserializer',
  `month` int COMMENT 'from deserializer',
  `date` int COMMENT 'from deserializer',
  `hour` int COMMENT 'from deserializer')
PARTITIONED BY (
  `partition_year` string)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'paths'='device_id, uuid, appid, country, year, month, date, hour')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET_NAME>/'
TBLPROPERTIES (
  'serialization.encoding'='UTF8')
