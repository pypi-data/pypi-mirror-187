'''Simplified Incompressible Fluid'''

import string
from math import sqrt
import traceback
from prism.props import prolib
from prism.fortran import corr_states
from prism.MassItem import MassItem
from prism.Summary import Summary
from prism.props import dsat
from prism.utils.Goal import Goal

#print corr_states.__file__
#print prolib.__file__

class Inc_liquid(MassItem):
    '''Simple Incompressible Fluid'''
    
    atm = 14.69595 # atmospheres in lbf/cu in
    R = 1.9872  # universal gas constant (used in Cv calc)
    
    # the symbol used to index these arrays MUST be added to the cea thermo.inp file
    fluidNames = {"MMH":"Monomethyl Hydrazine", "NH3":"Ammonia",
                  "AM20":"Ammoniated M20", 
                  "N2O4":"Nitrogen Tetroxide", "N2H4":"Hydrazine",
                  "MHF3":"Mixed Hydrazine Fuel-3", 
                  "CLF5":"Chlorine Petafluoride", "MON25":"MON-25",
                  "RP1":"RP1", "A50":"Aerozine 50",
                  "IRFNA":"Inhibited Red Fuming Nitric Acid",
                  "Ethanol": "Ethanol(C2H5OH)", 
                  "Methanol": "Methanol(CH3OH)",
                  "HAN269":"HAN269MEO15",
                  "HPB24":"HPB-2400",
                  "HAN315":"AF-M315E (E formulation)"}
    
    def __init__(self,symbol="RP1",T=None,P=None, child=0, mass_lbm=0.0, 
        suppressGasWarning=0, assumeSaturation=1, minSummary=0 ):
        '''Init simple incompressible Fluid'''
        
        
        self.symbol = string.upper(symbol)
        if self.symbol[-3:] == "(G)":
            self.symbol = self.symbol[:-3]
        try:
            self.name = Inc_liquid.fluidNames[self.symbol]
        except:
            self.name = self.symbol
        
        self.massBreakdown = []
        MassItem.__init__(self, self.name, type="propellant", 
            mass_lbm=mass_lbm)
        
        self.suppressGasWarning = suppressGasWarning
        self.assumeSaturation = assumeSaturation
        self.minSummary = minSummary  # minimum summary output
            
        self.Pc,self.Tc,self.Pref,self.Tref,self.RhoRef,\
            self.ViscRef,self.CondRef,self.Tnbp,self.CpRef,\
            self.WtMol,self.CPCONA,self.CPCONB,self.CPCONC,\
            self.CPCOND,self.DHvap,self.SurfRef = prolib.getRefProps( name=self.symbol )
            
        # see if we are assuming a saturated liquid
        self.useDsat = 0
        if assumeSaturation:
            rhoDsat, densDsat, sgDsat = dsat.getSatDensity( symbol=self.symbol, TdegR=self.Tref )
            if rhoDsat:
                self.RhoRef = rhoDsat
                self.useDsat = 1
        
        self.CondRefFTHR = self.CondRef * 3600.0 * 12.0
        self.ViscRefFT = self.ViscRef * 12.0
        
        if T==None:
            self.T = self.Tref
        else:
            self.T = T

        self.Pvap = corr_states.lvpres(self.T,self.Tc,self.Pc,self.Tnbp)

        if P==None:
            self.P = self.Pref
        else:
            self.P = P
            
        if self.P < self.Pvap:
            print 'WARNING... %s overriding P=%g'%(self.symbol,self.P),'to saturation pressure=%g'%self.Pvap
            self.P = self.Pvap + 0.0001  # make sure we're liquid to start
            
        self.child = child
            
        self.Dref = self.RhoRef * 1728.0

        self.Dc,self.Vcrit,self.v65,self.Ccrit,\
            self.omega,self.cpfact,self.iphase  \
            = corr_states.inprop(self.Pc,self.Tc,self.P,self.T,self.RhoRef,\
            self.ViscRef,self.CondRef,self.Tnbp,self.CpRef,self.WtMol,\
            self.CPCONA,self.CPCONB,self.CPCONC,self.CPCOND)

        self.SurfTen, self.IerrSurfTen = corr_states.surten(self.T,self.Tc,self.Pc,
                                          self.Tnbp,self.SurfRef,self.Tref,self.omega)

        self.Zc = 0.29       # dummy value

        self.Href = 0.0        
        self.setTP(self.T,self.P)
        self.Href = self.H
        
        #self.setTP(self.T,self.P)
        self.Volume = self.mass_lbm / self.rho
        
        if self.Q == "GAS" and not self.suppressGasWarning:
            print "============== GAS PHASE ========================"
            print "WARNING... Liquid",self.name,"is GAS PHASE"
            print "============== GAS PHASE ========================"
            self.printProps()
            print "============== GAS PHASE ========================"
            tbList = traceback.format_stack() 
            for line in tbList[:-1]:
                print line
            
        if child==1: self.dup = Inc_liquid(symbol=self.symbol,T=self.T,P=self.P, child=0)

    def adjustViscRef(self, viscRef=None):
        self.ViscRef = float( viscRef )

        self.Dc,self.Vcrit,self.v65,self.Ccrit,\
            self.omega,self.cpfact,self.iphase  \
            = corr_states.inprop(self.Pc,self.Tc,self.P,self.T,self.RhoRef,\
            self.ViscRef,self.CondRef,self.Tnbp,self.CpRef,self.WtMol,\
            self.CPCONA,self.CPCONB,self.CPCONC,self.CPCOND)
            
        self.SurfTen, self.IerrSurfTen = corr_states.surten(self.T,self.Tc,self.Pc,
                                          self.Tnbp,self.SurfRef,self.Tref,self.omega)
            
        self.setTP(self.T,self.P)

    def adjustRhoRef(self, rhoRef=None):
        self.RhoRef = float( rhoRef )
        self.Dref = self.RhoRef * 1728.0

        self.Dc,self.Vcrit,self.v65,self.Ccrit,\
            self.omega,self.cpfact,self.iphase  \
            = corr_states.inprop(self.Pc,self.Tc,self.P,self.T,self.RhoRef,\
            self.ViscRef,self.CondRef,self.Tnbp,self.CpRef,self.WtMol,\
            self.CPCONA,self.CPCONB,self.CPCONC,self.CPCOND)
            
        self.SurfTen, self.IerrSurfTen = corr_states.surten(self.T,self.Tc,self.Pc,
                                          self.Tnbp,self.SurfRef,self.Tref,self.omega)
            
        self.setTP(self.T,self.P)

    def reCalc(self, autoCalc=1):
        self.autoCalc = autoCalc
        self.Volume = self.mass_lbm / self.rho

    def dH_FromHZero(self):
        return self.H - self.Href

        #if self.child:
        #    self.dup.setTP( self.Tref, self.Pref)
        #else:
        #    self.child = 1
        #    self.dup = Inc_liquid(symbol=self.symbol,T=self.Tref,P=self.Pref, child=0)
        #return self.H - self.dup.H


    def restoreFromDup(self):
        '''restore properties from duplicate Inc_liquid'''
        self.T = self.dup.T
        self.P = self.dup.P
        self.D = self.dup.D
        self.rho = self.dip.rho
        self.E = self.dup.E
        self.H = self.dup.H
        self.S = self.dup.S
        self.Cp = self.dup.Cp
        self.Cv = self.dup.Cv
        self.sonicV = self.dup.sonicV
        self.Visc = self.dup.Visc
        self.Cond = self.dup.Cond
        self.Q = self.dup.Q

    def saveToDup(self):
        '''save properties to duplicate Inc_liquid'''
        self.dup.T = self.T
        self.dup.P = self.P
        self.dup.D = self.D
        self.dup.rho = self.rho
        self.dup.E = self.E
        self.dup.H = self.H
        self.dup.S = self.S
        self.dup.Cp = self.Cp
        self.dup.Cv = self.Cv
        self.dup.sonicV = self.sonicV
        self.dup.Visc = self.Visc
        self.dup.Cond = self.Cond
        self.dup.Q = self.Q

    def initFromObj(self, obj):
        '''initialize properties from another Inc_liquid object'''
        if  string.upper(self.symbol) == string.upper(obj.symbol):
            #self.setTD(T=obj.T,D=obj.D)
            self.T = obj.T
            self.P = obj.P
            self.D = obj.D
            self.rho = obj.rho
            self.E = obj.E
            self.H = obj.H
            self.S = obj.S
            self.Cp = obj.Cp
            self.Cv = obj.Cv
            self.sonicV = obj.sonicV
            self.Visc = obj.Visc
            self.Cond = obj.Cond
            self.Q = obj.Q
        else:
            raise Exception('Wrong fluid for initializing')

    def gamma(self):
        '''calculate ratio of specific heats from Cp and Cv'''
        try:
            g = self.Cp / self.Cv
            return g
        except:
            return 1.0

    def getStrTransport(self):
        '''create a string from the Transport properties'''
        return  "%s Cp=%6g Cv=%6g gamma=%.4f Visc=%6g ThCond=%6g SurfTen=%6g" %\
        (self.symbol,self.Cp, self.Cv, self.gamma(), self.Visc, self.Cond,self.SurfTen)

    def getStrTPDPlus(self):
        '''create a string from the TPDEHS properties'''
        return  "%s T=%6.1f P=%6.1f D=%.4f E=%6.2f H=%6.2f S=%.3f Q=%s" %\
        (self.symbol,self.T, self.P, self.D, self.E, self.H, self.S, self.Q)

    def getStrTPD(self):
        '''create a string from the TPDEHS properties'''
        return  "%s T=%6.1f P=%6.1f D=%.4f rho=%.5f Q=%s" %\
        (self.symbol,self.T, self.P, self.D, self.rho, self.Q)

    def printTPD(self):
        '''print a string from the TPDEHS properties'''
        print  self.getStrTPD()

    def html_desc(self):
        '''html output a multiline property summary with units'''
        return '<table><th colspan="3" align="left">&nbsp;&nbsp;&nbsp;for fluid "'+ str(self.name)+ " (" + str(self.symbol) + ')"</th>' \
            + "<tr><td>T = </td><td>" + "%5g"%self.T + "</td><td> degR &nbsp;&nbsp;(Tc=" + "%5g"%self.Tc + ")"+ "</td></tr>" \
            + "<tr><td>P = </td><td>" + "%5g"%self.P + "</td><td> psia &nbsp;&nbsp;&nbsp;(Pc=" + "%5g"%self.Pc + ")"+ "</td></tr>" \
            + "<tr><td>D = </td><td>" + "%5g"%self.D + "</td><td> lbm/cu ft &nbsp;&nbsp;"+ "</td></tr>" \
            + "<tr><td>D = </td><td>" + "%.5f"%self.rho + "</td><td> lbm/cu in &nbsp;&nbsp;"+ "</td></tr>" \
            + "<tr><td>E = </td><td>" + "%5g"%self.E + "</td><td> BTU/lbm"+ "</td></tr>" \
            + "<tr><td>H = </td><td>" + "%5g"%self.H + "</td><td> BTU/lbm"+ "</td></tr>" \
            + "<tr><td>S = </td><td>" + "%5g"%self.S + "</td><td> BTU/lbm degR"+ "</td></tr>" \
            + "<tr><td>Cv= </td><td>" + "%5g"%self.Cv + "</td><td> BTU/lbm degR"+ "</td></tr>" \
            + "<tr><td>Cp= </td><td>" + "%5g"%self.Cp + "</td><td>BTU/lbm degR"+ "</td></tr>" \
            + "<tr><td>A = </td><td>" + "%5g"%self.sonicV + "</td><td> ft/sec"+ "</td></tr>" \
            + "<tr><td>MW= </td><td>" + "%5g"%self.WtMol + "</td><td> lbm/lbmmole"+ "</td></tr>" \
            + "<tr><td>Q = </td><td>" + "%s"%self.Q + "</td><td> phase"+  "</td></tr></table>"

    def printProps(self):
        '''print a multiline property summary with units'''
        print "for fluid",self.name,"("+self.symbol+")"
        print "T  =%8g"%self.T," degR (Tc=%8g"%self.Tc,", Tnbp=%8g"%self.Tnbp,")"
        print "P  =%8g"%self.P," psia (Pc=%8g"%self.Pc,")"
        print "D  =%8g"%self.D," lbm/cu ft"
        print "rho=%8.5f"%self.rho," lbm/cu in"
        print "E  =%8g"%self.E," BTU/lbm"
        print "H  =%8g"%self.H," BTU/lbm"
        print "S  =%8g"%self.S," BTU/lbm degR"
        print "Cv =%8g"%self.Cv," BTU/lbm degR"
        print "Cp =%8g"%self.Cp," BTU/lbm degR"
        print "g  =%8g"%self.gamma()," Cp/Cv (-)"
        print "A  =%8g"%self.sonicV," ft/sec"
        print "V  =%8g"%self.Visc," viscosity [1.0E5 * lb/ft-sec]"
        print "C  =%8g"%self.Cond," thermal conductivity [BTU/ft-hr-R]"
        print "SfT=%8g"%self.SurfTen," surface tension [lbf/in]"
        print "MW =%8g"%self.WtMol," lbm/lbmmole"
        print "Q  =%s"%self.Q," Phase"
        print "Pvap=%8g"%self.Pvap," psia"


    def kinematicVisc(self):
        ''' units of in^2/sec '''
        return 144.0 * self.Visc / self.D / 100000.0 # in^2/s

    def compressibility(self):
        '''calculates Z'''
        dIdeal = self.P*self.WtMol/self.T/10.729
        return dIdeal / self.D
        
    def constP_newH(self,H):
        '''Calc properties at new H with same P'''
        #Really meant for small tweeks to the enthalpy
        #The setPH routine can often fail
        #self.maybeLoadPropFile()

        Cp = self.Cp
        dH = H - self.H
        dT = dH / Cp
        T = self.T + dT
        self.setTP(T,self.P)
    
    def constH_newP(self,P=1000.0):
        '''Calc properties at new P with same H'''
        
        self.P = float(P)
        Hcomp = 0.7074163*(P-self.Pref)/self.RhoRef/12.0/550.0
        
        dT = (self.H - self.Href - Hcomp) * self.Cp
        self.T = self.Tref + dT        
        self.setTP(self.T,P)
    
    def setPH(self,P,H):
        '''Calc properties at P and H'''
        Hcomp = 0.7074163*(P-self.Pref)/self.RhoRef/12.0/550.0
        dT = (H - self.Href - Hcomp) * self.Cp
        T = self.Tref + dT
        self.setTP(T,P)
        
    
    def constS_newP(self,P=1000.0):
        '''Calc properties at new P with same S'''
        #self.T = no change
        self.setTP(self.T,P)


    # calling this is an ERROR for incompressible liquid
    #def setTD(self,T=530.0,D=0.01):
    
    # calling this is an ERROR for incompressible liquid
    #def setPD(self,P=1000.0,D=0.01):


    def setTP(self,T=530.0,P=1000.0):
        '''Calc props from T and P'''
        
        
        self.P = float(P)
        self.T = float(T)
        
        iphflg = 0 # 0=CALCULATE PHASE, 1=ASSUME GAS, 2=ASSUME LIQUID
        self.rho,self.Cond,self.Visc,self.iphase \
            = corr_states.flupro(T,P,self.Tc,self.Pc,self.Dc,
            self.Vcrit,self.Ccrit,self.Tnbp,self.omega,iphflg)

        if self.useDsat:
            self.rho, densDsat, sgDsat = dsat.getSatDensity( symbol=self.symbol, TdegR=self.T )

        #print 'self.rho,self.Cond,self.Visc,self.iphase',self.rho,self.Cond,self.Visc,self.iphase

        self.Cond = self.Cond * 3600.0 * 12.0 # put into BTU/ft-hr-R
        self.Visc = self.Visc * 1.0E5 *12.0 # put into lb/ft-sec * 1.0E5

        self.SurfTen, self.IerrSurfTen = corr_states.surten(self.T,self.Tc,self.Pc,
                                          self.Tnbp,self.SurfRef,self.Tref,self.omega)

        self.D = self.rho * 1728.0
        #print '     setTP T,P,D=',self.T,self.P,self.D
        
        self.Pvap = corr_states.lvpres(T,self.Tc,self.Pc,self.Tnbp)
        
        self.Cp = self.CpRef
        self.Cv = self.Cp - Inc_liquid.R / self.WtMol
        self.Q = ['SUPERCRITICAL', 'GAS', 'LIQUID'][self.iphase]
        self.sonicV = sqrt( 32.174*18540.0*T*self.Cp/self.Cv/12.0/self.WtMol )
        
        Hcomp = 0.7074163*(P-self.Pref)/self.RhoRef/12.0/550.0
        dT = (T-self.Tref)
        self.H = self.Href + Hcomp + dT*self.Cp
        self.E = self.H - 0.7074163*P/self.RhoRef/12.0/550.0
        self.S = (self.H - Hcomp) / T
            

    def getSatP(self):
        '''Assume calc'd in setTP, or __init__'''
        return self.Pvap
        
    def calcTsat(self, P):
        if P>self.Pc:
            return self.Tc
            
        Tmax = self.Tc-1.
        Tmin = 1.
        
        def testT( T ):
            Pvap = corr_states.lvpres(T,self.Tc,self.Pc,self.Tnbp)
            return Pvap
        
        G = Goal(goalVal=P, minX=Tmin, maxX=Tmax, 
                funcOfX=testT, tolerance=1.0E-8, maxLoops=40, failValue=self.Tc)
        Tsat, ierror = G()
        return Tsat
        
        
    def buildSummary(self):
        
        summ = Summary(  summName='Incompressible Liquid',
        componentName=self.name, mass_lbm=self.mass_lbm, type=self.type)
        
        summ.addAssumption( self.symbol+' Properties Calculated by Method of Corresponding States' )
        # add inputs
        summ.addInput('T', self.T, 'degR', '%.1f')
        summ.addInput('P', self.P, 'psia', '%.1f')
        summ.addInput('Tref', self.Tref, 'degR', '%.1f')
        
        if not self.minSummary:
            summ.addInput('Tnbp', self.Tnbp, 'degR', '%.1f')
            summ.addInput('Tcrit', self.Tc, 'degR', '%.1f')
        summ.addInput('Pref', self.Pref, 'psia', '%.1f')
        if not self.minSummary:
            summ.addInput('Pcrit', self.Pc, 'psia', '%.1f')
            summ.addInput('WtMol', self.WtMol, '', '%g')
        summ.addInput('RhoRef', self.RhoRef, 'lb/cuin', '%g')
        if not self.minSummary:
            summ.addInput('ViscRefFT', self.ViscRefFT, 'lb/ft-sec', '%g')
            summ.addInput('CondRefFTHR', self.CondRefFTHR, 'BTU/ft-hr-R', '%g')
            summ.addInput('CpRef', self.CpRef, 'BTU/lbm degR', '%g')
        
        if len( self.massBreakdown ) > 0:
            for n,v in self.massBreakdown:
                summ.addInput(n, v, 'lbm', '%.3f')
        
        # add outputs
        summ.addOutput( 'D', self.D, 'lbm/cuft', '%.3f' )
        summ.addOutput( 'rho', self.rho, 'lbm/cuin (%g SG)'%(self.rho/0.03612729,), '%g' )
        if not self.minSummary:
            summ.addOutput( 'Cp', self.Cp, 'BTU/lbm degR', '%g' )
            summ.addOutput( 'Visc', self.Visc, '[1.0E5 * lb/ft-sec]', '%g')  #self.Visc," viscosity [1.0E5 * lb/ft-sec]"
            summ.addOutput( 'Cond', self.Cond, 'BTU/ft-hr-R', '%g')
            summ.addOutput( 'SurfTen', self.SurfTen, 'lbf/in', '%g')
            summ.addOutput( 'phase', self.Q, '', '%s' )
            summ.addOutput( 'Pvap', self.Pvap, 'psia', '%g' )
        summ.addOutput( 'Vcuft', self.Volume/1728.0, 'cuft', '%g' )
        summ.addOutput( 'Volume', self.Volume, 'cuin', '%g' )

        return summ

    def setMassBreakdown(self, nameValueList=None):
        self.massBreakdown = []
        self.mass_lbm = 0.0
        for n,v in nameValueList:
            self.massBreakdown.append( (n,v) )
            self.mass_lbm += v
        self.reCalc()

if __name__ == "__main__": #Self Test
    h = Inc_liquid("M20")
    h.printTPD()
    h.setTP(T=600.0, P=500.0)
    h.printTPD()
    h.constS_newP(P=1000.0)
    D = h.D
    E = h.E
    h.printTPD()
    h.constH_newP(P=50.0)
    h.printTPD()
    print "-------------"

    h = Inc_liquid("N2O4", mass_lbm=100.0)
    h.setMassBreakdown( nameValueList=[('Burned Axial',10.0),
        ('Burned RCS',2.5),('Residual',1.2)])
    h.printTPD()
    h.setTP(T=600.0, P=500.0)
    h.printTPD()
    h.constS_newP(P=1000.0)
    D = h.D
    E = h.E
    h.printTPD()
    h.constH_newP(P=50.0)
    h.printTPD()
    print "-------------"
    h.printProps()
    print "class=", h.__class__
    
    print h.getSummary()
    h.adjustRhoRef(rhoRef=0.06)
    print '======= adjusted rhoRef ========='
    print h.getSummary()
 
    print 
    print 'check fuel blends of MMH and N2H4'
    h = Inc_liquid("MMH")
    h.printTPD()
    h = Inc_liquid("N2H4")
    h.printTPD()
    h = Inc_liquid("M20")
    h.printTPD()
    print '\n creating M20'
    h = Inc_liquid("M20")
    h.setTP(T=550.0,P=60.0)
    h.printTPD()

    print '\n creating N2H4'
    h = Inc_liquid("N2H4")
    h.setTP(T=550.0,P=60.0)
    h.printTPD()

    print '\n creating N2O4'
    h = Inc_liquid("N2O4",P=60.0)
    h.setTP(T=550.0,P=60.0)
    h.printTPD()


    if 0:
        from numpy import arange
        tArr = arange(450.0,701.0,10.0)
        
        nameL = ['N2O4','M20','AM20','MMH','N2H4','MON25']
        row = ['T']
        for name in nameL:
            row.append( 'D_%s'%name )
        rs = [ row ]
        
        
        for T in tArr:    
            row = [T]
            for name in nameL:
                h = Inc_liquid(name,T=T,P=60.0)
                #h.setTP(T=T,P=60.0)
                row.append( h.D )
                #row.append( h.Pvap )
            
            rs.append( row )
        
        #print rs
        
        from prism.utils import xlChart
        
        xl = xlChart.xlChart()
        
        xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message
        #xl.makeDataSheet( _resultsRS, sheetName="Tank Fill")
        
        xl.makeChart(rs,  
                    title="Saturated Density",nCurves = len(nameL),
                    chartName="DSat",
                    sheetName="FillData",yLabel="Density (lbm/cuft)", xLabel="Temperature (degR)")
        #xl.putSeriesOnSecondary(2)
        #xl.putSeriesOnSecondary(3, y2Label="Temperature (degR), Cstar (ft/sec)")
        #xl.makeNewChartOfPlottedColumns(cols=(7,), ZeroBased=0, chartName='Quality')
        #xl.changePlotTitle( 'Quality of %s'%tf.gasData.name )
        #xl.labelPrimaryYAxis( 'Quality of %s (fraction gas)'%tf.gasData.name )
        #xl.labelXAxis( 'time (sec)' )
        xl.setXrange( 450, 700)


    Tcold = 489.7
    Thot = 579.7
    print '\n creating COLD M20'
    h = Inc_liquid("M20")
    h.setTP(T=Tcold,P=60.0)
    h.printTPD()

    print '\n creating COLD N2O4'
    h = Inc_liquid("N2O4",P=60.0)
    h.setTP(T=Tcold,P=60.0)
    h.printTPD()

    print '\n creating HOT M20'
    h = Inc_liquid("M20")
    h.setTP(T=Thot,P=60.0)
    h.printTPD()

    print '\n creating HOT N2O4'
    h = Inc_liquid("N2O4",P=60.0)
    h.setTP(T=Thot,P=60.0)
    h.printTPD()
    
    print 'Test calc of Tsat'
    h.setTP(T=Tcold,P=60.0)
    print 'at T=',Tcold,' Pvap=',h.Pvap
    print 'at P=',h.Pvap,' Tsat=',h.calcTsat( h.Pvap )
