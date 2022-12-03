import threading
from classData import DataBase
from telebot import types


class Consl:
    def __init__(self, bd, bot):

        self.threadingID = None
        self.bd: DataBase = bd
        self.bot = bot

    def StopApp(self):
        self.bot.stop_bot()
        self.bd.close()

        print("BOT STOP")

    def AddAdmin(self, c):
        self.bd.admins[c[1]] = {"state": ""}
        print("ok Added")

    def DelAdmin(self, c):
        del self.bd.admins[c[1]]
        print("ok Deleted")

    def main(self):
        while 1:
            try:
                c = input().split()
            except EOFError:
                self.StopApp()
                break

            ####
            if c[0] in ["s", "stop"]:
                self.StopApp()
                break

            if c[0] in ["addA", "addAdmin"]:
                self.AddAdmin(c)
            elif c[0] in ["delA", "delAdmin"]:
                self.AddAdmin(c)

            elif c[0] in ["sendPro"]:
                try:
                    k = int(c[-1])
                except:
                    print("Опять забыл параметр !!! долбаеб")
                    continue

                kol = min(int(k), len(self.bd.proposed.keys()))
                for i in list(self.bd.proposed.values())[:kol]:
                    print(i.media)

            elif c[0] in ["info", "i"]:
                print(f"Reged users: {len(self.bd.users.keys())}")
                print(f"Proposed: {len(self.bd.proposed.keys())}")



            else:
                print("Чтото дакой команды нет command not found")

    def run(self):

        self.threadingID = threading.Thread(target=self.main)
        self.threadingID.start()
        return self
