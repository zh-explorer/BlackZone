import sys
import web
import threading
import time
#from ..container import Container
from ..containermanager import ContainerManager
urls = (
     '/', 'Demo'
)


sys.argv.append('4406')
app = web.application(urls, globals())

manager_list=[]

class Demo:
    
    def __init__(self):
        print 'init is called'
        print manager_list
    def GET(self):
        argv = web.input(cmd="",password="")
        cmd = argv.cmd
        password = argv.password

        if password == "test":
            r = self.solve_cmd(cmd)
            return r
        return ''
    
    def solve_cmd(self,cmd):
        cmd = cmd.split(' ')

        print cmd[0] 
        if cmd[0] == 'create':
            m = ContainerManager()
            manager_list.append(m)
            while 1:
                pass
            return "create_success"
             
        if cmd[0] == 'ps':
            a=''
            for manager in self.manager_list:
                a += self.detail(manager)
                print a
            return a
        
        if cmd[0] == 'start' or cmd[0] == 'stop' or cmd[0] == 'kill':
            if len(cmd) != 2:
                return 'Error: start/stop/kill container_id'
            container_id = cmd[1]
            manager = self.find(container_id)
            if manager == None:
                return 'Error: container is not exist'
            if manager.state() == "running" and cmd[0] == 'start':
                return 'Error: container is running'
            if manager.state() == "stoped" and cmd[0] == 'stop':
                return 'Error: container is already stoped'
            if cmd[0] == 'stop':
                manager.stop()
            if cmd[0] == 'start':
                manager.start()
            if cmd[0] == 'kill':
                manager.kill()
                manager.clear()
                manager_list.remove(manager)
            return 'success'
        if cmd[0] == 'limit':
            if len(cmd) != 4:
                return 'Error: limit container_id cpu/mem value'
            container_id = cmd[1]
            manager = self.find(container_id)
            
            if manager == None:
                return 'Error: container is not exist'
            
            if cmd[2] != 'cpu' and cmd[2] != 'mem':
                return 'Error: not supported now'
            
            manager.update_cgroup(cmd[2],cmd[3])
        
        if cmd[0] == 'netblock':
            if len(cmd) != 2:
                return 'Error: netblock container_id'
            container_id = cmd[1]
            manager = self.find(container_id)
            if manager == None:
                return 'Error: container is not exist'
            manager.net_block()

        if cmd[0] == 'log':
            if len(cmd) != 4:
                return 'Error: log container_id [start time] [end time]'
            container_id = cmd[1]
#            Logger.select_log(cmd[1],cmd[2],cmd[3])
    def detail(self,manager):
        return manager.get_container_info()
    
    def find(self,container_id):
        for manager in self.manager_list:
            if manager.container_id == container_id:
                return manager
        return None
    
    
if __name__ == "__main__":    
    app.run()
