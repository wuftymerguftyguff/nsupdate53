#!/usr/bin/env python
import cmd
import r53
import sys
import argparse
import creds

class updatecommand(cmd.Cmd):
    RRECORDTYPES = ["A"]

    def do_add(self,args):
        # args should have this format here
        # myhost.jeffarthur.co.uk. [ttl] IN A 1.2.3.4
        subcmds = args.split()
        print "Add"
        if 4 <= len(subcmds) <= 5:
            updatehost = subcmds[0]
            ip = subcmds[-1]
            type = subcmds[-2]
            if type == "A":
                r53.addArecord(updatehost, ip)
            else:
                print "Unsupported Record Type"
                quit(1)

        else:
            print "Incorrect number of parameters for add"
            quit(1)


    def do_delete(self,args):
        # args should have this format here
        # myhost.jeffarthur.co.uk. IN A
        print "Delete"
        subcmds = args.split()
        if 3 <= len(subcmds) < 4:
            updatehost = subcmds[0]
            if updatehost:
                if subcmds[1] == "IN" and subcmds[2] in self.RRECORDTYPES:
                    r53.delArecord(updatehost)
                else:
                    print "Incorrect number of parameters for delete"
                    quit(1)
        else:
            print "Incorrect number of parameters for delete"
            quit(1)





class nsupdate53(cmd.Cmd):
    """Simple command processor example."""

    UPDATECMDS = ["delete", "add"]

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
        updateparser = updatecommand()
        updateparser.onecmd(args)
        print "Doing Update"
        subcmds=args.split()
        updatecmd=subcmds[0]
        updatehost=subcmds[1]
        if updatecmd and updatecmd in self.UPDATECMDS:
            print "Doing " + updatecmd



    def do_send(self,args):
            r53.commit()

    def emptyline(self):
        pass

    def do_gethostedzones(self,line):
        """Get All Hosted Zones"""
        print r53.getHostedZoneList()

    def do_quit(self,line):
        return self.do_EOF

    def do_EOF(self, line):
        return True


if __name__ == '__main__':
    r53 = r53.R53(creds.awsac, creds.awssc)
    parser = argparse.ArgumentParser(description='Emulate nsupdate using AWS Route53')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('filename', nargs='?', type=argparse.FileType('r'),default=sys.stdin)
    ourargs = parser.parse_args()
    u = nsupdate53(stdin=ourargs.filename)
    if ourargs.filename:
        u.use_rawinput = False
    u.prompt = '> '
    u.cmdloop()