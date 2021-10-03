#!/usr/bin/env python3
import argparse
import logging
import os
from configparser import ConfigParser

import boto3


class BucketTransfer:
    def __init__(self, bucket, dry_run_=False):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket
        self.dry_run = dry_run_

    def upload_file(self, file_name, object_name=None, args_=None):
        if object_name is None:
            object_name = file_name
        if not self.dry_run:
            self.s3_client.upload_file(file_name, self.bucket, object_name, ExtraArgs=args_)
        logging.info(f"'{file_name}' successfully uploaded to '{self.bucket}' as '{object_name}'")

    def upload_directory(self, local_directory, prefix, args_=None):
        logging.info(f"uploading files from `{local_directory}`")
        for root, dirs, files in os.walk(local_directory):
            nested_dir = root.replace(local_directory, '')
            if nested_dir:
                nested_dir = nested_dir.replace('/', '', 1) + '/'
            for file in files:
                complete_file_path = os.path.join(root, file)
                file = nested_dir + file if nested_dir else file
                file = f"{prefix}/{file}".replace('\\', '/').replace("//", "/")
                logging.info(f"uploading '{complete_file_path}' to '{self.bucket}' as '{file}'")
                self.upload_file(complete_file_path, file, args_)


if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=argparse.FileType("r"),
        dest="configfile",
        default="bucket-transfer.ini",
        help="The config file to use",
    )
    args = parser.parse_args()

    # instantiate config parser
    config = ConfigParser(interpolation=None)

    # parse config file
    config.read_file(args.configfile)

    bucket_transfer_config = {}
    config_section = "bucket_transfer"
    if not config.has_section(config_section):
        raise RuntimeError(
            f"ERROR: Config file {args.configfile} missing required {config_section} section"
        )
    for required_option in ["bucket", "object_prefix", "local_directory"]:
        if not config.has_option(config_section, required_option):
            raise RuntimeError(
                f"ERROR: Config file {args.configfile} missing {required_option} in the {config_section} section"
            )
        else:
            bucket_transfer_config[required_option] = config.get(config_section, required_option)

    dry_run = False
    if config.has_option(config_section, "dry_run"):
        dry_run = config.getboolean(config_section, "dry_run")

    if config.has_option(config_section, "verbosity"):
        verbosity = config.get(config_section, "verbosity").lower().strip()
        if verbosity == "info":
            logging.basicConfig(level=logging.INFO)
        elif verbosity == "debug":
            logging.basicConfig(level=logging.DEBUG)

    bucket_transfer = BucketTransfer(bucket_transfer_config["bucket"], dry_run)
    bucket_transfer.upload_directory(bucket_transfer_config["local_directory"], bucket_transfer_config["object_prefix"])
