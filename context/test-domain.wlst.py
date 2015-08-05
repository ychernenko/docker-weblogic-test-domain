########################################################################
#
# Weblogic test domain
# Includes:
#	- Admin Server
#	- 2 Manged Servers in Cluster
#	- File Stores for each Managed Server
#	- Machine with all servers and Node Manager
#	- JMS Module with Connection Factory and Distributed Topic
#
#########################################################################
import os
import sys


class ManagedServer:
    def __init__(self, name, port, address, fileStore, jmsServer, jvmOpts):
        self.name = name
        self.port = port
        self.address = address
        self.fileStore = fileStore
        self.jmsServer = jmsServer
        self.jvmOpts = jvmOpts




try:
    WL_HOME = os.environ['WL_HOME']
except:
    print('Error: WL_HOME is not set')
    exit()
try:
    MW_HOME = os.environ['MW_HOME']
except:
    print('Error: MW_HOME is not set')
    exit()

try:
    NODE_MANAGER = os.environ['NODE_MANAGER']
except:
    print('Warning: NODE_MANAGER is not set')

TEMPLATE = WL_HOME + '/common/templates/domains/wls.jar'

DOMAIN_NAME = 'test'
DOMAIN_PATH = MW_HOME + '/user_projects/domains/' + DOMAIN_NAME

NODE_MANAGER_HOME = WL_HOME + '/common/nodemanager'

ADMIN_SERVER_NAME = 'AdminServer'
ADMIN_SERVER_ADDRESS = ''
ADMIN_SERVER_PORT = 7001
ADMIN_SERVER_CONNECTION_URL = 't3://localhost:' + str(ADMIN_SERVER_PORT)

ADMIN_USER_NAME = 'admin'
ADMIN_USER_PASS = 'admin123'

MANAGED_SERVER_JVM_OPTS = '-Xms256m -Xmx1024m -XX:PermSize=512m -XX:MaxPermSize=512m'
MANAGED_SERVER_1 = ManagedServer('ManagedServer_1', 7003, '', 'FileStore_1', 'JmsServer_1', MANAGED_SERVER_JVM_OPTS)
MANAGED_SERVER_2 = ManagedServer('ManagedServer_2', 7004, '', 'FileStore_2', 'JmsServer_2', MANAGED_SERVER_JVM_OPTS)
MANAGED_SERVERS = [MANAGED_SERVER_1, MANAGED_SERVER_2]

CLUSTER_NAME = 'MainCluster'
CLUSTER_SERVERS = [MANAGED_SERVER_1.name, MANAGED_SERVER_2.name]

MACHINE_NAME = 'MainMachine'
MACHINE_ADDRESS = NODE_MANAGER
MACHINE_SERVERS = [ADMIN_SERVER_NAME] + CLUSTER_SERVERS

JMS_MODULE_NAME = 'MainJmsModule'
JMS_SUBDEPLOYMENT_NAME = 'MainJmsSubdeployment'
JMS_MODULE_PATH = '/JMSSystemResources/' + JMS_MODULE_NAME + '/JMSResource/' + JMS_MODULE_NAME

JMS_CONNECTION_FACTORY_NAME = 'jmsConnFactory'
JMS_CONNECTION_FACTORY_JNDI_NAME = 'test/connFactory'

JMS_DESTINATION_NAME = 'mainTopic'
JMS_DESTINATION_JNDI_NAME = 'test/mainTopic'




def go():
    doOfflinePart()
    doOnlinePart()
    print('All Done')



def doOfflinePart():
    readPredefinedTemplate()
    createAdminServer()
    createAdminUser()
    createManagedServers()
    createCluster()
    createMachine()
    saveDomain()


def doOnlinePart():
    try:
        startAdminServer()
        connectToAdminServer()
        edit()
        startEdit()
        createJmsServers()
        createJmsModule()
        createSubdeployment()
        createConnectionFactory()
        createDestination()
        configureManagedServers()
        save()
        activate()
        enrollNodeManager()
    finally:
        stopAdminServer()



def readPredefinedTemplate():
    print 'Reading Template - ' + TEMPLATE + ' ... ',
    readTemplate(TEMPLATE)
    set('name', DOMAIN_NAME)
    print 'Done'

def createAdminServer():
    print 'Creating Admin Server at port ' + str(ADMIN_SERVER_PORT)  + ' ... ',
    cd('/Servers/AdminServer')
    set('name', ADMIN_SERVER_NAME)
    set('ListenAddress', ADMIN_SERVER_ADDRESS)
    set('ListenPort', ADMIN_SERVER_PORT)
    print 'Done'

def createAdminUser():
    print 'Creating user ' + ADMIN_USER_NAME + ' ... ',
    cd('/Security/' + DOMAIN_NAME + '/User/weblogic')
    set('name', ADMIN_USER_NAME)
    set('password', ADMIN_USER_PASS)
    print 'Done'

def createManagedServers():
    for server in MANAGED_SERVERS:
        createManagedServer(server)
        createFileStore(server)

def createManagedServer(managedServer):
    print 'Creating Managed Server - ' + managedServer.name + ' on Port ' + str(managedServer.port) + ' ... ',
    cd('/')
    create(managedServer.name, 'Server')
    cd('Server/' + managedServer.name)
    set('ListenPort', managedServer.port)
    set('ListenAddress', managedServer.address)
    print 'Done'

def createFileStore(managedServer):
    print 'Creating File Store ' +  MACHINE_NAME + ' and assigning all servers ... ',
    cd('/')
    create(managedServer.fileStore,'FileStore')
    cd('FileStore/' + managedServer.fileStore)
    set('Target', managedServer.name)
    print 'Done'


def createCluster():
    print 'Creating cluster ' + CLUSTER_NAME + ' with managed servers ... ',
    cd('/')
    create(CLUSTER_NAME, 'Cluster')
    assign('Server', ','.join(CLUSTER_SERVERS), 'Cluster', CLUSTER_NAME)
    print 'Done'

def createMachine():
    print 'Creating machine ' +  MACHINE_NAME + ' and assigning all servers ... ',
    cd('/')
    create(MACHINE_NAME, 'Machine')
    assign('Server', ','.join(MACHINE_SERVERS), 'Machine', MACHINE_NAME)
    cd('/Machine/' + MACHINE_NAME)
    create(MACHINE_NAME, 'NodeManager')
    cd('NodeManager/' + MACHINE_NAME)
    set('ListenAddress', MACHINE_ADDRESS)
    # set('NMType', 'Plain')
    print 'Done'

def saveDomain():
    print 'Writing domain to ' + DOMAIN_PATH + ' ... ',
    setOption('OverwriteDomain', 'true')
    writeDomain(DOMAIN_PATH)
    closeTemplate()
    print 'Done'





def startAdminServer():
    print 'Starting admin server ... '
    startServer(adminServerName=ADMIN_SERVER_NAME, domainName=DOMAIN_NAME, url=ADMIN_SERVER_CONNECTION_URL, username=ADMIN_USER_NAME, password=ADMIN_USER_PASS, domainDir=DOMAIN_PATH)

def connectToAdminServer():
    print 'Connecting ... '
    connect(ADMIN_USER_NAME, ADMIN_USER_PASS, ADMIN_SERVER_CONNECTION_URL)

def createJmsServers():
    for server in MANAGED_SERVERS:
        createJmsServer(server)

def createJmsServer(managedServer):
    print 'Creating JMS Server ' + managedServer.jmsServer + ' ... '
    cd('/')
    cmo.createJMSServer(managedServer.jmsServer)
    cd('/Deployments/' + managedServer.jmsServer)
    cmo.setPersistentStore(getMBean('/FileStores/' + managedServer.fileStore))
    set('Targets', jarray.array([ObjectName('com.bea:Name=' + managedServer.name + ',Type=Server')], ObjectName))

def createJmsModule():
    print 'Creating JMS Module ' + JMS_MODULE_NAME + ' ... '
    cd('/')
    module = create(JMS_MODULE_NAME, 'JMSSystemResource')
    cluster = getMBean('Clusters/' + CLUSTER_NAME)
    module.addTarget(cluster)

def createSubdeployment():
    print 'Creating JMS Subdeployment ' + JMS_SUBDEPLOYMENT_NAME + ' ... '
    cd('/SystemResources/' + JMS_MODULE_NAME)
    cmo.createSubDeployment(JMS_SUBDEPLOYMENT_NAME)
    cd('SubDeployments/' + JMS_SUBDEPLOYMENT_NAME)
    targets = []
    for server in MANAGED_SERVERS:
        targets.append(ObjectName('com.bea:Name=' + server.jmsServer + ',Type=JMSServer'))
    set('Targets', jarray.array(targets, ObjectName))

def createConnectionFactory():
    print 'Creating Connection Factory ' + JMS_CONNECTION_FACTORY_NAME + ' at ' + JMS_CONNECTION_FACTORY_JNDI_NAME + ' ... '
    cd(JMS_MODULE_PATH)
    create(JMS_CONNECTION_FACTORY_NAME, 'ConnectionFactory')
    cd('ConnectionFactories/' + JMS_CONNECTION_FACTORY_NAME)
    cmo.setJNDIName(JMS_CONNECTION_FACTORY_JNDI_NAME)
    cmo.setSubDeploymentName(JMS_SUBDEPLOYMENT_NAME)
    cd('ClientParams/' + JMS_CONNECTION_FACTORY_NAME)
    cmo.setSubscriptionSharingPolicy('Sharable')
    cmo.setClientIdPolicy('Unrestricted')

def createDestination():
    print 'Creating JMS Destination ' + JMS_DESTINATION_NAME + ' at ' + JMS_DESTINATION_JNDI_NAME + ' ... '
    cd(JMS_MODULE_PATH)
    cmo.createUniformDistributedTopic(JMS_DESTINATION_NAME)
    cd('UniformDistributedTopics/' + JMS_DESTINATION_NAME)
    cmo.setJNDIName(JMS_DESTINATION_JNDI_NAME)
    cmo.setSubDeploymentName(JMS_SUBDEPLOYMENT_NAME)
        
def configureManagedServers():
    for server in MANAGED_SERVERS:
        configureManagedServer(server)

def configureManagedServer(managedServer):
    cd('/Servers/' + managedServer.name + '/ServerStart/' + managedServer.name)
    cmo.setArguments(managedServer.jvmOpts)

def enrollNodeManager():
    nmEnroll(DOMAIN_PATH, NODE_MANAGER_HOME)

def stopAdminServer():
    print 'Stopping server ...'
    shutdown(name=ADMIN_SERVER_NAME);


go()

