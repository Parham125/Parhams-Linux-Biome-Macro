import requests
from datetime import datetime
from biome_data import BIOMES
from utils import get_version
def send_status_webhook(webhook_url,is_starting):
    if not webhook_url:
        return False
    if is_starting:
        embed={"title": "✅ Monitoring Started","description": "Biome monitoring is now active","color": 0x00FF00,"footer": {"text": f"Parham's Linux Biome Macro v{get_version()}"},"timestamp": datetime.utcnow().isoformat()}
    else:
        embed={"title": "🛑 Monitoring Stopped","description": "Biome monitoring has been stopped","color": 0xFF0000,"footer": {"text": f"Parham's Linux Biome Macro v{get_version()}"},"timestamp": datetime.utcnow().isoformat()}
    payload={"embeds": [embed]}
    try:
        response=requests.post(webhook_url,json=payload,timeout=10)
        return response.status_code in [200,204]
    except:
        return False
def send_biome_webhook(webhook_url,biome_name,ps_link,send_everyone,account_identifier=None):
    if not webhook_url or biome_name not in BIOMES:
        return False
    biome_info=BIOMES[biome_name]
    title=f"Biome Started: {biome_name}"
    if account_identifier:
        description=f"Account: `{account_identifier}`\n\nJoin the server below:\n{ps_link}" if ps_link else f"Account: `{account_identifier}`\n\nPrivate Server Link not configured"
    else:
        description=f"Join the server below:\n{ps_link}" if ps_link else "Private Server Link not configured"
    embed={"title": title,"description": description,"color": int(biome_info["color"],16),"footer": {"text": f"Parham's Linux Biome Macro v{get_version()}"},"timestamp": datetime.utcnow().isoformat()}
    if biome_info["thumbnail_url"]:
        embed["thumbnail"]={"url": biome_info["thumbnail_url"]}
    payload={"content": "@everyone" if send_everyone else "","embeds": [embed]}
    try:
        response=requests.post(webhook_url,json=payload,timeout=10)
        return response.status_code in [200,204]
    except:
        return False
def send_biome_ended_webhook(webhook_url,biome_name,account_identifier=None):
    if not webhook_url or biome_name not in BIOMES:
        return False
    biome_info=BIOMES[biome_name]
    title=f"Biome Ended: {biome_name}"
    description=f"Account: `{account_identifier}`" if account_identifier else ""
    embed={"title": title,"description": description,"color": int(biome_info["color"],16),"footer": {"text": f"Parham's Linux Biome Macro v{get_version()}"},"timestamp": datetime.utcnow().isoformat()}
    payload={"embeds": [embed]}
    try:
        response=requests.post(webhook_url,json=payload,timeout=10)
        return response.status_code in [200,204]
    except:
        return False
