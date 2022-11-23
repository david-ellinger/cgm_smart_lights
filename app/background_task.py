import threading
import time

from app.domain.workflow_manager import update_lights_workflow

INTERVAL = 60
class UpdateLightsTask(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            update_lights_workflow()
            time.sleep(INTERVAL)
