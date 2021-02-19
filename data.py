import os, time, json, string, re, random, threading, traceback, sys
import livejson, requests
from akad.ttypes import TalkException

class commands(threading.Thread):
    def __init__(self, fileName, client, app, uid):
        super(commands, self).__init__()
        self.fileName = fileName
        self.client = client
        self.app = app
        self.uid = uid
        self.db = livejson.File("database/%s.json"%fileName, True, True, 4)
        self.master = ["YOUR_MID"]
        self.settings = {
            "protect": False,
            "rname": fileName,
            "sname": "default"
        }
        if not "settings" in self.db:
            self.db['settings'] = self.settings
            self.settings = self.db["settings"]
            for oup in self.master:
                client.sendMessage(oup,"I'm just created.\nMy uid: %s"%uid)
        else:
            self.settings = self.db["settings"]
        self.stats = {
            "owners": [],
            "admins": [],
            "staffs": [],
            "bots": [],
            "antijs": [],
            "banned": []
        }
        if not "stats" in self.db:
            self.db['stats'] = self.stats
            self.stats = self.db["stats"]
        else:
            self.stats = self.db["stats"]

    def banned(self, user):
        if user in self.stats["banned"]:pass
        else:self.stats["banned"].append(user)
        return 1

    def mycmd(self, text, rname, sname):
        cmd = ""
        pesan = text
        if pesan.startswith(rname):
            pesan = pesan.replace(rname, "", 1)
            if " & " in text:
                cmd = pesan.split(" & ")
            else:
                cmd = [pesan]
        if pesan.startswith(sname):
            pesan = pesan.replace(sname, "", 1)
            if " & " in text:
                cmd = pesan.split(" & ")
            else:
                cmd = [pesan]
        return cmd

    def access(self, good):
        u = self.master
        if good in u:
            return 0
        u = self.stats['owners']
        if good in u:
            return 1
        u = self.stats['admins']
        if good in u:
            return 2
        u = self.stats['staffs']
        if good in u:
            return 3
        u = self.stats['bots']
        if good in u:
            return 4
        u = self.stats['antijs']
        if good in u:
            return 5
        return 1000

    def notif_kick_from_group(self, op):
        kickgroup = op.param1
        kicker = op.param2
        kicked = op.param3
        if not kicked in self.uid:
            if self.settings["protect"] and self.access(kicker) > 5:
                self.client.acceptGroupInvitation(kickgroup)
                self.client.kickoutFromGroup(kickgroup, [kicker])
                try:
                    good = []
                    good.append(kicked)
                    for _mid in self.stats['bots']:
                        good.append(_mid)
                    for _mid in self.stats['owners']:
                        good.append(_mid)
                    self.client.inviteIntoGroup(kickgroup, good)
                except TalkException as merror:
                    if merror.code == 10:
                        print("BOT NOT IN ROOM {}".format(self.client.getGroup(kickgroup).name))
                    elif merror.code == 35:
                        print("LIMIT NJIIR")
                        gc = self.client.getCompactGroup(kickgroup)
                        if gc.preventedJoinByTicket == True:
                            gc.preventedJoinByTicket = False
                            if links == True:
                                gc.preventedJoinByTicket = False
                                self.client.updateGroup(gc)
                            link = self.client.reissueGroupTicket(kickgroup)
                            for ang in self.stats['bots']:
                                self.client.sendMessage(ang, "%s %s" % (kickgroup, link))
                            for ren in self.stats['owners']:
                                self.client.sendMessage(ren,"Room rata oi join buru:\nline://ti/g/" + link)
                self.banned(kicker)
                    
            elif self.access(kicked) < 6 and self.access(kicker) > 5:
                self.client.acceptGroupInvitation(kickgroup)
                self.client.kickoutFromGroup(kickgroup, [kicker])
                try:
                    good = []
                    good.append(kicked)
                    for _mid in self.stats['bots']:
                        good.append(_mid)
                    for _mid in self.stats['owners']:
                        good.append(_mid)
                    self.client.inviteIntoGroup(kickgroup, good)
                except TalkException as merror:
                    if merror.code == 10:
                        print("BOT NOT IN ROOM {}".format(self.client.getGroup(kickgroup).name))
                    elif merror.code == 35:
                        print("LIMIT NJIIR")
                        gc = self.client.getCompactGroup(kickgroup)
                        if gc.preventedJoinByTicket == True:
                            gc.preventedJoinByTicket = False
                            if links == True:
                                gc.preventedJoinByTicket = False
                                self.client.updateGroup(gc)
                            link = self.client.reissueGroupTicket(kickgroup)
                            for ang in self.stats['bots']:
                                self.client.sendMessage(ang, "%s %s" % (kickgroup, link))
                            for ren in self.stats['owners']:
                                self.client.sendMessage(ren,"Room rata oi join buru:\nline://ti/g/" + link)
                self.banned(kicker)

    def receive_message(self, op):
        try:
            msg = op.message
            to = msg.to
            of = msg._from
            iz = msg.id
            text = msg.text
            if msg.contentType == 0:
                if None == msg.text:
                    return
                if text.lower().startswith(self.settings["rname"].lower() + " "):
                    rname = self.settings["rname"].lower() + " "
                else:
                    rname = self.settings["rname"].lower()
                if text.lower().startswith(self.settings["sname"].lower() + " "):
                    sname = self.settings["sname"].lower() + " "
                else:
                    sname = self.settings["sname"].lower()
                if msg.toType == 0:
                    if self.access(of) < 6:
                        if not rname in text.lower():
                            asw = text.split(" ")
                            if len(asw) == 2:
                                gid = msg.text.split()[0]
                                link = msg.text.split()[1]
                                self.client.acceptGroupInvitationByTicket(gid, link)
                    if self.access(of) < 3:
                        if "/ti/g/" in text:
                            regex = re.compile("(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?")
                            links = regex.findall(text)
                            tickets = []
                            gids = self.client.getGroupIdsJoined()
                            for link in links:
                                if link not in tickets:
                                    tickets.append(link)
                            for ticket in tickets:
                                try:
                                    group = self.client.findGroupByTicket(ticket)
                                except:
                                    continue
                                if group.id in gids:
                                    continue
                                self.client.acceptGroupInvitationByTicket(group.id, ticket)

                txt = msg.text.lower()
                txt = " ".join(txt.split())
                mykey = []
                if (txt.startswith(rname) or txt.startswith(sname)):
                    mykey = self.mycmd(txt, rname, sname)
                else:
                    mykey = []
                if txt == "rname" and self.access(of) < 4:
                    self.client.sendMessage(to,self.settings['rname'])
                    print(self.settings['rname'])
                if txt == "sname" and self.access(of) < 4:
                    self.client.sendMessage(to,self.settings['sname'])
                    print(self.settings['sname'])
                for a in mykey:
                    txt = a
                    if self.access(of) == 0:
                        if txt == "reboot":
                            self.client.sendMessage(to, "Restarting bot system...")
                            time.sleep(1)
                            python3 = sys.executable
                            os.execl(python3, python3, *sys.argv)
                        elif txt == "bye":
                            self.client.leaveGroup(to)
                        elif txt.startswith("gprotect "):
                            jancok = txt.replace("gprotect ", "")
                            if jancok == "on":
                                if self.settings['protect']:
                                    self.client.sendMessage(to,"Global Protect already enabled.")
                                else:
                                    self.settings["protect"] = True
                                    self.client.sendMessage(to,"Global Protect enabled.")
                            elif jancok == "off":
                                if self.settings['protect']:
                                    self.settings["protect"] = False
                                    self.client.sendMessage(to,"Global Protect disabled.")
                                else:
                                    self.client.sendMessage(to,"Global Protect already disabled.")
                        elif txt.startswith("uprname "):
                            string = txt.split(" ")[1]
                            self.settings['rname'] = string
                            self.client.sendMessage(to, "responsename update to {}".format(self.settings['rname']))
                        elif txt.startswith("upsname "):
                            string = txt.split(" ")[1]
                            self.settings['sname'] = string
                            self.client.sendMessage(to, "squadname update to {}".format(self.settings['sname']))
                        elif txt == "cban":
                            amount = len(self.stats["banned"])
                            self.stats["banned"] = []
                            self.client.sendMessage(to,"Unbanned %s people."%amount)
                        
        except Exception as e:
            e = traceback.format_exc()
            if "EOFError" in e:
                pass
            elif "ShouldSyncException" in e or "LOG_OUT" in e:
                python3 = sys.executable
                os.execl(python3, python3, *sys.argv)
            else:
                traceback.print_exc()
