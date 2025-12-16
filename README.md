# Parham's Linux Biome Macro

A Python GUI application for monitoring Sol's RNG (Roblox game) biome changes and automating item usage with Discord webhook notifications.

## Features

- **Real-time Biome Monitoring**: Automatically detects biome changes by monitoring Sober/Vinegar log files
- **Discord Webhooks**: Sends rich embed notifications with customizable settings per biome
- **Item Automation**: Automated item usage with configurable intervals and biome-specific filters
- **Per-Biome Settings**: Configure notifications individually (Off/Send/Send @everyone)
- **Auto-Update**: Built-in updater for seamless updates
- **Dark Theme GUI**: Modern CustomTkinter interface with always-on-top option
- **Persistent Configuration**: Settings saved in config.json

## Supported Biomes (16)

WINDY • RAINY • SNOWY • SAND STORM • HELL • STARFALL • CORRUPTION • NULL • GLITCHED • DREAMSPACE • CYBERSPACE • BLOOD RAIN • PUMPKIN MOON • GRAVEYARD • HEAVEN • NORMAL

## Requirements

- **OS**: Linux (tested on systems with Sober/Vinegar)
- **Python**: 3.13+
- **Dependencies**: See requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Parham's Linux Macro"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install system dependencies (for item automation):
```bash
sudo apt install wmctrl  # For window focusing
```

## Usage

Run the application:
```bash
python3.13 main.py
```

### Configuration

1. **Settings Tab**:
   - Add your Discord webhook URL
   - Configure your private server link
   - Set per-biome notification preferences

2. **Item Use Tab**:
   - Enable/disable automated item usage
   - Configure coordinates for UI automation
   - Set item intervals and biome filters (whitelist/blacklist)
   - Add custom items

3. **Main Tab**:
   - View current biome
   - Start/Stop monitoring
   - Check monitoring status

## How It Works

The application monitors the Sober log file located at:
```
~/.var/app/org.vinegarhq.Sober/data/sober/sober_logs/latest.log
```

It parses BloxstrapRPC JSON data from the log file to detect biome changes:
```json
[BloxstrapRPC] {"command":"SetRichPresence","data":{"largeImage":{"hoverText":"BIOME_NAME"}}}
```

When a new biome is detected, it:
1. Checks the biome's notification setting
2. Sends a Discord webhook with embed (if configured)
3. Updates the GUI display
4. Triggers item automation (if enabled and biome matches filters)

## Discord Webhook Format

Biome notifications include:
- **Title**: "Biome Started: {biome_name}"
- **Description**: Join link with your private server
- **Color**: Biome-specific hex color
- **Thumbnail**: Biome image
- **Footer**: "Parham's Linux Biome Macro"
- **Timestamp**: Current UTC time
- **@everyone mention**: Optional (configurable per biome)

## Item Automation

The item executor can automatically use items in-game at configured intervals. Features:
- Biome-specific filters (whitelist/blacklist)
- Customizable intervals per item
- Configurable amount per usage
- Automatic window focusing and UI interaction
- Predefined items: Biome Randomizer, Strange Controller

## Project Structure

```
.
├── main.py                 # Application entry point
├── biome_data.py           # Biome definitions (emoji, color, thumbnail)
├── item_data.py            # Predefined items
├── config_manager.py       # Configuration persistence
├── log_monitor.py          # Log file monitoring (threading)
├── item_executor.py        # Item automation (pynput)
├── discord_webhook.py      # Discord webhook sender
├── updater.py              # Auto-update functionality
├── utils.py                # Utility functions
├── gui/
│   ├── main_window.py      # Main application window
│   ├── main_tab.py         # Biome display and monitoring controls
│   ├── settings_tab.py     # Webhook and notification settings
│   ├── item_use_tab.py     # Item automation configuration
│   └── credits_tab.py      # Credits and attribution
└── requirements.txt        # Python dependencies
```

## Configuration File

Settings are stored in `config.json`:
```json
{
  "webhook_url": "https://discord.com/api/webhooks/...",
  "ps_link": "https://www.roblox.com/games/...",
  "last_biome": "NORMAL",
  "biome_settings": {
    "HELL": "send_everyone",
    "STARFALL": "send",
    "NORMAL": "off"
  },
  "item_use": {
    "enabled": true,
    "coordinates": {...},
    "items": [...],
    "custom_items": [...]
  }
}
```

## Security & Privacy

- No data is collected or transmitted except to your configured Discord webhook
- All credentials (webhook URLs) are stored locally in config.json
- Item automation uses local mouse/keyboard control only

## Troubleshooting

**Log file not found error:**
- Ensure Sober/Vinegar is installed and has run at least once
- Check that the log path exists: `~/.var/app/org.vinegarhq.Sober/data/sober/sober_logs/latest.log`

**Webhook not sending:**
- Verify your webhook URL is valid
- Check your internet connection
- Ensure Discord webhook is not rate-limited

**Item automation not working:**
- Install wmctrl: `sudo apt install wmctrl`
- Configure UI coordinates in Item Use tab
- Ensure Sober window is accessible (not minimized when setting coordinates)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Attribution

When distributing or modifying this software, you must include proper attribution as specified in the [NOTICE](NOTICE) file.

## Credits

**Developer**: Parham
**Project**: Sol's RNG Biome Macro for Linux

Special thanks to:
- Manas (Discord: referenced in credits tab)
- The Sol's RNG community
- CustomTkinter developers
- Sober/Vinegar developers

## Disclaimer

This tool is for educational purposes. Use at your own risk. The developers are not responsible for any bans or issues that may arise from using automation tools in Roblox games. Always review the game's Terms of Service before using automation tools.
