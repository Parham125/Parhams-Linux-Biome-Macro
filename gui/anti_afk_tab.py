import customtkinter as ctk
import time
class AntiAfkTab(ctk.CTkFrame):
    def __init__(self,parent,config_manager,afk_executor):
        super().__init__(parent)
        self.config_manager=config_manager
        self.afk_executor=afk_executor
        ctk.CTkLabel(self,text="Anti-AFK Configuration",font=("Arial",18,"bold")).pack(pady=(30,20))
        config=self.config_manager.load_config()
        anti_afk_config=config.get("anti_afk",{})
        settings_frame=ctk.CTkFrame(self)
        settings_frame.pack(pady=20,padx=40,fill="x")
        self.enable_switch=ctk.CTkSwitch(settings_frame,text="Enable Anti-AFK",font=("Arial",14))
        self.enable_switch.pack(pady=20,padx=20,anchor="w")
        if anti_afk_config.get("enabled",False):
            self.enable_switch.select()
        interval_frame=ctk.CTkFrame(settings_frame,fg_color="transparent")
        interval_frame.pack(fill="x",padx=20,pady=10)
        ctk.CTkLabel(interval_frame,text="Press Space Every:",font=("Arial",13)).pack(side="left",padx=5)
        self.interval_entry=ctk.CTkEntry(interval_frame,width=100)
        self.interval_entry.insert(0,str(anti_afk_config.get("interval_seconds",300)))
        self.interval_entry.pack(side="left",padx=5)
        self.interval_unit=ctk.CTkSegmentedButton(interval_frame,values=["Seconds","Minutes"])
        self.interval_unit.set("Seconds")
        self.interval_unit.pack(side="left",padx=5)
        save_btn=ctk.CTkButton(settings_frame,text="Save Settings",command=self.save_settings,width=200,height=40,font=("Arial",14,"bold"))
        save_btn.pack(pady=30)
        status_frame=ctk.CTkFrame(self)
        status_frame.pack(pady=20,padx=40,fill="x")
        ctk.CTkLabel(status_frame,text="Status",font=("Arial",16,"bold")).pack(pady=(10,5),padx=20,anchor="w")
        self.status_label=ctk.CTkLabel(status_frame,text="Waiting for monitoring to start",font=("Arial",12))
        self.status_label.pack(pady=5,padx=20,anchor="w")
        self.next_press_label=ctk.CTkLabel(status_frame,text="Next press in: --",font=("Arial",11,"italic"))
        self.next_press_label.pack(pady=5,padx=20,anchor="w")
        info_frame=ctk.CTkFrame(self,fg_color="transparent")
        info_frame.pack(pady=20,padx=40,fill="both",expand=True)
        info_text="Anti-AFK will automatically press the Space key at your configured interval to prevent being kicked for inactivity.\n\nThis feature requires wmctrl to be installed:\nsudo apt install wmctrl"
        ctk.CTkLabel(info_frame,text=info_text,font=("Arial",11),text_color="gray",justify="left",wraplength=450).pack(pady=10)
        self._update_status()
    def save_settings(self):
        config=self.config_manager.load_config()
        interval_val=int(self.interval_entry.get())
        if self.interval_unit.get()=="Minutes":
            interval_val*=60
        anti_afk_config={"enabled": self.enable_switch.get()==1,"interval_seconds": interval_val}
        config["anti_afk"]=anti_afk_config
        if self.config_manager.save_config(config):
            success_label=ctk.CTkLabel(self,text="✓ Settings saved successfully!",text_color="green",font=("Arial",12,"bold"))
            success_label.pack(pady=5)
            self.after(2000,success_label.destroy)
            if self.afk_executor.is_running:
                self.afk_executor.stop()
                self.afk_executor.start()
    def _update_status(self):
        config=self.config_manager.load_config()
        if self.afk_executor.is_running and config.get("anti_afk",{}).get("enabled",False):
            self.status_label.configure(text="Active - pressing space at intervals")
            next_time=self.afk_executor.get_next_press_time()
            if next_time==0:
                self.next_press_label.configure(text="Next press in: --")
            else:
                remaining=max(0,next_time-time.time())
                if remaining==0:
                    self.next_press_label.configure(text="Next press in: Ready")
                else:
                    minutes=int(remaining//60)
                    seconds=int(remaining%60)
                    self.next_press_label.configure(text=f"Next press in: {minutes}m {seconds}s")
        else:
            self.status_label.configure(text="Waiting for monitoring to start")
            self.next_press_label.configure(text="Next press in: --")
        self.after(1000,self._update_status)
