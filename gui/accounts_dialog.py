import customtkinter as ctk
from tkinter import filedialog
class AccountsDialog(ctk.CTkToplevel):
    def __init__(self,parent,existing_accounts,account_to_edit=None):
        super().__init__(parent)
        self.result=None
        self.existing_accounts=existing_accounts
        self.account_to_edit=account_to_edit
        self.title("Add Account" if not account_to_edit else "Edit Account")
        self.geometry("500x380")
        self.transient(parent)
        self.after(100,self.grab_set)
        ctk.CTkLabel(self,text="Account Identifier",font=("Arial",12,"bold")).pack(pady=(20,5),anchor="w",padx=20)
        self.identifier_entry=ctk.CTkEntry(self,width=460,placeholder_text="e.g., Account1, Main, Alt1")
        self.identifier_entry.pack(pady=5,padx=20)
        ctk.CTkLabel(self,text="Log File Path",font=("Arial",12,"bold")).pack(pady=(15,5),anchor="w",padx=20)
        log_frame=ctk.CTkFrame(self,fg_color="transparent")
        log_frame.pack(pady=5,padx=20,fill="x")
        self.log_path_entry=ctk.CTkEntry(log_frame,width=380,placeholder_text="~/.var/app/org.vinegarhq.Sober/...")
        self.log_path_entry.pack(side="left",padx=(0,5))
        browse_btn=ctk.CTkButton(log_frame,text="Browse",width=70,command=self._browse_log_file)
        browse_btn.pack(side="left")
        ctk.CTkLabel(self,text="Private Server Link",font=("Arial",12,"bold")).pack(pady=(15,5),anchor="w",padx=20)
        self.ps_link_entry=ctk.CTkEntry(self,width=460,placeholder_text="https://www.roblox.com/games/...")
        self.ps_link_entry.pack(pady=5,padx=20)
        self.error_label=ctk.CTkLabel(self,text="",text_color="red",font=("Arial",10))
        self.error_label.pack(pady=5)
        button_frame=ctk.CTkFrame(self,fg_color="transparent")
        button_frame.pack(pady=20)
        cancel_btn=ctk.CTkButton(button_frame,text="Cancel",command=self.destroy,width=120,fg_color="gray")
        cancel_btn.pack(side="left",padx=10)
        save_btn=ctk.CTkButton(button_frame,text="Save",command=self._save,width=120)
        save_btn.pack(side="left",padx=10)
        if account_to_edit:
            self.identifier_entry.insert(0,account_to_edit["identifier"])
            self.log_path_entry.insert(0,account_to_edit["log_path"])
            self.ps_link_entry.insert(0,account_to_edit["ps_link"])
    def _browse_log_file(self):
        filename=filedialog.askopenfilename(title="Select Log File",filetypes=[("Log Files","*.log"),("All Files","*.*")])
        if filename:
            self.log_path_entry.delete(0,"end")
            self.log_path_entry.insert(0,filename)
    def _save(self):
        identifier=self.identifier_entry.get().strip()
        log_path=self.log_path_entry.get().strip()
        ps_link=self.ps_link_entry.get().strip()
        if not identifier:
            self.error_label.configure(text="Identifier is required")
            return
        if not log_path:
            self.error_label.configure(text="Log file path is required")
            return
        for acc in self.existing_accounts:
            if acc["identifier"]==identifier and (not self.account_to_edit or self.account_to_edit["identifier"]!=identifier):
                self.error_label.configure(text="Identifier already exists")
                return
        self.result={"identifier": identifier,"log_path": log_path,"ps_link": ps_link}
        self.destroy()
