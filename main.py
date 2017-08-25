#!/usr/bin/env python
import cmd
import r53

awsac="AKIAJKEIBTFAOMHZA3JQ"
awssc="4NwB5cvRI+M5q41wUGdusQ7d0bGzMAkBdn3btRbF"



class nsupdate53(cmd.Cmd):

    UPDATECMDS = ["delete", "add"]

    """Simple command processor example."""
    def __init__(self):
        self.r53 = r53.R53(awsac, awssc)
        cmd.Cmd.__init__(self)

    def do_server(self,line):
        """A dummy function to emulate nsupdate"""
        pass

    def do_zone(self,line):
        """A dummy function to emulate nsupdate"""
        pass

    def do_answer(self, line):
        """A dummy function to emulate nsupdate"""
        pass



    def do_update(self,args):
        """Update a DNS Record"""
        print "Doing Update"
        subcmds=args.split()
        updatecmd=subcmds[0]
        updatehost=subcmds[1]
        if updatecmd and updatecmd in self.UPDATECMDS:
            print "Doing " + updatecmd
            if updatehost and updatecmd == "add":
              if 3 <= len(subcmds) < 4:
                ip = subcmds[2]
                self.r53.addArecord(updatehost,ip)
            if updatehost and updatecmd == "delete":
                if len(subcmds) == 2:
                    self.r53.delArecord(updatehost)

    def do_send(self,args):
            self.r53.commit()

    def emptyline(self):
        pass

    def do_gethostedzones(self,line):
        """Get All Hosted Zones"""
        print self.r53.getHostedZoneList()


    def do_EOF(self, line):
        return True


if __name__ == '__main__':
    u = nsupdate53()
    u.prompt = '> '
    u.cmdloop()