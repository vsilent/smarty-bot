# vim:syntax=python:sw=4:ts=4:expandtab

from core.config.settings import logger
import math

SYSINFO = '/sys/class/power_supply/'
FILE_BAT_INFO = SYSINFO + 'BAT1'
AC_ONLINE = SYSINFO + 'ACAD/online'
ENERGY_FULL = FILE_BAT_INFO + '/energy_full'
ENERGY_NOW = FILE_BAT_INFO + '/energy_now'
POWER_NOW = FILE_BAT_INFO + '/energy_now'
ALARM = FILE_BAT_INFO + '/alarm'


def interval():
    return 5


def info():
    bat = '--'
    time_left = ''
    status = ''
    try:

        with open(ENERGY_FULL) as eff:
            energy_full = float(eff.read())

        with open(ENERGY_NOW) as enf:
            energy_now = float(enf.read())

        with open(POWER_NOW) as pnf:
            power_now = float(pnf.read())

        with open(ALARM) as af:
            alarm = float(af.read())

        with open(AC_ONLINE) as aof:
            ac_online = float(aof.read())


        if power_now != 0:
            #current_usage = power_now/1000000
            time_left = ' %3.2f h ' % ( energy_now / power_now)
            percent = math.floor( energy_now * 100 / energy_full )
            bat = '%d%%' % percent

            if percent < 25:
                status = 'critical'
            elif percent < 50:
                status = 'medium'
            else:
                status = "normal"

        if ac_online:
            bat = 'AC'
            time_left = ''

    except Exception as e:
        logger.exception(e)

    return 'BAT: %s%s %s' % ( bat, time_left , status )
