from threading import Thread
import subprocess
from Queue import Queue


class pinger():

    response = {}

    #wraps system ping command
    def pinger(self, i, q):
        """Pings subnet"""
        while True:
            host = q.get()
            print("\npinging %s" % host)
            ret = subprocess.call("ping -c 3 %s" % host,
                                shell=True,
                                stdout=open('/dev/null', 'w'),
                                stderr=subprocess.STDOUT)
            if ret == 0:
                self.response[host] = 'up'
            else:
                self.response[host] = 'down'
            q.task_done()

    def ping(self, hosts):
        """ping"""
        num_threads = len(hosts)
        queue = Queue()

        #Spawn thread pool
        for i in range(num_threads):
            worker = Thread(target=self.pinger, args=(i, queue))
            worker.setDaemon(True)
            worker.start()
        #Place work in queue
        for host in hosts:
            queue.put(host)
        #Wait until worker threads are done to exit
        queue.join()
