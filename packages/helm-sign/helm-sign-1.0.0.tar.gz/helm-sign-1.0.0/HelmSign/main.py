# This file is part of the helm-sign Python package
#    https://gitlab.com/MatthiasLohr/helm-sign
#
# Copyright 2020 Matthias Lohr <mail@mlohr.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os

import gnupg  # type: ignore
import yaml

from .chart import HelmChart


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("chart", help="Helm Chart file")
    argument_parser.add_argument("--gnupg-home", help="GnuPG home/keyring directory")
    argument_parser.add_argument("--keyring", help="GnuPG Keyring File")
    argument_parser.add_argument("--key", help="Key to be used for encryption")

    args = argument_parser.parse_args()

    chart = HelmChart(filename=args.chart)

    message = yaml.dump(chart.get_chart_meta())
    message += "\n...\n"
    message += yaml.dump({"files": {os.path.basename(chart.filename): "sha256:" + chart.checksum("sha256")}})

    gpg = gnupg.GPG(gnupghome=args.gnupg_home, keyring=args.keyring)
    signed_data = gpg.sign(message, keyid=args.key)
    with open(chart.filename + ".prov", "wb") as f:
        f.write(signed_data.data)
    return 0
