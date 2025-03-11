# Copyright (C) 2019 The Android Open Source Project
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

import hashlib
import common
import os

TARGET_DIR = os.getenv('OUT')
def FullOTA_InstallBegin(self):
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/abl.elf"), "firmware-update/abl.elf")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/aop.mbn"), "firmware-update/aop.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/BTFM.bin"), "firmware-update/BTFM.bin")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/cmnlib64.mbn"), "firmware-update/cmnlib64.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/cmnlib.mbn"), "firmware-update/cmnlib.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/dspso.bin"), "firmware-update/dspso.bin")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/devcfg.mbn"), "firmware-update/devcfg.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/hyp.mbn"), "firmware-update/hyp.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/featenabler.mbn"), "firmware-update/featenabler.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/km4.mbn"), "firmware-update/km4.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/NON-HLOS.bin"), "firmware-update/NON-HLOS.bin")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/storsec.mbn"), "firmware-update/storsec.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/tz.mbn"), "firmware-update/tz.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/qupv3fw.elf"), "firmware-update/qupv3fw.elf")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/uefi_sec.mbn"), "firmware-update/uefi_sec.mbn")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/xbl_4.elf"), "firmware-update/xbl_4.elf")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/xbl_5.elf"), "firmware-update/xbl_5.elf")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/xbl_config_4.elf"), "firmware-update/xbl_config_4.elf")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/xbl_config_5.elf"), "firmware-update/xbl_config_5.elf")
  
# Write Firmware updater-script
  self.script.AppendExtra('')
  self.script.AppendExtra('# ---- radio update tasks ----')
  self.script.AppendExtra('')
  self.script.AppendExtra('ui_print("Patching firmware images...");')
  self.script.AppendExtra('package_extract_file("firmware-update/cmnlib64.mbn", "/dev/block/bootdevice/by-name/cmnlib64");')
  self.script.AppendExtra('package_extract_file("firmware-update/cmnlib.mbn", "/dev/block/bootdevice/by-name/cmnlib");')
  self.script.AppendExtra('package_extract_file("firmware-update/hyp.mbn", "/dev/block/bootdevice/by-name/hyp");')
  self.script.AppendExtra('package_extract_file("firmware-update/tz.mbn", "/dev/block/bootdevice/by-name/tz");')
  self.script.AppendExtra('package_extract_file("firmware-update/storsec.mbn", "/dev/block/bootdevice/by-name/storsec");')
  self.script.AppendExtra('package_extract_file("firmware-update/abl.elf", "/dev/block/bootdevice/by-name/abl");')
  self.script.AppendExtra('package_extract_file("firmware-update/dspso.bin", "/dev/block/bootdevice/by-name/dsp");')
  self.script.AppendExtra('package_extract_file("firmware-update/featenabler.mbn", "/dev/block/bootdevice/by-name/featenabler");')
  self.script.AppendExtra('package_extract_file("firmware-update/devcfg.mbn", "/dev/block/bootdevice/by-name/devcfg");')
  self.script.AppendExtra('package_extract_file("firmware-update/km4.mbn", "/dev/block/bootdevice/by-name/keymaster");')
  self.script.AppendExtra('package_extract_file("firmware-update/cmnlib64.mbn", "/dev/block/bootdevice/by-name/cmnlib64bak");')
  self.script.AppendExtra('package_extract_file("firmware-update/cmnlib.mbn", "/dev/block/bootdevice/by-name/cmnlibbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/hyp.mbn", "/dev/block/bootdevice/by-name/hypbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/tz.mbn", "/dev/block/bootdevice/by-name/tzbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/abl.elf", "/dev/block/bootdevice/by-name/ablbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/devcfg.mbn", "/dev/block/bootdevice/by-name/devcfgbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/storsec.mbn", "/dev/block/bootdevice/by-name/storsecbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/aop.mbn", "/dev/block/bootdevice/by-name/aopbak");')
  self.script.AppendExtra('package_extract_file("firmware-update/uefi_sec.mbn", "/dev/block/bootdevice/by-name/uefisecapp");')
  self.script.AppendExtra('package_extract_file("firmware-update/NON-HLOS.bin", "/dev/block/bootdevice/by-name/modem");')
  self.script.AppendExtra('package_extract_file("firmware-update/qupv3fw.elf", "/dev/block/bootdevice/by-name/qupfw");')
  self.script.AppendExtra('package_extract_file("firmware-update/BTFM.bin", "/dev/block/bootdevice/by-name/bluetooth");')
  self.script.AppendExtra('package_extract_file("firmware-update/aop.mbn", "/dev/block/bootdevice/by-name/aop");')
  self.script.AppendExtra('package_extract_file("firmware-update/xbl_4.elf", "/dev/block/bootdevice/by-name/xbl_4");')
  self.script.AppendExtra('package_extract_file("firmware-update/xbl_5.elf", "/dev/block/bootdevice/by-name/xbl_5");')
  self.script.AppendExtra('package_extract_file("firmware-update/xbl_config_4.elf", "/dev/block/bootdevice/by-name/xbl_config_4");')
  self.script.AppendExtra('package_extract_file("firmware-update/xbl_config_5.elf", "/dev/block/bootdevice/by-name/xbl_config_5");')
  
# Firmware - sagit
def FullOTA_InstallEnd(self):
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/dtbo.img"), "firmware-update/dtbo.img")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/logo.img"), "firmware-update/logo.img")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/vbmeta.img"), "firmware-update/vbmeta.img")
  self.output_zip.write(os.path.join(TARGET_DIR, "firmware-update/vbmeta_system.img"), "firmware-update/vbmeta_system.img")

# Write Firmware updater-script
  self.script.AppendExtra('')
  self.script.AppendExtra('# ---- radio update tasks 2 ---')
  self.script.AppendExtra('')
  self.script.AppendExtra('ui_print("Patching vbmeta dtbo logo binimages...");')
  self.script.AppendExtra('package_extract_file("firmware-update/dtbo.img", "/dev/block/bootdevice/by-name/dtbo");')
  self.script.AppendExtra('package_extract_file("firmware-update/logo.img", "/dev/block/bootdevice/by-name/logo");')
  self.script.AppendExtra('package_extract_file("firmware-update/vbmeta.img", "/dev/block/bootdevice/by-name/vbmeta");')
  self.script.AppendExtra('package_extract_file("firmware-update/vbmeta_system.img", "/dev/block/bootdevice/by-name/vbmeta_system");')