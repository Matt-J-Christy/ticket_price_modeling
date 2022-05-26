# Docker Notes

## Register with GCP

Link: 
[tutorial link](https://towardsdatascience.com/the-easiest-way-to-run-python-in-google-cloud-illustrated-d307c9e1651c)

Tag image: 

```{shell}
docker tag [IMAGE] gcr.io/[PROJECT-ID]/[IMAGE]

```

 Build & push the image:

```{shell}
docker build us-central1-docker.pkg.dev/ticket-model-app/ticket-models/ticket-app

docker push us-central1-docker.pkg.dev/ticket-model-app/ticket-models/ticket-app
```

configure docker permissions:
`gcloud auth configure-docker `

## Work with DBs & writing data to storage bucket

https://docs.docker.com/get-started/05_persisting_data/

https://lemaizi.com/blog/dockerize-your-machine-learning-model-to-train-it-on-gcp/


```{python}

from google.cloud import storage


def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
    )

```

