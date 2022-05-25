# Docker Notes

## Register with GCP

Link: 
https://support.terra.bio/hc/en-us/articles/360035638032-Publish-a-Docker-container-image-to-Google-Container-Registry-GCR-

Tag image: 

```{shell}
docker tag [IMAGE] gcr.io/[PROJECT-ID]/[IMAGE]

docker tage ticket-app gcr.io[PROJECT-ID]/[ticket-app]
```

Push the image:

```{shell}
docker push gcr.io/[PROJECT-ID]/[ticket-app]

```

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


def download_byte_range(
    bucket_name, source_blob_name, start_byte, end_byte, destination_file_name
):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The starting byte at which to begin the download
    # start_byte = 0

    # The ending byte at which to end the download
    # end_byte = 20

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name, start=start_byte, end=end_byte)

    print(
        "Downloaded bytes {} to {} of object {} from bucket {} to local file {}.".format(
            start_byte, end_byte, source_blob_name, bucket_name, destination_file_name
        )
    )

```

