import subprocess

# Definiere den PowerShell-Befehle
commands = [
    r"cd C:\Users\kamal\PycharmProjects\RB_Fonds_Analytics",
    r"py -m streamlit run Main.py"
]

# PowerShell-Befehle joinen
command = "; ".join(commands)

# Führe den PowerShell-Code mit den obigen befehlen aus
result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
