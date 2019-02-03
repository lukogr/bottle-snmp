from bottle import route, run
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

temp_snmp_config = {
    'community': 'public',
    'endpoint': ('192.168.180.100', 161),
    'oid' : '1.3.6.1.3.1.1.3.1.1.5.116.101.109.112.49'
}

def get_snmp_f(community,endpoint,oid):
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget(endpoint),
        oid
    )

    if errorIndication:
        return(errorIndication)
    elif errorStatus:
        return('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            return(' = '.join([x.prettyPrint() for x in varBind]))



@route('/get_temp')
def temperature():
    community = temp_snmp_config['community']
    endpoint = temp_snmp_config['endpoint']
    oid = temp_snmp_config['oid']

    temp = get_snmp_f(community,endpoint,oid)
    if "SNMPv2-SMI::experimental.1.1.3.1.1.5.116.101.109.112.49" in str(temp):
        return {"temp_in_A1":float(str(temp).split("= ")[1])/1000}

    return temp

@route('/test')
def test():
    return {"test":"ok:)"}

run(host='localhost', port=8888, debug=True)