#!/bin/sh

curl --fail -dH -X POST "$(terraform output -raw cd_webhook)"