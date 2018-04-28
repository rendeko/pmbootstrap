"""
Copyright 2018 Oliver Smith

This file is part of pmbootstrap.

pmbootstrap is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pmbootstrap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pmbootstrap.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import glob
import pmb.chroot.apk
import pmb.install


def kernel_flavors_installed(args, suffix, autoinstall=True):
    """
    Get all installed kernel flavors and make sure that there's at least one

    :param suffix: the chroot suffix, e.g. "native" or "rootfs_qemu-amd64"
    :param autoinstall: make sure that at least one kernel flavor is installed
    :returns: list of installed kernel flavors, e.g. ["postmarketos-mainline"]
    """
    # Automatically install the selected kernel
    if autoinstall:
        packages = (["device-" + args.device] +
                    pmb.install.get_kernel_package(args, args.device))
        pmb.chroot.apk.install(args, packages, suffix)

    # Find all kernels in /boot
    prefix = "vmlinuz-"
    prefix_len = len(prefix)
    pattern = args.work + "/chroot_" + suffix + "/boot/" + prefix + "*"
    ret = []
    for file in glob.glob(pattern):
        flavor = os.path.basename(file)[prefix_len:]
        if flavor[-4:] == "-dtb":
            flavor = flavor[:-4]
        ret.append(flavor)

    # Return without duplicates
    return list(set(ret))


def tempfolder(args, path, suffix="native"):
    """
    Create a temporary folder inside the chroot, that belongs to "user".
    The folder gets deleted, if it already exists.

    :param path: of the temporary folder inside the chroot
    :returns: the path
    """
    if os.path.exists(args.work + "/chroot_" + suffix + path):
        pmb.chroot.root(args, ["rm", "-r", path])
    pmb.chroot.user(args, ["mkdir", "-p", path])
    return path
