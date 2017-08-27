#!/usr/bin/env python
import cmd
import r53
import sys
import argparse
import creds

class updatecommand(cmd.Cmd):
    RRECORDTYPES = ["A", "PTR"]

    def do_add(self,args):
        # args should have this format here
        # myhost.jeffarthur.co.uk. [ttl] IN A 1.2.3.4
        subcmds = args.split()
        print "Add"
        if 4 <= len(subcmds) <= 5:
            updatehost = subcmds[0]
            ip = subcmds[-1]
            type = subcmds[-2]
            ttl = subcmds[-4]
            if type == "A":
                r53.addArecord(updatehost, ip, ttl)
            elif type == "PTR":
                r53.addPTRrecord(updatehost, ip, ttl)
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
            type = subcmds[-1]
            if updatehost:
                if subcmds[1] == "IN" and type in self.RRECORDTYPES:
                    if  type == 'A':
                        r53.delArecord(updatehost)
                    if  type == 'PTR':
                        r53.delPTRrecord(updatehost)
                else:
                    print "Incorrect parameters for delete"
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

    def do_zone(self,args):
        """A set the DNS zone that we are working on"""
        subcmds = args.split()
        if  len(subcmds) == 1:
            zone = subcmds[0]
            if not r53.setzone(zone):
                print "Zone %s does not exist in our DNS, or we don't manage it" % zone
                quit(1)


        else:
            print "Incorrect number of parameters for zone"
            quit(1)

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
    print sys.argv[1:]
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