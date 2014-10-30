# vim:syntax=python:sw=4:ts=4:expandtab

import re
from core.config.settings import logger
from core.utils.utils import parse_file


def interval():
    return 2


SYSINFO = '/sys/class/thermal/'
FILE_TEMP = SYSINFO + 'thermal_zone0/temp'
RE_CPU = re.compile(r'^cpu MHz\s*:\s*(?P<mhz>\d+).*$')
RE_STATS = re.compile(r'^cpu  (?P<user>\d+) (?P<system>\d+) (?P<nice>\d+) (?P<idle>\d+).*$')
OLD_STATS = dict(user=0, system=0, nice=0, idle=0)


def info():
    #cpu_vals = parse_file('/proc/cpuinfo', RE_CPU)
    stat_vals = parse_file('/proc/stat', RE_STATS)
    temp_vals = ''
    status = ''

    try:
        tf = open(FILE_TEMP)
        temp_vals = int(tf.read()) / 1000
    except Exception, e:
        logger.exception(e)

    tf.close()

    #cpu = '--'

    #try:
        #cpu = '/'.join(cpu_vals['mhz'])
    #except Exception as e:
        #logger.exception(e)

    load = '--'
    try:
        # convert values to int's
        stat_vals = dict([(k, int(v[0])) for k, v in stat_vals.items()])
        dtotal = stat_vals['user'] - OLD_STATS['user'] + \
                 stat_vals['system'] - OLD_STATS['system'] + \
                 stat_vals['nice'] - OLD_STATS['nice'] + \
                 stat_vals['idle'] - OLD_STATS['idle']
        if dtotal > 0:
            load = 100 - ((stat_vals['idle'] - OLD_STATS['idle']) * 100 / dtotal)
            loadstr = '%02d' % (load)

        if load > 50:
            status = 'critical'
        elif 20 < load < 50:
            status = 'medium'
        else:
            status = 'normal'

        OLD_STATS.update(stat_vals)
    except Exception as e:
        logger.exception(e)

    tempr = '--'
    try:
        tempr = temp_vals
    except Exception as e:
        logger.exception(e)

    return 'CPU: %s%% temperature [%s] %s' % (loadstr, tempr, status)
