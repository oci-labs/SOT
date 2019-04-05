gcloud dataflow jobs run JOB_NAME \
    --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery \
    --parameters \
inputTopic=projects/securityofthings/topics/sot-topic,\
outputTableSpec=securityofthings:security_dataset.sot_table