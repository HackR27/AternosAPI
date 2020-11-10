from mechanicalsoup import StatefulBrowser
import json
from user_agent import generate_user_agent

class AternosAPI(StatefulBrowser):
    def __init__(self, cookies):
        self.headers = {}
        self.reqheaders = {}
        self.cookies = {}
        self.user_agent = generate_user_agent()
        self.headers['User-Agent'] = self.user_agent
        self.headers['Cookie'] = cookies
        super().__init__(soup_config={'features':'lxml'},raise_on_404=True,user_agent=self.user_agent) 
        # self.SEC = SEC
        self.JavaSoftwares = ['Vanilla', 'Spigot', 'Forge', 'Magma', 'Snapshot', 'Bukkit', 'Paper', 'Modpacks', 'Glowstone']
        self.BedrockSoftwares = ['Bedrock', 'Pocketmine-MP']
        self.CheckVaildInput()

    def CheckVaildInput(self):
        webserver = self.open(url='https://aternos.org/server/',headers=self.headers)
        if len(webserver.soup.find_all('span',class_='logout'))>0:
            print('Cookie validated')
        else:
            print("Invaild cookie")

    def GetStatus(self):
        webserver = self.open(url='https://aternos.org/server/',headers=self.headers)
        status = webserver.soup.find('span', class_='statuslabel-label').get_text().strip()
        return status
    
    def StartServer(self):
        serverstatus = self.GetStatus()
        if serverstatus == "Online":
            return "Server Already Running"
        else:
            self.setSec()
            startserver = self.open(url=f"https://aternos.org/panel/ajax/start.php",params={'headstart':0,'SEC':self.sec}, headers=self.reqheaders)
            self.skip_queue()
    
    def StopServer(self):
        self.setSec()
        serverstatus = self.GetStatus()
        if serverstatus == "Offline":
            return "Server Already Offline"
        else:
            stopserver = self.open(url=f"https://aternos.org/panel/ajax/stop.php",params={'SEC':self.sec},headers=self.reqheaders)
            return "Server Stopped"

    def GetServerInfo(self):
        ServerInfo = self.open(url='https://aternos.org/server/',headers=self.headers).soup

        server_info = ServerInfo.head.find_all('script')
        for stat in server_info:
            if 'lastStatus' in stat.text:
                string = stat.text.split(' = ')[1]
                data = json.loads(string[:600])
                self.lastStatus = data
                return f'Software:{data["software"]}\nIP:{data["ip"]}\nPort:{data["port"]}'
                break

    def queue_confirm(self):
        self.setSec()
        confirm = self.open(url=f'https://aternos.org/panel/ajax/confirm.php',params={'SEC':self.sec},headers=self.reqheaders)
        return confirm.status_code

    def queue_number(self):
        webserver = self.open(url='https://aternos.org/server/',headers=self.headers)
        webdata = webserver.soup
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

    def setSec(self):
        key = self.keygen()
        value = self.keygen()
        self.reqheaders['User-Agent'] = self.user_agent
        self.reqheaders['Cookie'] = f'ATERNOS_SEC_{key}={value}; '+self.headers['Cookie']
        self.sec = key+':'+value

    def keygen(self):
        data = self.open('https://www.random.org/strings/',params={
            'num':1,
            'len':16,
            'digits':'on',
            'upperalpha':'off',
            'loweralpha':'on',
            'unique':'off',
            'format':'plain',
            'rnd':'new'})
        if data.status_code != 503:
            return data.text.strip('\n')

if __name__ == "__main__":
    api = AternosAPI(cookies='__cfduid=d3fa0d88095829528bb6f323b7825b84a1604714248; ATERNOS_LANGUAGE=en; PHPSESSID=3bb7k35r4evv526oonriot8kkj; ATERNOS_STYLE=dark; _ga=GA1.2.1611040091.1604715330; _gid=GA1.2.1685488237.1604715330; __gads=ID=c4b56dfe7041e604:T=1604715332:S=ALNI_MZ7gSk_v__suK1mFh624f4lVF-8wA; cnx_userId=e5b6a491d804497c9d085a64cd7a007e; fileDownload=true; SKpbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMOHk6CB7VbgfhNpd2eqFFHiixfg79Nw6CZgnoVBQ%22%2C%22ID5ID_CREATED_AT%22%3A%222020-11-07T02%3A15%3A30Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; ATERNOS_SESSION=GAzZ83qTl5xNInA34b08JMFpv7rdaYPnxwHizvwajiMIGaVLRUc3I9wOTdTTaSsRwCeHuHUEDeDQYdlAKmI6PIgL7rwHY3vnfrsM; ATERNOS_SERVER=1e3IweOlsYTdbTms; cto_bidid=yCbdSl9ob3c4YjF1anB5d2N5c1glMkJRa05NMXVnc2lrTW5jZW5jWVQ5NGs1TE5GYTQ4JTJCRTAyT1FJWHdidmtpTHVqUGtwOXQ5Mm9HSW55a2FkcSUyQmZYVzJLaHpVQSUzRCUzRA; cto_bundle=otMBGV9QJTJCUlUySlRuV3U4YXdIdjZXYzEwRjNYSnpxdDJUaGdEbUtzbUliWFpxelA5Wmx0aUdlQTZvbTBxR1glMkI4d0klMkZpNUhiU0hQZlJGZFlvWmRGJTJGMWNJUVQ2cXhzeEt4SHRGc2p4NVc4WTNKbDlQcnM1SDFUWU1oZkZ6RTBSRlc0ZnglMkI; SKpbjs-unifiedid=%7B%22TDID%22%3A%22d1a2a172-8786-4dcb-8ddd-abef54981613%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222020-10-09T03%3A32%3A14%22%7D; SKpbjs-unifiedid_last=Mon%2C%2009%20Nov%202020%2003%3A32%3A15%20GMT; SKpbjs-id5id_last=Mon%2C%2009%20Nov%202020%2003%3A32%3A15%20GMT; id5id.1st_364_nb=5; GED_PLAYLIST_ACTIVITY=W3sidSI6IjhYbWoiLCJ0c2wiOjE2MDQ5MTEwNzAsIm52IjoxLCJ1cHQiOjE2MDQ5MDk1NjUsImx0IjoxNjA0OTExMDY5fV0')
    api.StopServer()