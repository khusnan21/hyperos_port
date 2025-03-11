#!/usr/bin/env python3
#
# Copyright (C) 2022 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import logging
from common import OPTIONS

logger = logging.getLogger(__name__)


class PayloadSigner(object):
  """A class that wraps the payload signing works.

  When generating a Payload, hashes of the payload and metadata files will be
  signed with the device key, either by calling an external payload signer or
  by calling openssl with the package key. This class provides a unified
  interface, so that callers can just call PayloadSigner.Sign().

  If an external payload signer has been specified (OPTIONS.payload_signer), it
  calls the signer with the provided args (OPTIONS.payload_signer_args). Note
  that the signing key should be provided as part of the payload_signer_args.
  Otherwise without an external signer, it uses the package key
  (OPTIONS.package_key) and calls openssl for the signing works.
  """

  def __init__(self, package_key=None, private_key_suffix=None, pw=None, payload_signer=None,
               payload_signer_args=None, payload_signer_maximum_signature_size=None):
    if package_key is None:
      package_key = OPTIONS.package_key
    if private_key_suffix is None:
      private_key_suffix = OPTIONS.private_key_suffix
    if payload_signer_args is None:
      payload_signer_args = OPTIONS.payload_signer_args
    if payload_signer_maximum_signature_size is None:
      payload_signer_maximum_signature_size = OPTIONS.payload_signer_maximum_signature_size

    if payload_signer is None:
      # Prepare the payload signing key.
      private_key = package_key + private_key_suffix

      cmd = ["openssl", "pkcs8", "-in", private_key, "-inform", "DER"]
      cmd.extend(["-passin", "pass:" + pw] if pw else ["-nocrypt"])
      signing_key = common.MakeTempFile(prefix="key-", suffix=".key")
      cmd.extend(["-out", signing_key])
      common.RunAndCheckOutput(cmd, verbose=True)

      self.signer = "openssl"
      self.signer_args = ["pkeyutl", "-sign", "-inkey", signing_key,
                          "-pkeyopt", "digest:sha256"]
      self.maximum_signature_size = self._GetMaximumSignatureSizeInBytes(
          signing_key)
    else:
      self.signer = payload_signer
      self.signer_args = payload_signer_args
      if payload_signer_maximum_signature_size:
        self.maximum_signature_size = int(
            payload_signer_maximum_signature_size)
      else:
        # The legacy config uses RSA2048 keys.
        logger.warning("The maximum signature size for payload signer is not"
                       " set, default to 256 bytes.")
        self.maximum_signature_size = 256

  @staticmethod
  def _GetMaximumSignatureSizeInBytes(signing_key):
    out_signature_size_file = common.MakeTempFile("signature_size")
    cmd = ["delta_generator", "--out_maximum_signature_size_file={}".format(
        out_signature_size_file), "--private_key={}".format(signing_key)]
    common.RunAndCheckOutput(cmd, verbose=True)
    with open(out_signature_size_file) as f:
      signature_size = f.read().rstrip()
    logger.info("%s outputs the maximum signature size: %s", cmd[0],
                signature_size)
    return int(signature_size)

  @staticmethod
  def _Run(cmd):
    common.RunAndCheckOutput(cmd, stdout=None, stderr=None)

  def SignPayload(self, unsigned_payload):

    # 1. Generate hashes of the payload and metadata files.
    payload_sig_file = common.MakeTempFile(prefix="sig-", suffix=".bin")
    metadata_sig_file = common.MakeTempFile(prefix="sig-", suffix=".bin")
    cmd = ["brillo_update_payload", "hash",
           "--unsigned_payload", unsigned_payload,
           "--signature_size", str(self.maximum_signature_size),
           "--metadata_hash_file", metadata_sig_file,
           "--payload_hash_file", payload_sig_file]
    self._Run(cmd)

    # 2. Sign the hashes.
    signed_payload_sig_file = self.SignHashFile(payload_sig_file)
    signed_metadata_sig_file = self.SignHashFile(metadata_sig_file)

    # 3. Insert the signatures back into the payload file.
    signed_payload_file = common.MakeTempFile(prefix="signed-payload-",
                                              suffix=".bin")
    cmd = ["brillo_update_payload", "sign",
           "--unsigned_payload", unsigned_payload,
           "--payload", signed_payload_file,
           "--signature_size", str(self.maximum_signature_size),
           "--metadata_signature_file", signed_metadata_sig_file,
           "--payload_signature_file", signed_payload_sig_file]
    self._Run(cmd)
    return signed_payload_file


  def SignHashFile(self, in_file):
    """Signs the given input file. Returns the output filename."""
    out_file = common.MakeTempFile(prefix="signed-", suffix=".bin")
    cmd = [self.signer] + self.signer_args + ['-in', in_file, '-out', out_file]
    common.RunAndCheckOutput(cmd)
    return out_file
