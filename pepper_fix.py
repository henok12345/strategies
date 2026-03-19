import socket, ssl, time, threading, os
from simplefix import FixMessage

class PepperstoneFIX:
    def __init__(self):
        self.host = "demo-uk-eqx-01.p.c-trader.com"
        self.port = 5212
        self.username = "demo.pepperstone.5244103"
        self.password = os.getenv('PEPPER_PASS')
        self.target_id = "cServer"
        self.seq_num = 1
        self.sock = None
        self.is_running = False

    def _create_header(self, msg, msg_type):
        msg.append_pair(8, "FIX.4.4", header=True)
        msg.append_pair(35, msg_type, header=True)
        msg.append_pair(49, self.username, header=True)
        msg.append_pair(56, self.target_id, header=True)
        msg.append_pair(34, self.seq_num, header=True)
        msg.append_utc_timestamp(52, header=True)
        self.seq_num += 1

    def connect(self):
        try:
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ssl.wrap_socket(raw_sock)
            self.sock.connect((self.host, self.port))
            logon = FixMessage()
            self._create_header(logon, "A")
            logon.append_pair(98, 0)
            logon.append_pair(108, 30)
            logon.append_pair(554, self.password)
            self.sock.send(logon.encode())
            self.is_running = True
            threading.Thread(target=self._heartbeat_loop, daemon=True).start()
            return "✅ Connected to Pepperstone FIX"
        except Exception as e:
            return f"❌ Connection Failed: {str(e)}"

    def _heartbeat_loop(self):
        while self.is_running:
            time.sleep(30)
            hb = FixMessage()
            self._create_header(hb, "0")
            try: self.sock.send(hb.encode())
            except: self.is_running = False

    def buy_gold(self):
        order = FixMessage()
        self._create_header(order, "D")
        order.append_pair(11, f"ORD-{int(time.time())}")
        order.append_pair(55, "XAUUSD")
        order.append_pair(54, 1) # 1 = Buy
        order.append_pair(60, time.strftime("%Y%m%d-%H:%M:%S", time.gmtime()))
        order.append_pair(38, 1000) # Volume
        order.append_pair(40, 1) # Market
        self.sock.send(order.encode())
        return "🚀 Gold Buy Order Sent!"
