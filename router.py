class Module:
    __idcounter = 0
    allmodules = []

    def __init__(self,name):
        self.name = name
        self.__class__.allmodules.append(self)
        self.id = Module.__idcounter
        Module.__idcounter += 1

    def run(self,bwPaket):
        print("Das BWPaket ist: " + bwPaket)
        print("Das Modul ist:" + self.name)
        return bwPaket



class Route:
    __idcounter = 0
    allroutes = []

    def __init__(self,modulefrom,moduleto):
        self.id = Route.__idcounter
        Route.__idcounter += 1
        self.mfrom = modulefrom
        self.mto = moduleto

    def change_from_modul(self,modul):
        self.mfrom = modul

    def add_to_modul(self,modul):
        self.mto.append(modul)




class Router:
    __idcounter = 0
    allrouters = []
    def __init__(self,name):
        self.name = name
        self.id = Router.__idcounter
        Router.__idcounter += 1
        self.routes = []


    def add_route(self,route):
        self.routes.append(route)

    def get_route(self,frommodule):
        for route in self.routes:
            if route.mfrom is frommodule:
                return route
        return None

    def get_init_route(self):
        for route in self.routes:
            if route.mfrom.name is "init":
                return route


    def call(self,bwPaket):
        route = self.get_init_route()

        while route is not None:
            bwPaket = route.mto.run(bwPaket)
            route = self.get_route(route.mto)





init = Module("init")
double = Module("double")
telegram = Module("telegram")

route_init_double = Route (init,double)
route_double_telegram = Route (double,telegram)

Router1 = Router("Test")
Router1.add_route(route_double_telegram)
Router1.add_route(route_init_double)


Router1.call("Test123")
