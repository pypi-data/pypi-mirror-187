# Applied Python PRISM
# (PRISM) PaRametrIc System Model
#
# Written by Charlie Taylor <cet@appliedpython.com> 
# Oct,21 2005

from prism.utils import LikeDict # want case-insensitive dictionary for users (i.e. "Ti" == "TI")

class Material(object):
    '''A material and it's properties'''
    
    def __init__(self, name="Al", fullname="Aluminum", type="metal",
        assumptions="room temperature", minGauge=0.03,
        rho=0.1, desStress=45000.0, modulus=10.0E6,
        ultStress=0.0, yieldStress=0.0):
        
        self.name = name
        self.fullname = fullname
        self.type = type
        self.assumptions = assumptions
        self.minGauge = minGauge
        self.rho = rho # lbm/cuin
        self.desStress = desStress #psi
        self.modulus = modulus  #psi
        self.ultStress = ultStress
        self.yieldStress = yieldStress
        
    def calcDesignStress(self, sfUlt=1.25, sfYield=1.0):
        if self.ultStress>0.0 and self.yieldStress>0.0:
            self.desStress = min( self.ultStress/sfUlt, self.yieldStress/sfYield )
        return self.desStress
        
    def getProps(self):
        ''' returns all mechanical properties at once.'''
        return self.rho,self.desStress,self.modulus,self.minGauge
        
    def getPropsStr(self):
        ''' returns all mechanical properties at once.'''
        if self.ultStress>0.0 and self.yieldStress>0.0:
            s = '\n ultimate %.0f psi\n yield %.0f psi'%(self.ultStress, self.yieldStress)
        else:
            s = ''
        return ' density = %.4f lbm/cuin\n design stress = %.0f\n modulus = %.2e\n min gauge = %.3f in'%\
            ( self.rho,self.desStress,self.modulus,self.minGauge) + s
        
    def getPropsStrHTML(self):
        s = self.getPropsStr()
        return s.replace('\n','<br>')
        
    def getDesc(self):
        return self.fullname + ' (' + self.type + ') ' + self.assumptions


class Materials(object):
    '''A material and it's properties'''
    
    def getMatlProps(self, name='Al'):
        if self.matlDict.has_key(name):
            return self.matlDict[name].getProps()
        else:
            print 'ERROR... Non existant material (%s) called in Materials'%name
            return 1.0E6,1.0,1.0,10.0 # return non-sense materials, make heavy
            
    def getMatlPropsStr(self, name='Al'):
        if self.matlDict.has_key(name):
            return self.matlDict[name].getPropsStr()
        else:
            return 'ERROR... Non existant material (%s) called in Materials'%name
            
    def getMatlPropsStrHTML(self, name='Al'):
        if self.matlDict.has_key(name):
            return self.matlDict[name].getPropsStrHTML()
        else:
            return 'ERROR... Non existant material (%s) called in Materials'%name
            
    def getMatlDesc(self, name='Al'):
        if self.matlDict.has_key(name):
            return self.matlDict[name].getDesc()
        else:
            return 'ERROR... Non existant material (%s) called in Materials'%name
    
    def __init__(self):
        self.matlDict = LikeDict.LikeDict()
        
    def addMatl(self,  name="Al", fullname="Aluminum", type="metal",
        assumptions="room temperature", minGauge=0.03,
        rho=0.1, desStress=45000.0, modulus=10.0E6,
        ultStress=0.0, yieldStress=0.0):
        
        self.matlDict[name] = Material(name, fullname, type,
        assumptions=assumptions, minGauge=minGauge,
        rho=rho, desStress=desStress, modulus=modulus,
        ultStress=ultStress, yieldStress=yieldStress) 
        
        if desStress <= 0.0:
            self.matlDict[name].calcDesignStress()
        
    def calcDesignStress(self, name='Ti800F', sfUlt=1.25, sfYield=1.0):
        if self.matlDict.has_key(name):
            return self.matlDict[name].calcDesignStress(sfUlt=sfUlt, sfYield=sfYield)
        else:
            return 'ERROR... Non existant material (%s) called in Materials'%name
            
        
# create basic list of materials

_myMatls = Materials()


def addMatl(  name="Al", fullname="Aluminum", type="metal",
        assumptions="room temperature", minGauge=0.03,
        rho=0.1, desStress=45000.0, modulus=10.0E6,
        ultStress=0.0, yieldStress=0.0, **kwords):
            
    _myMatls.addMatl(name, fullname, type,
        assumptions=assumptions, minGauge=minGauge,
        rho=rho, desStress=desStress, modulus=modulus,
        ultStress=ultStress, yieldStress=yieldStress) 
        
    for k,v in kwords.items():
        #print "adding",k,'value of',v
        setattr( _myMatls.matlDict[name], k, v)

def getMatlProps( name='Al'):
    return _myMatls.getMatlProps( name )
            
def getMatlPropsStr( name='Al'):
    return _myMatls.getMatlPropsStr( name )
            
def getMatlPropsStrHTML( name='Al'):
    return _myMatls.getMatlPropsStrHTML( name )
            
def getMatlDesc( name='Al'):
    return _myMatls.getMatlDesc( name )

def calcDesignStress( name='Ti800F', sfUlt=1.25, sfYield=1.0):
    return _myMatls.calcDesignStress(name, sfUlt=sfUlt, sfYield=sfYield)
            
def getMatlAttr( name='Al', attr="Flag"):
    return getattr( _myMatls.matlDict[ name ], attr, None)
    
addMatl("Al", "Aluminum", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.1, desStress=45000.0, modulus=10.0E6) 
    
addMatl("Al-Sc", "SHS-Aluminum", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.102, desStress=82400.0, modulus=10.0E6) 

addMatl("CuZr", "Zirconium-Copper", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.322, desStress=13000.0, modulus=19.0E6) 

addMatl("CRES_301", "CRES 301", "metal",
assumptions="room temperature", minGauge=0.014,
rho=0.3, desStress=240000.0, modulus=28.0E6) 

addMatl("CRES_301_aged", "CRES 301 Aged", "metal",
assumptions="room temperature", minGauge=0.014,
rho=0.3, desStress=290000.0, modulus=28.0E6) 

addMatl("grEpox", "Graphite Epoxy", "composite",
assumptions="room temperature", minGauge=0.008,
rho=0.0637, desStress=393000.0, modulus=35.0E6) 

# Requested properties from Tom F. 4/4/2013
addMatl("TomFgrEpox", "Tom F. Graphite Epoxy", "composite",
assumptions="room temperature", minGauge=0.008,
rho=0.0637, desStress=450000.0, modulus=35.0E6) 

addMatl("kevEpox", "Kevlar Epoxy", "composite",
assumptions="room temperature", minGauge=0.008,
rho=0.047, desStress=185000.0, modulus=10.0E6) 

addMatl("Ni", "Nickel", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.322, desStress=50000.0, modulus=30.0E6) 

addMatl("SS", "Stainless Steel", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.28, desStress=50000.0, modulus=29.0E6) 

addMatl("4130_Steel", "4130 Steel", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.284, desStress=100000.0, modulus=29.7E6) 

addMatl("Inconel", "Inconel", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.296, desStress=100000.0, modulus=30.0E6) 

addMatl("Monel", "Monel", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.32, desStress=25000.0, modulus=25.0E6) 

addMatl("Ti", "Titanium", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.16, desStress=119000.0, modulus=15.0E6) 

addMatl("Ti_aged", "Titanium Aged", "metal",
assumptions="room temperature", minGauge=0.03,
rho=0.16, desStress=147000.0, modulus=15.0E6) 

addMatl("Ti550F", "Titanium at 550degF", "metal",
assumptions="550 degF", minGauge=0.03,
rho=0.16, desStress=0.0, modulus=15.0E6,
ultStress=115102.0, yieldStress=90644.0) # with ult/yld leave desStress=0.0 to autocalc 

addMatl("Ti800F", "Titanium at 800degF", "metal",
assumptions="800 degF", minGauge=0.03,
rho=0.16, desStress=0.0, modulus=15.0E6,
ultStress=108500.0, yieldStress=84700.0) # with ult/yld leave desStress=0.0 to autocalc 

addMatl("ARI-2718", "D5 Insulation/Inhibitor", "insulation",
assumptions="", minGauge=0.03,
rho=0.042, desStress=0.0, modulus=0.0E6)  

addMatl("ARI-2727MOD", "D5 Insulation/Inhibitor", "insulation",
assumptions="", minGauge=0.03,
rho=0.038, desStress=0.0, modulus=0.0E6)  

addMatl("PKWu_Composite", "PK Wu Composite", "composite",
assumptions="350F or 800F", minGauge=0.008,
rho=0.057, desStress=150000.0, modulus=35.0E6) 


addMatl("Cb103", "Columbium 103", "metal",
assumptions="high temp use (1000F)", minGauge=0.02,               # min gauge ???
rho=0.3096109, desStress=22020.0, modulus=35.0E6, InsFlag=1) # modulus ???

addMatl("Cb103(1000F)", "Columbium 103", "metal",
assumptions="high temp use (1000F)", minGauge=0.02,               # min gauge ???
rho=0.3096109, desStress=22020.0, modulus=35.0E6, InsFlag=1) # modulus ???

addMatl("Cb103(2250F)", "Columbium 103", "metal",
assumptions="high temp use (2250F)", minGauge=0.02,               # min gauge ???
rho=0.3096109, desStress=12498.7, modulus=35.0E6, InsFlag=1) # modulus ???

addMatl("Cb103(3000F)", "Columbium 103", "metal",
assumptions="high temp use (3000F)", minGauge=0.02,               # min gauge ???
rho=0.3096109, desStress=1724.8, modulus=35.0E6, InsFlag=1) # modulus ???

addMatl("C-Sic", "Carbon SiC", "non-metallic",
assumptions="high temp use (1000F)", minGauge=0.03,               # min gauge ???
rho=0.06864185, desStress=6000.0, modulus=35.0E6, InsFlagHT=1, InsFlag=2) # modulus ???

addMatl("C-Sic(72F)", "Carbon SiC", "non-metallic",
assumptions="roomtemp use (72F)", minGauge=0.03,               # min gauge ???
rho=0.06864185, desStress=4130.0, modulus=35.0E6, InsFlagHT=1, InsFlag=2) # modulus ???

addMatl("Re", "Rhenium", "metal",
assumptions="high temp use (1000F)", minGauge=0.03,               # min gauge ???
rho=0.7586731, desStress=95380.0, modulus=35.0E6, InsFlag=2) # modulus ???

addMatl("Ta-10W", "Tungsten", "metal",
assumptions="high temp use (1000F)", minGauge=0.03,               # min gauge ???
rho=0.6094674, desStress=49800.0, modulus=35.0E6, InsFlag=5) # modulus ???

addMatl("Ta-10W(3000F)", "Tungsten", "metal",
assumptions="high temp use (3000F)", minGauge=0.03,               # min gauge ???
rho=0.607, desStress=13684.0, modulus=35.0E6) # modulus ???

addMatl("TZM", "TZM", "metal",
assumptions="high temp use (1000F)", minGauge=0.03,               # min gauge ???
rho=0.3692209, desStress=94090.0, modulus=35.0E6, InsFlag=6) # modulus ???

addMatl("TZM(2200F)", "TZM", "metal",
assumptions="high temp use (2200F)", minGauge=0.03,# min gauge ??? Added by E Brannam 1/6/06
rho=0.3692209, desStress=47488.0, modulus=35.0E6, InsFlagHT=4, InsFlag=6) # modulus ???

addMatl("TZM(2250F)", "TZM", "metal",
assumptions="high temp use (2250F)", minGauge=0.03,# min gauge ??? Added by E Brannam 1/6/06
rho=0.3692209, desStress=33000.0, modulus=35.0E6, InsFlagHT=4, InsFlag=6) # modulus ???

addMatl("TZM(3000F)", "TZM", "metal",
assumptions="high temp use (3000F)", minGauge=0.03,# min gauge ??? Added by E Brannam 1/6/06
rho=0.3692209, desStress=9250.0, modulus=35.0E6, InsFlagHT=4, InsFlag=6) # modulus ???

addMatl("W-25Re(3000F)", "Tungsten - Rhenium", "metal",
assumptions="high temp use (3000F)", minGauge=0.03,# min gauge ??? Added by E Brannam 1/6/06
rho=0.7126108, desStress=13888.0, modulus=35.0E6) # modulus ???

addMatl("W-25Re(4200F)", "Tungsten - Rhenium", "metal",
assumptions="high temp use (4200F)", minGauge=0.03,# min gauge ??? Added by E Brannam 1/6/06
rho=0.7126108, desStress=3381.0, modulus=35.0E6)# modulus ???

addMatl("SiPhen_A", "Silica Phenolic - Elastomer-modified phenylsilane resin", "composite",
assumptions="room temperature", minGauge=0.01,
rho=0.04586, desStress=4100.0, modulus=0.19E6) 

addMatl("SiPhen_B", "Silica Phenolic - Polyamide-modified phenolic (unfilled) resin", "composite",
assumptions="room temperature", minGauge=0.01,
rho=0.06359, desStress=25000.0, modulus=3.32E6) 

addMatl("SiPhen_C", "Silica Phenolic - Filled phenolic resin", "composite",
assumptions="room temperature", minGauge=0.01,
rho=0.0635, desStress=14000.0, modulus=2.0E6)

addMatl("Cork", "External Cork Insulation", "composite",
assumptions="room temperature", minGauge=0.01,
rho=0.02, desStress=75.0, modulus=1.0E6)

addMatl("silCork", "Silicon-Cork External Insulation", "composite",
assumptions="room temperature", minGauge=0.01,
rho=0.024, desStress=75.0, modulus=1.0E6)

addMatl("silEPDM", "Silicon Rubber", "composite",
assumptions="room temperature", minGauge=0.01,
rho=0.049, desStress=75.0, modulus=1.0E6)

addMatl("CPR-488", "Spray-On Foam Insulation", "composite",
assumptions="room temperature", minGauge=0.25,
rho=0.00127, desStress=1.0, modulus=1.0E6)  # desStress and modulus numbers are WRONG

if __name__ == "__main__":  #self test

    m = Material()
    print m.getProps()
    print m.getDesc()
    print m.getPropsStr()
    print m.getPropsStrHTML()
    print
    
    name='TZM(2200F)'
    print getMatlDesc( name)
    print getMatlProps( name)
    print getMatlPropsStr( name)
    print getMatlPropsStrHTML( name)
    print calcDesignStress( name ),'= calculated design stress'
    
    name='W-25Re(3000F)'
    print getMatlDesc( name)
    print getMatlProps( name)
    print getMatlPropsStr( name)
    print getMatlPropsStrHTML( name)
    print calcDesignStress( name ),'= calculated design stress'

    name='W-25Re(4200F)'
    print getMatlDesc( name)
    print getMatlProps( name)
    print getMatlPropsStr( name)
    print getMatlPropsStrHTML( name)
    print calcDesignStress( name ),'= calculated design stress'

    print
    print 'get special flag attribute'
    print "InsFlag =",getMatlAttr( "Cb103", attr="InsFlag" )
    print "InsFlag =",getMatlAttr( "TZM", attr="InsFlag" )
    
    print
    keyL = sorted( _myMatls.matlDict.keys(), key=str.lower )
    print keyL
    '''
    self.name = name
    self.fullname = fullname
    self.type = type
    self.assumptions = assumptions
    self.minGauge = minGauge
    self.rho = rho # lbm/cuin
    self.desStress = desStress #psi
    self.modulus = modulus  #psi
    self.ultStress = ultStress
    self.yieldStress = yieldStress
    '''
 