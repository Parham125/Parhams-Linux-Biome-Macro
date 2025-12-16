import threading
import time
import subprocess
from pynput.mouse import Controller,Button
from pynput.keyboard import Controller as KeyboardController,Key
class ItemExecutor:
    def __init__(self,config_manager):
        self.config_manager=config_manager
        self.mouse=Controller()
        self.keyboard=KeyboardController()
        self.is_running=False
        self.thread=None
        self.stop_flag=False
        self.next_execution_times={}
        self.lock=threading.Lock()
        self.window=None
    def set_window(self,window):
        self.window=window
    def start(self):
        if self.is_running:
            return False
        self.stop_flag=False
        self.is_running=True
        config=self.config_manager.load_config()
        with self.lock:
            self.next_execution_times={}
            all_items=config.get("item_use",{}).get("items",[])+config.get("item_use",{}).get("custom_items",[])
            for item in all_items:
                if item.get("enabled",False):
                    self.next_execution_times[item["id"]]=time.time()
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
            self.next_execution_times={}
    def _execution_loop(self):
        while not self.stop_flag:
            try:
                config=self.config_manager.load_config()
                all_items=config.get("item_use",{}).get("items",[])+config.get("item_use",{}).get("custom_items",[])
                for item in all_items:
                    if not item.get("enabled",False):
                        continue
                    item_id=item["id"]
                    should_execute=False
                    with self.lock:
                        if item_id not in self.next_execution_times:
                            self.next_execution_times[item_id]=time.time()
                        if time.time()>=self.next_execution_times[item_id]:
                            if self._should_execute_item(item,config):
                                should_execute=True
                    if should_execute:
                        self._execute_item_sequence(item,config)
                        with self.lock:
                            self.next_execution_times[item_id]=time.time()+item.get("interval_seconds",300)
            except Exception as e:
                pass
            time.sleep(0.5)
    def _should_execute_item(self,item,config):
        current_biome=config.get("last_biome","NORMAL")
        mode=item.get("biome_filter_mode","whitelist")
        biome_filter=item.get("biome_filter",[])
        if mode=="whitelist":
            return current_biome in biome_filter
        elif mode=="blacklist":
            return current_biome not in biome_filter
        return True
    def _focus_sober_window(self):
        try:
            subprocess.run(["wmctrl","-a","sober"],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            time.sleep(0.3)
        except:
            pass
    def _execute_item_sequence(self,item,config):
        try:
            was_minimized=False
            if self.window:
                try:
                    was_minimized=self.window.wm_state()=="iconic"
                    if not was_minimized:
                        self.window.iconify()
                        time.sleep(0.2)
                except:
                    pass
            self._focus_sober_window()
            coordinates=config.get("item_use",{}).get("coordinates",{})
            if not all(coordinates.get(key,{}).get("x",0)!=0 or coordinates.get(key,{}).get("y",0)!=0 for key in ["inventory_button","items_button","search_box","first_item_box","amount_box","use_button","close_button"]):
                if self.window and not was_minimized:
                    try:
                        self.window.deiconify()
                    except:
                        pass
                return
            inv_coord=coordinates.get("inventory_button",{})
            self.mouse.position=(inv_coord.get("x",0),inv_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.1)
            self.mouse.click(Button.left,1)
            time.sleep(0.5)
            items_coord=coordinates.get("items_button",{})
            self.mouse.position=(items_coord.get("x",0),items_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.5)
            search_coord=coordinates.get("search_box",{})
            self.mouse.position=(search_coord.get("x",0),search_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.2)
            item_name=item.get("name","")
            for char in item_name:
                self.keyboard.press(char)
                self.keyboard.release(char)
            time.sleep(1.0)
            first_item_coord=coordinates.get("first_item_box",{})
            self.mouse.position=(first_item_coord.get("x",0),first_item_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.1)
            self.mouse.click(Button.left,1)
            time.sleep(0.5)
            amount_coord=coordinates.get("amount_box",{})
            self.mouse.position=(amount_coord.get("x",0),amount_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.1)
            self.mouse.click(Button.left,1)
            time.sleep(0.2)
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('a')
            self.keyboard.release('a')
            self.keyboard.release(Key.ctrl)
            self.keyboard.press(Key.backspace)
            self.keyboard.release(Key.backspace)
            time.sleep(0.1)
            amount_text=item.get("amount","1")
            for char in amount_text:
                self.keyboard.press(char)
                self.keyboard.release(char)
            time.sleep(0.5)
            use_coord=coordinates.get("use_button",{})
            self.mouse.position=(use_coord.get("x",0),use_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.1)
            self.mouse.click(Button.left,1)
            time.sleep(0.5)
            close_coord=coordinates.get("close_button",{})
            self.mouse.position=(close_coord.get("x",0),close_coord.get("y",0))
            self.mouse.click(Button.left,1)
            time.sleep(0.1)
            self.mouse.click(Button.left,1)
            if self.window and not was_minimized:
                try:
                    self.window.deiconify()
                except:
                    pass
        except Exception as e:
            if self.window and not was_minimized:
                try:
                    self.window.deiconify()
                except:
                    pass
    def get_next_execution_time(self,item_id):
        with self.lock:
            return self.next_execution_times.get(item_id,0)
