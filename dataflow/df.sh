python apache_beam_pub_sub_to_bq.py \
    --input_topic=projects/securityofthings/topics/device-only \
    --output_path=gs://pub_sub_temp/temp/ \
    --input_subscription=projects/securityofthings/subscriptions/sot-subscription \
    --experiments=allow_non_updatable_job