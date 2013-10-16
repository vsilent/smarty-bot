import re
import logging
from core.utils.utils import process_by_pipe

logger = logging.getLogger('statusbar.iface')

def info():
    try:
        s = ""
        for iface in ['eth0', 'wlan0']:
            s += iface + ": "
            out, err = process_by_pipe(['ip', 'a', 's', iface])
            lines = out.split('\n')

            if re.search("UP", lines[0]) == None:
                s += "off "
            for l in lines[1:]:
                mo = re.search("inet\s*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", l)
                if mo:
                    s += mo.group(1) + " "

        return s
    except Exception, e:
        logger.exception(e)
