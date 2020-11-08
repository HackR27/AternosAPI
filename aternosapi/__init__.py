import requests
from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser
import json

class AternosAPI(StatefulBrowser):
    def __init__(self, headers, cookie):
        self.headers = {}
        self.cookies = {}
        self.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.106 Safari/537.36"
        self.headers['Cookie'] = headers
        self.cookies['ATERNOS_SESSION'] = cookie
        super().__init__(soup_config={'features':'lxml'},raise_on_404=True,user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.106 Safari/537.36')
        # self.SEC = SEC
        self.JavaSoftwares = ['Vanilla', 'Spigot', 'Forge', 'Magma', 'Snapshot', 'Bukkit', 'Paper', 'Modpacks', 'Glowstone']
        self.BedrockSoftwares = ['Bedrock', 'Pocketmine-MP']
        self.CheckVaildInput()

    def CheckVaildInput(self):
        webserver = self.open(url='https://aternos.org/server/',cookies=self.cookies,headers=self.headers)
        if len(webserver.soup.find_all('span',class_='logout'))>0:
            print('Cookie validated')
        else:
            return "Invaild cookie"

    def GetStatus(self):
        webserver = self.open(url='https://aternos.org/server/',headers=self.headers)
        status = webserver.soup.find('span', class_='statuslabel-label').get_text().strip()
        return status
    
    def StartServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Online":
            return "Server Already Running"
        else:
            startserver = self.open(url=f"https://aternos.org/panel/ajax/start.php?headstart=0&SEC={self.SEC}", headers=self.headers)
            self.skip_queue()
    
    def StopServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Offline":
            return "Server Already Offline"
        else:
            stopserver = requests.get(url=f"https://aternos.org/panel/ajax/stop.php?SEC={self.SEC}",headers=self.headers)
            return "Server Stopped"

    def GetServerInfo(self):
        ServerInfo = self.open(url='https://aternos.org/server/',headers=self.headers).soup

        server_info = ServerInfo.head.find_all('script')
        for stat in server_info:
            if 'lastStatus' in stat.text:
                string = stat.text.split(' = ')[1]
                data = json.loads(string[:600])
                return f'Software:{data["software"]}\nIP:{data["ip"]}\nPort:{data["port"]}'
                break

    def queue_confirm(self):
        confirm = requests.get(url=f'https://aternos.org/panel/ajax/confirm.php?SEC={self.SEC}',cookies=self.cookies,headers=self.headers)
        return confirm.status_code

    def queue_number(self):
        webserver = requests.get(url='https://aternos.org/server/',cookies=self.cookies,headers=self.headers)
        webdata = BeautifulSoup(webserver.content, 'html.parser')
        status = webdata.find('span', class_='server-status-label-right').get_text()
        return status.strip()

    def skip_queue(self):
        i = 0
        while i < 1:
            serverstatus = self.GetStatus()
            queue_number = self.queue_number()
            confirm = self.queue_confirm()
            print(serverstatus+" : "+queue_number+" : "+str(confirm)+"\r", end="")
            if serverstatus == "Online":
                i = 1
                return "Server Started"

if __name__ == "__main__":
    api = AternosAPI(
        headers='__cfduid=d3fa0d88095829528bb6f323b7825b84a1604714248; ATERNOS_LANGUAGE=en; PHPSESSID=3bb7k35r4evv526oonriot8kkj; ATERNOS_SESSION=oGgKBNgQWmOGClphN7P0f9hcsYMjvyplx7hm8290x1OmH6OrIt7rKxIF1PkybrMdMIJbZSftpcswGHwXVBAUcOC2SPmXjeyVgdGr; ATERNOS_STYLE=dark; _ga=GA1.2.1611040091.1604715330; _gid=GA1.2.1685488237.1604715330; __gads=ID=c4b56dfe7041e604:T=1604715332:S=ALNI_MZ7gSk_v__suK1mFh624f4lVF-8wA; cnx_userId=e5b6a491d804497c9d085a64cd7a007e; fileDownload=true; ATERNOS_SERVER=1e3IweOlsYTdbTms; SKpbjs-unifiedid=%7B%22TDID%22%3A%22d1a2a172-8786-4dcb-8ddd-abef54981613%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222020-10-08T09%3A36%3A30%22%7D; SKpbjs-unifiedid_last=Sun%2C%2008%20Nov%202020%2009%3A36%3A30%20GMT; SKpbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMOHk6CB7VbgfhNpd2eqFFHiixfg79Nw6CZgnoVBQ%22%2C%22ID5ID_CREATED_AT%22%3A%222020-11-07T02%3A15%3A30Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; SKpbjs-id5id_last=Sun%2C%2008%20Nov%202020%2009%3A36%3A30%20GMT; cto_bidid=jkVPn19ob3c4YjF1anB5d2N5c1glMkJRa05NMXVnc2lrTW5jZW5jWVQ5NGs1TE5GYTQ4JTJCRTAyT1FJWHdidmtpTHVqUGtwOWxwMVZTM1ROeXFIJTJCWTRLVkc1UzBlZyUzRCUzRA; cto_bundle=46tj0l9QJTJCUlUySlRuV3U4YXdIdjZXYzEwRnliVjZUTkFwNGpZNnZnSTJVcXVESE5JajAzaURJakgzVUpGUWVldkxRQjZVNVIwSVIlMkJyRnhqeUhLWlRrbUNSdkFCVGFQeUZpamloWjRkNEY0eFl4VjlJSU85V3o5JTJCVnNSTWJTV3FTNmRrWg; GED_PLAYLIST_ACTIVITY=W3sidSI6IjhYbWoiLCJ0c2wiOjE2MDQ4NTcxMjgsIm52IjoxLCJ1cHQiOjE2MDQ4NTY5NTksImx0IjoxNjA0ODU3MTI2fV0.; id5id.1st_364_nb=7',
        cookie='oGgKBNgQWmOGClphN7P0f9hcsYMjvyplx7hm8290x1OmH6OrIt7rKxIF1PkybrMdMIJbZSftpcswGHwXVBAUcOC2SPmXjeyVgdGr'
        )
    print(api.GetServerInfo())
