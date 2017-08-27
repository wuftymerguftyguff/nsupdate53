from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets
import urllib2
import re

class R53:

    changes = None
    zone = None
    zoneid = None

    def __init__(self,awsac,awssc):
        self.ar53 = Route53Connection(aws_access_key_id=awsac,aws_secret_access_key=awssc,debug=1)

    def setzone(self,zone):
        validzone =  self.validateZoneName(zone)
        zid = self.getZoneId(validzone)
        if zid:
            self.zone = zone
            self.zoneid = zid
            return True
        else:
            self.zone = None
            self.zoneid = None
            return False

    def getExternalIP(self):
        ext_ip = urllib2.urlopen('http://ipv4.icanhazip.com').read()
        regex = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        return unicode(regex.findall(ext_ip)[0])


    def getHostedZoneList(self):
        hostedZone = self.ar53.get_all_hosted_zones()
        return hostedZone.ListHostedZonesResponse.HostedZones


    def getResourceRecords(self,zoneID=None):
        rr = self.ar53.get_all_rrsets(zoneID)
        return rr


    def getRecordForZone(self,type):
        rr = self.getResourceRecords(self.zoneid);
        for rset in rr:
            if rset.name == self.zone and rset.type == type:
                return rset


    def getRecord(self, type, host):
         rr = self.getResourceRecords(self.zoneid)
         for rset in rr:
             if rset.name == host and rset.type == type:
                 return rset




    def getZoneId(self, zone):
        zone = self.validateZoneName(zone)
        for Zone in self.getHostedZoneList():
            if zone in Zone.Name:
                ZoneId = Zone.Id.replace('/hostedzone/', '')
                return ZoneId


    def validateZoneName(self,zone=None):
        if zone[-1] != ".":
            zone = zone + "."
        return zone

    def zoneNameFromHostname(self,hostname=None):
        if hostname:
            s = '.'
            splitted = hostname.split(s)[1:]
            return s.join(splitted)

    def addArecord(self, host, ip, ttl=300):
        self._addRR("A",host,ip,ttl)

    def addPTRrecord(self, host, ip, ttl=300):
        self._addRR("PTR", host, ip, ttl)

    def delArecord(self, host):
        self._delRR("A", host)

    def delPTRrecord(self, host):
        self._delRR("PTR", host)

    def _addRR(self,rectype,host,ip,ttl=300):
        if self.zoneid is not None:
            if self.changes is None:
                self.changes = ResourceRecordSets(self.ar53, self.zoneid)
            change = self.changes.add_change("CREATE", host, rectype, ttl)
            change.add_value(ip)
        else:
            print "Zone not set, or does not exist in DNS"



    def _delRR(self,rectype,host,ttl=300):
        if self.zoneid is not None:
            #zone = self.zoneNameFromHostname(host)
            ARecord = self.getRecord(rectype,host)
            if ARecord:
                oldIP = ARecord.resource_records[0]
                oldttl = ARecord.ttl
                if oldttl:
                    ttl = oldttl
                if oldIP:
                    if self.changes is None:
                        self.changes = ResourceRecordSets(self.ar53, self.zoneid)
                    change = self.changes.add_change("DELETE", host, rectype, ttl)
                    change.add_value(oldIP)
        else:
            print "Zone not set, or does not exist in DNS"

    def commit(self):
        if self.changes is not None:
                self.changes.commit()
                self.changes = None
                self.zoneid = None
                self.zone = None
        else:
            print "No Changes to send"



