#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib
from tempfile import NamedTemporaryFile

from codemagic_cli_tools import cli

DEFAULT_BUCKET = 'secure.codemagic.io'


class StorageError(cli.CliAppException):
    pass


def _existing_path(path_str: str) -> pathlib.Path:
    path = pathlib.Path(path_str)
    if path.exists():
        return path
    raise argparse.ArgumentTypeError(f'Path "{path}" does not exist')


class StorageArgument(cli.Argument):
    BUCKET_NAME = cli.ArgumentProperties(
        key='bucket',
        flags=('--bucket',),
        argparse_kwargs={'default': DEFAULT_BUCKET, 'required': False},
        description='Name of the Cloud Storage bucket containing the object. For example, "my-bucket".',
    )
    OBJECT_NAME = cli.ArgumentProperties(
        key='object_name',
        description='Name of object you are interacting with. For example, "pets/dog.png".',
    )
    SAVE_TO_LOCATION = cli.ArgumentProperties(
        key='save_to_location',
        type=pathlib.Path,
        description='Local path where you are saving your object. For example, "Desktop/Images".',
    )


@cli.common_arguments(StorageArgument.BUCKET_NAME)
class Storage(cli.CliApp):
    """
    Utility to download files from Google Cloud Storage
    """

    def __init__(self, bucket_name: str = DEFAULT_BUCKET, **kwargs):
        super().__init__(**kwargs)
        self.bucket_name = bucket_name

    @classmethod
    def from_cli_args(cls, cli_args: argparse.Namespace) -> Storage:
        default_bucket = StorageArgument.BUCKET_NAME.get_default()
        bucket_name = StorageArgument.BUCKET_NAME.from_args(cli_args, default_bucket)
        return Storage(bucket_name, **cls._parent_class_kwargs(cli_args))

    @cli.action('save-to-file',
                StorageArgument.OBJECT_NAME,
                StorageArgument.SAVE_TO_LOCATION)
    def save_to_file(self, object_name: str, save_to_location: pathlib.Path) -> pathlib.Path:
        """
        Save specified object from Cloud Storage bucket to local disk
        """
        process = self.execute(
            ['gsutil', 'cp', f'gs://{self.bucket_name}/{object_name}', save_to_location], show_output=False)
        if process.returncode != 0:
            error = f'Unable to save file: "{object_name}" does not exist in bucket "{self.bucket_name}"'
            raise StorageError(error, process)
        return save_to_location

    @cli.action('show-contents', StorageArgument.OBJECT_NAME)
    def show_contents(self, object_name) -> str:
        """
        Print contents of specified object from Cloud Storage bucket to STDOUT
        """
        with NamedTemporaryFile() as tf:
            process = self.execute(
                ['gsutil', 'cp', f'gs://{self.bucket_name}/{object_name}', tf.name], show_output=False)
            if process.returncode != 0:
                error = f'Unable to show contents: "{object_name}" does not exist in bucket "{self.bucket_name}"'
                raise StorageError(error, process)
            contents = open(tf.name).read()
            print(contents)
        return contents


if __name__ == '__main__':
    Storage.invoke_cli()
