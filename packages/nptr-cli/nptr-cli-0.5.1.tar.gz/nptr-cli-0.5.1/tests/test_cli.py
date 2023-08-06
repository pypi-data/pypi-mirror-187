import os
import random
import re
import string
import sys
from unittest.mock import patch

import validators

import nptr_cli.nptr

TEST_SERVER = os.getenv("TEST_SERVER")
if TEST_SERVER is None:
    print("Please provide TEST_SERVER environment variable")
    exit(1)


def mock_config():
    return {
        "default_instance": "test",
        "instances": {
            "test": {
                "url": TEST_SERVER,
                "username": os.getenv("TEST_SERVER_USERNAME"),
                "password": os.getenv("TEST_SERVER_PASSWORD"),
            }
        },
    }


@patch("nptr_cli.nptr.CLI.parse_config", mock_config)
def test_upload_and_delete(tmp_path, capfd):
    dir = tmp_path / "upload"
    dir.mkdir()
    upload_file = dir / "upload.txt"
    upload_file.write_text(
        "".join(
            random.choice(string.ascii_letters)
            for i in range(random.randint(500, 1000))
        )
    )
    with patch.object(sys, "argv", ["0x0", "u", str(upload_file)]):
        nptr_cli.nptr.run()
        out, err = capfd.readouterr()
        out_lines = out.splitlines()
        assert len(out_lines) == 3
        assert validators.url(out_lines[0])
        assert re.match(r"^Expires: [0-9\.]*$", out_lines[1]) is not None
        assert out_lines[2].startswith("Token: ")

    with patch.object(
        sys, "argv", ["0x0", "d", out_lines[0], out_lines[2].split(" ")[1]]
    ):
        nptr_cli.nptr.run()
        out, err = capfd.readouterr()
        assert out.splitlines()[0] == f"Successfully deleted {out_lines[0]}"
