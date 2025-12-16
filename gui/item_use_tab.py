import customtkinter as ctk
import threading
import time
from biome_data import BIOMES
class ItemUseTab(ctk.CTkScrollableFrame):
    def __init__(self,parent,config_manager,item_executor):
        super().__init__(parent)
        self.config_manager=config_manager
        self.item_executor=item_executor
        self.coord_buttons={}
        self.item_frames={}
        self.item_widgets={}
        ctk.CTkLabel(self,text="Coordinate Configuration",font=("Arial",16,"bold")).pack(pady=(20,10),anchor="w",padx=20)
        coord_frame=ctk.CTkFrame(self)
        coord_frame.pack(fill="x",padx=20,pady=10)
        self.coord_names=["inventory_button","items_button","search_box","first_item_box","amount_box","use_button","close_button"]
        self.coord_labels=["Inventory Button","Items Button","Search Box","First Item Box","Amount Box","Use Button","Close Button"]
        for idx,coord_name in enumerate(self.coord_names):
            row=idx//2
            col=idx%2
            btn=ctk.CTkButton(coord_frame,text=self._get_coord_button_text(coord_name),command=lambda cn=coord_name: self._capture_coordinate(cn),width=250)
            btn.grid(row=row,column=col,padx=10,pady=5)
            self.coord_buttons[coord_name]=btn
        coord_frame.columnconfigure(0,weight=1)
        coord_frame.columnconfigure(1,weight=1)
        ctk.CTkLabel(self,text="Items",font=("Arial",16,"bold")).pack(pady=(30,10),anchor="w",padx=20)
        add_item_btn=ctk.CTkButton(self,text="+ Add Custom Item",command=self._add_custom_item,width=200)
        add_item_btn.pack(pady=10,padx=20,anchor="w")
        self.items_container=ctk.CTkFrame(self,fg_color="transparent")
        self.items_container.pack(fill="both",expand=True,padx=20,pady=10)
        ctk.CTkLabel(self,text="Status",font=("Arial",16,"bold")).pack(pady=(20,10),anchor="w",padx=20)
        self.status_label=ctk.CTkLabel(self,text="Waiting for monitoring to start",font=("Arial",12))
        self.status_label.pack(pady=5,padx=20,anchor="w")
        self.error_label=ctk.CTkLabel(self,text="",text_color="red",font=("Arial",11))
        self.error_label.pack(pady=5,padx=20,anchor="w")
        save_btn=ctk.CTkButton(self,text="Save Settings",command=self.save_settings,width=200,height=40,font=("Arial",14,"bold"))
        save_btn.pack(pady=30)
        self.load_items()
        self._update_execution_times()
    def _get_coord_button_text(self,coord_name):
        config=self.config_manager.load_config()
        coords=config.get("item_use",{}).get("coordinates",{}).get(coord_name,{})
        x=coords.get("x",0)
        y=coords.get("y",0)
        label=self.coord_labels[self.coord_names.index(coord_name)]
        if x==0 and y==0:
            return f"{label} (Not Set)"
        return f"{label} ({x}, {y})"
    def _capture_coordinate(self,coord_name):
        btn=self.coord_buttons[coord_name]
        label=self.coord_labels[self.coord_names.index(coord_name)]
        btn.configure(text=f"{label} - Click in game window...")
        listener_thread=threading.Thread(target=self._listen_for_click,args=(coord_name,),daemon=True)
        listener_thread.start()
    def _listen_for_click(self,coord_name):
        from pynput import mouse
        def on_click(x,y,button,pressed):
            if pressed:
                self.after(0,lambda: self._save_coordinate(coord_name,x,y))
                return False
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
    def _save_coordinate(self,coord_name,x,y):
        config=self.config_manager.load_config()
        if "item_use" not in config:
            config["item_use"]={"coordinates": {},"items": [],"custom_items": []}
        config["item_use"]["coordinates"][coord_name]={"x": x,"y": y}
        self.config_manager.save_config(config)
        self.coord_buttons[coord_name].configure(text=self._get_coord_button_text(coord_name))
    def load_items(self):
        for widget in self.items_container.winfo_children():
            widget.destroy()
        self.item_frames={}
        self.item_widgets={}
        config=self.config_manager.load_config()
        all_items=config.get("item_use",{}).get("items",[])+config.get("item_use",{}).get("custom_items",[])
        for item in all_items:
            self._create_item_frame(item,is_custom=item.get("id","").startswith("custom_"))
    def _create_item_frame(self,item,is_custom=False):
        item_id=item["id"]
        frame=ctk.CTkFrame(self.items_container)
        frame.pack(fill="x",pady=10,padx=10)
        header_frame=ctk.CTkFrame(frame,fg_color="transparent")
        header_frame.pack(fill="x",padx=10,pady=5)
        ctk.CTkLabel(header_frame,text=item["name"],font=("Arial",14,"bold")).pack(side="left",padx=5)
        if is_custom:
            delete_btn=ctk.CTkButton(header_frame,text="Delete",command=lambda: self._delete_item(item_id),width=80,fg_color="red")
            delete_btn.pack(side="right",padx=5)
        enable_switch=ctk.CTkSwitch(frame,text="Enable")
        enable_switch.pack(pady=5,padx=10,anchor="w")
        if item.get("enabled",False):
            enable_switch.select()
        interval_frame=ctk.CTkFrame(frame,fg_color="transparent")
        interval_frame.pack(fill="x",padx=10,pady=5)
        ctk.CTkLabel(interval_frame,text="Interval:").pack(side="left",padx=5)
        interval_entry=ctk.CTkEntry(interval_frame,width=100)
        interval_entry.insert(0,str(item.get("interval_seconds",300)))
        interval_entry.pack(side="left",padx=5)
        interval_unit=ctk.CTkSegmentedButton(interval_frame,values=["Seconds","Minutes"])
        interval_unit.set("Seconds")
        interval_unit.pack(side="left",padx=5)
        amount_frame=ctk.CTkFrame(frame,fg_color="transparent")
        amount_frame.pack(fill="x",padx=10,pady=5)
        ctk.CTkLabel(amount_frame,text="Amount:").pack(side="left",padx=5)
        amount_entry=ctk.CTkEntry(amount_frame,width=100)
        amount_entry.insert(0,item.get("amount","1"))
        amount_entry.pack(side="left",padx=5)
        filter_frame=ctk.CTkFrame(frame,fg_color="transparent")
        filter_frame.pack(fill="x",padx=10,pady=5)
        ctk.CTkLabel(filter_frame,text="Biome Filter:").pack(side="left",padx=5)
        filter_mode=ctk.CTkSegmentedButton(filter_frame,values=["Whitelist","Blacklist"])
        filter_mode.set(item.get("biome_filter_mode","whitelist").capitalize())
        filter_mode.pack(side="left",padx=5)
        biome_checkboxes_frame=ctk.CTkFrame(frame)
        biome_checkboxes_frame.pack(fill="both",expand=True,padx=10,pady=5)
        biome_checkboxes={}
        biome_list=list(BIOMES.keys())
        for idx,biome in enumerate(biome_list):
            row=idx//2
            col=idx%2
            biome_info=BIOMES[biome]
            checkbox=ctk.CTkCheckBox(biome_checkboxes_frame,text=f"{biome_info['emoji']} {biome}")
            checkbox.grid(row=row,column=col,padx=5,pady=3,sticky="w")
            if biome in item.get("biome_filter",[]):
                checkbox.select()
            biome_checkboxes[biome]=checkbox
        biome_checkboxes_frame.columnconfigure(0,weight=1)
        biome_checkboxes_frame.columnconfigure(1,weight=1)
        next_exec_label=ctk.CTkLabel(frame,text="Next use in: --",font=("Arial",11,"italic"))
        next_exec_label.pack(pady=5,padx=10,anchor="w")
        self.item_frames[item_id]=frame
        self.item_widgets[item_id]={"enable_switch": enable_switch,"interval_entry": interval_entry,"interval_unit": interval_unit,"amount_entry": amount_entry,"filter_mode": filter_mode,"biome_checkboxes": biome_checkboxes,"next_exec_label": next_exec_label}
    def _add_custom_item(self):
        dialog=ctk.CTkToplevel(self)
        dialog.title("Add Custom Item")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.after(100,dialog.grab_set)
        ctk.CTkLabel(dialog,text="Item Name:",font=("Arial",12)).pack(pady=10,padx=20,anchor="w")
        name_entry=ctk.CTkEntry(dialog,width=350)
        name_entry.pack(pady=5,padx=20)
        def add_item():
            name=name_entry.get().strip()
            if not name:
                return
            config=self.config_manager.load_config()
            import uuid
            item_id=f"custom_{uuid.uuid4().hex[:8]}"
            new_item={"id": item_id,"name": name,"enabled": False,"interval_seconds": 300,"biome_filter_mode": "whitelist","biome_filter": ["NORMAL"],"amount": "1"}
            if "item_use" not in config:
                config["item_use"]={"coordinates": {},"items": [],"custom_items": []}
            config["item_use"]["custom_items"].append(new_item)
            self.config_manager.save_config(config)
            dialog.destroy()
            self.load_items()
        add_btn=ctk.CTkButton(dialog,text="Add Item",command=add_item,width=150)
        add_btn.pack(pady=20)
    def _delete_item(self,item_id):
        config=self.config_manager.load_config()
        config["item_use"]["custom_items"]=[item for item in config["item_use"]["custom_items"] if item["id"]!=item_id]
        self.config_manager.save_config(config)
        self.load_items()
    def save_settings(self):
        config=self.config_manager.load_config()
        all_items=[]
        for item_id,widgets in self.item_widgets.items():
            config_items=config.get("item_use",{}).get("items",[])+config.get("item_use",{}).get("custom_items",[])
            item=[i for i in config_items if i["id"]==item_id]
            if not item:
                continue
            item=item[0]
            item["enabled"]=widgets["enable_switch"].get()==1
            interval_val=int(widgets["interval_entry"].get())
            if widgets["interval_unit"].get()=="Minutes":
                interval_val*=60
            item["interval_seconds"]=interval_val
            item["amount"]=widgets["amount_entry"].get()
            item["biome_filter_mode"]=widgets["filter_mode"].get().lower()
            selected_biomes=[biome for biome,checkbox in widgets["biome_checkboxes"].items() if checkbox.get()==1]
            item["biome_filter"]=selected_biomes
            all_items.append(item)
        predefined_items=[item for item in all_items if not item["id"].startswith("custom_")]
        custom_items=[item for item in all_items if item["id"].startswith("custom_")]
        config["item_use"]["items"]=predefined_items
        config["item_use"]["custom_items"]=custom_items
        if self.config_manager.save_config(config):
            success_label=ctk.CTkLabel(self,text="✓ Settings saved successfully!",text_color="green",font=("Arial",12,"bold"))
            success_label.pack(pady=5)
            self.after(2000,success_label.destroy)
    def _update_execution_times(self):
        if self.item_executor.is_running:
            self.status_label.configure(text="Active - checking items every 0.5s")
        else:
            self.status_label.configure(text="Waiting for monitoring to start")
        for item_id,widgets in self.item_widgets.items():
            next_time=self.item_executor.get_next_execution_time(item_id)
            if next_time==0:
                widgets["next_exec_label"].configure(text="Next use in: --")
            else:
                remaining=max(0,next_time-time.time())
                if remaining==0:
                    widgets["next_exec_label"].configure(text="Next use in: Ready to execute")
                else:
                    minutes=int(remaining//60)
                    seconds=int(remaining%60)
                    widgets["next_exec_label"].configure(text=f"Next use in: {minutes}m {seconds}s")
        self.after(1000,self._update_execution_times)
