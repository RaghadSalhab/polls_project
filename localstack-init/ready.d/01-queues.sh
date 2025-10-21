#!/bin/bash
echo 'Setting up SQS queues...'
awslocal sqs create-queue --queue-name question-queue
awslocal sqs create-queue --queue-name question-dlq
awslocal sqs create-queue --queue-name choice-queue
awslocal sqs create-queue --queue-name choice-dlq
awslocal sqs create-queue --queue-name user-queue
awslocal sqs create-queue --queue-name user-dlq
awslocal sqs create-queue --queue-name stats-queue
awslocal sqs create-queue --queue-name stats-dlq
echo 'Queues created!'