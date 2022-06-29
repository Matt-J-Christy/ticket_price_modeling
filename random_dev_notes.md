# Random Dev Notes

## Docker

### Register with GCP

Link: 
[tutorial link](https://towardsdatascience.com/the-easiest-way-to-run-python-in-google-cloud-illustrated-d307c9e1651c)

Tag image: 

```{shell}
docker tag [IMAGE] gcr.io/[PROJECT-ID]/[IMAGE]

```

 Build & push the image:

```{shell}
docker build -t us-central1-docker.pkg.dev/ticket-model-app/ticket-models/ticket-app .

docker push us-central1-docker.pkg.dev/ticket-model-app/ticket-models/ticket-app
```

If you want to test different versions of a Dockerfile: 

```{shell}
docker build -f Dockerfile-test -t us-central1-docker.pkg.dev/ticket-model-app/ticket-models/ticket-app .
```

configure docker permissions:
`gcloud auth configure-docker `

## Work with DBs & writing data to storage bucket

https://docs.docker.com/get-started/05_persisting_data/

https://lemaizi.com/blog/dockerize-your-machine-learning-model-to-train-it-on-gcp/

### Python 

Write data to GCS Bucket 

```{python}

from google.cloud import storage


def upload_blob_from_memory(storage_client, bucket_name, df, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "ticket-data-dump"

    # The contents to upload to the file
    contents = df.to_csv(index=False)

    # The ID of your GCS object
    # destination_blob_name = "event_ids"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} with {df.shape[0]} event ids uploaded to {bucket_name}."
    )

```
Read from GCS Bucket

```{python}
with open('gcp_creds.json') as file:
    creds_dict = json.load(file)

creds = service_account.Credentials.from_service_account_info(creds_dict)

storage_client = storage.Client(credentials=creds)

event_id_table = f"event_ids_{today}.csv"

def read_from_gcs(storage_client, bucket_name, blob_name):

    bucket = storage_client.bucket(bucket_name)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    blob = bucket.blob(blob_name)

    output_table = pd.read_csv(StringIO(blob.open('r').read()), sep=',')

    return output_table

id_table = read_from_gcs(
    storage_client,
    'ticket-data-dump',
    event_id_table
)

```

### Setting up a job 

https://schedule.readthedocs.io/en/stable/examples.html#run-all-jobs-now-regardless-of-their-scheduling
