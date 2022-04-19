1. replace the "source_bucket_name" to yours
2. ./deploy.sh
3. Add partition

```sql
MSCK REPAIR TABLE sample_table;
```

or

replace "yyyy" to yours

```sql
ALTER TABLE sample_table ADD PARTITION (partition_year='yyyy') LOCATION 's3://<S3_BUCKET_NAME>/';
```
