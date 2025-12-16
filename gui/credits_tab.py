import customtkinter as ctk
from PIL import Image
import webbrowser
import os
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_resource_path
class CreditsTab(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        container=ctk.CTkFrame(self,fg_color="transparent")
        container.pack(expand=True)
        credits_frame=ctk.CTkFrame(container,fg_color="transparent")
        credits_frame.pack(pady=20)
        credits_data=[{"image": "assets/Parham.png","name": "Parham","role": "Main Developer","link": None},{"image": "assets/Manas.png","name": "Manas","role": "Helper","link": "https://discord.gg/oppression"},{"image": "assets/Maxstellar.png","name": "Maxstellar","role": "Biome Icons","link": None}]
        for i,credit in enumerate(credits_data):
            credit_frame=ctk.CTkFrame(credits_frame,fg_color="transparent")
            credit_frame.grid(row=0,column=i,padx=30)
            img_path=get_resource_path(credit["image"])
            if os.path.exists(img_path):
                img=Image.open(img_path)
                img=img.resize((100,100),Image.Resampling.LANCZOS)
                ctk_img=ctk.CTkImage(light_image=img,dark_image=img,size=(100,100))
                img_label=ctk.CTkLabel(credit_frame,image=ctk_img,text="")
                img_label.pack()
            name_frame=ctk.CTkFrame(credit_frame,fg_color="transparent")
            name_frame.pack(pady=5)
            name_label=ctk.CTkLabel(name_frame,text=credit["name"],font=("Arial",18,"bold"))
            name_label.pack(side="left")
            if credit["link"]:
                discord_icon_path=get_resource_path("assets/discord.png")
                if os.path.exists(discord_icon_path):
                    discord_icon_img=Image.open(discord_icon_path)
                    discord_icon_img=discord_icon_img.resize((18,18),Image.Resampling.LANCZOS)
                    discord_icon_ctk=ctk.CTkImage(light_image=discord_icon_img,dark_image=discord_icon_img,size=(18,18))
                    discord_badge=ctk.CTkButton(name_frame,image=discord_icon_ctk,text="",width=24,height=24,fg_color="transparent",hover_color="#1a1a1a",command=lambda url=credit["link"]: webbrowser.open(url))
                    discord_badge.pack(side="left",padx=5)
            role_label=ctk.CTkLabel(credit_frame,text=credit["role"],font=("Arial",13),text_color="gray70")
            role_label.pack(pady=2)
