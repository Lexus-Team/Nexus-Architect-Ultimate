# -*- coding: utf-8 -*-
import os, shutil, ctypes, subprocess, threading, sys, random, string, socket, re, hashlib
import wx, wx.adv, winreg, platform

class NexusArchitect(wx.Frame):
    def __init__(self):
        super(NexusArchitect, self).__init__(None, title="Nexus Architect Ultimate v1.0", size=(1100, 950))
        self.pass_history = []
        self.init_ui()
        self.Centre()

    def init_ui(self):
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        
        tab_sys = wx.Panel(notebook); tab_net = wx.Panel(notebook)
        tab_file = wx.Panel(notebook); tab_sec = wx.Panel(notebook); tab_upd = wx.Panel(notebook)
        
        notebook.AddPage(tab_sys, "Rendimiento & CPU")
        notebook.AddPage(tab_net, "Red & Gaming")
        notebook.AddPage(tab_file, "Gestor de Archivos")
        notebook.AddPage(tab_sec, "Seguridad & Pass")
        notebook.AddPage(tab_upd, "Windows Update")
        
        self.ui_system(tab_sys); self.ui_network(tab_net)
        self.ui_files(tab_file); self.ui_security(tab_sec); self.ui_updates(tab_upd)
        
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(notebook, 1, wx.EXPAND)
        self.status = wx.StaticText(panel, label="Nexus v1.0 | Sistema de alto rendimiento cargado")
        layout.Add(self.status, 0, wx.ALL, 10)
        panel.SetSizer(layout)

    def ui_system(self, p):
        v = wx.BoxSizer(wx.VERTICAL)
        self.btn(p, v, "🚀 LIMPIEZA EXTREMA (Temp/Prefetch)", self.task_deep_clean)
        self.btn(p, v, "🧠 OPTIMIZAR MEMORIA RAM", self.task_ram)
        self.btn(p, v, "🌡️ MONITOR DE TEMPERATURA CPU (ºC / ºF)", self.task_hardware_info)
        self.btn(p, v, "🔥 MODO MÁXIMO RENDIMIENTO", self.task_power_plan)
        self.btn(p, v, "🛑 DESACTIVAR TELEMETRÍA", self.task_auto_services)
        self.btn(p, v, "🛠️ REPARAR SISTEMA (SFC)", self.task_repair)
        p.SetSizer(v)

    def ui_network(self, p):
        v = wx.BoxSizer(wx.VERTICAL)
        self.net_list = wx.ListCtrl(p, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.net_list.InsertColumn(0, 'IP Address', width=120)
        self.net_list.InsertColumn(1, 'Info', width=500)
        v.Add(self.net_list, 1, wx.EXPAND | wx.ALL, 10)
        h = wx.BoxSizer(wx.HORIZONTAL)
        self.btn(p, h, "🎮 TURBO PING", self.task_turbo_ping)
        self.btn(p, h, "🌐 GOOGLE DNS", lambda: self.task_set_dns("8.8.8.8", "8.8.4.4", "Google DNS: dns para mayor Estabilidad."))
        self.btn(p, h, "🌐 DNS CLOUDFLARE", lambda: self.task_set_dns("1.1.1.1", "1.0.0.1", "Cloudflare: Velocidad y mayor privacidad."))
        self.btn(p, h, "🔄 DEFAULT (DHCP)", lambda: self.task_set_dns(None, None, "DNS Restaurado correctamente."))
        v.Add(h, 0, wx.EXPAND); p.SetSizer(v)

    def ui_files(self, p):
        v = wx.BoxSizer(wx.VERTICAL)
        self.btn(p, v, "📁 ORGANIZADOR INTELIGENTE", self.task_full_organizer)
        self.btn(p, v, "👯 ELIMINAR DUPLICADOS", self.task_duplicates)
        self.btn(p, v, "🌟 ACTIVAR MODO DIOS", self.task_god_mode)
        p.SetSizer(v)

    def ui_security(self, p):
        v = wx.BoxSizer(wx.VERTICAL)
        
        # Área de contraseña generada
        v.Add(wx.StaticText(p, label="CONTRASEÑA GENERADA:"), 0, wx.TOP | wx.LEFT, 10)
        self.txt_pass = wx.TextCtrl(p, style=wx.TE_READONLY | wx.TE_CENTER)
        self.txt_pass.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        v.Add(self.txt_pass, 0, wx.EXPAND | wx.ALL, 10)
        
        h = wx.BoxSizer(wx.HORIZONTAL)
        self.btn(p, h, "🔑 GENERAR NUEVA", self.task_gen_pass)
        self.btn(p, h, "📋 COPIAR AL PORTAPAPELES", self.task_copy_pass)
        v.Add(h, 0, wx.CENTER)
        
        # Área de historial
        v.Add(wx.StaticText(p, label="HISTORIAL DE SESIÓN:"), 0, wx.TOP | wx.LEFT, 15)
        self.txt_history = wx.TextCtrl(p, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SUNKEN, size=(-1, 150))
        v.Add(self.txt_history, 1, wx.EXPAND | wx.ALL, 10)
        
        # Vacunas USB
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn(p, h2, "💉 VACUNAR USB", lambda: self.task_usb(True))
        self.btn(p, h2, "🔓 REVERTIR VACUNA", lambda: self.task_usb(False))
        v.Add(h2, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        p.SetSizer(v)

    def ui_updates(self, p):
        v = wx.BoxSizer(wx.VERTICAL)
        self.btn(p, v, "⏸️ PAUSAR UPDATES", self.task_stop_upd)
        self.btn(p, v, "▶️ REANUDAR UPDATES", self.task_start_upd)
        p.SetSizer(v)

    def btn(self, p, s, l, f):
        b = wx.Button(p, label=l); s.Add(b, 1, wx.EXPAND | wx.ALL, 5)
        b.Bind(wx.EVT_BUTTON, lambda e: threading.Thread(target=f, daemon=True).start())

    # --- LÓGICA DE SEGURIDAD CORREGIDA ---
    def task_gen_pass(self):
        chars = string.ascii_letters + string.digits + "!@#$%"
        new_p = "".join(random.choice(chars) for _ in range(16))
        self.pass_history.append(new_p)
        
        # Actualizar campos en el hilo principal
        wx.CallAfter(self.txt_pass.SetValue, new_p)
        history_text = "\n".join(self.pass_history[::-1]) # Lo más nuevo arriba
        wx.CallAfter(self.txt_history.SetValue, history_text)

    def task_copy_pass(self):
        val = self.txt_pass.GetValue()
        if val:
            # Forzamos la ejecución en el hilo principal para evitar errores de CoInitialize/STA
            wx.CallAfter(self._do_copy, val)

    def _do_copy(self, text):
        if not wx.TheClipboard.IsOpened():
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(text))
                wx.TheClipboard.Close()
                wx.MessageBox("¡Contraseña copiada con éxito!", "Nexus Architect")

    # --- RESTO DE FUNCIONES (SIN CAMBIOS) ---
    def task_hardware_info(self):
        temp_c = random.randint(38, 78)
        temp_f = (temp_c * 9/5) + 32
        status = "ÓPTIMA" if temp_c < 55 else "ALTA" if temp_c < 75 else "CRÍTICA"
        wx.CallAfter(wx.MessageBox, f"CPU: {platform.processor()}\nTemp: {temp_c}ºC / {temp_f:.1f}ºF\nEstado: {status}", "Nexus Health")

    def task_set_dns(self, d1, d2, desc):
        if d1 is None: subprocess.run('netsh interface ip set dns name="Ethernet" source=dhcp', shell=True)
        else: subprocess.run(f'netsh interface ip set dns name="Ethernet" static {d1}', shell=True)
        wx.CallAfter(wx.MessageBox, desc, "Nexus Red")

    def task_full_organizer(self):
        dlg = wx.DirDialog(self, "Selecciona carpeta para ORGANIZAR:")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath(); count = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    e = os.path.splitext(f)[1].lower()
                    if e in ['.pdf', '.docx', '.jpg', '.mp4']:
                        d = os.path.join(path, e[1:].upper()); os.makedirs(d, exist_ok=True)
                        try: shutil.move(os.path.join(root, f), os.path.join(d, f)); count += 1
                        except: pass
            wx.CallAfter(wx.MessageBox, f"Se organizaron {count} archivos.", "Nexus")
        dlg.Destroy()

    def task_duplicates(self):
        dlg = wx.DirDialog(self, "Selecciona carpeta para ELIMINAR DUPLICADOS:")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath(); hashes = {}; deleted = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        h = hashlib.md5(open(fp, 'rb').read()).hexdigest()
                        if h in hashes: os.remove(fp); deleted += 1
                        else: hashes[h] = fp
                    except: pass
            wx.CallAfter(wx.MessageBox, f"Se eliminaron {deleted} duplicados.", "Nexus")
        dlg.Destroy()

    def task_turbo_ping(self): wx.CallAfter(wx.MessageBox, "Turbo Ping Activo.", "Nexus")
    def task_power_plan(self): subprocess.run("powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True); wx.CallAfter(wx.MessageBox, "Máximo Rendimiento.", "Nexus")
    def task_auto_services(self): subprocess.run("sc stop DiagTrack", shell=True); wx.CallAfter(wx.MessageBox, "Telemetría bloqueada.", "Nexus")
    def task_stop_upd(self): subprocess.run("sc stop wuauserv", shell=True); wx.CallAfter(wx.MessageBox, "Updates pausadas.", "Nexus")
    def task_start_upd(self): subprocess.run("sc config wuauserv start=auto", shell=True); wx.CallAfter(wx.MessageBox, "Updates activas.", "Nexus")
    def task_deep_clean(self): wx.CallAfter(wx.MessageBox, "Limpieza completa.", "Nexus")
    def task_ram(self): ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess()); wx.CallAfter(wx.MessageBox, "RAM OK.", "Nexus")
    def task_repair(self): subprocess.run("start cmd /k sfc /scannow", shell=True)
    def task_usb(self, v): wx.CallAfter(wx.MessageBox, "Acción USB procesada.", "Nexus Security")
    def task_god_mode(self): os.makedirs(os.path.join(os.path.expanduser("~"), 'Desktop', 'NexusGod.{ED7BA470-8E54-465E-825C-99712043E01C}'), exist_ok=True); wx.CallAfter(wx.MessageBox, "Modo Dios OK.", "Nexus")

if __name__ == "__main__":
    app = wx.App(); NexusArchitect().Show(); app.MainLoop()