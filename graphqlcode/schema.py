import graphene
#import validation
import variables
import agent_info as agent



#host = variables.host
#cronFile = variables.cronfile
frequency = variables.deviceFrequency

class IsConnectionAvailable(graphene.ObjectType):
    connectionValue= graphene.Int()
    isConnected = graphene.String()


class CreateConnection(graphene.ObjectType):
    connectionStatus = graphene.String()

# class RunAgent(graphene.ObjectType):
# 	agentStatus = graphene.String()

class RunDevice(graphene.ObjectType):
    deviceStatus = graphene.String()

class Disconnect(graphene.ObjectType):
    connectionStatus = graphene.String()

class CheckConnection(graphene.ObjectType):
    connectionStatus = graphene.String()

class setDeviceFrequency(graphene.ObjectType):
    #frequency = graphene.Int()
    frequencyStatus = graphene.String()



class Query(graphene.ObjectType):
    isConnectionAvailable = graphene.Field(IsConnectionAvailable)
    createConnection = graphene.Field(CreateConnection, host=graphene.String())
    #runAgent = graphene.Field(RunAgent)
    runDevice = graphene.Field(RunDevice)
    disconnect = graphene.Field(Disconnect, host=graphene.String())
    checkConnection = graphene.Field(CheckConnection, host=graphene.String())
    setDeviceFrequency = graphene.Field(setDeviceFrequency, time=graphene.Int())

    #This function returns whether puppet master is connected or not
    def resolve_isConnectionAvailable(self, args, context, info):
        IsConnectionAvailable.connectionValue = variables.connection
        if IsConnectionAvailable.connectionValue == 0:
            return IsConnectionAvailable(isConnected = "puppet app is connected to Puppet master")
        else:
            return IsConnectionAvailable(isConnected = "puppet app is not connected to Puppet master")



    def resolve_createConnection(self, args, context, info):
        host = args.get("host")
        if agent.is_valid_ipv4_address(host):
            name, altname, address = agent.getHostByAddr(host)
            if not name == "none":
                print name,altname,address
                agent.StartScript(address[0], name)
                if agent.runDevice() == 0:
                    agent.checkConnection(name)
                    variables.connection = 0
                    return CreateConnection(connectionStatus="connection created with puppet master")
            else:
                variables.connection = 1
                return CreateConnection(connectionStatus="Given Ip address is not resolvable")
        else:
            name = agent.getHostByName(host)
            if not name == "none":
                print name
                agent.StartScript(name, host)
                if agent.runDevice() == 0:
                    agent.checkConnection(name)
                    variables.connection = 0
                    return CreateConnection(connectionStatus="connection created with puppet master")
            else:
                variables.connection = 1
                return CreateConnection(connectionStatus="given hostname is not resolvable")

        # if agent.checkConnection("%s" % host) != 0:
        #     agent.disconnect("%s" % host)
        #     variables.connection = 1




    def resolve_runDevice(self, args, context, info):
        if agent.runDevice() == 0:
            return RunDevice(deviceStatus = "pupet device ran successfully")
        else:
            return RunDevice(deviceStatus="pupet device ran with errors")

    def resolve_checkConnection(self, args, context, info):
            host = args.get("host")
            if agent.checkConnection(host) == 0:
                variables.connection = 0
            else:
                variables.connection = 1

    def resolve_disconnect(self, args, context, info):
        host = args.get("host")
        #agent.deleteHostEntry("%s" % host)
        agent.disconnect(host)
        variables.connection = 1
        #return IsConnectionAvailable(isConnected="puppet app is not connected to Puppet master")

    def resolve_setDeviceFrequency(self, args, context, info):
        cronFile = variables.cronfile
        frequency = args.get("time")
        agent.setFrequency(frequency)
        cron_script_command = ['bash', cronFile]
        agent.myrun(cron_script_command)
        #function for running rundevice












schema = graphene.Schema(query=Query)
