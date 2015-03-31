
class NetElement:
    """Clase que engloba cualquier elemento de red"""
    def __init__(self,name):
        self.name = name
        self.subelements = []

    def add_subelement(self,element):
    """ Agrega un subelemento al elemento, solo usar para los que se sepa
        estan subordinados a este (y no a mas de uno por ejemplo) """
        self.subelements.append(element)

class Chasis(NetElement):
    """cualquier elemento de red fisico"""
    def __init__(self,hostname):
        self.hostname = hostname


class VirtualSwitch(NetElement):
    """switch virtual, contiene elementos broadcast doamins"""

class BroadCastDomain(NetElement):
    """agrupa interfases fisicas en un switch"""

class JuniperRouter(Chasis):
    """Router Juniper"""
    def __init__(self,hostname,extraparams=''):
        self.name = hostname
        self.hostname = hostname
        self.global_logical_system = LogicalSystem('__global')
        self.logical_systems=[self.global_logical_system]
        self.extraparams = extraparams


class LogicalSystem(NetElement):
    """Logical System dentro de un router"""
    def __init__(self,name,extraparams= ''):
        self.name = name
        self.global_routing_instance = RoutingInstance(name = '__global', instance_type = '__global')
        self.extraparams = extraparams

class RoutingInstance(NetElement):
    """Instancia de ruteo dentro de un sistema logico"""
    def __init__(self,name,instance_type, extraparams=''):
        self.name = name
        self.instance_type = instance_type
        self.extraparams = extraparams
        self.subelements= []
    
    


class PhisicalInterface(NetElement):
    """Interfaz fisica, asociada a un chasis"""
    def __init__(name,interface_type = 'unknown', internal=False,extraparams=''):
        self.name = name
        self.interface_type=interface_type
        self.internal=internal
        self.extraparams = extraparams

class LogicalInterface(NetElement):
    """Interfaz logica, asociada a un Routing Instance y los protocolosde ruteo
        que sean necesarios"""
    def __init__(name,interface_type = 'unknown', internal=False,extraparams=''):
        self.name = name
        self.interface_type=interface_type
        self.internal=internal
        self.extraparams = extraparams
    
    def add_ipv4(self,address):
        f = Family('inet')
        f.add_element(Address(address))
        slef.add_element(f)
    
    def gen_config (self)

class Family(NetElement):
    """familia en el sentido de Juniper, asociada a un Logical Interface"""

class Address(NetElement):
    """direccion asociada a una family"""


