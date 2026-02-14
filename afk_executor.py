import threading
import time
import subprocess
from pynput.keyboard import Controller,Key
class AfkExecutor:
    def __init__(self,config_manager):
        self.config_manager=config_manager
        self.keyboard=Controller()
        self.is_running=False
        self.thread=None
        self.stop_flag=False
        self.next_press_time=0
        self.lock=threading.Lock()
        self.window=None
    def set_window(self,window):
        self.window=window
    def start(self):
        if self.is_running:
            return False
        config=self.config_manager.load_config()
        if not config.get("anti_afk",{}).get("enabled",False):
            return False
        self.stop_flag=False
        self.is_running=True
        with self.lock:
            self.next_press_time=time.time()
        self.thread=threading.Thread(target=self._execution_loop,daemon=True)
        self.thread.start()
        return True
    def stop(self):
        if not self.is_running:
            return
        self.stop_flag=True
        self.is_running=False
        if self.thread:
            self.thread.join(timeout=2)
        with self.lock:
            self.next_press_time=0
    def _execution_loop(self):
        while not self.stop_flag:
            try:
                config=self.config_manager.load_config()
                if not config.get("anti_afk",{}).get("enabled",False):
                    break
                with self.lock:
                    if time.time()>=self.next_press_time:
                        self._press_space()
                        interval=config.get("anti_afk",{}).get("interval_seconds",300)
                        self.next_press_time=time.time()+interval
            except Exception as e:
                pass
            time.sleep(0.5)
    def _focus_sober_window(self):
        try:
            subprocess.run(["wmctrl","-a","sober"],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            time.sleep(0.3)
        except:
            pass
    def _press_space(self):
        was_minimized=False
        try:
            if self.window:
                try:
                    was_minimized=self.window.wm_state()=="iconic"
                    if not was_minimized:
                        self.window.after(0,self.window.iconify)
                        time.sleep(0.2)
                except:
                    pass
            self._focus_sober_window()
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
            time.sleep(0.1)
        finally:
            if self.window and not was_minimized:
                try:
                    self.window.after(0,self.window.deiconify)
                except:
                    pass
    def get_next_press_time(self):
        with self.lock:
            return self.next_press_time
