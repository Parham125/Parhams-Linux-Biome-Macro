import json
import os
from biome_data import BIOMES
FORCE_PING_BIOMES=["CYBERSPACE","GLITCHED","DREAMSPACE"]
class ConfigManager:
    def __init__(self,config_path="config.json"):
        self.config_path=config_path
    def get_default_config(self):
        biome_settings={biome: "off" for biome in BIOMES}
        for biome in FORCE_PING_BIOMES:
            if biome in biome_settings:
                biome_settings[biome]="send_everyone"
        return {"webhook_url": "","ps_link": "","biome_settings": biome_settings,"last_biome": "","window_geometry": "550x600","item_use": {"coordinates": {"inventory_button": {"x": 0,"y": 0},"items_button": {"x": 0,"y": 0},"search_box": {"x": 0,"y": 0},"first_item_box": {"x": 0,"y": 0},"amount_box": {"x": 0,"y": 0},"use_button": {"x": 0,"y": 0},"close_button": {"x": 0,"y": 0}},"items": [{"id": "biome_randomizer","name": "Biome Randomizer","enabled": False,"interval_seconds": 2100,"biome_filter_mode": "blacklist","biome_filter": ["CYBERSPACE","GLITCHED","DREAMSPACE"],"amount": "1"},{"id": "strange_controller","name": "Strange Controller","enabled": False,"interval_seconds": 1200,"biome_filter_mode": "blacklist","biome_filter": ["CYBERSPACE","GLITCHED","DREAMSPACE"],"amount": "1"}],"custom_items": []}}
    def load_config(self):
        if not os.path.exists(self.config_path):
            return self.get_default_config()
        try:
            with open(self.config_path,"r") as f:
                config=json.load(f)
            default_config=self.get_default_config()
            for key in default_config:
                if key not in config:
                    config[key]=default_config[key]
            if "biome_settings" in config:
                for biome in BIOMES:
                    if biome not in config["biome_settings"]:
                        config["biome_settings"][biome]="off"
                for biome in FORCE_PING_BIOMES:
                    if biome in BIOMES and biome not in config["biome_settings"]:
                        config["biome_settings"][biome]="send_everyone"
            return config
        except:
            return self.get_default_config()
    def save_config(self,config):
        try:
            with open(self.config_path,"w") as f:
                json.dump(config,f,indent=2)
            return True
        except:
            return False
