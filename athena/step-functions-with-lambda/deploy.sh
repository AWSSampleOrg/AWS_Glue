#!/usr/bin/env bash

SOURCE_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}) && pwd)
cd ${SOURCE_DIR}

PROFILE="default"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile ${PROFILE})
AWS_REGION=$(aws configure get region --profile ${PROFILE})


S3_BUCKET="your-bucket-name"
aws cloudformation package \
    --template-file template.yml \
    --s3-bucket ${S3_BUCKET} \
    --output-template-file packaged_template.yml

source_bucket_name="<S3_BUCKET_NAME>"

aws cloudformation deploy \
    --template-file packaged_template.yml \
    --stack-name athena \
    --parameter-overrides \
        SourceBucketName=${source_bucket_name} \
    --capabilities CAPABILITY_NAMED_IAM
