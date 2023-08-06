
from prism.props import prolib
from prism.utils import LikeDict
from prism.fortran import corr_states

_dsatDict = LikeDict.LikeDict() # case-insensitive dictionary

def getSatDensity( symbol='M20', TdegR=None, TdegF=None, TdegC=None, TdegK=None ):
    try:
        return _dsatDict[symbol].dsat( TdegR=TdegR, TdegF=TdegF, TdegC=TdegC, TdegK=TdegK)
    except:
        return None, None, None

def getDsatCorrelationRange( symbol='M20' ):
    """Return the temperature range over which the correlation applies"""
    try:
        return _dsatDict[symbol].TlowCorrR, _dsatDict[symbol].ThiCorrR
    except:
        return None, None

class DSatLiquid( object ):
    
    '''Models saturated density of liquids
       (typical density correlations)
       eqn must use TdegR, TdegF, TdegC, or TdegK for temperature'''
    
    def __init__(self,symbol="M20", TlowCorrR=500.0, ThiCorrR=560.0,
        rhoEqn=None, densEqn=None, sgEqn=None):
            
        self.symbol = symbol
        self.TlowCorrR = TlowCorrR
        self.ThiCorrR = ThiCorrR
        
        # can choose an equation for rho(lbm/cuin), dens(lbm/cuft), or SG(g/cc)
        # eqn must use TdegR, TdegF, TdegC, or TdegK for temperature
        self.rhoEqn = rhoEqn
        self.densEqn = densEqn
        self.sgEqn = sgEqn
        
        self.Pc,self.Tc,self.Pref,self.Tref,self.RhoRef,\
            self.ViscRef,self.CondRef,self.Tnbp,self.CpRef,\
            self.WtMol,self.CPCONA,self.CPCONB,self.CPCONC,\
            self.CPCOND,self.DHvap,self.SurfRef = prolib.getRefProps( name=self.symbol )
        
        self.Dc,self.Vcrit,self.v65,self.Ccrit,\
            self.omega,self.cpfact,self.iphase  \
            = corr_states.inprop(self.Pc,self.Tc,self.Pref,self.Tref,self.RhoRef,\
            self.ViscRef,self.CondRef,self.Tnbp,self.CpRef,self.WtMol,\
            self.CPCONA,self.CPCONB,self.CPCONC,self.CPCOND)
    
    def evalRho(self, TdegR=530.0):
        
        # assume that TdegR is set above
        TdegF = TdegR - 459.67
        TdegK = TdegR / 1.8
        TdegC = TdegK - 273.15
        
        if self.rhoEqn:
            rho = eval( self.rhoEqn )
            dens = rho * 1728.0
            sg = rho / 0.03612729
        elif self.densEqn:
            dens = eval( self.densEqn )
            rho = dens / 1728.0
            sg = rho / 0.03612729
        elif self.sgEqn:
            sg = eval( self.sgEqn )
            rho = sg * 0.03612729
            dens = rho * 1728.0
            
        return rho, dens, sg
        
    def getCorrStateRho(self, TdegR):
        Pvap = 14.7# corr_states.lvpres(TdegR,self.Tc,self.Pc,self.Tnbp) + 0.0001
        
        iphflg = 3 # 0=CALCULATE PHASE, 1=ASSUME GAS, 2=ASSUME LIQUID
        rho,Cond,Visc,iphase \
            = corr_states.flupro(TdegR,Pvap ,self.Tc,self.Pc,self.Dc,
            self.Vcrit,self.Ccrit,self.Tnbp,self.omega,iphflg)
            
        return rho
    
    def dsat(self, TdegR=None, TdegF=None, TdegC=None, TdegK=None):
        
        if TdegF:
            TdegR = TdegF + 459.67
        elif TdegK:
            TdegR = TdegK * 1.8
        elif TdegC:
            TdegR = (TdegC + 273.15) * 1.8
            
        # check for bounds of correlation
        
        if TdegR > self.ThiCorrR:
            rhoRef = self.getCorrStateRho(self.ThiCorrR)
            rhoLimit, dens, sg = self.evalRho( self.ThiCorrR )
            scaleFactor = rhoLimit / rhoRef
            
            rho =  self.getCorrStateRho(TdegR) * scaleFactor

            dens = rho * 1728.0
            sg = rho / 0.03612729
            
            
        elif TdegR < self.TlowCorrR:
            rhoRef = self.getCorrStateRho(self.TlowCorrR)
            rhoLimit, dens, sg = self.evalRho( self.TlowCorrR )
            scaleFactor = rhoLimit / rhoRef
            
            rho =  self.getCorrStateRho(TdegR) * scaleFactor

            dens = rho * 1728.0
            sg = rho / 0.03612729
            
            
        else:
            rho, dens, sg = self.evalRho( TdegR )
            

        return rho, dens, sg
        
def addFluid( symbol="M20", TlowCorrR=500.0, ThiCorrR=560.0,
        rhoEqn=None, densEqn=None, sgEqn=None):
            
    _dsatDict[symbol] = DSatLiquid(symbol=symbol, TlowCorrR=TlowCorrR, ThiCorrR=ThiCorrR, 
        rhoEqn=rhoEqn, densEqn=densEqn, sgEqn=sgEqn)
        
# from Roger Anderson Memo Dec 10, 1987
addFluid(symbol="M20", TlowCorrR=480.0, ThiCorrR=660.0,
        rhoEqn=None, densEqn='63.2845 - 0.03126*TdegF', sgEqn=None)

# from Divert Engine IRAD Test Plan Final Version.doc  
# Cherie Cotter Memo March 27, 1998 has an AM20 density that is 4% lower than this equation
addFluid(symbol="AM20", TlowCorrR=480.0, ThiCorrR=580.0,  # temperature range is a guess
        rhoEqn=None, densEqn=None, sgEqn='1.0338-0.00099858 * TdegF')


# from CPIA Liquid Propellant manual
addFluid(symbol="MMH", TlowCorrR=400.0, ThiCorrR=650.0,
        rhoEqn=None, densEqn='71.8132 - 0.032584*TdegR', sgEqn=None)


# from CPIA Liquid Propellant manual
addFluid(symbol="MHF3", TlowCorrR=400.0, ThiCorrR=650.0,
        rhoEqn=None, densEqn='73.1416 - 0.03289*TdegR', sgEqn=None)


# from CPIA Liquid Propellant manual
addFluid(symbol="N2H4", TlowCorrR=492.0, ThiCorrR=800.0,
        rhoEqn=None, densEqn='76.8353 - 0.021735*TdegR - 8.7254E-6*TdegR**2', sgEqn=None)


# from CPIA Liquid Propellant manual
addFluid(symbol="N2O4", TlowCorrR=470.0, ThiCorrR=580.0,
        rhoEqn=None, densEqn=None, sgEqn='2.066-0.001979 * TdegK - 0.0000004826 * TdegK**2')

# from CPIA Liquid Propellant manual
#addFluid(symbol="MON10", TlowCorrR=450.0, ThiCorrR=675.0,
#        rhoEqn=None, densEqn=None, sgEqn='1.5825 + 1.28E-3 * TdegK - 6.26E-6 * TdegK**2')

# from CPIA Liquid Propellant manual
addFluid(symbol="MON25", TlowCorrR=400.0, ThiCorrR=675.0,
        rhoEqn=None, densEqn=None, sgEqn='1.6679 + 4.622E-4 * TdegK - 4.8E-6 * TdegK**2')

# from CPIA Liquid Propellant manual
#addFluid(symbol="MON30", TlowCorrR=350.0, ThiCorrR=675.0,
#        rhoEqn=None, densEqn=None, sgEqn='1.6688 + 2.846E-4 * TdegK - 4.31E-6 * TdegK**2')


if __name__ == "__main__": #Self Test
    
    print 'M20',getSatDensity(symbol='M20', TdegR=580.0, TdegF=None, TdegC=None, TdegK=None )
    print
    print 'N2O4',getSatDensity(symbol='N2O4', TdegR=580.0, TdegF=None, TdegC=None, TdegK=None )
    print
    print 'MMH',getSatDensity(symbol='MMH', TdegR=580.0, TdegF=None, TdegC=None, TdegK=None )
    print

    print
    print 'AM20',getSatDensity(symbol='AM20', TdegR=None, TdegF=70.0, TdegC=None, TdegK=None ),'at 70F'
    print 'AM20',getSatDensity(symbol='AM20', TdegR=None, TdegF=90.0, TdegC=None, TdegK=None ),'at 90F'
    print
    print 'M20',getSatDensity(symbol='M20', TdegR=None, TdegF=90., TdegC=None, TdegK=None ),'at 90F'
    print
    print 'N2O4',getSatDensity(symbol='N2O4', TdegR=None, TdegF=70., TdegC=None, TdegK=None ),'at 70F'
    print 'N2O4',getSatDensity(symbol='N2O4', TdegR=None, TdegF=90., TdegC=None, TdegK=None ),'at 90F'
    print

    if 1:
        from numpy import arange
        tArr = arange(450.0,701.0,10.0)
        
        
        rs = [ ['T','D_N2O4','D_M20','D_AM20'] ]
        
        for T in tArr:    
            rhoN2O4, densN2O4, sg = getSatDensity(symbol='N2O4', TdegR=T)
            rhoM20, densM20, sg = getSatDensity(symbol='M20', TdegR=T)
            rhoAM20, densAM20, sg = getSatDensity(symbol='AM20', TdegR=T)
            rs.append( [T, densN2O4, densM20, densAM20] )
        
        #print rs
        
        from prism.utils import xlChart
        
        xl = xlChart.xlChart()
        
        xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message
        #xl.makeDataSheet( _resultsRS, sheetName="Tank Fill")
        
        xl.makeChart(rs,  
                    title="Saturated Density",nCurves = 3,
                    chartName="DSat",
                    sheetName="FillData",yLabel="Density (lbm/cuft)", xLabel="Temperature (degR)")
        #xl.putSeriesOnSecondary(2)
        #xl.putSeriesOnSecondary(3, y2Label="Temperature (degR), Cstar (ft/sec)")
        #xl.makeNewChartOfPlottedColumns(cols=(7,), ZeroBased=0, chartName='Quality')
        #xl.changePlotTitle( 'Quality of %s'%tf.gasData.name )
        #xl.labelPrimaryYAxis( 'Quality of %s (fraction gas)'%tf.gasData.name )
        #xl.labelXAxis( 'time (sec)' )
        xl.setXrange( 450, 700)
