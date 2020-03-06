#!/bin/bash

AWS_ACCESS_KEY_ID=AKIA5PV4VQIY4HJLNP4B
AWS_SECRET_ACCESS_KEY=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
requirements="mozilla-taar3==0.4.8 mozilla-srgutil==0.2.1 python-decouple==3.1 click==7.0 boto3==1.7.71 dockerflow==2018.4.0"

gcloud beta dataproc clusters create jupyter-ensemble-broken-${RANDOM} \
    --bucket jupyter-ensemble \
    --enable-component-gateway \
    --image-version=1.4 \
    --initialization-actions gs://dataproc-initialization-actions/python/pip-install.sh \
    --max-idle 10m \
    --metadata "PIP_PACKAGES=${requirements}" \
    --optional-components=ANACONDA,JUPYTER \
    --project moz-fx-data-bq-srg \
    --properties "spark:spark.jars=gs://spark-lib/bigquery/spark-bigquery-latest.jar#spark:spark.hadoop.fs.s3a.access.key=${AWS_ACCESS_KEY_ID}#spark:spark.hadoop.fs.s3a.secret.key=${AWS_SECRET_ACCESS_KEY}#spark:spark.python.profile=true" \
    --region us-west1 
