import threading
import time
import json
import os
from biome_data import BIOMES
class LogMonitor:
    def __init__(self,log_path,callback):
        self.log_path=os.path.expanduser(log_path)
        self.callback=callback
        self.stop_flag=False
        self.thread=None
        self.is_running=False
    def start(self):
        if self.is_running:
            return False
        if not os.path.exists(self.log_path):
            return False
        self.stop_flag=False
        self.is_running=True
        self.thread=threading.Thread(target=self._monitor_loop,daemon=True)
        self.thread.start()
        return True
    def stop(self):
        if not self.is_running:
            return
        self.stop_flag=True
        self.is_running=False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
    def _monitor_loop(self):
        try:
            with open(self.log_path,"r") as f:
                f.seek(0,2)
                last_size=f.tell()
                while not self.stop_flag:
                    current_size=os.path.getsize(self.log_path)
                    if current_size<last_size:
                        f.seek(0,2)
                        last_size=current_size
                        continue
                    line=f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    try:
                        if "[BloxstrapRPC]" in line:
                            json_start=line.find("{")
                            if json_start!=-1:
                                json_str=line[json_start:]
                                data=json.loads(json_str.strip())
                                if data.get("command")=="SetRichPresence":
                                    biome=data.get("data",{}).get("largeImage",{}).get("hoverText")
                                    if biome and biome in BIOMES:
                                        self.callback(biome)
                    except json.JSONDecodeError:
                        pass
                    except Exception:
                        pass
        except Exception:
            pass
        finally:
            self.is_running=False
