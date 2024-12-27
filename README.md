# Overview

## Prerequisites
```bash
terraform init
terraform apply
```

## Lambda Package creation
```bash
# Add python package
pip3 install --target package pymysql
# Create lambda package
cd package
zip -r ../lambda_function.zip .
```
