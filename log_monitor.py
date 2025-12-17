import threading
import time
import json
import os
from biome_data import BIOMES
class LogMonitor:
    def __init__(self,log_path,callback):
        self.default_log_path=os.path.expanduser(log_path)
        self.callback=callback
        self.stop_flag=False
        self.threads=[]
        self.is_running=False
        self.mode="single"
        self.accounts=[]
    def set_mode(self,mode,accounts=None):
        self.mode=mode
        self.accounts=accounts if accounts else []
    def start(self):
        if self.is_running:
            return False
        if self.mode=="single":
            expanded_path=os.path.expanduser(self.default_log_path)
            if os.path.exists(expanded_path):
                resolved_path=os.path.realpath(expanded_path)
            elif os.path.islink(expanded_path):
                target=os.readlink(expanded_path)
                target_filename=os.path.basename(target)
                symlink_parent=os.path.dirname(expanded_path)
                actual_path=os.path.join(symlink_parent,target_filename)
                if os.path.exists(actual_path):
                    resolved_path=actual_path
                else:
                    return False
            else:
                return False
            self.stop_flag=False
            self.is_running=True
            thread=threading.Thread(target=self._monitor_loop,args=(resolved_path,None),daemon=True)
            thread.start()
            self.threads.append(thread)
        else:
            if not self.accounts:
                return False
            valid_accounts=[]
            for acc in self.accounts:
                expanded_path=os.path.expanduser(acc["log_path"])
                if os.path.exists(expanded_path):
                    resolved_path=os.path.realpath(expanded_path)
                elif os.path.islink(expanded_path):
                    target=os.readlink(expanded_path)
                    target_filename=os.path.basename(target)
                    symlink_parent=os.path.dirname(expanded_path)
                    actual_path=os.path.join(symlink_parent,target_filename)
                    if os.path.exists(actual_path):
                        resolved_path=actual_path
                    else:
                        continue
                else:
                    continue
                acc_copy=acc.copy()
                acc_copy["log_path"]=resolved_path
                valid_accounts.append(acc_copy)
            if not valid_accounts:
                return False
            self.stop_flag=False
            self.is_running=True
            for account in valid_accounts:
                log_path=account["log_path"]
                identifier=account["identifier"]
                thread=threading.Thread(target=self._monitor_loop,args=(log_path,identifier),daemon=True)
                thread.start()
                self.threads.append(thread)
        return True
    def stop(self):
        if not self.is_running:
            return
        self.stop_flag=True
        self.is_running=False
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
        self.threads=[]
    def _monitor_loop(self,log_path,account_identifier):
        try:
            with open(log_path,"r") as f:
                f.seek(0,2)
                last_size=f.tell()
                while not self.stop_flag:
                    current_size=os.path.getsize(log_path)
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
                                        self.callback(biome,account_identifier)
                    except json.JSONDecodeError:
                        pass
                    except Exception:
                        pass
        except Exception:
            pass
        finally:
            self.is_running=False
