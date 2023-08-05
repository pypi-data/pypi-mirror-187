#!/usr/bin/python -u
# -u is for unbuffered stdout
# Copyright (C) 2016 Red Hat, Inc.
# python-stqe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-stqe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-stqe.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Bruno Goncalves   <bgoncalv@redhat.com>

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import traceback
import stqe.host.tc
import libsan.host.lvm as lvm
import libsan.host.loopdev as loopdev
import libsan.host.linux as linux

from stqe.host.lvm import check_lv_expected_value
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"


def _convert():
    global TestObj, vg_name

    # Convert an LV to thin pool
    TestObj.tok("lvcreate -l20 -n %s/pool" % vg_name)
    TestObj.tok("lvconvert --thinpool %s/pool -y" % vg_name)
    check_lv_expected_value(TestObj, "pool", vg_name, {"lv_attr": "twi-a-tz--"})
    TestObj.tok("lvremove -ff %s" % vg_name)

    # Convert an inactive LV to thin pool
    TestObj.tok("lvcreate --zero n -an -l20 -n %s/pool" % vg_name)
    TestObj.tok("lvconvert --thinpool %s/pool -y" % vg_name)
    check_lv_expected_value(TestObj, "pool", vg_name,
                            {"lv_attr": "twi---tz--", "discards": "passdown"})
    TestObj.tok("lvremove -ff %s" % vg_name)

    # Convert to thin pool and set parameters
    TestObj.tok("lvcreate -l20 -n %s/pool" % vg_name)
    TestObj.tok(
        "lvconvert --thinpool  %s/pool -c 256 -Z y --discards nopassdown --poolmetadatasize 4M -r 16 -y" % vg_name)
    check_lv_expected_value(TestObj, "pool", vg_name,
                            {"chunksize": "256.00k", "discards": "nopassdown",
                             "lv_metadata_size": "4.00m", "lv_size": "80.00m"})
    TestObj.tok("lvremove -ff %s" % vg_name)

    TestObj.tok("lvcreate -l20 -n %s/pool" % vg_name)
    TestObj.tok("lvcreate -l10 -n %s/metadata" % vg_name)
    TestObj.tok("lvconvert -y --thinpool %s/pool --poolmetadata %s/metadata" % (vg_name, vg_name))
    check_lv_expected_value(TestObj, "pool", vg_name,
                            {"lv_size": "80.00m", "lv_metadata_size": "40.00m"})
    TestObj.tok("lvremove -ff %s" % vg_name)


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Pool Convert test")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        new_dev = loopdev.create_loopdev(size=128)
        if not new_dev:
            TestObj.tfail("Could not create loop device to be used as dev%s" % dev_num)
            return False
        loop_dev["dev%s" % dev_num] = new_dev

    pvs = ""
    for dev in loop_dev.keys():
        pvs += " %s" % (loop_dev[dev])
    if not lvm.vg_create(vg_name, pvs, force=True):
        TestObj.tfail("Could not create VG")
        return False

    _convert()

    return True


def _clean_up():
    if not lvm.vg_remove(vg_name, force=True):
        TestObj.tfail("Could not delete VG \"%s\"" % vg_name)

    if loop_dev:
        for dev in loop_dev.keys():
            if not lvm.pv_remove(loop_dev[dev]):
                TestObj.tfail("Could not delete PV \"%s\"" % loop_dev[dev])
            # Sleep a bit to avoid problem of device still being busy
            linux.sleep(1)
            if not loopdev.delete_loopdev(loop_dev[dev]):
                TestObj.tfail("Could not remove loop device %s" % loop_dev[dev])


def main():
    global TestObj

    TestObj = stqe.host.tc.TestClass()

    linux.install_package("lvm2")

    try:
        start_test()
    except Exception as e:
        print(e)
        traceback.print_exc()
        TestObj.tfail("There was some problem while running the test (%s)" % e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
