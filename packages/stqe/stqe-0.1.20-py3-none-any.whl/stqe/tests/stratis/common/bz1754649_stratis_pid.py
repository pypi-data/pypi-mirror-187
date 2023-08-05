#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.linux import service_start, service_stop
from libsan.host.cmdline import run


def stratis_pid():
    errors = []

    atomic_run("Stopping stratisd service",
               service_name="stratisd",
               command=service_stop,
               errors=errors
               )

    atomic_run("Removing symbolic link /var/run",
               cmd="unlink /var/run",
               command=run,
               errors=errors
               )

    atomic_run("Starting stratisd service",
               service_name="stratisd",
               command=service_start,
               errors=errors
               )

    atomic_run("Restoring symbolic link to /run",
               cmd="ln -s /run /var/run",
               command=run,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = stratis_pid()
    exit(parse_ret(errs))
