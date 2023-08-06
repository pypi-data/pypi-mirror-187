
from rocketprops.InterpProp_scipy import InterpProp

def convert_deg( degK, units='degR' ):
    if units == 'degK':
        return degK
    elif units == 'degC':
        return degK - 273.15
    elif units == 'degF':
        return degK*9./5. - 459.67
    elif units == 'degR':
        return degK*9./5.
    else:
        print( 'ERROR... illegal units in convert_deg: "%s"'%units)
    

def get_freezing_pt( name, units='degR' ):
    """Return freezing point in designated units."""
    
    name = name.upper()
    
    if name in freezeD:
        return convert_deg( freezeD[name], units=units)
    
    # check for Mnn blend (e.g M20)
    is_Mx, mmhPcent = isAnMMH_N2H4_Blend( name )
    if is_Mx:
        return convert_deg( MNN_terp( mmhPcent ), units=units)
        
    # check for mixed oxide of nitrogen (e.g. MON10, MON25, MON30)
    is_MON, noPcent = isMON_Ox( name )
    if is_MON:
        return convert_deg( MON_terp( noPcent ), units=units)
        
    print( 'ERROR in get_freezing_pt... propellant "%s" not found.'%name)
    
# Freezing point of mixture of MMH with N2H4
wtPcentMMH =       [0.0,    16.1057,26.3705,35.4891,43.3123,50.8364,59.9052, 86.0,    100.0]
pcentMMH_FreezeK = [274.678,269.95, 266.316,262.641,259.168,255.493,250.647, 219.261, 220.761] # degK
#                   N2H4                                                              MMH

MNN_terp = InterpProp( wtPcentMMH, pcentMMH_FreezeK )


freezeD = {} # index=propellant name, value=freezing pt degK

freezeD['RP1'] = 233 # degK  (200K to 233K)
freezeD['A50'] = 290.45 # degK
freezeD['UDMH'] = 267.594 # degK
freezeD['MMH'] = 220.761 # degK
freezeD['N2H4'] = 274.678 # degK
freezeD['NH3'] = 195.45 # degK
freezeD['MHF3'] = 219.261 # degK  86%MMH + 14%N2H4  == 394.6698 degR
freezeD['MHF5'] = 231.15 # degK   55%MMH + 26%N2H4 + 19%N2H5NH3

freezeD['C2H5OH'] = 158.706 # degK  (ethyl alcohol)

freezeD['N2O4'] = 261.8 # degK
#freezeD['MON3'] = 258.15 # degK
#freezeD['MON10'] = 250.15 # degK
#freezeD['MON25'] = 218.15 # degK
#freezeD['MON30'] = 192.15 # degK
#MON_terp = InterpProp.InterpProp( [0.,       3.0,    10.,   25.0,    30.], 
#                                  [261.8, 258.15, 250.15, 218.15, 192.15] )

ONpcentL = [0.0,2.54567,5.03106,7.51645,10.0684,12.5477,15.0717,17.0373,18.8689,20.0974,22.0183,22.6214,23.8275,25.1454,26.6196,27.6917,28.8085,29.7913,30.7294,31.5335,32.293,33.0077,33.7895,35.018,37.5197,40.0213]
#MONfreezeL_degRL = [471.241,466.135,461.159,455.529,449.709,443.27,436.026,429.945,423.596,418.23,409.824,406.336,399.897,391.223,380.223,370.297,360.281,350.354,340.338,330.054,320.306,310.111,298.486,303.315,308.502,310.737]
MONfreezeKL = [261.8, 258.96, 256.2, 253.07, 249.84, 246.26, 242.24, 238.86, 235.33, 232.35, 227.68, 225.74, 222.16, 217.35, 211.24, 205.72, 200.16, 194.64, 189.08, 183.36, 177.95, 172.28, 165.83, 168.51, 171.39, 172.63]
MON_terp = InterpProp( ONpcentL, MONfreezeKL )


freezeD['IRFNA'] = 224.3 # degK
freezeD['H2O2_100'] = 272.7 # degK

freezeD['CLF3'] = 196.85 # degK
freezeD['CLF5'] = 170.15 # degK

freezeD['F2'] = 52.594 # degK
freezeD['O2'] = 54.261 # degK
freezeD['H2'] = 14.01 # degK

freezeD['H2O'] = 273.15 # degK


def isAnMMH_N2H4_Blend( name ):
    # check for an MMH + N2H4 blend
    try:
        mmhPcent = float( name[1:] ) 
    except:
        mmhPcent = -1.0 # fails to have an mmhFrac in legal range
        
    if name[0] in ['M','m']:
        if mmhPcent>=0.0 and mmhPcent<=100.0:
            return True, mmhPcent
    return False, None

def isMON_Ox( name ):
    # check for MON oxidizer (MON1 to MON30)
    try:
        noPcent = float( name[3:] ) 
    except:
        noPcent = -1.0 # fails to have an mmhFrac in legal range
        
    if name[:3] in ['MON','mon']:
        if noPcent>=0.0 and noPcent<=30.0:  # 48% is theoritical max
            return True, noPcent
    return False, None


if __name__ == "__main__":  #self test
    
    for units in ['degK','degR']:
        for name in ['RP1','A50', 'M20', 'MON3', 'MON10','MON25', 'MON30','H2O']:#, 'xxx']:
            print( '%8s'%name, '%8.2f'%get_freezing_pt( name, units=units ),units)
        print( '-'*33)

