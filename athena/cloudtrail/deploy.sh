#!/usr/bin/env bash

SOURCE_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}) && pwd)
cd ${SOURCE_DIR}

PROFILE="default"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile ${PROFILE})
AWS_REGION=$(aws configure get region --profile ${PROFILE})


source_bucket_name="<S3_BUCKET_NAME>"

aws cloudformation deploy \
    --template-file template.yml \
    --stack-name athena \
    --parameter-overrides \
        SourceBucketName=${source_bucket_name} \
    --capabilities CAPABILITY_NAMED_IAM
