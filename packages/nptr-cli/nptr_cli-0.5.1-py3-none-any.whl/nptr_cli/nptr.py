#!/usr/bin/env python3
import argparse
import json
import os
import sys
import warnings
from pathlib import Path
from typing import Optional
from urllib import parse

import _io
import appdirs
import requests
import tomli
import validators
from requests.auth import HTTPBasicAuth


def raise_for_status(response: requests.Response):
    """A wrapper for the :py:meth:`~requests.Response.raise_for_status` method.

    Also prints the response body, to better understand the error.

    Args:
        response (requests.Response): response to raise status for.
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as he:
        print(response.content)
        raise he


class NullPointer:
    """The NullPointer class to abstract away 0x0 API."""

    def __init__(
        self,
        instance_url: str = "https://0x0.st",
        username: Optional[str] = None,
        password: Optional[str] = None,
        log_dir: Optional[Path] = None,
    ):
        """Initialize NullPointer with an instance_url.

        Args:
            instance_url (str): the 0x0 instance
                defaults to 'https://0x0.st'.
            username (Optional[str]): basic auth username
            password (Optional[str]): basic auth password
        """
        self.instance_url = instance_url
        self.instance_domain = parse.urlparse(self.instance_url)[1]
        if username is not None and password is not None:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = None
        self.log_dir = log_dir

        if self.log_dir is not None:
            self.log_dir = Path(self.log_dir).joinpath(self.instance_domain)
            self.log_dir.mkdir(exist_ok=True)

    def upload(self, file: bytes, filename: str = "file", secret: bool = True):
        """Upload a file to a 0x0 instance.

        Args:
            file (bytes): the bytes content of the file to upload
            secret (bool): sets the secret flag for 0x0
                which makes the path of the returned url longer and
                more unguessable

        Raises:
            :py:class:`~requests.HTTPError`

        Returns:
            dict:
                `url` is the returned content, which should be the url.
                `expires` is the X-Expires header which returns
                the expiration time of the file submitted
                or no-expires, when the header did not exist
                `token` is the X-Token header
                with this token you are able to delete the file later on
                or no-token when the header did not exist
                which usually means that a file
                with the same content was already uploaded
        """
        upload_response = requests.post(
            self.instance_url,
            data={"secret": ""} if secret else None,
            files={"file": (filename, file)},
            auth=self.auth,
        )
        raise_for_status(upload_response)
        response = {
            "url": upload_response.content.decode("UTF-8").strip(),
            "expires": upload_response.headers.get("X-Expires", "no-expires"),
            "token": upload_response.headers.get("X-Token", "no-token"),
        }
        if self.log_dir is not None:
            id = response["url"].split("/")[-1].split(".")[0]
            id_file = self.log_dir.joinpath(id)
            if id_file.exists():
                with open(str(id_file), "r") as id_fd:
                    id_json = json.load(id_fd)
                    if response["token"] == "no-token":
                        response["token"] = id_json["token"]

            with open(str(id_file), "w+") as log_file:
                log_file.write(json.dumps(response))

        return response

    def delete(self, url: str, token: str):
        """Delete a file from 0x0.

        Args:
            url (str): the url for the file to delete
            token (str): the token that was returned
                via the X-Token header when the file
                was created
        Raises:
            :py:class:`~requests.HTTPError`

        Returns:
            bool:
                true for success
                false for failure
        """
        if self.log_dir is not None:
            if validators.url(url):
                id = url.split("/")[-1].split(".")[0]
                id_file = self.log_dir / id
            else:
                id_file = self.log_dir / url
            if id_file.exists():
                with open(str(id_file), "r") as id_fd:
                    id_json = json.load(id_fd)
                    url = id_json["url"]
                    if id_json["token"] != "no-token":
                        token = id_json["token"]
        if token is None:
            return False

        delete_response = requests.post(
            url, data={"token": token, "delete": ""}, auth=self.auth
        )
        if delete_response.status_code == 404:
            return False
        raise_for_status(delete_response)
        if id_file:
            id_file.unlink(missing_ok=True)
        return True


class CLI:
    @staticmethod
    def upload(args: argparse.Namespace, args_help):
        """CLI wrapper for the upload method.

        Args:
            args (argparse.Namespace): the args parsed by argparse
            args_help: the print_help function from the argparse parser
        """
        # stdin is normally in text mode, but the underlying buffer is in binary mode
        file = args.file
        filename = (
            Path(file.name).name if isinstance(file, _io.TextIOWrapper) else "file"
        )
        input = file.buffer.read()
        if len(input) == 0:
            args_help()
            exit(1)
        npu = NullPointer(
            args.instance,
            args.username if "username" in args else None,
            args.password if "password" in args else None,
            args.logdir if not args.no_log else None,
        )
        response = npu.upload(input, filename, args.secret)
        print(response["url"])
        if not args.quiet:
            print("Expires: " + str(response["expires"]))
            print("Token: " + str(response["token"]))

    @staticmethod
    def delete(args, args_help):
        """CLI wrapper for the delete method.

        Args:
            args (argparse.Namespace): the args parsed by argparse
            args_help: the print_help function from the argparse parser
        """
        npu = NullPointer(
            args.instance,
            args.username if "username" in args else None,
            args.password if "password" in args else None,
            args.logdir if not args.no_log else None,
        )
        if npu.delete(args.url, args.token):
            print(f"Successfully deleted {args.url}")
        else:
            print(f"Deleting {args.url} failed")
            exit(1)

    @staticmethod
    def parse_config(
        file: str = Path(appdirs.user_config_dir(appname="0x0")).joinpath(
            "config.toml"
        ),
    ) -> dict:
        """Parses the config file to override defaults."""
        if os.path.isfile(file):
            try:
                with open(file, "rb") as confd:
                    config = tomli.load(confd)
                if config:
                    return config
                else:
                    return {}
            except IOError as ie:
                warnings.warn(ie.strerror)
                return {}
        else:
            return {}

    @staticmethod
    def parse_args():
        """Parses the args with argparse."""
        config = CLI.parse_config()

        parser = argparse.ArgumentParser(description="Upload/Delete on 0x0.st")
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="The expires time and the token will not be printed."
            "Useful for scripts",
            default=config.get("quiet", False),
        )
        parser.add_argument(
            "-i",
            "--instance",
            type=str,
            help="Alias or URL of the 0x0 instance, the default is 0x0",
            default=config.get("default_instance", "https://0x0.st"),
        )
        parser.add_argument(
            "-l",
            "--logdir",
            type=argparse_directory,
            help="Directory to keep track of the urls,"
            "tokens and expiry times of the stuff you upload."
            f"(default is {Path(appdirs.user_data_dir(appname='0x0'))})",
            default=argparse_directory(
                config.get("logdir", appdirs.user_data_dir(appname="0x0"))
            ),
        )
        parser.add_argument(
            "-n",
            "--no-log",
            action="store_true",
            help="Disables logging for this upload.",
            default=config.get("no_logging", False),
        )
        subparsers = parser.add_subparsers(title="Sub-Command", required=os.isatty(0))

        upload_parser = subparsers.add_parser(
            "upload", aliases=["u", "up"], help="Upload a file or read from stdin."
        )
        upload_parser.add_argument(
            "-s",
            "--secret",
            action="store_true",
            help="Make link more obscure and unguessable.",
            default=config.get("secret", False),
        )
        upload_parser.add_argument(
            "file",
            nargs="?",
            type=argparse.FileType("r"),
            default=sys.stdin,
            help="File to upload, if none is provided, read from stdin.",
        )
        upload_parser.set_defaults(func=CLI.upload)

        delete_parser = subparsers.add_parser(
            "delete", aliases=["d", "del"], help="Delete files from 0x0.st."
        )

        delete_parser.add_argument(
            "url", type=str, help="The url where the file to be deleted is located."
        )
        delete_parser.add_argument(
            "token",
            type=str,
            help="The token, which was sent back as header X-Token on upload.",
            default=None,
            nargs="?",
        )
        delete_parser.set_defaults(func=CLI.delete)

        if not os.isatty(0):
            parser.set_defaults(
                func=CLI.upload, file=sys.stdin, secret=config.get("secret", False)
            )
        args = parser.parse_args()
        # Check if instance is not the default instance or a valid url
        if args.instance != "https://0x0.st" and not validators.url(args.instance):
            # check if user has instances configured in his config
            if instances := config.get("instances"):
                # check if instance alias exists in his config
                if instance := instances.get(args.instance):
                    args.username = instance.get("username")
                    args.password = instance.get("password")
                    args.instance = instance.get("url")
                    # if all is set, return early
                    # to write a general error message below
                    return (args, parser)

            print(f"{args.instance} is not a valid instance")
            exit(1)

        return (args, parser)


def argparse_directory(dir):
    os.makedirs(dir, exist_ok=True)
    return Path(dir)


def run():
    args, parser = CLI.parse_args()
    args.func(args, parser.print_help)


if __name__ == "__main__":
    run()
