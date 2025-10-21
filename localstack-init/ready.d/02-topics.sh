#!/bin/bash
echo 'Setting up SNS topics...'
awslocal sns create-topic --name question-topic
awslocal sns create-topic --name choice-topic
awslocal sns create-topic --name user-topic
awslocal sns create-topic --name stats-topic
echo 'Topics created!'