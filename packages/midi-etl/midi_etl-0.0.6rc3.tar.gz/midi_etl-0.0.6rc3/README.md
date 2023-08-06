# MIDI ETL

This repository contains an implementation of a modern data stack for building and analyzing MIDI datasets at scale. The stack is composed of several open source technologies, including DBT, Dagster, Trino, and Minio.

DBT (Data Build Tool) is used to transform and optimize MIDI data as it is ingested from various sources into a data warehouse. DBT scripts are used to clean and preprocess the data, extract relevant metadata, and load it into a staging table.

Dagster is used to define and execute data pipelines that fetch MIDI data from online sources using web scraping and API calls, and then load the data into the staging table in the data warehouse. It provides a framework for building, testing, and deploying these pipelines in a robust and scalable way.

Trino is used to analyze the MIDI datasets stored in the data warehouse. It provides a distributed SQL query engine that can handle complex queries and large volumes of data efficiently. This allows data analysts and scientists to extract insights and trends from the MIDI datasets.

Minio is used to store and retrieve the MIDI datasets and other data used in the stack. It is a lightweight, scalable object storage solution that can handle large volumes of data.

Overall, this data stack provides a powerful and scalable platform for building and analyzing MIDI datasets. It can be used by data engineers, data scientists, and data analysts to extract insights and trends from music data at scale.

## Prerequisites

Before you can use this repository, you will need to install the following:

- Docker : Follow the instructions at https://docs.docker.com/get-docker/ to install Docker on your machine.
- Docker Compose: follow the instructions at https://docs.docker.com/compose/install/ to install Docker Compose.

## Installation

You can install `midi_etl` using pip:

``` pip install midi_etl ```

## Usage

To use this repository, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone git@gitlab.com:nintorac-audio/midi_etl.git
```

2. Navigate to the repository directory:

```bash
cd midi_etl
```

3. Build and start the Docker containers:

```bash
docker-compose up --build
```

This will build the Docker containers for the etl platform and deploy all the infra needed to run the project

4. Navigate to [dagit](http://localhost:3000) to initiate jobs 

5. Download DBeaver (or your favourite DB IDE) to run queries over your data lake, navigate to [minio](http://localhost:9001) to review the files in your data lake or use pyarrow to load the dataset in python eg.

```python
# First, import the necessary libraries
import pyarrow as pa
import pyarrow.parquet as pq
import s3fs
import duckdb

# Connect to Minio using s3fs
fs = s3fs.S3FileSystem(
    anon=False,
    use_ssl=False,
    client_kwargs={
        "region_name": "us-east-1",
        "endpoint_url": "http://localhost:9000",
        "aws_access_key_id": "minio",
        "aws_secret_access_key": "minio123",
        "verify": False,
    }
)

# Create a Parquet dataset for the path "midi_etl/midi" in the "datasets" bucket
note_ons = pq.ParquetDataset("midi_etl/midi/note_ons", filesystem=fs).read()

# Open a connection to a DuckDB database
conn = duckdb.connect()

# Now you can run SQL queries on the table using the connection
cursor = conn.cursor()
cursor.execute("SELECT * FROM note_ons LIMIT 10")
print(cursor.fetchall())
```

### Makefile

`load_env` is a make target that exports variables from a .env file into your local shell

`get_trino_cli` is a make target that downloads the Trino command-line interface (CLI) from a URL. This is then mounted into the trino container to provide CLI Trino access. 
 
## Available Datasets

- [Lakh MIDI Dataset](https://colinraffel.com/projects/lmd/): The Lakh MIDI dataset is a collection of 176,581 MIDI files, 45,129 of which have been matched and aligned to entries in the Million Song Dataset, and is intended for use in large-scale music information retrieval


## License

This repository is licensed under the MIT license. See [LICENSE](LICENSE) for more information.

## Versioning

For now consider every version change a potentially breaking change. If I ever get around to adding tests
and such then I will add semantic versioning.
