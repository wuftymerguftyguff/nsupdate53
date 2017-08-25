from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets
import urllib2
import re

class R53:

    changes = None

    def __init__(self,awsac,awssc):
        self.ar53 = Route53Connection(aws_access_key_id=awsac,aws_secret_access_key=awssc,debug=1)

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


    def getARecordForZone(self, zoneid, Zone):
        Zone = self.validateZoneName(Zone)
        rr = self.getResourceRecords(zoneid);
        for rset in rr:
            if rset.name == Zone and rset.type == "A":
                return rset


    def getARecord(self, zoneid, Zone, host):
        Zone = self.validateZoneName(Zone)
        rr = self.getResourceRecords(zoneid)
        for rset in rr:
            if rset.name == host and rset.type == "A":
                return rset




    def getZoneId(self, zone=None):
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

    def addArecord(self, host, ip, ttl=86400):
        zone = self.zoneNameFromHostname(host)
        zoneID = self.getZoneId(zone)
        self._addRR(zoneID,"A",host,ip,ttl)

    def delArecord(self, host):
        zone = self.zoneNameFromHostname(host)
        zoneID = self.getZoneId(zone)
        self._delRR(zoneID, "A", host)

    def _addRR(self,zoneid,rectype,host,ip,ttl=86400):
        if self.changes is None:
            self.changes = ResourceRecordSets(self.ar53, zoneid)
        change = self.changes.add_change("CREATE", host, rectype, ttl)
        change.add_value(ip)


    def _delRR(self,zoneid,rectype,host,ttl=86400):
        zone = self.zoneNameFromHostname(host)
        ARecord = self.getARecord(zoneid, zone, host)
        if ARecord:
            oldIP = ARecord.resource_records[0]
            if oldIP:
                if self.changes is None:
                    self.changes = ResourceRecordSets(self.ar53, zoneid)
                change = self.changes.add_change("DELETE", host, rectype, ttl)
                change.add_value(oldIP)

    def commit(self):
        if self.changes is not None:
                self.changes.commit()
                self.changes = None



