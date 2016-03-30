
''' junosconfig.py
    --------------

    Implementa configuraciones de Juniper '''


indent = '    '

class JuniperConf :
    '''Implementa la configuracion de un Router Juniper entera'''
    def __init__(self):
        self.statements = []
        self.jerarquias = []
    pass
    def __str__(self):
        r = ''
        for s in self.statements:
            r = r + str(s) + '\n'
        for j in self.jerarquias :
            r = r + str (j) + '\n'
        return r
    def search_jerarquia(self, jname):
        
        try:
            c = filter(lambda x: x.name == jname[0] ,self.jerarquias)[0]
        except  IndexError:
            raise ValueError('No esta la jerarquia ' + str(jname))
        if len(jname) == 1:
            return c
        else:
            return c.search_jerarquia(jname[1:])
    def add_jerarquia(self,jname):
        """Agrega la jerarquia jname, si es una jeraruia la agrega de una,
            si es un string crea una jerarquia con ese nombre. Devuelve 
            la jerarquia agregada"""
        if not isinstance (jname , JuniperJerarquia):
            j = JuniperJerarquia(jname)
        else:
            j = jname
        self.jerarquias.append(j)
        return j

    def add_jerarquia_long(self,jnames):
        """agrega una serie de jerarquias anidadas, Devuelve la ultima"""

        #vemos si la primer jeraruia esta, entonces se lo pasamos a esa
        try:
            j = self.search_jerarquia(jnames[0:1])
        except ValueError:
            j = self.add_jerarquia(jnames[0])
        if len(jnames) == 1:
            return j
        else:
            return j.add_jerarquia_long(jnames[1:])
        
           

    def get_jerarquia(self,jname):
        """Devuelve una jerarquia con ese nombre, si no existe hasta ahora
        la crea"""
        try:
            c = self.search_jerarquia(jname)
            return c
        except ValueError:
            return self.add_jerarquia_long(jname)

class JuniperJerarquia(JuniperConf):
    '''Implementa una jerarquia de config de juniper'''
    def __init__(self,name):
        self.name = name
        self.statements = []
        self.jerarquias = []
    def __str__(self):
        if len(self.statements) == 0 and len (self.jerarquias) == 0 :
            return self.name + ';'
        r = self.name + ' {\n'
        r = r + '\n'.join([indent + x for x in [str(s) for s in self.statements]])
        if len(self.jerarquias) > 0 and len(self.statements) > 0 :
            r = r + '\n'
        r = r + '\n'.join([indent + x for x in  '\n'.join([str(j) for j in self.jerarquias]).split('\n')  ])
        r = r + '\n}'
        return r
    def add_statement(self,statement):
        if statement[-1] != ';':
            statement = statement + ';'
        self.statements.append(statement)
        
#    def search_jerarquia(self, jname):
#        
#        c = filter(lambda x: x.name == jname[0] ,self.jerarquias)[0]
#        if len(jname) == 1:
#            return c
#        else:
#            return c.search_jerarquia(jname[1:])
#


class JuniperStatement(str):
    '''Implementa un statement. Por ahora es directamente un str, la idea es 
    ampliarla despues a listas, etc'''



if __name__ == '__main__' :
    a = JuniperStatement ('vlan-id 0')
    b = JuniperStatement ('vlan-id 1')
    c = JuniperJerarquia ('unit 0')
    c.statements = [a]
    d = JuniperJerarquia ('unit 1')
    d.statements = [b]
    e = JuniperJerarquia ('fe-1/0/0')
    e.jerarquias = [c,d]
    f = JuniperJerarquia ('interfaces')
    f.jerarquias = [e]

    conf = JuniperConf()
    conf.jerarquias = [f]


    conf2 = JuniperConf()
    j = conf2.add_jerarquia('interfaces')
    j2 = conf2.get_jerarquia (['protocols','ospf','area 0','interfaces', 'ge-0/0/0'])
    print conf2


    print conf
    print '-------'
    print f
    print '-------'
    print e
    print '-------'
    print d
    print '-------'

    print 'buscamos interfaces fe-1/0/0'
    print conf.search_jerarquia(['interfaces','fe-1/0/0']) 
    print '***********'
    print 'buscamos interfaces fe-1/0/0 unit 1'
    print conf.search_jerarquia(['interfaces','fe-1/0/0','unit 1']) 
    print '***********'

    
    
