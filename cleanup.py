
import os
import os.path

from google.cloud import bigquery

credentials_path = os.path.join(
    os.environ["TRAVIS_BUILD_DIR"], "ci", "travis_gbq.json"
)

project_id = os.environ.get("GBQ_PROJECT_ID") or os.environ.get(
    "GOOGLE_CLOUD_PROJECT"
)

client = bigquery.Client.from_service_account_json(
    credentials_path, project=project_id
)

all_datasets = list(client.list_datasets())
for dataset in all_datasets:
    if 'pandas_gbq_' not in dataset.dataset_id:
        print('Skipping dataset {}'.format(dataset.dataset_id))
        continue
    client.delete_dataset(dataset.reference, delete_contents=True)
