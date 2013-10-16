#
# Copyright (C) 2007 Rico Schiekel (fire at downgra dot de)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# vim:syntax=python:sw=4:ts=4:expandtab

import re
from core.config.settings import logger
from utils.utils import process_by_pipe


RE_MEM = re.compile('^Mem:\s*(?P<total>\d+)\s+(?P<used>\d+)\s+(?P<free>\d+)\s+(?P<shared>\d+)\s+(?P<buffers>\d+)\s+(?P<cached>\d+).*$')
RE_SWAP = re.compile('^Swap:\s*(?P<total>\d+)\s+(?P<used>\d+)\s+(?P<free>\d+).*$')


def info():
    try:
        out, err = process_by_pipe(['free', '-m'])
        lines = out.split('\n')

        mem = RE_MEM.match(lines[1])
        swap = RE_SWAP.match(lines[3])

        if mem and swap:
            mem = dict([(k, float(v)) for k, v in mem.groupdict().items()])
            swap = dict([(k, float(v)) for k, v in swap.groupdict().items()])

            mem_used = mem['used'] - mem['buffers'] - mem['cached']
            mem_usage = mem_used / mem['total'] * 100.0

            swap_usage = swap['used'] / swap['total'] * 100.0

            return 'RAM: %d (%02d%%) SWAP: %d (%02d%%) ' %  (mem_used, mem_usage, swap['used'], swap_usage)

        else:
            return 'RAM: %d (%02d%%) ' %  (mem_used, mem_usage)

    except Exception, e:
        logger.exception(e)

    return 'RAM: -- MB (--%%) SWAP: -- MB (--%%)'
