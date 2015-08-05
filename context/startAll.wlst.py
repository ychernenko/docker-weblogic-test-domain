import os
import time

try:
    NM_HOME = os.environ['NM_HOME']
except:
    print('Error: NM_HOME is not set')
    exit()

ADMIN_USER_NAME='admin'
ADMIN_USER_PASS='admin123'
DOMAIN_NAME='test'
ADMIN_SERVER='AdminServer'
JVM_ARGS="Arguments=\"-Xms256m -Xmx1024m -XX:PermSize=512m -XX:MaxPermSize=512m -Djava.security.egd=file:/dev/./urandom -Dweblogic.security.SSL.ignoreHostnameVerification=true -Dweblogic.nodemanager.sslHostNameVerificationEnabled=false\""
PROPERTIES = makePropertiesObject(JVM_ARGS)


def startAdminServerFromNodeManager():
    while True:
        try:
            nmConnect(ADMIN_USER_NAME, ADMIN_USER_PASS, domainName=DOMAIN_NAME)
            break
        except:
            time.sleep(5)
            print 'Reconnecting ...'
    nmStart(ADMIN_SERVER, props=PROPERTIES)
    nmDisconnect()


def startOtherServersFromAdmin():
    connect(ADMIN_USER_NAME, ADMIN_USER_PASS)
    domainConfig()
    svrs = cmo.getServers()
    domainRuntime()
    for server in svrs:
        if server.getName() != ADMIN_SERVER:
            print "Starting " + server.getName();
            start(server.getName())
    disconnect()


def main():
    startAdminServerFromNodeManager()
    startOtherServersFromAdmin()


if __name__== "main":
    main()