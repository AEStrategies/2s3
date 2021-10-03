# 2s3

Tools to copy local files to AWS S3 buckets.

## Setup

1. Create a python virtual environment:

```shell
python3 -m venv venv
```

2. Activate the virtual environment:

```shell
source ./venv/bin/activate
```

3. Install package requirements:

```shell
pip install -r requirements.txt
```

4. Configure AWS:

```{shell}
aws configure
```

Type the default region name (e.g., `us-east-1`). Type `json` as the default output format.

5. Verify connectivity:

```{shell}
python get-identity.py
```

Output should look something like this:

```{shell}
{
    "UserId": "XXXXXXXXXXXXXXXXX4AQN",
    "Account": "XXXXXXXXX350",
    "Arn": "arn:aws:iam::XXXXXXXXX350:user/tiffany.steward"
}
```

## Configure the bucket transfer

Create `bucket-transfer.ini` file in the same directory as `bucket-transfer.py`:

```{ini}
[bucket_transfer]
bucket = <YOUR REMOTE BUCKET>
object_prefix = <YOUR REMOTE OBJECT PREFIX>
local_directory = <YOUR LOCAL DIRECTORY>
dry_run = False
verbosity = info
```

Run the transfer (be sure the virtual environment is activated):

```{shell}
python ./bucket-transfer.py
```
