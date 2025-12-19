import customtkinter as ctk
from biome_data import BIOMES
from discord_webhook import send_biome_webhook,send_status_webhook,send_biome_ended_webhook
import os
class MainTab(ctk.CTkFrame):
    def __init__(self,parent,config_manager,log_monitor,item_executor,afk_executor):
        super().__init__(parent)
        self.config_manager=config_manager
        self.log_monitor=log_monitor
        self.item_executor=item_executor
        self.afk_executor=afk_executor
        self.is_monitoring=False
        main_frame=ctk.CTkFrame(self,fg_color="transparent")
        main_frame.pack(expand=True)
        self.biome_display_frame=ctk.CTkFrame(main_frame,width=500,height=200,corner_radius=20)
        self.biome_display_frame.pack(pady=30)
        self.biome_display_frame.pack_propagate(False)
        self.biome_label=ctk.CTkLabel(self.biome_display_frame,text="🌳 NORMAL",font=("Arial",36,"bold"))
        self.biome_label.pack(expand=True)
        status_frame=ctk.CTkFrame(main_frame,fg_color="transparent")
        status_frame.pack(pady=10)
        ctk.CTkLabel(status_frame,text="Status:",font=("Arial",14)).pack(side="left",padx=5)
        self.status_indicator=ctk.CTkLabel(status_frame,text="●",font=("Arial",20),text_color="red")
        self.status_indicator.pack(side="left")
        self.status_text=ctk.CTkLabel(status_frame,text="Stopped",font=("Arial",14))
        self.status_text.pack(side="left",padx=5)
        self.toggle_btn=ctk.CTkButton(main_frame,text="Start Monitoring",command=self.toggle_monitoring,width=200,height=40,font=("Arial",14,"bold"))
        self.toggle_btn.pack(pady=20)
        self.error_label=ctk.CTkLabel(main_frame,text="",text_color="red",font=("Arial",12))
        self.error_label.pack(pady=5)
        config=self.config_manager.load_config()
        last_biome=config.get("last_biome","NORMAL")
        if last_biome in BIOMES:
            self.update_biome_display(last_biome)
    def toggle_monitoring(self):
        config=self.config_manager.load_config()
        webhook_url=config.get("webhook_url","")
        mode=config.get("mode","single")
        accounts=config.get("accounts",[])
        if not self.is_monitoring:
            self.log_monitor.set_mode(mode,accounts)
            if self.log_monitor.start():
                self.is_monitoring=True
                if mode=="single":
                    self.item_executor.start()
                    self.afk_executor.start()
                self.status_indicator.configure(text_color="green")
                self.status_text.configure(text="Running")
                self.toggle_btn.configure(text="Stop Monitoring")
                self.error_label.configure(text="")
                if webhook_url:
                    send_status_webhook(webhook_url,True)
            else:
                if mode=="single":
                    self.error_label.configure(text="Error: Log file not found!")
                else:
                    self.error_label.configure(text="Error: No valid log files found!")
        else:
            self.log_monitor.stop()
            self.item_executor.stop()
            self.afk_executor.stop()
            self.is_monitoring=False
            self.status_indicator.configure(text_color="red")
            self.status_text.configure(text="Stopped")
            self.toggle_btn.configure(text="Start Monitoring")
            if webhook_url:
                send_status_webhook(webhook_url,False)
    def on_biome_detected(self,biome_name,account_identifier=None):
        self.after(0,lambda: self._handle_biome_change(biome_name,account_identifier))
    def _handle_biome_change(self,biome_name,account_identifier=None):
        config=self.config_manager.load_config()
        mode=config.get("mode","single")
        webhook_url=config.get("webhook_url","")
        if mode=="single":
            previous_biome=config.get("last_biome")
            if biome_name==previous_biome:
                return
            ps_link=config.get("ps_link","")
            if previous_biome and previous_biome in BIOMES and webhook_url:
                send_biome_ended_webhook(webhook_url,previous_biome,None)
        else:
            last_biome_key=f"last_biome_{account_identifier}" if account_identifier else "last_biome"
            previous_biome=config.get(last_biome_key)
            if biome_name==previous_biome:
                return
            ps_link=""
            for account in config.get("accounts",[]):
                if account["identifier"]==account_identifier:
                    ps_link=account["ps_link"]
                    break
            if previous_biome and previous_biome in BIOMES and webhook_url:
                send_biome_ended_webhook(webhook_url,previous_biome,account_identifier)
        setting=config.get("biome_settings",{}).get(biome_name,"off")
        if setting!="off":
            webhook_url=config.get("webhook_url","")
            send_everyone=(setting=="send_everyone")
            success=send_biome_webhook(webhook_url,biome_name,ps_link,send_everyone,account_identifier)
            if success:
                if mode=="single":
                    config["last_biome"]=biome_name
                else:
                    last_biome_key=f"last_biome_{account_identifier}" if account_identifier else "last_biome"
                    config[last_biome_key]=biome_name
                self.config_manager.save_config(config)
            else:
                self.error_label.configure(text="Failed to send webhook!")
                self.after(3000,lambda: self.error_label.configure(text=""))
        else:
            if mode=="single":
                config["last_biome"]=biome_name
            else:
                last_biome_key=f"last_biome_{account_identifier}" if account_identifier else "last_biome"
                config[last_biome_key]=biome_name
            self.config_manager.save_config(config)
        display_text=biome_name
        if account_identifier:
            display_text=f"[{account_identifier}] {biome_name}"
        self.update_biome_display(display_text)
    def update_biome_display(self,display_text):
        biome_name=display_text
        if "[" in display_text and "]" in display_text:
            biome_name=display_text.split("]")[-1].strip()
        if biome_name not in BIOMES:
            return
        biome_info=BIOMES[biome_name]
        label_text=f"{biome_info['emoji']} {display_text}" if "[" not in display_text else f"{biome_info['emoji']} {display_text}"
        self.biome_label.configure(text=label_text)
        color_hex=biome_info["color"]
        try:
            color_int=int(color_hex,16)
            r=(color_int>>16)&0xFF
            g=(color_int>>8)&0xFF
            b=color_int&0xFF
            dark_r=int(r*0.3)
            dark_g=int(g*0.3)
            dark_b=int(b*0.3)
            bg_color=f"#{dark_r:02x}{dark_g:02x}{dark_b:02x}"
            self.biome_display_frame.configure(fg_color=bg_color)
        except:
            pass
