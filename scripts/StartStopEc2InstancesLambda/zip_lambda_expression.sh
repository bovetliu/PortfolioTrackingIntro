#!/usr/bin/env bash

zip -r ../StartStopEc2InstancesLambdaContent.zip ./* -x "zip_lambda_expression.sh" -x "install_dependency.sh"