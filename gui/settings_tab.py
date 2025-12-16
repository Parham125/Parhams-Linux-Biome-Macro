import customtkinter as ctk
from biome_data import BIOMES
from config_manager import FORCE_PING_BIOMES
class SettingsTab(ctk.CTkScrollableFrame):
    def __init__(self,parent,config_manager):
        super().__init__(parent)
        self.config_manager=config_manager
        self.biome_toggles={}
        ctk.CTkLabel(self,text="Discord Webhook URL",font=("Arial",14,"bold")).pack(pady=(20,5),anchor="w",padx=20)
        self.webhook_entry=ctk.CTkEntry(self,width=600,placeholder_text="https://discord.com/api/webhooks/...")
        self.webhook_entry.pack(pady=5,padx=20)
        ctk.CTkLabel(self,text="Private Server Link",font=("Arial",14,"bold")).pack(pady=(20,5),anchor="w",padx=20)
        self.ps_link_entry=ctk.CTkEntry(self,width=600,placeholder_text="https://www.roblox.com/games/...")
        self.ps_link_entry.pack(pady=5,padx=20)
        ctk.CTkLabel(self,text="Biome Notification Settings",font=("Arial",16,"bold")).pack(pady=(30,10),anchor="w",padx=20)
        biomes_frame=ctk.CTkFrame(self,fg_color="transparent")
        biomes_frame.pack(fill="both",expand=True,padx=20,pady=10)
        biome_list=list(BIOMES.keys())
        for idx,biome in enumerate(biome_list):
            row=idx//2
            col=idx%2
            biome_container=ctk.CTkFrame(biomes_frame)
            biome_container.grid(row=row,column=col,padx=10,pady=10,sticky="ew")
            biome_info=BIOMES[biome]
            label_text=f"{biome_info['emoji']} {biome}"
            ctk.CTkLabel(biome_container,text=label_text,font=("Arial",12)).pack(pady=5)
            toggle=ctk.CTkSegmentedButton(biome_container,values=["Off","Send","Send @everyone"])
            toggle.set("Off")
            toggle.pack(pady=5,padx=10)
            self.biome_toggles[biome]=toggle
        biomes_frame.columnconfigure(0,weight=1)
        biomes_frame.columnconfigure(1,weight=1)
        save_btn=ctk.CTkButton(self,text="Save Settings",command=self.save_settings,width=200,height=40,font=("Arial",14,"bold"))
        save_btn.pack(pady=30)
        self.load_settings()
    def load_settings(self):
        config=self.config_manager.load_config()
        self.webhook_entry.delete(0,"end")
        self.webhook_entry.insert(0,config.get("webhook_url",""))
        self.ps_link_entry.delete(0,"end")
        self.ps_link_entry.insert(0,config.get("ps_link",""))
        for biome,toggle in self.biome_toggles.items():
            setting=config.get("biome_settings",{}).get(biome,"off")
            if setting=="off":
                toggle.set("Off")
            elif setting=="send":
                toggle.set("Send")
            elif setting=="send_everyone":
                toggle.set("Send @everyone")
    def save_settings(self):
        config=self.config_manager.load_config()
        force_ping_changed=False
        for biome in FORCE_PING_BIOMES:
            if biome in self.biome_toggles:
                current_value=self.biome_toggles[biome].get()
                if current_value!="Send @everyone":
                    force_ping_changed=True
                    break
        if force_ping_changed:
            self._show_force_ping_warning(config)
        else:
            self._apply_settings(config)
    def _apply_settings(self,config):
        config["webhook_url"]=self.webhook_entry.get()
        config["ps_link"]=self.ps_link_entry.get()
        for biome,toggle in self.biome_toggles.items():
            value=toggle.get()
            if value=="Off":
                config["biome_settings"][biome]="off"
            elif value=="Send":
                config["biome_settings"][biome]="send"
            elif value=="Send @everyone":
                config["biome_settings"][biome]="send_everyone"
        if self.config_manager.save_config(config):
            self._show_save_success()
    def _show_force_ping_warning(self,config):
        dialog=ctk.CTkToplevel(self)
        dialog.title("⚠️ Warning: Rare Biome Protection")
        dialog.geometry("500x250")
        dialog.transient(self)
        dialog.after(100,dialog.grab_set)
        message_label=ctk.CTkLabel(dialog,text="CYBERSPACE, GLITCHED, and DREAMSPACE are extremely rare biomes.\n\nDisabling @everyone ping may result in wasted biomes if players\ndon't join quickly.\n\nDo you accept the risk of potentially wasting these rare biomes?",font=("Arial",12),justify="center")
        message_label.pack(pady=30,padx=20)
        button_frame=ctk.CTkFrame(dialog,fg_color="transparent")
        button_frame.pack(pady=20)
        cancel_btn=ctk.CTkButton(button_frame,text="Cancel",command=lambda: self._cancel_warning(dialog),width=150,height=40,fg_color="gray")
        cancel_btn.pack(side="left",padx=10)
        accept_btn=ctk.CTkButton(button_frame,text="I Accept the Risk",command=lambda: self._accept_warning(dialog,config),width=150,height=40,fg_color="red")
        accept_btn.pack(side="left",padx=10)
    def _cancel_warning(self,dialog):
        self.load_settings()
        dialog.destroy()
    def _accept_warning(self,dialog,config):
        dialog.destroy()
        self._apply_settings(config)
    def _show_save_success(self):
        success_label=ctk.CTkLabel(self,text="✓ Settings saved successfully!",text_color="green",font=("Arial",12,"bold"))
        success_label.pack(pady=5)
        self.after(2000,success_label.destroy)
