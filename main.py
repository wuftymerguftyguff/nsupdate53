#!/usr/bin/env python
import cmd
import r53
import sys
import argparse

awsac="AKIAJKEIBTFAOMHZA3JQ"
awssc="4NwB5cvRI+M5q41wUGdusQ7d0bGzMAkBdn3btRbF"



class nsupdate53(cmd.Cmd):

    UPDATECMDS = ["delete", "add"]
    r53 = r53.R53(awsac, awssc)

    """Simple command processor example."""

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
              else:
                  print "Incorrect number of parameters for add"
                  quit(1)
            if updatehost and updatecmd == "delete":
                if len(subcmds) == 2:
                    self.r53.delArecord(updatehost)
                else:
                    print "Incorrect number of parameters for delete"
                    quit(1)

    def do_send(self,args):
            self.r53.commit()

    def emptyline(self):
        pass

    def do_gethostedzones(self,line):
        """Get All Hosted Zones"""
        print self.r53.getHostedZoneList()

    def do_quit(self,line):
        return self.do_EOF

    def do_EOF(self, line):
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Emulate nsupdate using AWS Route53')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('filename', nargs='?', type=argparse.FileType('r'),default=sys.stdin)
    ourargs = parser.parse_args()
    u = nsupdate53(stdin=ourargs.filename)
    if ourargs.filename:
        u.use_rawinput = False
    u.prompt = '> '
    u.cmdloop()