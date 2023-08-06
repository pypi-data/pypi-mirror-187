#!/bin/bash
source ./mlops/setup_deploy_params.sh

YAML=./deploy/app-gcp_gae-devland.yaml

gcloud app deploy ${YAML} --image-url="${IMAGE_NAME}" --project="${PROJECT_ID}"
echo "${IMAGE_NAME}" > last_deployed_image.txt
