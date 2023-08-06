# Data Lake Utility
Package to manipulate data from/into Amazon S3 using partitions compatible with Apache Hadoop filesystem.
At this moment, this package was conceived to handle JSON and Parquet formats. That being said, it expects a Pandas DataFrame.

Data will be written into Amazon S3 as a multi-line JSON or Apache Parquet, compressed as GZIP.
## Features
Convert list of dictionaries...
```python
[
    {"brand": "Ford","model": "Mustang","year": 1965},
    {"brand": "Pontiac","model": "GTO","year": 1964},
    {"brand": "Lamborghini","model": "Miura","year": 1966}
]
```
...to multi-line JSON compressed as GZIP
```text
{"brand": "Ford","model": "Mustang","year": 1965}
{"brand": "Pontiac","model": "GTO","year": 1964}
{"brand": "Lamborghini","model": "Miura","year": 1966}
```

...or to Apache Parquet compressed as GZIP


## How to use
This package does not slice data into partitions at the moment. You must handle slicing of data to write into partitions desired.

Check this example below:
```python
from datalake_utils.utils import DataLake
import pandas

data = [
    {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1965
    },
    {
        "brand": "Pontiac",
        "model": "GTO",
        "year": 1964
    },
    {
        "brand": "Lamborghini",
        "model": "Miura",
        "year": 1966
    }
]

datalake = DataLake(
    bucket_name="vehicles",
    schema="motor_vehicles",
    table="cars",
    partitions=[
        {
            "key": "decade",
            "value": "1960s"
        }
    ],
)

datalake.append_to_s3(data=pandas.DataFrame(data), file_format="json")
```

It will create an object into Amazon S3 with the following structure:
```
motor_vehicles/
`-- cars/
    `-- decade=1960s/
        `-- 2c0fea6c-444e-11ed-969f-acde48001122.json.gz
```

To read all files from partition, do:
```python
retrieved_data = datalake.read_from_s3(file_format="json")
```
`retrieved_data` is a Pandas DataFrame object. It is not possible to read a specific file using this function.


To delete all files from partition, do:
```python
datalake.delete_from_s3()
```