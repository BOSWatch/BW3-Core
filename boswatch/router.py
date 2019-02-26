class Module:
    def __init__(self, name):
        self.__name = name

    def run(self, bwPacket):
        print("-- run module:", self.__name)
        return bwPacket


class Plugin:
    def __init__(self, name):
        self.__name = name

    def run(self, bwPacket):
        print("-- run plugin:", self.__name)


class Router:
    def __init__(self, name):
        self.__name = name
        self.__modules = []
        self.__endpoints = []
        self.__bwPacket = None

    def addModule(self, module):
        if type(module) is Module:
            self.__modules.append(module)
        else:
            print("not a instance of module class:", module)

    def addEndpoint(self, endpoint):
        if (type(endpoint) is Plugin) or (type(endpoint) is Router):
            self.__endpoints.append(endpoint)
        else:
            print("not a instance of plugin class:", endpoint)

    def call(self, bwPacket):
        # bwPacket has to be copied for each router
        # make it possible to run more routers parallel
        print("call router:", self.__name)
        for module in self.__modules:
            bwPacket = module.run(bwPacket)
        self.__callEndpoints(bwPacket)
        print("router finished:", self.__name)

    def __callEndpoints(self, bwPacket):
        print("call endpoints:", self.__name)
        for endpoint in self.__endpoints:
            if type(endpoint) is not Router:
                endpoint.run(bwPacket)
            else:
                print("> endpoint is a new router")
                endpoint.call(bwPacket)


# modules
double = Module("double")
descriptor = Module("descriptor")
# boswatch plugins
telegram = Plugin("telegram")
mysql = Plugin("mysql")

Router1 = Router("R1")
Router2 = Router("R2")

# Router 1 modules
Router1.addModule(double)
Router1.addModule(descriptor)
Router1.addModule(double)
Router1.addModule(double)
Router1.addModule(descriptor)
# Router 1 endpoints
Router1.addEndpoint(telegram)
Router1.addEndpoint(mysql)
Router1.addEndpoint(Router2)

# Router 2 modules
Router2.addModule(double)
Router2.addModule(descriptor)
# Router 2 endpoints
Router2.addEndpoint(telegram)
Router2.addEndpoint(mysql)

Router1.call("Test123")
