from ..container import Container
from ..libs import processSynClass
from ..logger import Logger
from ..tubes.process import Process
#from ..context import context
#from ..container import FsManager,ContainerConfig
#import time
class ContainerManager:
    def __init__(self):
        c = processSynClass.get_process_syn(Container)
        c = c('208ccdee98bc0039c8283ca2e0c8053c75d8f4457cb7f0c9d9dd7bd03f719a3f')
        c.start()
#        container_id = str(time.time())
#        fs = FsManager("208ccdee98bc0039c8283ca2e0c8053c75d8f4457cb7f0c9d9dd7bd03f719a3f", container_id)
#        config = ContainerConfig(None)
#        self.container_id = container_id
#        p = Process([context.runc,"run","-b",fs.container_dir,self.container_id])

        self.s = 1
#        print p.read()
        
    def clear(self):
        return 
    def start(self):
        return
    def get_event(self):
        return
    def state(self):
        if self.s == 1:
            return 'running'
        elif self.s == 2:
            return 'stoped'
        elif self.s == 3:
            return 'ended'
        else:
            return 'error'
        return
    def stop(self):
        
        return

    def kill(self):
        return

    def update_cgroup(self,t,limit):
        return

    def netblock(self):
        return

    def get_container_info(self):
        return 'a'
