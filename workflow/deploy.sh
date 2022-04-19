#!/usr/bin/env bash

function main() {
    aws cloudformation deploy \
        --template-file template.yml \
        --stack-name devices-data-analytics-stack \
        --capabilities CAPABILITY_NAMED_IAM \
        --no-fail-on-empty-changeset

    if [ $? -ne 0 ] ; then
        return $?
    fi

    PROFILE="default"
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile ${PROFILE})
    AWS_REGION=$(aws configure get region --profile ${PROFILE})


    aws s3 cp devices-etl.py \
        s3://devices-data-analytics-${ACCOUNT_ID}-${AWS_REGION}/glue-job-script/devices-etl.py
    aws s3 cp devices-sjis-to-utf8.py \
        s3://devices-data-analytics-${ACCOUNT_ID}-${AWS_REGION}/glue-job-script/devices-sjis-to-utf8.py

    # data
    iconv -f utf8 -t sjis raw-utf8-data.csv > raw-sjis-data.csv
    # aws s3 cp raw-sjis-data.csv s3://devices-raw-data-${ACCOUNT_ID}-${AWS_REGION}/sjis-data/raw-sjis-data.csv

    return 0
}

main
