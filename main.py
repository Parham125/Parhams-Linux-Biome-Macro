#!/usr/bin/env python
from config_manager import ConfigManager
from log_monitor import LogMonitor
from item_executor import ItemExecutor
from gui.main_window import MainWindow
from updater import auto_update
def main():
    auto_update()
    config_manager=ConfigManager()
    log_path="~/.var/app/org.vinegarhq.Sober/data/sober/sober_logs/latest.log"
    log_monitor=LogMonitor(log_path,lambda biome: None)
    item_executor=ItemExecutor(config_manager)
    app=MainWindow(config_manager,log_monitor,item_executor)
    item_executor.set_window(app)
    log_monitor.callback=app.main_tab.on_biome_detected
    app.mainloop()
if __name__=="__main__":
    main()
