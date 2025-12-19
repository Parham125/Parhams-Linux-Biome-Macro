import customtkinter as ctk
from PIL import Image
import webbrowser
import os
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_resource_path
from gui.main_tab import MainTab
from gui.settings_tab import SettingsTab
from gui.credits_tab import CreditsTab
from gui.item_use_tab import ItemUseTab
from gui.anti_afk_tab import AntiAfkTab
from discord_webhook import send_status_webhook
class MainWindow(ctk.CTk):
    def __init__(self,config_manager,log_monitor,item_executor,afk_executor):
        super().__init__()
        self.config_manager=config_manager
        self.log_monitor=log_monitor
        self.item_executor=item_executor
        self.afk_executor=afk_executor
        self.config=self.config_manager.load_config()
        self.title("Parham's Linux Biome Macro")
        geometry=self.config.get("window_geometry","550x600")
        self.geometry(geometry)
        self.attributes("-topmost",True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        header_frame=ctk.CTkFrame(self,fg_color="transparent",height=40)
        header_frame.pack(fill="x",padx=10,pady=(10,0))
        header_frame.pack_propagate(False)
        icon_container=ctk.CTkFrame(header_frame,fg_color="transparent")
        icon_container.pack(side="left",padx=5)
        github_path=get_resource_path("assets/github.png")
        discord_path=get_resource_path("assets/discord.png")
        if os.path.exists(github_path):
            github_img=Image.open(github_path)
            github_img=github_img.resize((24,24),Image.Resampling.LANCZOS)
            github_ctk_img=ctk.CTkImage(light_image=github_img,dark_image=github_img,size=(24,24))
            github_btn=ctk.CTkButton(icon_container,image=github_ctk_img,text="",width=30,height=30,fg_color="transparent",hover_color="#1a1a1a",command=lambda: webbrowser.open("https://github.com/Parham125/Parhams-Linux-Biome-Macro"))
            github_btn.pack(side="left",padx=2)
        if os.path.exists(discord_path):
            discord_img=Image.open(discord_path)
            discord_img=discord_img.resize((24,24),Image.Resampling.LANCZOS)
            discord_ctk_img=ctk.CTkImage(light_image=discord_img,dark_image=discord_img,size=(24,24))
            discord_btn=ctk.CTkButton(icon_container,image=discord_ctk_img,text="",width=30,height=30,fg_color="transparent",hover_color="#1a1a1a",command=lambda: webbrowser.open("https://discord.gg/oppression"))
            discord_btn.pack(side="left",padx=2)
        self.tabview=ctk.CTkTabview(self)
        self.tabview.pack(fill="both",expand=True,padx=10,pady=(5,10))
        self.tabview.add("Main")
        self.tabview.add("Settings")
        self.tabview.add("Credits")
        self.tabview.add("Item Use")
        self.tabview.add("Anti-AFK")
        self.main_tab=MainTab(self.tabview.tab("Main"),self.config_manager,self.log_monitor,self.item_executor,self.afk_executor)
        self.main_tab.pack(fill="both",expand=True)
        self.settings_tab=SettingsTab(self.tabview.tab("Settings"),self.config_manager,self._on_mode_change)
        self.settings_tab.pack(fill="both",expand=True)
        self.credits_tab=CreditsTab(self.tabview.tab("Credits"))
        self.credits_tab.pack(fill="both",expand=True)
        self.item_use_tab=ItemUseTab(self.tabview.tab("Item Use"),self.config_manager,self.item_executor)
        self.item_use_tab.pack(fill="both",expand=True)
        self.anti_afk_tab=AntiAfkTab(self.tabview.tab("Anti-AFK"),self.config_manager,self.afk_executor)
        self.anti_afk_tab.pack(fill="both",expand=True)
        self._update_tab_states()
        self.protocol("WM_DELETE_WINDOW",self._on_close)
    def _on_mode_change(self,mode):
        self._update_tab_states()
    def _update_tab_states(self):
        config=self.config_manager.load_config()
        mode=config.get("mode","single")
        if mode=="multi":
            for widget in self.tabview.tab("Item Use").winfo_children():
                widget.pack_forget()
            ctk.CTkLabel(self.tabview.tab("Item Use"),text="Item Use is disabled in Multi mode",font=("Arial",16),text_color="gray").pack(expand=True)
            for widget in self.tabview.tab("Anti-AFK").winfo_children():
                widget.pack_forget()
            ctk.CTkLabel(self.tabview.tab("Anti-AFK"),text="Anti-AFK is disabled in Multi mode",font=("Arial",16),text_color="gray").pack(expand=True)
        else:
            for widget in self.tabview.tab("Item Use").winfo_children():
                widget.destroy()
            self.item_use_tab=ItemUseTab(self.tabview.tab("Item Use"),self.config_manager,self.item_executor)
            self.item_use_tab.pack(fill="both",expand=True)
            for widget in self.tabview.tab("Anti-AFK").winfo_children():
                widget.destroy()
            self.anti_afk_tab=AntiAfkTab(self.tabview.tab("Anti-AFK"),self.config_manager,self.afk_executor)
            self.anti_afk_tab.pack(fill="both",expand=True)
    def _on_close(self):
        if self.log_monitor.is_running:
            webhook_url=self.config.get("webhook_url","")
            send_status_webhook(webhook_url,False)
        self.config=self.config_manager.load_config()
        self.config["window_geometry"]=self.geometry()
        self.config_manager.save_config(self.config)
        self.log_monitor.stop()
        self.item_executor.stop()
        self.afk_executor.stop()
        self.destroy()
