import netconnections
import junosconfig
import igraph
import netaddr
import pygraphviz as pgv


ifa = 'fxp1'
ifb = 'fxp2'


        


def get_router_list(conexiones):
    rlist = []
    for c in conexiones:
        for r in c[0:2]:
            if r not in rlist:
                rlist.append(r)
    return rlist

        




def geninterfaces_generic(j,connectionlist):
    G = pgv.AGraph(strict=False)
    G.edge_attr['fontsize']=10
    G.edge_attr['fontcolor']='blue'
    G.node_attr['shape'] = 'circle'



    for i in range(len(connectionlist)):
        ra = j.get_jerarquia([connectionlist[i][0]])
        rb = j.get_jerarquia([connectionlist[i][1]])
        if len(connectionlist[i]) > 2:
            params = connectionlist[i][2]
        else:
            params = None

        vlanid = 100 + i
        subnet = netaddr.IPNetwork('10.0.0.' + str(i*4) + '/30')

        G.add_edge(ra.name,rb.name,label='vlan ' + str(vlanid) + '\n' + str(subnet), taillabel = '.' + str(subnet[1].words[3]),
                    headlabel = '.' + str(subnet[2].words[3]))
        
        subifa = ra.get_jerarquia(['interfaces',ifa,'unit ' + str(vlanid)])
        subifa.add_statement('vlan-id ' + str(vlanid))
        subifa.add_statement('description "to  ' + rb.name + '"')
        subifa.get_jerarquia(['family inet']).add_statement('address ' + str(subnet[1])  + '/30')
        subifb = rb.get_jerarquia(['interfaces',ifb,'unit ' + str(vlanid)])
        subifb.add_statement('vlan-id ' + str(vlanid))
        subifb.add_statement('description "to  ' + ra.name + '"')
        subifb.get_jerarquia(['family inet']).add_statement('address ' + str(subnet[2])  + '/30')

        #iso
        if params and 'iso' in params:
            subifa.get_jerarquia(['family iso'])
            subifb.get_jerarquia(['family iso'])
        
        #ospf
        if params and 'ospf-area' in params:
            area = params['ospf-area']
            ra.get_jerarquia(['protocols','ospf','area 0.0.0.'+ str(area),'interface ' + ifa + \
                '.' + str(vlanid)])
            rb.get_jerarquia(['protocols','ospf','area 0.0.0.'+ str(area),'interface ' + ifb + \
                '.' + str(vlanid)])
    return G


def gen_loopbacks_generic(j,conexiones,G=None):
    subin = 100
    done = []
    for r in get_router_list(conexiones):
        lo = j.get_jerarquia([r,'interfaces','lo0','unit ' + str(subin), 'family inet'])
        lo.add_statement ('address 192.168.' + str(subin/10) + '.1/32')
        if G:
            G.get_node(r).attr['label']=r + '\nlo.' + str(subin) + '=192.168.' + str(subin/10) + '.1'
        subin = subin + 100

def add_loopbacks_ospf(j,conexiones):
    for r in get_router_list(conexiones):
        interf = j.get_jerarquia([r,'interfaces'])
        for i  in interf.jerarquias:
            if i.name[0:2] == 'lo':
                for subi in i.jerarquias:
                    if subi.name[0:4] == 'unit':
                        subin = subi.name.split()[1].strip()

        ospf = j.get_jerarquia([r,'protocols','ospf'])
        try: 
            area = ospf.search_jerarquia(['area 0.0.0.0'])
        except ValueError:
            area = filter(lambda x: x.name[0:4] == 'area', ospf.jerarquias)[0]
        olo = area.get_jerarquia(['interface lo0.' + str(subin)])
        olo.add_statement('passive')
    

if __name__ == '__main__':
    conexiones = [('R1','R2'),('R1','R3'),('R2','R4'),('R3','R4'),('R4','R5'),
            ('R4','R6'),('R6','R7'),('R5','R7')]
    ciso = [x + ({'iso':None},) for x in conexiones]
    ls = junosconfig.JuniperJerarquia('logical-systems')
    G = geninterfaces_generic (ls,ciso)
    gen_loopbacks_generic(ls,ciso,G)
    for p in ['neato','dot','twopi','circo','fdp','nop']:
        G.draw(p + '.png',prog=p)
    print "replace: ",ls
            
    
    print "\n\n\n--------------------------\n\n\n"

    virtual_link = [ ('A1','A2',{'ospf-area':0}),
            ('A1','A3',{'ospf-area':0}),
            ('A2','A3',{'ospf-area':0}),
            ('A4','A2',{'ospf-area':10}),
            ('A4','A3',{'ospf-area':10}),
            ('A4','A5',{'ospf-area':10}),
            ('B1','B2',{'ospf-area':0}),
            ('B1','B3',{'ospf-area':0}),
            ('B2','B4',{'ospf-area':0}),
            ('B4','B3',{'ospf-area':0}),
            ('B5','B2',{'ospf-area':10}),
            ('B5','B4',{'ospf-area':10}),
            ('B5','B6',{'ospf-area':10}),
            ('A5','B5',{'ospf-area':10})]

    multi_area = [('R1','R2',{'ospf-area':0}),
                    ('R1','R3',{'ospf-area':100}),
                    ('R1','R4',{'ospf-area':100}),
                    ('R2','R3',{'ospf-area':100}),
                    ('R2','R4',{'ospf-area':100})]

    c = virtual_link
    ls2 = junosconfig.JuniperJerarquia('logical-systems')
    G = geninterfaces_generic(ls2,c)
    gen_loopbacks_generic(ls2,c,G)
    add_loopbacks_ospf(ls2,c)

    G.draw('gen.png',prog='dot')
        
    print 'replace: ',ls2

    
    
