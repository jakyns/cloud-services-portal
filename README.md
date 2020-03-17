# Cloud Services Portal

Repository that try to gather several frequently used services from each 
cloud providers and make it simpler.

## Dependencies

- Python 3.7.x or higher
- [Pipfile](https://github.com/pypa/pipfile)

## Installation

Initiate virtual environment and generate Pipfile and Pipfile.lock by running:

```sh
pipenv lock
```

Install dependencies and get into virtual environment.

```sh
pipenv install && pipenv shell
```

## Usage

It might need to have credential files from each cloud provider to be set in
environment variable.

eg.

```
export GOOGLE_APPLICATION_CREDENTIALS=
```

### Storage

available for
- GCP Storage

```sh
>>> from services.storage import StorageService
>>> service = StorageService("GCP")
```

Set and get bucket

```sh
>>> service.set_bucket("bucket")
>>> service.get_bucket()
'bucket'
```

Upload

```sh
>>> service.request_upload("remote_path/file.txt", "local_path/file.txt")
```

Delete

```sh
>>> service.request_delete("remote_path/file.txt")
```

### Vision

available for
- GCP Vision API
