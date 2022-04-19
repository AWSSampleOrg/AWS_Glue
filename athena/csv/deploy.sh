#!/usr/bin/env bash

SOURCE_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}) && pwd)
cd ${SOURCE_DIR}

PROFILE="default"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile ${PROFILE})
AWS_REGION=$(aws configure get region --profile ${PROFILE})


function main() {
    source_bucket_name="<S3_BUCKET_NAME>"

    aws cloudformation deploy \
        --template-file template.yml \
        --stack-name athena \
        --parameter-overrides \
            SourceBucketName=${source_bucket_name} \
        --capabilities CAPABILITY_NAMED_IAM

    if [ $? -ne 0 ] ; then
        return $?
    fi

    aws s3 cp ${SOURCE_DIR}/data.csv s3://${source_bucket_name}/partition_year=$(date +"%Y")/data.csv
    return $?
}

main
