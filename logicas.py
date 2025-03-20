from github import Github
from config import GITHUB_TOKEN, GITHUB_REPO  # Changed to import from config
import sys
import os
import clr
import re
from System.Collections.Generic import List

#v1.0.0: versão inicial.
#v1.1.0: inclusão de limpeza de cache e recarregar biblioteca logicas.py ao atualizar get_current_values e ajustado lógica devido seccionamento em PSO2.
#v1.1.1: entrada parcial SE Caxias Norte.
#v1.1.2: entrada seccionamento LT 230 kV CHA/SCR1
#v1.1.3: entrada cne/mcl e cne/vin
#v1.1.4: alteração da IO-OI.S.PPE, revisão 37 e IO-OI.S.PPE, revisão 27
#v1.1.5: seccionamento LT 230 kV Caxias 2 / Farroupilha na SE Caxias Norte - 10/03/25
#v2.0.0: nova interface gráfica com melhorias

def extract_tags_from_code():
    """Extract all PI tags from the code automatically"""
    with open(__file__, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match tag names like 'RSXXX_230_CHXXX_S.s'
    pattern = r"status\.get\('([A-Z0-9]+_230_[A-Z0-9]+_S\.s)'\)"
    
    # Find all unique matches
    tags = set(re.findall(pattern, content))
    return sorted(list(tags))

tags = extract_tags_from_code()

def find_dll():
    """Find and load OSIsoft.AFSDK dll from _internal folder"""
    try:
        # Get program's root directory (where main.py is)
        root_dir = os.path.dirname(os.path.dirname(__file__))  # Go up one level from logicas.py
        
        # Path to _internal folder
        internal_path = os.path.join(root_dir, "_internal")
        
        # Add _internal to system path if not already there
        if internal_path not in sys.path:
            sys.path.append(internal_path)
        
        # Try to load the DLL
        clr.AddReference('OSIsoft.AFSDK')
        return True
        
        print(f"CARREGADO COM SUCESSO:")
            
    except Exception as e:
        print(f"Error loading OSIsoft SDK: {e}")
        return False

# Initialize OSIsoft SDK
if not find_dll():
    raise ImportError("Could not load OSIsoft.AFSDK")

from OSIsoft.AF.PI import PIServers, PIPoint, PIPointList
from OSIsoft.AF.Time import AFTime, AFTimeRange
from OSIsoft.AF.Data import AFBoundaryType

# Inicializar conexão com o PI Server
pi_servers = PIServers()
pi_server = pi_servers.get_Item("his1.5")

config = {}  # Dicionário de configuração

def get_current_values(tags):
    """Get current values for multiple tags using batch request"""
    values = {}
    try:
        # Create List[str] for PI SDK
        pi_tags = List[str]()
        for tag in tags:
            pi_tags.Add(tag)
        
        # Get all points in one batch using FindPIPoints
        piPoints = PIPointList(PIPoint.FindPIPoints(pi_server, pi_tags))
        
        # Get all current values in one batch
        piCurrentValues = piPoints.CurrentValue()
        
        # Process results
        for point in piCurrentValues:
            try:
                values[point.PIPoint.Name] = str(point.Value)
            except Exception as e:
                print(f"Error reading tag {point.PIPoint.Name}: {e}")
                values[point.PIPoint.Name] = None
                
        return values
        
    except Exception as e:
        print(f"Error getting current values: {e}")
        return {}
    
def atualizar_get_current_values():
    global config, status
    status = get_current_values(tags)

    # Exemplo de lógica de configuração

    #RIO GRANDE DO SUL

    # ATLÂNTIDA 2 
    if (status.get('RSATL2_230_CH847_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSATL2_230_CH867_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSATL2_230_CH877_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSATL2_230_CH887_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSATL2_230_CH897_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSATL2_230_CH917_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0

    elif (status.get('RSATL2_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH891_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH911_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSATL2_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH893_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH913_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0

    elif (status.get('RSATL2_230_CH911_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH891_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSATL2_230_CH913_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH893_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0

    elif (status.get('RSATL2_230_CH911_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSATL2_230_CH913_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0


    elif (status.get('RSATL2_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH891_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSATL2_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH893_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0


    elif (status.get('RSATL2_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSATL2_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0

    elif (status.get('RSATL2_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSATL2_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSATL2_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['ATL2'] = 0

    else:
        config['ATL2'] = 1

    # CACHOEIRINHA 3 
    if (status.get('RSCAC3_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAC3_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAC3_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAC3_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAC3_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAC3_230_CH8952_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAC3_230_CH8960_S.s') == 'Estado do ponto digital:on'):
        
        config['CAC3'] = 0

    elif (status.get('RSCAC3_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8954_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAC3_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8956_S.s') == 'Estado do ponto digital:on'):
        
        config['CAC3'] = 0

    elif (status.get('RSCAC3_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8914_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAC3_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['CAC3'] = 0

    elif (status.get('RSCAC3_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAC3_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAC3_230_CH8932_S.s') == 'Estado do ponto digital:on'):
        
        config['CAC3'] = 0

    else:
        config['CAC3'] = 1

    # CAMAQUÃ 3 
    if (status.get('RSCAM3_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAM3_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAM3_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAM3_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAM3_230_CH8908_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAM3_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['CAM3'] = 0

    elif (status.get('RSCAM3_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAM3_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAM3_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAM3_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['CAM3'] = 0

    elif (status.get('RSCAM3_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAM3_230_CH8902_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAM3_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAM3_230_CH8904_S.s') == 'Estado do ponto digital:on'):
        
        config['CAM3'] = 0

    elif (status.get('RSCAM3_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAM3_230_CH8910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAM3_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAM3_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['CAM3'] = 0

    else:
        config['CAM3'] = 1

    #CANDELARIA 2 
    if (status.get('RSCDL2_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCDL2_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCDL2_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCDL2_230_CH8936_S.s') == 'Estado do ponto digital:on'):
        
        config['CDL2'] = 0

    elif (status.get('RSCDL2_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCDL2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCDL2_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCDL2_230_CH8932_S.s') == 'Estado do ponto digital:on'):
        
        config['CDL2'] = 0

    elif (status.get('RSCDL2_230_CH8908_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCDL2_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCDL2_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCDL2_230_CH8918_S.s') == 'Estado do ponto digital:on'):
        
        config['CDL2'] = 0

    else:
        config['CDL2'] = 1

    # CANDIOTA 2 
    if (status.get('RSCTA2_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCTA2_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCTA2_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCTA2_230_CH8908_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCTA2_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['CTA2'] = 0

    elif (status.get('RSCTA2_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCTA2_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCTA2_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCTA2_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['CTA2'] = 0

    elif (status.get('RSCTA2_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCTA2_230_CH8910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCTA2_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCTA2_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['CTA2'] = 0

    else:
        config['CTA2'] = 1



    #CANOAS 1 
    if (status.get('RSCNA1_230_CH8962_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNA1_230_CH8970_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNA1_230_CH8978_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNA1_230_CH8986_S.s') == 'Estado do ponto digital:on'):
        
        config['CNA1'] = 0

    elif (status.get('RSCNA1_230_CH8956_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA1_230_CH8964_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNA1_230_CH8958_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA1_230_CH8966_S.s') == 'Estado do ponto digital:on'):
        
        config['CNA1'] = 0

    elif (status.get('RSCNA1_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA1_230_CH8980_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNA1_230_CH8974_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA1_230_CH8982_S.s') == 'Estado do ponto digital:on'):
        
        config['CNA1'] = 0

    else:
        config['CNA1'] = 1

    #CANOAS 2 
    if (status.get('RSCNA2_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNA2_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNA2_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNA2_230_CH8960_S.s') == 'Estado do ponto digital:on'):
        
        config['CNA2'] = 0

    elif (status.get('RSCNA2_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA2_230_CH8954_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNA2_230_CH8934_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA2_230_CH8958_S.s') == 'Estado do ponto digital:on'):
        
        config['CNA2'] = 0

    elif (status.get('RSCNA2_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA2_230_CH8914_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNA2_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNA2_230_CH8918_S.s') == 'Estado do ponto digital:on'):
        
        config['CNA2'] = 0

    else:
        config['CNA2'] = 1

    # CAPIVARI DO SUL 
    if (status.get('RSCPS_230_CH7017_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCPS_230_CH7027_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCPS_230_CH7047_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCPS_230_CH7057_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCPS_230_CH7067_S.s') == 'Estado do ponto digital:on'):
        
        config['CPS'] = 0

    elif (status.get('RSCPS_230_CH7011_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCPS_230_CH7051_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCPS_230_CH7015_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCPS_230_CH7055_S.s') == 'Estado do ponto digital:on'):
        
        config['CPS'] = 0

    elif (status.get('RSCPS_230_CH7041_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCPS_230_CH7061_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCPS_230_CH7045_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCPS_230_CH7065_S.s') == 'Estado do ponto digital:on'):
        
        config['CPS'] = 0

    else:
        config['CPS'] = 1     

    # CAXIAS
    if (status.get('RSCAX_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX'] = 0

    elif (status.get('RSCAX_230_CH731_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH791_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH761_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH811_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH711_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH781_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH831_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSCAX_230_CH733_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH793_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH763_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH813_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH713_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH783_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH833_S.s') == 'Estado do ponto digital:on')):
        
        config['CAX'] = 0

    elif (status.get('RSCAX_230_CH751_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH791_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH761_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH811_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH711_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH781_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH831_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSCAX_230_CH753_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH793_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH763_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH813_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH713_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH783_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH833_S.s') == 'Estado do ponto digital:on')):
        
        config['CAX'] = 0

    elif (status.get('RSCAX_230_CH771_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH791_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH761_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH811_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH711_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH781_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH831_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSCAX_230_CH773_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH793_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH763_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH813_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH713_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH783_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH833_S.s') == 'Estado do ponto digital:on')):
        
        config['CAX'] = 0

    elif (status.get('RSCAX_230_CH741_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH791_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH761_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH811_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH711_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH781_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH831_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSCAX_230_CH743_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSCAX_230_CH793_S.s') == 'Estado do ponto digital:on' or
          status.get('RSCAX_230_CH763_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH813_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH713_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH783_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCAX_230_CH833_S.s') == 'Estado do ponto digital:on')):
        
        config['CAX'] = 0

    else:
        config['CAX'] = 1

    # CAXIAS DO SUL 5
    if (status.get('RSCAX5_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX5_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX5_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX5_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX5_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX5_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX5'] = 0

    elif (status.get('RSCAX5_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX5_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH8910_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX5'] = 0

    elif (status.get('RSCAX5_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX5_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH8910_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX5'] = 0

    elif (status.get('RSCAX5_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX5_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH8910_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX5'] = 0

    elif (status.get('RSCAX5_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX5_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX5'] = 0

    elif (status.get('RSCAX5_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX5_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX5_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX5'] = 0

    else:
        config['CAX5'] = 1

    #CAXIAS DO SUL 6
    if (status.get('RSCAX6_230_CH898_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX6_230_CH8916_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX6_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX6_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAX6_230_CH757_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX6'] = 0

    elif (status.get('RSCAX6_230_CH892_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX6_230_CH8910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX6_230_CH894_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX6_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX6'] = 0

    elif (status.get('RSCAX6_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX6_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAX6_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAX6_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['CAX6'] = 0       

    else:
        config['CAX6'] = 1

    # CAXIAS NORTE
    if (status.get('RSCNE_230_CH024_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNE_230_CH048_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNE_230_CH072_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNE_230_CH104_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCNE_230_CH120_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH136_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH152_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH160_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH196_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH727_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH737_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH89168_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCNE_230_CH89176_S.s') == 'Estado do ponto digital:on'):
        
        config['CNE'] = 0

    elif (status.get('RSCNE_230_CH018_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH042_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH066_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNE_230_CH020_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH044_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH068_S.s') == 'Estado do ponto digital:on'):
        
        config['CNE'] = 0

    elif (status.get('RSCNE_230_CH98_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH114_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH130_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNE_230_CH100_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH116_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH132_S.s') == 'Estado do ponto digital:on'):
        
        config['CNE'] = 0

    elif (status.get('RSCNE_230_CH146_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH154_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNE_230_CH148_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH156_S.s') == 'Estado do ponto digital:on'):
        
        config['CNE'] = 0

    elif (status.get('RSCNE_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH89170_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNE_230_CH723S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH89172_S.s') == 'Estado do ponto digital:on'):
        
        config['CNE'] = 0

    elif (status.get('RSCNE_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH89162_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCNE_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCNE_230_CH89164_S.s') == 'Estado do ponto digital:on'):
        
        config['CNE'] = 0

    else:
        config['CNE'] = 1

    # CERRO CHATO
    if (status.get('RSCCH_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH837_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH847_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH867_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCCH_230_CH887_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 3 4 5
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 3 4 6
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 3 4 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 3 5 6
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0       
# 1 2 3 5 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 3 6 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 4 5 6
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 2 4 5 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0    
# 1 2 4 6 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0   
# 1 2 5 6 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0  
# 1 3 4 5 6
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 3 4 5 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 1 3 4 6 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0     
# 1 3 5 6 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0    
# 1 4 5 6 7
    elif (status.get('RSCCH_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0  
# 2 3 4 5 6
    elif (status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0
# 2 3 4 5 7
    elif (status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0  
# 2 3 4 6 7
    elif (status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0  
# 2 3 5 6 7
    elif (status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0 
# 2 4 5 6 7
    elif (status.get('RSCCH_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0 
# 3 4 5 6 7
    elif (status.get('RSCCH_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH841_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH843_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0 

    elif (status.get('RSCCH_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCCH_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCCH_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['CCH'] = 0

    else:
        config['CCH'] = 1       

    # CHARQUEADAS
    if (status.get('RSCHA_230_CH739_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCHA_230_CH749_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCHA_230_CH759_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCHA_230_CH819_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA'] = 0

    elif (status.get('RSCHA_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA'] = 0

    elif (status.get('RSCHA_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH743_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH741_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA'] = 0

    elif (status.get('RSCHA_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH743_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH741_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA'] = 0

    elif (status.get('RSCHA_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH743_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH741_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA'] = 0

    elif (status.get('RSCHA_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA'] = 0

    else:
        config['CHA'] = 1

    #CHARQUEADAS 3
    if (status.get('RSCHA3_230_CH08_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCHA3_230_CH24_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCHA3_230_CH36_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCHA3_230_CH52_S.s') == 'Estado do ponto digital:on' or
        status.get('RSCHA3_230_CH140_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCHA3_230_CH152_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCHA3_230_CH160_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA3'] = 0

    elif (status.get('RSCHA3_230_CH146_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA3_230_CH154_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA3_230_CH150_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA3_230_CH158_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA3'] = 0

    elif (status.get('RSCHA3_230_CH04_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA3_230_CH32_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA3_230_CH06_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA3_230_CH34_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA3'] = 0  

    elif (status.get('RSCHA3_230_CH134_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA3_230_CH48_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCHA3_230_CH138_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCHA3_230_CH50_S.s') == 'Estado do ponto digital:on'):
        
        config['CHA3'] = 0  

    else:
        config['CHA3'] = 1

    # CIDADE INDUSTRIAL
    if  (status.get('RSCIN_230_CH8916_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89256_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8946_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8960_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89286_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8980_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89100_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89110_S.s') == 'Estado do ponto digital:on' or 
#        status.get('RSCIN_230_CH89120_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8990_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8970_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89226_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89266_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89236_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH8926_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89246_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSCIN_230_CH89276_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0
#A1
    elif ((status.get('RSCIN_230_CH8918_S.s') == 'Estado do ponto digital:on') and 
          (status.get('RSCIN_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
           status.get('RSCIN_230_CH8938_S.s') == 'Estado do ponto digital:on')) or \
         ((status.get('RSCIN_230_CH8920_S.s') == 'Estado do ponto digital:on') and 
          (status.get('RSCIN_230_CH8930_S.s') == 'Estado do ponto digital:on'  or 
           status.get('RSCIN_230_CH8940_S.s') == 'Estado do ponto digital:on')):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH8928_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH8940_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCIN_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH8938_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH89228_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89258_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCIN_230_CH89230_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89260_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH89238_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89268_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCIN_230_CH89240_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89270_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89248_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCIN_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89250_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0
#A2
    elif ((status.get('RSCIN_230_CH8962_S.s') == 'Estado do ponto digital:on') and 
          (status.get('RSCIN_230_CH89218_S.s') == 'Estado do ponto digital:on' or 
           status.get('RSCIN_230_CH8982_S.s') == 'Estado do ponto digital:on' or 
           status.get('RSCIN_230_CH89112_S.s') == 'Estado do ponto digital:on' or 
           status.get('RSCIN_230_CH8952_S.s') == 'Estado do ponto digital:on')) or \
         ((status.get('RSCIN_230_CH8964_S.s') == 'Estado do ponto digital:on') and 
          (status.get('RSCIN_230_CH89220_S.s') == 'Estado do ponto digital:on'  or 
           status.get('RSCIN_230_CH8984_S.s') == 'Estado do ponto digital:on' or 
           status.get('RSCIN_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
           status.get('RSCIN_230_CH8954_S.s') == 'Estado do ponto digital:on')):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH89218_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCIN_230_CH8982_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCIN_230_CH89112_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCIN_230_CH8952_S.s') == 'Estado do ponto digital:on') and \
         (status.get('RSCIN_230_CH89220_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCIN_230_CH8984_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCIN_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSCIN_230_CH8954_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89278_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCIN_230_CH8974_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89280_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0

    elif (status.get('RSCIN_230_CH8992_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89102_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCIN_230_CH8994_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCIN_230_CH89104_S.s') == 'Estado do ponto digital:on'):
        
        config['CIN'] = 0        

    else:
        config['CIN'] = 1

    #CRUZ ALTA 2
    if (status.get('RSCAL2_230_CH8908_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAL2_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAL2_230_CH2924_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSCAL2_230_CH2936_S.s') == 'Estado do ponto digital:on'):
        
        config['CAL2'] = 0

    elif (status.get('RSCAL2_230_CH2918_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAL2_230_CH2930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAL2_230_CH2922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAL2_230_CH2934_S.s') == 'Estado do ponto digital:on'):
        
        config['CAL2'] = 0

    elif (status.get('RSCAL2_230_CH8904_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAL2_230_CH8912_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSCAL2_230_CH8906_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSCAL2_230_CH8914_S.s') == 'Estado do ponto digital:on'):
        
        config['CAL2'] = 0       

    else:
        config['CAL2'] = 1

    #ELDORADO DO SUL 
    if (status.get('RSELD_230_CH8952_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSELD_230_CH8960_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSELD_230_CH8968_S.s') == 'Estado do ponto digital:on'):
        
        config['ELD'] = 0

    elif (status.get('RSELD_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSELD_230_CH8956_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSELD_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSELD_230_CH8954_S.s') == 'Estado do ponto digital:on'):
        
        config['ELD'] = 0

    else:
        config['ELD'] = 1

    # FARROUPILHA 
    if (status.get('RSFAR_230_CH715_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH725_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH735_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH745_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH755_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH765_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH775_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH785_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH795_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH805_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFAR_230_CH815_S.s') == 'Estado do ponto digital:on'):
        
        config['FAR'] = 0

    elif (status.get('RSFAR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFAR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['FAR'] = 0          

    elif (status.get('RSFAR_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFAR_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['FAR'] = 0  

    elif (status.get('RSFAR_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFAR_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['FAR'] = 0  

    elif (status.get('RSFAR_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFAR_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['FAR'] = 0  

    elif (status.get('RSFAR_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFAR_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFAR_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['FAR'] = 0  

    else:
        config['FAR'] = 1

    # GRAVATAÍ 2
    if ((status.get('RSGRA2_230_CH8926_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8946_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8956_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8966_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8976_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8986_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH8996_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89106_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89116_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89126_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89136_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89146_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89166_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89176_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89186_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89196_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89206_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89216_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89226_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89236_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89246_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSGRA2_230_CH89256_S.s') == 'Estado do ponto digital:on')):
        
        config['GRA2'] = 0
# A1 e B1
    elif (status.get('RSGRA2_230_CH8998_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89118_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH89100_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89120_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH8918_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8928_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH8920_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8930_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH8958_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8968_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH8960_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8970_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH8978_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8988_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH8980_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8990_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif((status.get('RSGRA2_230_CH89108_S.s') == 'Estado do ponto digital:on') and 
         (status.get('RSGRA2_230_CH8938_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH8948_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('RSGRA2_230_CH89110_S.s') == 'Estado do ponto digital:on') and 
         (status.get('RSGRA2_230_CH8940_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH8950_S.s') == 'Estado do ponto digital:on')):
        
        config['GRA2'] = 0  

    elif (status.get('RSGRA2_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8950_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8948_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0 

# A2 e B2
    elif (status.get('RSGRA2_230_CH89198_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89208_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH89200_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89210_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH89178_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89188_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH89180_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89190_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH89238_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89248_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH89240_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89250_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH89168_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89228_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH89170_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH89230_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0

    elif (status.get('RSGRA2_230_CH89158_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH89138_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH89218_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH89128_S.s') == 'Estado do ponto digital:on') and \
         (status.get('RSGRA2_230_CH89160_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH89140_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH89220_S.s') == 'Estado do ponto digital:on' or
          status.get('RSGRA2_230_CH89130_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0  

    elif (status.get('RSGRA2_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8950_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA2_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA2_230_CH8948_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA2'] = 0       

    else:
        config['GRA2'] = 1

    # GRAVATAÍ 3 
    if (status.get('RSGRA3_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGRA3_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGRA3_230_CH847_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGRA3_230_CH892_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGRA3_230_CH897_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGRA3_230_CH907_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGRA3_230_CH8910_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA3'] = 0

    elif (status.get('RSGRA3_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA3_230_CH901_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA3_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA3_230_CH903_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA3'] = 0

    elif (status.get('RSGRA3_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA3_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA3_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA3_230_CH8914_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA3'] = 0

    elif (status.get('RSGRA3_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA3_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGRA3_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGRA3_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['GRA3'] = 0

    else:
        config['GRA3'] = 1

    # GUAÍBA 3 
    if (status.get('RSGUA3_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGUA3_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGUA3_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGUA3_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSGUA3_230_CH767_S.s') == 'Estado do ponto digital:on'):
        
        config['GUA3'] = 0

    elif (status.get('RSGUA3_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGUA3_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGUA3_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGUA3_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['GUA3'] = 0

    elif (status.get('RSGUA3_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGUA3_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSGUA3_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSGUA3_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['GUA3'] = 0

    else:
        config['GUA3'] = 1

    # IJUÍ 2 
    if (status.get('RSIJU2_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSIJU2_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSIJU2_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSIJU2_230_CH898_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSIJU2_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['IJU2'] = 0

    elif (status.get('RSIJU2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSIJU2_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSIJU2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSIJU2_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['IJU2'] = 0

    elif (status.get('RSIJU2_230_CH892_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSIJU2_230_CH8910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSIJU2_230_CH894_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSIJU2_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['IJU2'] = 0

    else:
        config['IJU2'] = 1

    # JARDIM BOTÂNICO 
    if (status.get('RSJBO_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSJBO_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSJBO_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSJBO_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSJBO_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSJBO_230_CH8952_S.s') == 'Estado do ponto digital:on'):
        
        config['JBO'] = 0

    elif (status.get('RSJBO_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8932_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8948_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSJBO_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8934_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8950_S.s') == 'Estado do ponto digital:on'):
        
        config['JBO'] = 0

    elif (status.get('RSJBO_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8924_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSJBO_230_CH8918_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8926_S.s') == 'Estado do ponto digital:on'):
        
        config['JBO'] = 0

    elif (status.get('RSJBO_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8940_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSJBO_230_CH8918_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8942_S.s') == 'Estado do ponto digital:on'):
        
        config['JBO'] = 0
# PAL1 P e PA10 PT - PA10 P e PAL1 PT
    elif (status.get('RSJBO_230_CH8942_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8924_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSJBO_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSJBO_230_CH8926_S.s') == 'Estado do ponto digital:on'):
        
        config['JBO'] = 0

    else:
        config['JBO'] = 1

    # LAGOA VERMELHA 2 
    if (status.get('RSLVE2_230_CH8910_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLVE2_230_CH8918_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLVE2_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLVE2_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLVE2_230_CH8974_S.s') == 'Estado do ponto digital:on'):
        
        config['LVE2'] = 0

    elif (status.get('RSLVE2_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLVE2_230_CH8932_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLVE2_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLVE2_230_CH8934_S.s') == 'Estado do ponto digital:on'):
        
        config['LVE2'] = 0

    elif (status.get('RSLVE2_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLVE2_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLVE2_230_CH8912_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLVE2_230_CH8920_S.s') == 'Estado do ponto digital:on'):
        
        config['LVE2'] = 0

    else:
        config['LVE2'] = 1                    

    # LAJEADO 3 
    if (status.get('RSLAJ3_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLAJ3_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLAJ3_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLAJ3_230_CH777_S.s') == 'Estado do ponto digital:on'):
        
        config['LAJ3'] = 0

    elif (status.get('RSLAJ3_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLAJ3_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLAJ3_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLAJ3_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['LAJ3'] = 0

    elif (status.get('RSLAJ3_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLAJ3_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLAJ3_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLAJ3_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['LAJ3'] = 0

    else:
        config['LAJ3'] = 1

    # LAJEADO GRANDE 
    if (status.get('RSLGR_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLGR_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLGR_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLGR_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLGR_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['LGR'] = 0

    elif (status.get('RSLGR_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLGR_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLGR_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLGR_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['LGR'] = 0

    elif (status.get('RSLGR_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLGR_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLGR_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLGR_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['LGR'] = 0

    else:
        config['LGR'] = 1

    # LIVRAMENTO 3
    if (status.get('RSLIV3_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8932_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8940_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8948_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8956_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8966_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8974_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH8984_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSLIV3_230_CH89104_S.s') == 'Estado do ponto digital:on'):
        
        config['LIV3'] = 0

    elif (status.get('RSLIV3_230_CH8934_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSLIV3_230_CH8926_S.s') == 'Estado do ponto digital:on' or
          status.get('RSLIV3_230_CH8998_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSLIV3_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSLIV3_230_CH8930_S.s') == 'Estado do ponto digital:on' or
          status.get('RSLIV3_230_CH89102_S.s') == 'Estado do ponto digital:on')):
        
        config['LIV3'] = 0

    elif (status.get('RSLIV3_230_CH8914_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSLIV3_230_CH8926_S.s') == 'Estado do ponto digital:on' or
          status.get('RSLIV3_230_CH8998_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSLIV3_230_CH8918_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSLIV3_230_CH8930_S.s') == 'Estado do ponto digital:on' or
          status.get('RSLIV3_230_CH89102_S.s') == 'Estado do ponto digital:on')):
        
        config['LIV3'] = 0

    elif (status.get('RSLIV3_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8978_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLIV3_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8982_S.s') == 'Estado do ponto digital:on'):
        
        config['LIV3'] = 0

    elif (status.get('RSLIV3_230_CH8942_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8960_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLIV3_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8964_S.s') == 'Estado do ponto digital:on'):
        
        config['LIV3'] = 0

    elif (status.get('RSLIV3_230_CH8950_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8968_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLIV3_230_CH8954_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8972_S.s') == 'Estado do ponto digital:on'):
        
        config['LIV3'] = 0

    elif (status.get('RSLIV3_230_CH8934_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8918_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLIV3_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8914_S.s') == 'Estado do ponto digital:on'):
        
        config['LIV3'] = 0 

    elif (status.get('RSLIV3_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH89102_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSLIV3_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSLIV3_230_CH8998_S.s') == 'Estado do ponto digital:on'):
        
        config['LIV3'] = 0 

    else:
        config['LIV3'] = 1 

    # MAÇAMBARÁ 3 
    if (status.get('RSMBR3_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMBR3_230_CH8922_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMBR3_230_CH8930_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMBR3_230_CH8940_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMBR3_230_CH8948_S.s') == 'Estado do ponto digital:on'):
        
        config['MBR3'] = 0

    elif (status.get('RSMBR3_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMBR3_230_CH8942_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMBR3_230_CH8928_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMBR3_230_CH8946_S.s') == 'Estado do ponto digital:on'):
        
        config['MBR3'] = 0

    elif (status.get('RSMBR3_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMBR3_230_CH8934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMBR3_230_CH8920_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMBR3_230_CH8938_S.s') == 'Estado do ponto digital:on'):
        
        config['MBR3'] = 0

    else:
        config['MBR3'] = 1 

    # MISSÕES 
    if (status.get('RSMIS_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMIS_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMIS_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMIS_230_CH892_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMIS_230_CH8910_S.s') == 'Estado do ponto digital:on'):
        
        config['MIS'] = 0

    elif (status.get('RSMIS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH761_S.s') == 'Estado do ponto digital:on' and
          status.get('RSMIS_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMIS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH763_S.s') == 'Estado do ponto digital:on' and
          status.get('RSMIS_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['MIS'] = 0

    elif (status.get('RSMIS_230_CH894_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH8912_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMIS_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['MIS'] = 0

    elif (status.get('RSMIS_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH731_S.s') == 'Estado do ponto digital:on'and 
          status.get('RSMIS_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMIS_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMIS_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH761_S.s') == 'Estado do ponto digital:on'):
        
        config['MIS'] = 0

    elif (status.get('RSMIS_230_CH8912_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH733_S.s') == 'Estado do ponto digital:on'and 
          status.get('RSMIS_230_CH753_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMIS_230_CH8912_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH763_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMIS_230_CH8912_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMIS_230_CH763_S.s') == 'Estado do ponto digital:on'):

        config['MIS'] = 0

    else:
        config['MIS'] = 1 

    # MONTE CLARO
    if (status.get('RSMCL_230_CH707_S.s') == 'Estado do ponto digital:on' or
        status.get('RSMCL_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSMCL_230_CH797_S.s') == 'Estado do ponto digital:on'):
        
        config['MCL'] = 0

    elif (status.get('RSMCL_230_CH771_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSMCL_230_CH751_S.s') == 'Estado do ponto digital:on' or
          status.get('RSMCL_230_CH791_S.s') == 'Estado do ponto digital:on' or
          status.get('RSMCL_230_CH711_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSMCL_230_CH773_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSMCL_230_CH753_S.s') == 'Estado do ponto digital:on' or
          status.get('RSMCL_230_CH793_S.s') == 'Estado do ponto digital:on' or
          status.get('RSMCL_230_CH713_S.s') == 'Estado do ponto digital:on')):
        
        config['MCL'] = 0

    elif (status.get('RSMCL_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMCL_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['MCL'] = 0 

    elif (status.get('RSMCL_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH701_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMCL_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH703_S.s') == 'Estado do ponto digital:on'):
        
        config['MCL'] = 0 

    elif (status.get('RSMCL_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMCL_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['MCL'] = 0 

    elif (status.get('RSMCL_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSMCL_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSMCL_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['MCL'] = 0 

    else:
        config['MCL'] = 1 
    #NOVA PETROPOLIS 2 
    if (status.get('RSNPE2_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPE2_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPE2_230_CH898_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPE2_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['NPE2'] = 0

    elif (status.get('RSNPE2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPE2_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNPE2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPE2_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['NPE2'] = 0

    elif (status.get('RSNPE2_230_CH892_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPE2_230_CH8910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNPE2_230_CH894_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPE2_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['NPE2'] = 0

    else:
        config['NPE2'] = 1

    # NOVA PRATA 2 
    if (status.get('RSNPR2_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPR2_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPR2_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPR2_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPR2_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPR2_230_CH89122_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSNPR2_230_CH89180_S.s') == 'Estado do ponto digital:on'):
        
        config['NPR2'] = 0

    elif (status.get('RSNPR2_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPR2_230_CH89174_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNPR2_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPR2_230_CH89176_S.s') == 'Estado do ponto digital:on'):
        
        config['NPR2'] = 0

    elif (status.get('RSNPR2_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPR2_230_CH8922_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNPR2_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPR2_230_CH8924_S.s') == 'Estado do ponto digital:on'):
        
        config['NPR2'] = 0

    elif (status.get('RSNPR2_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPR2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNPR2_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNPR2_230_CH8932_S.s') == 'Estado do ponto digital:on'):
        
        config['NPR2'] = 0        

    else:
        config['NPR2'] = 1 

    # NOVA SANTA RITA
    if  (status.get('RSNSR_230_CH737_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH767_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH797_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH807_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH847_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH877_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH887_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8924_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8932_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8940_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8972_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8980_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8988_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSNSR_230_CH8996_S.s') == 'Estado do ponto digital:on'):
        
        config['NSR'] = 0

    elif((status.get('RSNSR_230_CH8974_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8982_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8918_S.s') == 'Estado do ponto digital:on') and 
         (status.get('RSNSR_230_CH8990_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8934_S.s') == 'Estado do ponto digital:on' or
          status.get('RSNSR_230_CH8966_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8926_S.s') == 'Estado do ponto digital:on'  or 
          status.get('RSNSR_230_CH801_S.s') == 'Estado do ponto digital:on')):
        
        config['NSR'] = 0

    elif((status.get('RSNSR_230_CH8976_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8984_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8920_S.s') == 'Estado do ponto digital:on') and 
         (status.get('RSNSR_230_CH8992_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8936_S.s') == 'Estado do ponto digital:on' or
          status.get('RSNSR_230_CH8968_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSNSR_230_CH8928_S.s') == 'Estado do ponto digital:on'  or 
          status.get('RSNSR_230_CH803_S.s') == 'Estado do ponto digital:on')):
        
        config['NSR'] = 0

    elif (status.get('RSNSR_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNSR_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['NSR'] = 0

    elif (status.get('RSNSR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNSR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['NSR'] = 0

    elif (status.get('RSNSR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNSR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['NSR'] = 0

    elif (status.get('RSNSR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNSR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['NSR'] = 0

    elif (status.get('RSNSR_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSNSR_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSNSR_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['NSR'] = 0

    else:
        config['NSR'] = 1

    # OSÓRIO 3
    if   (status.get('RSOSO3_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSOSO3_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSOSO3_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSOSO3_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['OSO3'] = 0

    else:
        config['OSO3'] = 1

    # PASSO FUNDO
    if   (status.get('RSPFU_230_CH715_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH725_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH735_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH745_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH765_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH775_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH785_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH795_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH815_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSPFU_230_CH825_S.s') == 'Estado do ponto digital:on'):
        
        config['UHPF'] = 0

    elif (status.get('RSPFU_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH821_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPFU_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH823_S.s') == 'Estado do ponto digital:on'):
        
        config['UHPF'] = 0


    elif (status.get('RSPFU_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPFU_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['UHPF'] = 0

    elif (status.get('RSPFU_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPFU_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['UHPF'] = 0

    elif (status.get('RSPFU_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPFU_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['UHPF'] = 0

    elif (status.get('RSPFU_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPFU_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPFU_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['UHPF'] = 0

    else:
        config['UHPF'] = 1

    # PASSO REAL
    if   (status.get('RSUPRE_230_CH8918_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSUPRE_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSUPRE_230_CH8938_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSUPRE_230_CH8948_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSUPRE_230_CH8994_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSUPRE_230_CH89100_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSUPRE_230_CH89110_S.s') == 'Estado do ponto digital:on'):
        
        config['UPRE'] = 0

    elif (status.get('RSUPRE_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH89102_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSUPRE_230_CH8942_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH89104_S.s') == 'Estado do ponto digital:on'):
        
        config['UPRE'] = 0

    elif (status.get('RSUPRE_230_CH892_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH896_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSUPRE_230_CH894_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH898_S.s') == 'Estado do ponto digital:on'):
        
        config['UPRE'] = 0

    elif (status.get('RSUPRE_230_CH8920_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH8982_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSUPRE_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH8984_S.s') == 'Estado do ponto digital:on'):
        
        config['UPRE'] = 0

    elif (status.get('RSUPRE_230_CH8986_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH8910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSUPRE_230_CH8988_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSUPRE_230_CH8912_S.s') == 'Estado do ponto digital:on'):
        
        config['UPRE'] = 0

    else:
        config['UPRE'] = 1

# POLO PETROQUÍMICO
    if  ((status.get('RSPPE_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
        (status.get('RSPPE_230_CH8930_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSPPE_230_CH89108_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSPPE_230_CH8950_S.s') == 'Estado do ponto digital:on')) or 
	      (status.get('RSPPE_230_CH8942_S.s') == 'Estado do ponto digital:on' and 
        (status.get('RSPPE_230_CH8932_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSPPE_230_CH89110_S.s') == 'Estado do ponto digital:on' or 
         status.get('RSPPE_230_CH8952_S.s') == 'Estado do ponto digital:on'))):
        
        config['PPE'] = 0

    elif((status.get('RSPPE_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH896_S.s') == 'Estado do ponto digital:on') or
          (status.get('RSPPE_230_CH8912_S.s') == 'Estado do ponto digital:on' and
          status.get('RSPPE_230_CH898_S.s') == 'Estado do ponto digital:on')):

        config['PPE'] = 0

    elif((status.get('RSPPE_230_CH8964_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8960_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8972_S.s') == 'Estado do ponto digital:on' and
          status.get('RSPPE_230_CH8968_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8966_S.s') == 'Estado do ponto digital:on' and
          status.get('RSPPE_230_CH8962_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8974_S.s') == 'Estado do ponto digital:on' and
          status.get('RSPPE_230_CH8970_S.s') == 'Estado do ponto digital:on')):
        
        config['PPE'] = 0

    elif((status.get('RSPPE_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8968_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8964_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8968_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8960_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8964_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8960_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8968_S.s') == 'Estado do ponto digital:on' and
          status.get('RSPPE_230_CH8964_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8960_S.s') == 'Estado do ponto digital:on')):
        
        config['PPE'] = 0

    elif((status.get('RSPPE_230_CH8974_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8970_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8966_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8974_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8970_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8962_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8974_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8966_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8962_S.s') == 'Estado do ponto digital:on') or
         (status.get('RSPPE_230_CH8970_S.s') == 'Estado do ponto digital:on' and
          status.get('RSPPE_230_CH8966_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPPE_230_CH8962_S.s') == 'Estado do ponto digital:on')):
        
        config['PPE'] = 0

    else:
        config['PPE'] = 1

    # PORTO ALEGRE 1
    if   (status.get('RSPAL1_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL1_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL1_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL1_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL1'] = 0

    elif (status.get('RSPAL1_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL1_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL1_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL1_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL1_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL1_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL1'] = 0

    else:
        config['PAL1'] = 1

    # PORTO ALEGRE 4 
    if (status.get('RSPAL4_230_CH08_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH22_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH30_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH38_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH50_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH58_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH66_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL4_230_CH74_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    elif (status.get('RSPAL4_230_CH68_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH60_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH52_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH24_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL4_230_CH72_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH64_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH56_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH28_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    elif (status.get('RSPAL4_230_CH68_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH60_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH52_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH16_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL4_230_CH72_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH64_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH56_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH20_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    elif (status.get('RSPAL4_230_CH68_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH60_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH24_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH16_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL4_230_CH72_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH64_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH28_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH20_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    elif (status.get('RSPAL4_230_CH68_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH52_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH24_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH16_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL4_230_CH72_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH56_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH28_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH20_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    elif (status.get('RSPAL4_230_CH60_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH52_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH24_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH16_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL4_230_CH64_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH56_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH28_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH20_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    elif (status.get('RSPAL4_230_CH32_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH44_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL4_230_CH36_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL4_230_CH48_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL4'] = 0

    else:
        config['PAL4'] = 1

    # PORTO ALEGRE 6
    if (status.get('RSPAL6_230_CH8914_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH8924_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH8934_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH8954_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH8964_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL6_230_CH89134_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL6'] = 0

    elif (status.get('RSPAL6_230_CH8936_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH89126_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL6_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH8928_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH89128_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL6'] = 0

    elif (status.get('RSPAL6_230_CH89126_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH8946_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL6_230_CH89128_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH8948_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL6'] = 0

    elif (status.get('RSPAL6_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL6_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH8918_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL6'] = 0

    elif (status.get('RSPAL6_230_CH8956_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH89106_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL6_230_CH8958_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL6_230_CH89108_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL6'] = 0

    else:
        config['PAL6'] = 1

    # PORTO ALEGRE 8
    if (status.get('RSPAL8_230_CH896_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL8_230_CH8914_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL8_230_CH8922_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL8_230_CH8930_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL8_230_CH8938_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL8_230_CH8946_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL8'] = 0

    elif (status.get('RSPAL8_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL8_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL8_230_CH8924_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL8_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL8_230_CH8918_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL8_230_CH8926_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL8'] = 0

    elif (status.get('RSPAL8_230_CH8934_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL8_230_CH8942_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL8_230_CH8936_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL8_230_CH8944_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL8'] = 0

    else:
        config['PAL8'] = 1

    # PORTO ALEGRE 9
    if (status.get('RSPAL9_230_CH8914_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH8924_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH8934_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH89116_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH89126_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH89136_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH89146_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPAL9_230_CH89164_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL9'] = 0

    elif (status.get('RSPAL9_230_CH8936_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89118_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL9_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH8928_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89120_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL9'] = 0

    elif (status.get('RSPAL9_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89128_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL9_230_CH8928_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89130_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL9'] = 0

    elif (status.get('RSPAL9_230_CH89140_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89128_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL9_230_CH89138_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89130_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL9'] = 0

    elif (status.get('RSPAL9_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL9_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH8918_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL9'] = 0

    elif (status.get('RSPAL9_230_CH89108_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89158_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPAL9_230_CH89110_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPAL9_230_CH89156_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL9'] = 0

    else:
        config['PAL9'] = 1

    # PORTO ALEGRE 10 
    if (status.get('RSPA10_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA10_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA10_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA10_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA10_230_CH8952_S.s') == 'Estado do ponto digital:on'):
        
        config['PA10'] = 0

    elif (status.get('RSPA10_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA10_230_CH8946_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPA10_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA10_230_CH8948_S.s') == 'Estado do ponto digital:on'):
        
        config['PA10'] = 0

    elif (status.get('RSPA10_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA10_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPA10_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA10_230_CH8932_S.s') == 'Estado do ponto digital:on'):
        
        config['PA10'] = 0

    else:
        config['PA10'] = 1


    #PORTO ALEGRE 13
    if (status.get('RSPA13_230_CH89210_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA13_230_CH89218_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA13_230_CH89222_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPA13_230_CH89226_S.s') == 'Estado do ponto digital:on'):
        
        config['PA13'] = 0

    elif (status.get('RSPA13_230_CH8904_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA13_230_CH8908_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPA13_230_CH89220_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA13_230_CH89224_S.s') == 'Estado do ponto digital:on'):
        
        config['PA13'] = 0

    elif (status.get('RSPA13_230_CH89204_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA13_230_CH89212_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPA13_230_CH89206_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPA13_230_CH89214_S.s') == 'Estado do ponto digital:on'):
        
        config['PA13'] = 0

    else:
        config['PA13'] = 1

    #POVO NOVO 
    if (status.get('RSPNO_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPNO_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPNO_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSPNO_230_CH817_S.s') == 'Estado do ponto digital:on'):
        
        config['PNO'] = 0

    elif (status.get('RSPNO_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPNO_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPNO_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPNO_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['PNO'] = 0

    elif (status.get('RSPNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPNO_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSPNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSPNO_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['PNO'] = 0

    else:
        config['PNO'] = 1

    #RESTINGA 
    if (status.get('RSRES_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSRES_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSRES_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSRES_230_CH8936_S.s') == 'Estado do ponto digital:on'):
        
        config['RES'] = 0

    elif (status.get('RSRES_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSRES_230_CH8932_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSRES_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSRES_230_CH8930_S.s') == 'Estado do ponto digital:on'):
        
        config['RES'] = 0

    elif (status.get('RSRES_230_CH8910_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSRES_230_CH8918_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSRES_230_CH8908_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSRES_230_CH8916_S.s') == 'Estado do ponto digital:on'):
        
        config['RES'] = 0

    else:
        config['RES'] = 1

    # SANTA MARIA 3 
    if (status.get('RSSMA3_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH8978_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH8986_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH89106_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH89166_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH89176_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSMA3_230_CH89204_S.s') == 'Estado do ponto digital:on'):
        
        config['SMA3'] = 0

    elif (status.get('RSSMA3_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8980_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSMA3_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8932_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8982_S.s') == 'Estado do ponto digital:on'):
        
        config['SMA3'] = 0

    elif (status.get('RSSMA3_230_CH89100_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH89108_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSMA3_230_CH89102_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH89110_S.s') == 'Estado do ponto digital:on'):
        
        config['SMA3'] = 0

    elif (status.get('RSSMA3_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8972_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSMA3_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8974_S.s') == 'Estado do ponto digital:on'):
        
        config['SMA3'] = 0

    elif (status.get('RSSMA3_230_CH89162_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH89200_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSMA3_230_CH89160_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH89198_S.s') == 'Estado do ponto digital:on'):
        
        config['SMA3'] = 0


    elif (status.get('RSSMA3_230_CH89172_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8916_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSMA3_230_CH89170_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSMA3_230_CH8914_S.s') == 'Estado do ponto digital:on'):
        
        config['SMA3'] = 0

    else:
        config['SMA3'] = 1

    # SANTO ÂNGELO
    if (status.get('RSSTA_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSTA_230_CH817_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    elif (status.get('RSSTA_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSTA_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSTA_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['STA'] = 0

    else:
        config['STA'] = 1   

    # SÃO VICENTE DO SUL
    if (status.get('RSSVI_230_CH8910_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSVI_230_CH89110_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSVI_230_CH89118_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSVI_230_CH89122_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSSVI_230_CH89132_S.s') == 'Estado do ponto digital:on'):
        
        config['SVI'] = 0

    elif (status.get('RSSVI_230_CH89104_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSVI_230_CH89126_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSVI_230_CH89106_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSVI_230_CH89128_S.s') == 'Estado do ponto digital:on'):
        
        config['SVI'] = 0

    elif (status.get('RSSVI_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSVI_230_CH892_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSVI_230_CH89112_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSSVI_230_CH89114_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSVI_230_CH89120_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSSVI_230_CH89124_S.s') == 'Estado do ponto digital:on'):
        
        config['SVI'] = 0

    else:
        config['SVI'] = 1        

# SCHARLAU 2
    if((status.get('RSSCH2_230_DJ526_S.s') == 'Estado do ponto digital:on' and 
        status.get('RSSCH2_230_DJ527_S.s') == 'Estado do ponto digital:on' and 
        status.get('RSSCH2_230_DJ528_S.s') == 'Estado do ponto digital:on') or \
       (status.get('RSSCH2_230_DJ526_S.s') == 'Estado do ponto digital:on'  and 
        status.get('RSSCH2_230_DJ527_S.s') == 'Estado do ponto digital:off' and 
        status.get('RSSCH2_230_DJ528_S.s') == 'Estado do ponto digital:off') or \
       (status.get('RSSCH2_230_DJ526_S.s') == 'Estado do ponto digital:off' and 
        status.get('RSSCH2_230_DJ527_S.s') == 'Estado do ponto digital:on'  and 
        status.get('RSSCH2_230_DJ528_S.s') == 'Estado do ponto digital:off') or \
       (status.get('RSSCH2_230_DJ526_S.s') == 'Estado do ponto digital:off' and 
        status.get('RSSCH2_230_DJ527_S.s') == 'Estado do ponto digital:off' and 
        status.get('RSSCH2_230_DJ528_S.s') == 'Estado do ponto digital:on') or \
       (status.get('RSSCH2_230_DJ526_S.s') == 'Estado do ponto digital:off' and 
        status.get('RSSCH2_230_DJ527_S.s') == 'Estado do ponto digital:off' and 
        status.get('RSSCH2_230_DJ528_S.s') == 'Estado do ponto digital:off')):

        if (status.get('RSSCH2_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8952_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8960_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8968_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8976_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8984_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8954_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8962_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8956_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8964_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8970_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8978_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8980_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8954_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8956_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8932_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8962_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8964_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8932_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8954_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8962_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8956_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8964_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8932_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8938_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8932_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8940_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8914_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8922_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8924_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        else:
            config['SCH2'] = 1

    else:
        if (status.get('RSSCH2_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8952_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8960_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8968_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8976_S.s') == 'Estado do ponto digital:on' or 
            status.get('RSSCH2_230_CH8984_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8954_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8956_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8946_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8962_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8948_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8964_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8962_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8954_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8964_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8956_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8970_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8978_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8972_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8980_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8938_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8932_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8940_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        elif (status.get('RSSCH2_230_CH8914_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8922_S.s') == 'Estado do ponto digital:on') or \
             (status.get('RSSCH2_230_CH8916_S.s') == 'Estado do ponto digital:on' and 
              status.get('RSSCH2_230_CH8924_S.s') == 'Estado do ponto digital:on'):
            
            config['SCH2'] = 0

        else:
            config['SCH2'] = 1


    # TAPERA 2
    if (status.get('RSTPR2_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTPR2_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTPR2_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTPR2_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTPR2_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTPR2_230_CH8936_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0

    elif (status.get('RSTPR2_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTPR2_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0

    elif (status.get('RSTPR2_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTPR2_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8934_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0

    elif (status.get('RSTPR2_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTPR2_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8934_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0

    elif (status.get('RSTPR2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTPR2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8934_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0

    elif (status.get('RSTPR2_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTPR2_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8934_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0

    elif (status.get('RSTPR2_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8930_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTPR2_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTPR2_230_CH8934_S.s') == 'Estado do ponto digital:on'):
        
        config['TPR2'] = 0       

    else:
        config['TPR2'] = 1   

    # TAQUARA 
    if (status.get('RSTAQ_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTAQ_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTAQ_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTAQ_230_CH89130_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTAQ_230_CH89190_S.s') == 'Estado do ponto digital:on'):
        
        config['TAQ'] = 0

    elif (status.get('RSTAQ_230_CH896_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTAQ_230_CH89124_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTAQ_230_CH898_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTAQ_230_CH89126_S.s') == 'Estado do ponto digital:on'):
        
        config['TAQ'] = 0

    elif (status.get('RSTAQ_230_CH8922_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTAQ_230_CH89186_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTAQ_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTAQ_230_CH89184_S.s') == 'Estado do ponto digital:on'):
        
        config['TAQ'] = 0

    else:
        config['TAQ'] = 1

    #TORRES 2 
    if (status.get('RSTOR2_230_CH7011_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTOR2_230_CH7021_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTOR2_230_CH7031_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSTOR2_230_CH7041_S.s') == 'Estado do ponto digital:on'):
        
        config['TOR2'] = 0

    elif (status.get('RSTOR2_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTOR2_230_CH7043_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTOR2_230_CH7029_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTOR2_230_CH7049_S.s') == 'Estado do ponto digital:on'):
        
        config['TOR2'] = 0

    elif (status.get('RSTOR2_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTOR2_230_CH7033_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSTOR2_230_CH7019_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSTOR2_230_CH7039_S.s') == 'Estado do ponto digital:on'):
        
        config['TOR2'] = 0

    else:
        config['TOR2'] = 1

    # VIAMÃO 3 
    if (status.get('RSVIA3_230_CH8912_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH8920_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH8928_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH8936_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH8944_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH8952_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH89118_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIA3_230_CH89136_S.s') == 'Estado do ponto digital:on'):
        
        config['VIA3'] = 0

    elif (status.get('RSVIA3_230_CH8932_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8948_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89116_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8918_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8910_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSVIA3_230_CH8930_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8946_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8916_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8908_S.s') == 'Estado do ponto digital:on')):
        
        config['VIA3'] = 0

    elif (status.get('RSVIA3_230_CH8940_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8948_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89116_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8918_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8910_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSVIA3_230_CH8938_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8946_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8916_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8908_S.s') == 'Estado do ponto digital:on')):
        
        config['VIA3'] = 0

    elif (status.get('RSVIA3_230_CH89134_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8948_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89116_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8918_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8910_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSVIA3_230_CH89132_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8946_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8916_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8908_S.s') == 'Estado do ponto digital:on')):
        
        config['VIA3'] = 0

    elif (status.get('RSVIA3_230_CH8926_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8948_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89116_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8918_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8910_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('RSVIA3_230_CH8924_S.s') == 'Estado do ponto digital:on' and 
         (status.get('RSVIA3_230_CH8946_S.s') == 'Estado do ponto digital:on' or
          status.get('RSVIA3_230_CH89114_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8916_S.s') == 'Estado do ponto digital:on' or 
          status.get('RSVIA3_230_CH8908_S.s') == 'Estado do ponto digital:on')):
        
        config['VIA3'] = 0

    else:
        config['VIA3'] = 1

    # VILA MARIA 
    if (status.get('RSVMT_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVMT_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVMT_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVMT_230_CH837_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVMT_230_CH857_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVMT_230_CH877_S.s') == 'Estado do ponto digital:on'):
        
        config['VMT'] = 0

    elif (status.get('RSVMT_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVMT_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSVMT_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVMT_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['VMT'] = 0

    elif (status.get('RSVMT_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVMT_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSVMT_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVMT_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['VMT'] = 0

    elif (status.get('RSVMT_230_CH851_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVMT_230_CH871_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSVMT_230_CH853_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVMT_230_CH873_S.s') == 'Estado do ponto digital:on'):
        
        config['VMT'] = 0

    else:
        config['VMT'] = 1

    # VINHEDOS 
    if (status.get('RSVIN_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIN_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIN_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIN_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSVIN_230_CH777_S.s') == 'Estado do ponto digital:on'):
        
        config['VIN'] = 0

    elif (status.get('RSVIN_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVIN_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSVIN_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVIN_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['VIN'] = 0

    elif (status.get('RSVIN_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVIN_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSVIN_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSVIN_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['VIN'] = 0

    else:
        config['VIN'] = 1


    # SANTA CATARINA

    # ABDON BATISTA 
    if (status.get('SCABT_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCABT_230_CH827_S.s') == 'Estado do ponto digital:on'):
        
        config['ABT'] = 0

    elif (status.get('SCABT_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCABT_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['ABT'] = 0

    elif (status.get('SCABT_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCABT_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['ABT'] = 0

    elif (status.get('SCABT_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCABT_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['ABT'] = 0

    elif (status.get('SCABT_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH821_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCABT_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCABT_230_CH823_S.s') == 'Estado do ponto digital:on'):
        
        config['ABT'] = 0

    else:
        config['ABT'] = 1

    # BARRA GRANDE
    if (status.get('SCBGR_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBGR_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBGR_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBGR_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBGR_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBGR_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBGR_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBG'] = 0

    elif (status.get('SCBGR_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBGR_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBG'] = 0

    elif (status.get('SCBGR_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBGR_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBG'] = 0

    elif (status.get('SCBGR_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBGR_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBGR_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBG'] = 0

    else:
        config['UHBG'] = 1

    # BIGUAÇU 
    if (status.get('SCBIG_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH837_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH857_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH867_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH877_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH887_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCBIG_230_CH897_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH851_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH853_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH851_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH853_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH851_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH853_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH891_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH893_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH891_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH893_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH891_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH893_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH891_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH893_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH891_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH893_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0


    elif (status.get('SCBIG_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH701_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH703_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH871_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH701_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH873_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH703_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    elif (status.get('SCBIG_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCBIG_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCBIG_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['BIG'] = 0

    else:
        config['BIG'] = 1

    # CAMPOS NOVOS 
    if (status.get('SCCNO_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCCNO_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0  

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0  

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0  

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0  

    elif (status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0          

    elif (status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0     

    elif (status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0  

    elif (status.get('SCCNO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0  

    elif (status.get('SCCNO_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0 

    elif (status.get('SCCNO_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH821_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCCNO_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCCNO_230_CH823_S.s') == 'Estado do ponto digital:on'):
        
        config['CNO'] = 0      

    else:
        config['CNO'] = 1

    # FORQUILHINHA 
    if (status.get('SCFHA_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCFHA_230_CH807_S.s') == 'Estado do ponto digital:on'):
        
        config['FHA'] = 0

    elif (status.get('SCFHA_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCFHA_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['FHA'] = 0          

    elif (status.get('SCFHA_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCFHA_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['FHA'] = 0

    elif (status.get('SCFHA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCFHA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCFHA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['FHA'] = 0
    else:
        config['FHA'] = 1

    # FOZ DO CHAPECÓ 
    if (status.get('RSFCO_230_CH719_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH729_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH739_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH749_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH759_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH769_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH779_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH799_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH809_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH819_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH829_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH839_S.s') == 'Estado do ponto digital:on' or 
        status.get('RSFCO_230_CH849_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0


    elif (status.get('RSFCO_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH831_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH833_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH831_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH833_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH821_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH823_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH831_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH833_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0


    elif (status.get('RSFCO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    elif (status.get('RSFCO_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('RSFCO_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('RSFCO_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['UHFC'] = 0

    else:
        config['UHFC'] = 1

    # GASPAR 2 
    if (status.get('SCGAS2_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH857_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH867_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH877_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCGAS2_230_CH887_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0

    elif (status.get('SCGAS2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0          

    elif (status.get('SCGAS2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    elif (status.get('SCGAS2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    elif (status.get('SCGAS2_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    elif (status.get('SCGAS2_230_CH861_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH881_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH863_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH883_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    elif (status.get('SCGAS2_230_CH851_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH871_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH853_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH873_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    elif (status.get('SCGAS2_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    elif (status.get('SCGAS2_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCGAS2_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCGAS2_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['GAS2'] = 0 

    else:
        config['GAS2'] = 1

    # INDAIAL 
    if (status.get('SCIND_230_CH34T16_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCIND_230_CH34T26_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCIND_230_CH34S16_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCIND_230_CH34S26_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCIND_230_CH34F16_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCIND_230_CH34F26_S.s') == 'Estado do ponto digital:on'):
        
        config['IND'] = 0

    elif (status.get('SCIND_230_CH34T11_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCIND_230_CH34T21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCIND_230_CH34T12_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCIND_230_CH34T22_S.s') == 'Estado do ponto digital:on'):
        
        config['IND'] = 0

    elif (status.get('SCIND_230_CH34S11_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCIND_230_CH34S21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCIND_230_CH34S12_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCIND_230_CH34S22_S.s') == 'Estado do ponto digital:on'):
        
        config['IND'] = 0

    elif (status.get('SCIND_230_CH34F11_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCIND_230_CH34F21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCIND_230_CH34F12_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCIND_230_CH34F22_S.s') == 'Estado do ponto digital:on'):
        
        config['IND'] = 0

    else:
        config['IND'] = 1

    # ITAJAÍ 
    if (status.get('SCITJ_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCITJ_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCITJ_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCITJ_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCITJ_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCITJ_230_CH807_S.s') == 'Estado do ponto digital:on'):
        
        config['ITJ'] = 0

    elif (status.get('SCITJ_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCITJ_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['ITJ'] = 0

    elif (status.get('SCITJ_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCITJ_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['ITJ'] = 0

    elif (status.get('SCITJ_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCITJ_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['ITJ'] = 0

    elif (status.get('SCITJ_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCITJ_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['ITJ'] = 0                  

    elif (status.get('SCITJ_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCITJ_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCITJ_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['ITJ'] = 0

    else:
        config['ITJ'] = 1        

    # JOINVILLE NORTE
    if (status.get('SCJNO_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCJNO_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH801_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH803_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    elif (status.get('SCJNO_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCJNO_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCJNO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['JNO'] = 0

    else:
        config['JNO'] = 1

    # LAGES 
    if (status.get('SCLAG_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCLAG_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCLAG_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCLAG_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCLAG_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCLAG_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCLAG_230_CH797_S.s') == 'Estado do ponto digital:on'):
        
        config['LAG'] = 0

    elif (status.get('SCLAG_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCLAG_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['LAG'] = 0          

    elif (status.get('SCLAG_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCLAG_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['LAG'] = 0

    elif (status.get('SCLAG_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCLAG_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCLAG_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['LAG'] = 0        

    else:
        config['LAG'] = 1

    # MACHADINHO 
    if (status.get('SCMCH_525_CH1117_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCMCH_525_CH1147_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCMCH_525_CH1157_S.s') == 'Estado do ponto digital:on'):
        
        config['UHMA'] = 0

    elif (status.get('SCMCH_525_CH1011_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1021_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1031_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCMCH_525_CH1013_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1023_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1033_S.s') == 'Estado do ponto digital:on'):
        
        config['UHMA'] = 0          

    elif (status.get('SCMCH_525_CH1011_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1021_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1153_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCMCH_525_CH1013_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1023_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1151_S.s') == 'Estado do ponto digital:on'):
        
        config['UHMA'] = 0     

    elif (status.get('SCMCH_525_CH1011_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1031_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1153_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCMCH_525_CH1013_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1033_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1151_S.s') == 'Estado do ponto digital:on'):
        
        config['UHMA'] = 0        

    elif (status.get('SCMCH_525_CH1021_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1031_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1153_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCMCH_525_CH1023_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1033_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1151_S.s') == 'Estado do ponto digital:on'):
        
        config['UHMA'] = 0    

    elif (status.get('SCMCH_525_CH1111_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1141_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCMCH_525_CH1113_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCMCH_525_CH1143_S.s') == 'Estado do ponto digital:on'):
        
        config['UHMA'] = 0    

    else:
        config['UHMA'] = 1

    # PALHOÇA 
    if (status.get('SCPAL_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPAL_230_CH827_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL'] = 0

    elif (status.get('SCPAL_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPAL_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCPAL_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPAL_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL'] = 0

    elif (status.get('SCPAL_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPAL_230_CH821_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCPAL_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPAL_230_CH823_S.s') == 'Estado do ponto digital:on'):
        
        config['PAL'] = 0       

    else:
        config['PAL'] = 1

    # PINHALZINHO 2 
    if (status.get('SCPIN2_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPIN2_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPIN2_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPIN2_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPIN2_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPIN2_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCPIN2_230_CH797_S.s') == 'Estado do ponto digital:on'):
        
        config['PIN2'] = 0

    elif (status.get('SCPIN2_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCPIN2_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['PIN2'] = 0

    elif (status.get('SCPIN2_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCPIN2_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['PIN2'] = 0     

    elif (status.get('SCPIN2_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCPIN2_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCPIN2_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['PIN2'] = 0     

    else:
        config['PIN2'] = 1

    # RATONES
    if  (status.get('SCRAT_230_CH044_S.s') == 'Estado do ponto digital:on' and 
         status.get('SCRAT_230_CH060_S.s') == 'Estado do ponto digital:on') or \
        (status.get('SCRAT_230_CH046_S.s') == 'Estado do ponto digital:on' and 
         status.get('SCRAT_230_CH062_S.s') == 'Estado do ponto digital:on'):
        
        config['RAT'] = 0

    elif (status.get('SCRAT_230_CH028_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRAT_230_CH080_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCRAT_230_CH078_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRAT_230_CH026_S.s') == 'Estado do ponto digital:on'):
        
        config['RAT'] = 0

    else:
        config['RAT'] = 1


    # RIO DO SUL 
    if (status.get('SCRSU_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCRSU_230_CH787_S.s') == 'Estado do ponto digital:on'):
        
        config['RSU'] = 0

    elif (status.get('SCRSU_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCRSU_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['RSU'] = 0        

    elif (status.get('SCRSU_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCRSU_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['RSU'] = 0

    elif (status.get('SCRSU_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCRSU_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCRSU_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['RSU'] = 0            

    else:
        config['RSU'] = 1

    # SIDERÓPOLIS 2 
    if (status.get('SCSID2_230_CH7021_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCSID2_230_CH7031_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCSID2_230_CH7041_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCSID2_230_CH7061_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCSID2_230_CH7071_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCSID2_230_CH7081_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCSID2_230_CH7091_S.s') == 'Estado do ponto digital:on'):
        
        config['SID2'] = 0

    elif (status.get('SCSID2_230_CH7039_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7079_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7089_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCSID2_230_CH7033_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7073_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7083_S.s') == 'Estado do ponto digital:on'):
        
        config['SID2'] = 0

    elif (status.get('SCSID2_230_CH7099_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7029_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCSID2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7023_S.s') == 'Estado do ponto digital:on'):
        
        config['SID2'] = 0 

    elif (status.get('SCSID2_230_CH7069_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7049_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCSID2_230_CH7063_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCSID2_230_CH7043_S.s') == 'Estado do ponto digital:on'):
        
        config['SID2'] = 0    

    else:
        config['SID2'] = 1

    # TUBARÃO SUL 
    if (status.get('SCTSL_230_CH7021_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCTSL_230_CH7031_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCTSL_230_CH7041_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCTSL_230_CH7051_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCTSL_230_CH7061_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCTSL_230_CH7081_S.s') == 'Estado do ponto digital:on'):
        
        config['TSL'] = 0     

    elif (status.get('SCTSL_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCTSL_230_CH7043_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCTSL_230_CH7029_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCTSL_230_CH7049_S.s') == 'Estado do ponto digital:on'):
        
        config['TSL'] = 0

    elif (status.get('SCTSL_230_CH7063_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCTSL_230_CH7083_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCTSL_230_CH7069_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCTSL_230_CH7089_S.s') == 'Estado do ponto digital:on'):
        
        config['TSL'] = 0

    elif (status.get('SCTSL_230_CH7033_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCTSL_230_CH7053_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCTSL_230_CH7039_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCTSL_230_CH7059_S.s') == 'Estado do ponto digital:on'):
        
        config['TSL'] = 0               

    else:
        config['TSL'] = 1                  


    # VIDEIRA 
    if (status.get('SCVID_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCVID_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCVID_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCVID_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCVID_230_CH757_S.s') == 'Estado do ponto digital:on'):
        
        config['VID'] = 0     

    elif (status.get('SCVID_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCVID_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCVID_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCVID_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCVID_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCVID_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['VID'] = 0

    elif (status.get('SCVID_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCVID_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCVID_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCVID_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['VID'] = 0            

    else:
        config['VID'] = 1     

    # XANXERÊ 
    if (status.get('SCXAN_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH837_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH847_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH857_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCXAN_230_CH877_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0     

    elif (status.get('SCXAN_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH721_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH723_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0

    elif (status.get('SCXAN_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0          

    elif (status.get('SCXAN_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0  

    elif (status.get('SCXAN_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0  

    elif (status.get('SCXAN_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH821_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH823_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0  

    elif (status.get('SCXAN_230_CH851_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH871_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH853_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH873_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0  

    elif (status.get('SCXAN_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0  


    elif (status.get('SCXAN_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCXAN_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCXAN_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['XAN'] = 0          

    else:
        config['XAN'] = 1  

    # YTA 
    if (status.get('SCYTA_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCYTA_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCYTA_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCYTA_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCYTA_230_CH827_S.s') == 'Estado do ponto digital:on' or 
        status.get('SCYTA_230_CH847_S.s') == 'Estado do ponto digital:on'):
        
        config['YTA'] = 0     

    elif (status.get('SCYTA_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCYTA_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCYTA_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCYTA_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['YTA'] = 0

    elif (status.get('SCYTA_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCYTA_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCYTA_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCYTA_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['YTA'] = 0

    elif (status.get('SCYTA_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCYTA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SCYTA_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('SCYTA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['YTA'] = 0             

    else:
        config['YTA'] = 1 

    # PARANÁ

    # AREIA
    if (status.get('PRARE_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRARE_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['ARE'] = 0

    elif (status.get('PRARE_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRARE_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['ARE'] = 0

    elif (status.get('PRARE_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRARE_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['ARE'] = 0

    elif (status.get('PRARE_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRARE_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['ARE'] = 0

    elif (status.get('PRARE_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRARE_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRARE_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['ARE'] = 0

    else:
        config['ARE'] = 1  

    # ANDIRÁ LESTE
    if (status.get('PRADL_230_CH2941_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRADL_230_CH2950_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRADL_230_CH2956_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRADL_230_CH2963_S.s') == 'Estado do ponto digital:on'):
        
        config['ADL'] = 0

    elif (status.get('PRADL_230_CH2954_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRADL_230_CH2961_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRADL_230_CH2953_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRADL_230_CH2960_S.s') == 'Estado do ponto digital:on'):
        
        config['ADL'] = 0

    elif (status.get('PRADL_230_CH2939_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRADL_230_CH2948_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRADL_230_CH2938_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRADL_230_CH2947_S.s') == 'Estado do ponto digital:on'):
        
        config['ADL'] = 0

    else:
        config['ADL'] = 1


    # BATEIAS
    if (status.get('PRBTA_230_CH026_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29141_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29153_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29133_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29167_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29197_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29207_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29202_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH29146_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH058_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH052_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH046_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH031_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBTA_230_CH040_S.s') == 'Estado do ponto digital:on'):
        
        config['BTA'] = 0

    elif (status.get('PRBTA_230_CH29195_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29165_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH048_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH054_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29131_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH024_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29151_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRBTA_230_CH29196_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29166_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH051_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH057_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29132_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH025_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29152_S.s') == 'Estado do ponto digital:on')):
        
        config['BTA'] = 0


    elif (status.get('PRBTA_230_CH29142_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29165_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH048_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH054_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29131_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH024_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29151_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRBTA_230_CH29145_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29166_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH051_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH057_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29132_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH025_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29152_S.s') == 'Estado do ponto digital:on')):
        
        config['BTA'] = 0

    elif (status.get('PRBTA_230_CH042_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29165_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH048_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH054_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29131_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH024_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29151_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRBTA_230_CH045_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29166_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH051_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH057_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29132_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH025_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29152_S.s') == 'Estado do ponto digital:on')):
        
        config['BTA'] = 0

    elif (status.get('PRBTA_230_CH29139_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29165_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH048_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH054_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29131_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH024_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29151_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRBTA_230_CH29140_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRBTA_230_CH29166_S.s') == 'Estado do ponto digital:on' or
          status.get('PRBTA_230_CH051_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH057_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29132_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH025_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRBTA_230_CH29152_S.s') == 'Estado do ponto digital:on')):
        
        config['BTA'] = 0

    elif (status.get('PRBTA_230_CH29198_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBTA_230_CH29204_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRBTA_230_CH29201_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBTA_230_CH29207_S.s') == 'Estado do ponto digital:on'):
        
        config['BTA'] = 0

    elif (status.get('PRBTA_230_CH027_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBTA_230_CH036_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRBTA_230_CH030_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBTA_230_CH039_S.s') == 'Estado do ponto digital:on'):
        
        config['BTA'] = 0

    else:
        config['BTA'] = 1

    # CASCAVEL NORTE
    if (status.get('PRCVN_230_CH6C4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCVN_230_CH6D4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCVN_230_CH6E4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCVN_230_CH6G4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCVN_230_CH6H4_S.s') == 'Estado do ponto digital:on'):
        
        config['CVN'] = 0

    elif (status.get('PRCVN_230_CH6D1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCVN_230_CH6H1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCVN_230_CH6D2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCVN_230_CH6H2_S.s') == 'Estado do ponto digital:on'):
        
        config['CVN'] = 0

    elif (status.get('PRCVN_230_CH6C1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCVN_230_CH6G1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCVN_230_CH6C2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCVN_230_CH6G2_S.s') == 'Estado do ponto digital:on'):
        
        config['CVN'] = 0

    else:
        config['CVN'] = 1        

    # CASTRO NORTE
    if (status.get('PRCRN_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCRN_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCRN_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCRN_230_CH757_S.s') == 'Estado do ponto digital:on'):
        
        config['CRN'] = 0

    elif (status.get('PRCRN_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCRN_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCRN_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCRN_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['CRN'] = 0

    elif (status.get('PRCRN_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCRN_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCRN_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCRN_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['CRN'] = 0

    else:
        config['CRN'] = 1

    # CURITIBA CENTRO
    if  (status.get('PRCTC_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
         status.get('PRCTC_230_CH2929_S.s') == 'Estado do ponto digital:on') or \
        (status.get('PRCTC_230_CH2904_S.s') == 'Estado do ponto digital:on' and 
         status.get('PRCTC_230_CH2930_S.s') == 'Estado do ponto digital:on'):
        
        config['CTC'] = 0

    elif (status.get('PRCTC_230_CH2910_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTC_230_CH2922_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCTC_230_CH2911_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTC_230_CH2923_S.s') == 'Estado do ponto digital:on'):
        
        config['CTC'] = 0

    else:
        config['CTC'] = 1

    # CURITIBA LESTE
    if (status.get('PRCTL_230_CH6A4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTL_230_CH6C4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTL_230_CH6D4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTL_230_CH6E4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTL_230_CH6G4_S.s') == 'Estado do ponto digital:on'):
        
        config['CTL'] = 0

    elif (status.get('PRCTL_230_CH6A1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTL_230_CH6E1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCTL_230_CH6A2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTL_230_CH6E2_S.s') == 'Estado do ponto digital:on'):
        
        config['CTL'] = 0

    elif (status.get('PRCTL_230_CH6C1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTL_230_CH6G1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCTL_230_CH6C2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTL_230_CH6G2_S.s') == 'Estado do ponto digital:on'):
        
        config['CTL'] = 0

    elif (status.get('PRCTL_230_CH6I1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTL_230_CH6K1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCTL_230_CH6I2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTL_230_CH6K2_S.s') == 'Estado do ponto digital:on'):
        
        config['CTL'] = 0

    else:
        config['CTL'] = 1

    # CURITIBA NORTE
    if (status.get('PRCTN_230_CH2935_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTN_230_CH2944_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTN_230_CH2950_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTN_230_CH2955_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRCTN_230_CH2961_S.s') == 'Estado do ponto digital:on'):
        
        config['CTN'] = 0

    elif (status.get('PRCTN_230_CH2947_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTN_230_CH2958_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCTN_230_CH2948_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTN_230_CH2959_S.s') == 'Estado do ponto digital:on'):
        
        config['CTN'] = 0

    elif (status.get('PRCTN_230_CH2941_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTN_230_CH2952_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRCTN_230_CH2942_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRCTN_230_CH2953_S.s') == 'Estado do ponto digital:on'):
        
        config['CTN'] = 0

    else:
        config['CTN'] = 1

    # FOZ DO IGUAÇU NORTE
    if (status.get('PRFIN_230_CHSY601_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRFIN_230_CHSY602_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRFIN_230_CHSY605_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRFIN_230_CHSY606_S.s') == 'Estado do ponto digital:on'):
        
        config['FIN'] = 0

    elif (status.get('PRFIN_230_CHSB603_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRFIN_230_CHSB607_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRFIN_230_CHSB604_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRFIN_230_CHSB608_S.s') == 'Estado do ponto digital:on'):
        
        config['FIN'] = 0

    elif (status.get('PRFIN_230_CHSB601_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRFIN_230_CHSB605_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRFIN_230_CHSB602_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRFIN_230_CHSB606_S.s') == 'Estado do ponto digital:on'):
        
        config['FIN'] = 0

    else:
        config['FIN'] = 1

    # GOV. BENTO MUNHOZ
    if (status.get('PRGBM_525_CH008_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGBM_525_CH023_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGBM_525_CH038_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGBM_525_CH053_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH004_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH034_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH005_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH035_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH004_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH049_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH005_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH050_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH019_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH034_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH020_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH035_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH019_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH049_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH020_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH050_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH004_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH040_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH005_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH039_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH019_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH040_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH020_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH039_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH010_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH034_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH009_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH035_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    elif (status.get('PRGBM_525_CH010_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH049_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGBM_525_CH009_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGBM_525_CH050_S.s') == 'Estado do ponto digital:on'):
        
        config['GBM'] = 0

    else:
        config['GBM'] = 1

    # GUARAPUAVA OESTE
    if (status.get('PRGUO_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGUO_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGUO_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGUO_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGUO_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGUO_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRGUO_230_CH787_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0

    elif (status.get('PRGUO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGUO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0

    elif (status.get('PRGUO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGUO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0

    elif (status.get('PRGUO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGUO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0        

    elif (status.get('PRGUO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGUO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0   

    elif (status.get('PRGUO_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGUO_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0

    elif (status.get('PRGUO_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRGUO_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRGUO_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['GUO'] = 0

    else:
        config['GUO'] = 1         

    # IRATI NORTE
    if (status.get('PRIRN_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRIRN_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRIRN_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRIRN_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRIRN_230_CH767_S.s') == 'Estado do ponto digital:on'):
        
        config['IRN'] = 0

    elif (status.get('PRIRN_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRIRN_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRIRN_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRIRN_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['IRN'] = 0

    elif (status.get('PRIRN_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRIRN_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRIRN_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRIRN_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['IRN'] = 0

    else:
        config['IRN'] = 1

    # JAGUARIAÍVA
    if (status.get('PRJGI_230_CH09_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRJGI_230_CH15_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRJGI_230_CH20_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRJGI_230_CH29147_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRJGI_230_CH29161_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRJGI_230_CH29167_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRJGI_230_CH29184_S.s') == 'Estado do ponto digital:on'):
        
        config['JGI'] = 0

    elif (status.get('PRJGI_230_CH29148_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRJGI_230_CH16_S.s') == 'Estado do ponto digital:on' or
          status.get('PRJGI_230_CH29162_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRJGI_230_CH29149_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRJGI_230_CH17_S.s') == 'Estado do ponto digital:on' or
          status.get('PRJGI_230_CH29163_S.s') == 'Estado do ponto digital:on')):
        
        config['JGI'] = 0

    elif (status.get('PRJGI_230_CH10_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRJGI_230_CH16_S.s') == 'Estado do ponto digital:on' or
          status.get('PRJGI_230_CH29162_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRJGI_230_CH11_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRJGI_230_CH17_S.s') == 'Estado do ponto digital:on' or
          status.get('PRJGI_230_CH29163_S.s') == 'Estado do ponto digital:on')):
        
        config['JGI'] = 0        

    elif (status.get('PRJGI_230_CH29148_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRJGI_230_CH11_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRJGI_230_CH29149_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRJGI_230_CH10_S.s') == 'Estado do ponto digital:on'):
        
        config['JGI'] = 0  

    elif (status.get('PRJGI_230_CH29162_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRJGI_230_CH17_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRJGI_230_CH29163_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRJGI_230_CH16_S.s') == 'Estado do ponto digital:on'):
        
        config['JGI'] = 0 

    else:
        config['JGI'] = 1

    # KLACEL
    if (status.get('PRKCL_230_CH6A4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRKCL_230_CH6B4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRKCL_230_CH6C4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRKCL_230_CH6D4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRKCL_230_CH6E4_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRKCL_230_CH6G4_S.s') == 'Estado do ponto digital:on'):
        
        config['KCL'] = 0

    elif (status.get('PRKCL_230_CH6B1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRKCL_230_CH6D1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRKCL_230_CH6B2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRKCL_230_CH6D2_S.s') == 'Estado do ponto digital:on'):
        
        config['KCL'] = 0

    elif (status.get('PRKCL_230_CH6E1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRKCL_230_CH6G1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRKCL_230_CH6E2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRKCL_230_CH6G2_S.s') == 'Estado do ponto digital:on'):
        
        config['KCL'] = 0

    elif (status.get('PRKCL_230_CH6A1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRKCL_230_CH6C1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRKCL_230_CH6A2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRKCL_230_CH6C2_S.s') == 'Estado do ponto digital:on'):
        
        config['KCL'] = 0

    else:
        config['KCL'] = 1

    # LONDRINA SUL
    if (status.get('PRLNS_230_CH2905_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRLNS_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRLNS_230_CH737_S.s') == 'Estado do ponto digital:on'):
        
        config['LNS'] = 0

    elif (status.get('PRLNS_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRLNS_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRLNS_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRLNS_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['LNS'] = 0

    elif (status.get('PRLNS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRLNS_230_CH2901_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRLNS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRLNS_230_CH2904_S.s') == 'Estado do ponto digital:on'):
        
        config['LNS'] = 0

    else:
        config['LNS'] = 1

    # MAUÁ
    if (status.get('PRMUA_230_CH2904_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMUA_230_CH2910_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMUA_230_CH2916_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMUA_230_CH2923_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMUA_230_CH2933_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMUA_230_CH2939_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMUA_230_CH2948_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2922_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2924_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2922_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2924_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2922_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2924_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2903_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2908_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2909_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2915_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    elif (status.get('PRMUA_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2934_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2943_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMUA_230_CH2932_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2938_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMUA_230_CH2947_S.s') == 'Estado do ponto digital:on'):
        
        config['MUA'] = 0

    else:
        config['MUA'] = 1

    # MEDIANEIRA NORTE
    if (status.get('PRMDN_230_CH2913_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMDN_230_CH2919_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMDN_230_CH2924_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMDN_230_CH2930_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMDN_230_CH2935_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRMDN_230_CH2947_S.s') == 'Estado do ponto digital:on'):
        
        config['MDN'] = 0

    elif (status.get('PRMDN_230_CH2916_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMDN_230_CH2927_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMDN_230_CH2917_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMDN_230_CH2928_S.s') == 'Estado do ponto digital:on'):
        
        config['MDN'] = 0

    elif (status.get('PRMDN_230_CH2910_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMDN_230_CH2932_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMDN_230_CH2911_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMDN_230_CH2933_S.s') == 'Estado do ponto digital:on'):
        
        config['MDN'] = 0

    elif (status.get('PRMDN_230_CH2921_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMDN_230_CH2944_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRMDN_230_CH2922_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRMDN_230_CH2945_S.s') == 'Estado do ponto digital:on'):
        
        config['MDN'] = 0

    else:
        config['MDN'] = 1

    # PARANAVAÍ NORTE
    if (status.get('PRPRN_230_CH296_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPRN_230_CH2914_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPRN_230_CH2922_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPRN_230_CH2942_S.s') == 'Estado do ponto digital:on'):
        
        config['PRN'] = 0

    elif (status.get('PRPRN_230_CH2910_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPRN_230_CH2938_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPRN_230_CH2912_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPRN_230_CH2940_S.s') == 'Estado do ponto digital:on'):
        
        config['PRN'] = 0

    elif (status.get('PRPRN_230_CH292_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPRN_230_CH2918_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPRN_230_CH294_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPRN_230_CH2920_S.s') == 'Estado do ponto digital:on'):
        
        config['PRN'] = 0

    else:
        config['PRN'] = 1

    # PONTA GROSSA
    if (status.get('PRPGR_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRPGR_230_CH827_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH823_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH821_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH823_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH821_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH823_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH821_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    elif (status.get('PRPGR_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRPGR_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRPGR_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['PGR'] = 0

    else:
        config['PGR'] = 1

    # REALEZA SUL
    if (status.get('PRRZS_230_CH2905_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRRZS_230_CH2914_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRRZS_230_CH2920_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRRZS_230_CH2963_S.s') == 'Estado do ponto digital:on'):
        
        config['RZS'] = 0

    elif (status.get('PRRZS_230_CH2901_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRRZS_230_CH2910_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRRZS_230_CH2904_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRRZS_230_CH2913_S.s') == 'Estado do ponto digital:on'):
        
        config['RZS'] = 0

    elif (status.get('PRRZS_230_CH2916_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRRZS_230_CH2959_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRRZS_230_CH2917_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRRZS_230_CH2960_S.s') == 'Estado do ponto digital:on'):
        
        config['RZS'] = 0

    else:
        config['RZS'] = 1

    # SALTO OSÓRIO
    if (status.get('PRSOS_230_CH789_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH799_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH809_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH819_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH829_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH839_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH849_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH859_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH869_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSOS_230_CH879_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0

    elif (status.get('PRSOS_230_CH781_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH783_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0

    elif (status.get('PRSOS_230_CH821_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH871_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH823_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH873_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0

    elif (status.get('PRSOS_230_CH851_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH861_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH853_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH863_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0

    elif (status.get('PRSOS_230_CH831_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH841_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH833_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH843_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0
# 1 2 3 4
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0
# 1 2 3 5
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0
# 1 2 3 6
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0
# 1 2 4 5
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0        
# 1 2 4 6
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0   
# 1 2 5 6
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0  
# 1 3 4 5
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0 
# 1 3 4 6
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0  
# 1 3 5 6
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0         
# 1 4 5 6
    elif (status.get('PRSOS_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0 
# 2 3 4 5
    elif (status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0 
# 2 3 4 6
    elif (status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0 
# 2 3 5 6
    elif (status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0         
# 2 4 5 6
    elif (status.get('PRSOS_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0  
# 3 4 5 6
    elif (status.get('PRSOS_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSOS_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSOS_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['UHSO'] = 0 

    else:
        config['UHSO'] = 1

    # SANTA QUITÉRIA
    if   (status.get('PRSQT_230_CH2913_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSQT_230_CH2920_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSQT_230_CH2914_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSQT_230_CH2921_S.s') == 'Estado do ponto digital:on'):
        
        config['SQT'] = 0

    elif (status.get('PRSQT_230_CH2934_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSQT_230_CH2941_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSQT_230_CH2935_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSQT_230_CH2942_S.s') == 'Estado do ponto digital:on'):
        
        config['SQT'] = 0

    elif (status.get('PRSQT_230_CH2906_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSQT_230_CH2927_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSQT_230_CH2907_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSQT_230_CH2928_S.s') == 'Estado do ponto digital:on'):
        
        config['SQT'] = 0

    else:
        config['SQT'] = 1

    # SARANDI
    if (status.get('PRSDI_230_CH2929_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2934_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2939_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2975_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2982_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2988_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2993_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH2998_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH29158_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH29164_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRSDI_230_CH29169_S.s') == 'Estado do ponto digital:on'):
        
        config['SDI'] = 0

    elif (status.get('PRSDI_230_CH2989_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSDI_230_CH2994_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSDI_230_CH2992_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSDI_230_CH2997_S.s') == 'Estado do ponto digital:on'):
        
        config['SDI'] = 0

    elif (status.get('PRSDI_230_CH2977_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSDI_230_CH2983_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRSDI_230_CH2981_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRSDI_230_CH2987_S.s') == 'Estado do ponto digital:on'):
        
        config['SDI'] = 0

    elif (status.get('PRSDI_230_CH29153_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH29157_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0

    elif (status.get('PRSDI_230_CH29159_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH29163_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0

    elif (status.get('PRSDI_230_CH29165_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH29168_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0        

    elif (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0   

    elif (status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0 

    elif (status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0 

    elif (status.get('PRSDI_230_CH2973_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2935_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2930_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2940_S.s') == 'Estado do ponto digital:on')) or\
         (status.get('PRSDI_230_CH2976_S.s') == 'Estado do ponto digital:on' and 
         (status.get('PRSDI_230_CH2933_S.s') == 'Estado do ponto digital:on' or
          status.get('PRSDI_230_CH2928_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRSDI_230_CH2937_S.s') == 'Estado do ponto digital:on')):
        
        config['SDI'] = 0 

    else:
        config['SDI'] = 1

    # UHE BAIXO IGUAÇU
    if (status.get('PRBXI_230_CH2903_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBXI_230_CH89L16_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBXI_230_CH89G16_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBXI_230_CH89G26_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRBXI_230_CH89G36_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBI'] = 0

    elif (status.get('PRBXI_230_CH89G11_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBXI_230_CH89G21_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBXI_230_CH89G31_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRBXI_230_CH89G12_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBXI_230_CH89G22_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBXI_230_CH89G32_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBI'] = 0

    elif (status.get('PRBXI_230_CH2901_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBXI_230_CH89L11_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRBXI_230_CH2902_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRBXI_230_CH89L12_S.s') == 'Estado do ponto digital:on'):
        
        config['UHBI'] = 0

    else:
        config['UHBI'] = 1

    # UMBARÁ
    if   (status.get('PRUMB_230_CH043_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMB_230_CH118_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUMB_230_CH044_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMB_230_CH119_S.s') == 'Estado do ponto digital:on'):
        
        config['UMB'] = 0

    elif (status.get('PRUMB_230_CH2912_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMB_230_CH064_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUMB_230_CH2913_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMB_230_CH065_S.s') == 'Estado do ponto digital:on'):
        
        config['UMB'] = 0

    elif (status.get('PRUMB_230_CH019_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMB_230_CH2912_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUMB_230_CH020_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMB_230_CH2913_S.s') == 'Estado do ponto digital:on'):
        
        config['UMB'] = 0

    else:
        config['UMB'] = 1

    # UMUARAMA SUL
    if   (status.get('PRUMS_230_CH6C4_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRUMS_230_CH6D4_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRUMS_230_CH6G4_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRUMS_230_CH6H4_S.s') == 'Estado do ponto digital:on' or 
          status.get('PRUMS_230_CH2944_S.s') == 'Estado do ponto digital:on'):
        
        config['UMS'] = 0

    elif (status.get('PRUMS_230_CH6D1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMS_230_CH6H1_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUMS_230_CH6D2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMS_230_CH6H2_S.s') == 'Estado do ponto digital:on'):
        
        config['UMS'] = 0

    elif (status.get('PRUMS_230_CH6C1_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMS_230_CH2939_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUMS_230_CH6C2_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUMS_230_CH2943_S.s') == 'Estado do ponto digital:on'):
        
        config['UMS'] = 0

    else:
        config['UMS'] = 1

    # UNIÃO DA VITÓRIA NORTE
    if (status.get('PRUVN_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRUVN_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRUVN_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('PRUVN_230_CH767_S.s') == 'Estado do ponto digital:on'):
        
        config['UVN'] = 0

    elif (status.get('PRUVN_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUVN_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUVN_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUVN_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['UVN'] = 0

    elif (status.get('PRUVN_230_CH721_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUVN_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('PRUVN_230_CH723_S.s') == 'Estado do ponto digital:on' and 
          status.get('PRUVN_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['UVN'] = 0

    else:
        config['UVN'] = 1

    # MATO GROSSO DO SUL

    # ANASTÁCIO
    if (status.get('MSANA_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH787_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH807_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSANA_230_CH817_S.s') == 'Estado do ponto digital:on'):
        
        config['ANA'] = 0

    elif (status.get('MSANA_230_CH761_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH781_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSANA_230_CH763_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH783_S.s') == 'Estado do ponto digital:on'):
        
        config['ANA'] = 0

    elif (status.get('MSANA_230_CH791_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH801_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSANA_230_CH793_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH803_S.s') == 'Estado do ponto digital:on'):
        
        config['ANA'] = 0

    elif (status.get('MSANA_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH741_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSANA_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH743_S.s') == 'Estado do ponto digital:on'):
        
        config['ANA'] = 0

    elif (status.get('MSANA_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSANA_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['ANA'] = 0

    elif (status.get('MSANA_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH811_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSANA_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSANA_230_CH813_S.s') == 'Estado do ponto digital:on'):
        
        config['ANA'] = 0

    else:
        config['ANA'] = 1

    # CAMPO GRANDE 2
    if (status.get('MSCGT_230_CH709_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH719_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH729_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH749_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH759_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH7119_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH7129_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCGT_230_CH7139_S.s') == 'Estado do ponto digital:on'):
        
        config['CGT'] = 0

    elif (status.get('MSCGT_230_CH7113_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH7123_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH7133_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCGT_230_CH7117_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH7127_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH7137_S.s') == 'Estado do ponto digital:on'):
        
        config['CGT'] = 0

    elif (status.get('MSCGT_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH743_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCGT_230_CH707_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH747_S.s') == 'Estado do ponto digital:on'):
        
        config['CGT'] = 0

    elif (status.get('MSCGT_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH723_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCGT_230_CH717_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCGT_230_CH727_S.s') == 'Estado do ponto digital:on'):
        
        config['CGT'] = 0

    else:
        config['CGT'] = 1

    # CHAPADÃO
    if (status.get('MSCAO_230_CH7133_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7143_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7153_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7163_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7173_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7183_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7203_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7213_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCAO_230_CH7421_S.s') == 'Estado do ponto digital:on'):
        
        config['CAO'] = 0

    elif (status.get('MSCAO_230_CH7207_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7217_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCAO_230_CH7209_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7219_S.s') == 'Estado do ponto digital:on'):
        
        config['CAO'] = 0

    elif (status.get('MSCAO_230_CH7147_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7157_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCAO_230_CH7149_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7159_S.s') == 'Estado do ponto digital:on'):
        
        config['CAO'] = 0

    elif (status.get('MSCAO_230_CH7425_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7137_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCAO_230_CH7429_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7139_S.s') == 'Estado do ponto digital:on'):
        
        config['CAO'] = 0

    elif (status.get('MSCAO_230_CH7167_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7177_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7187_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCAO_230_CH7169_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7179_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCAO_230_CH7189_S.s') == 'Estado do ponto digital:on'):
        
        config['CAO'] = 0
   
    else:
        config['CAO'] = 1

    # CORUMBÁ 2
    if (status.get('MSCOR2_230_CH7017_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCOR2_230_CH7027_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCOR2_230_CH7117_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCOR2_230_CH7127_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCOR2_230_CH7137_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSCOR2_230_CH7147_S.s') == 'Estado do ponto digital:on'):
        
        config['COR2'] = 0

    elif (status.get('MSCOR2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCOR2_230_CH7131_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCOR2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCOR2_230_CH7135_S.s') == 'Estado do ponto digital:on'):
        
        config['COR2'] = 0

    elif (status.get('MSCOR2_230_CH7011_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCOR2_230_CH7021_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCOR2_230_CH7015_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCOR2_230_CH7025_S.s') == 'Estado do ponto digital:on'):
        
        config['COR2'] = 0

    elif (status.get('MSCOR2_230_CH7111_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCOR2_230_CH7141_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSCOR2_230_CH7115_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSCOR2_230_CH7145_S.s') == 'Estado do ponto digital:on'):
        
        config['COR2'] = 0

    else:
        config['COR2'] = 1

    # DOURADOS
    if (status.get('MSDOU_230_CH707_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH717_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH727_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH737_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH747_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH757_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH767_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH777_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH797_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH817_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU_230_CH837_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH771_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH731_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH751_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH773_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH733_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH753_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH711_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH731_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH713_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH733_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH751_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH771_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH753_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH773_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH741_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH791_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH743_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH793_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH701_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH761_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH703_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH763_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    elif (status.get('MSDOU_230_CH811_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH831_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU_230_CH813_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU_230_CH833_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU'] = 0

    else:
        config['DOU'] = 1

    # DOURADOS 2
    if (status.get('MSDOU2_230_CH34T16_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU2_230_CH34T26_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU2_230_CH34F16_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU2_230_CH34I16_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU2_230_CH34J16_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSDOU2_230_CH34N16_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU2'] = 0

    elif (status.get('MSDOU2_230_CH34T11_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU2_230_CH34T21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU2_230_CH34T12_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU2_230_CH34T22_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU2'] = 0

    elif (status.get('MSDOU2_230_CH34J11_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU2_230_CH34N11_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU2_230_CH34J12_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU2_230_CH34N12_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU2'] = 0

    elif (status.get('MSDOU2_230_CH34F11_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU2_230_CH34I11_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSDOU2_230_CH34F12_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSDOU2_230_CH34I12_S.s') == 'Estado do ponto digital:on'):
        
        config['DOU2'] = 0

    else:
        config['DOU2'] = 1

    # ILHA SOLTEIRA 2
    if (status.get('MSISO2_230_CH7097_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSISO2_230_CH7107_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSISO2_230_CH7117_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSISO2_230_CH7127_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSISO2_230_CH7147_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSISO2_230_CH7157_S.s') == 'Estado do ponto digital:on'):
        
        config['ISO2'] = 0

# C1 C2 T1 / C3 T2 T3
    elif((status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C1 C2 T2 / C3 T1 T3
    elif((status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C1 C2 T3 / C3 T1 T2
    elif((status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C1 C3 T1 / C2 T2 T3
    elif((status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C1 C3 T2 / C2 T1 T3
    elif((status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C1 C3 T3 / C2 T1 T2
    elif((status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C2 C3 T1 / C1 T2 T3
    elif((status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C2 C3 T2 / C1 T1 T3
    elif((status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

# C2 C3 T3 / C1 T1 T2
    elif((status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on')):
        
        config['ISO2'] = 0

    elif (status.get('MSISO2_230_CH7093_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7113_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7143_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSISO2_230_CH7095_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7115_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7145_S.s') == 'Estado do ponto digital:on'):
        
        config['ISO2'] = 0

    elif (status.get('MSISO2_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7121_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7151_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSISO2_230_CH7105_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7125_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSISO2_230_CH7155_S.s') == 'Estado do ponto digital:on'):
        
        config['ISO2'] = 0

    else:
        config['ISO2'] = 1

    # IMBIRUSSU
    if (status.get('MSIMB_230_CH7117_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7137_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7147_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7157_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7217_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7227_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7237_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIMB_230_CH7247_S.s') == 'Estado do ponto digital:on'):
        
        config['IMB'] = 0

    elif (status.get('MSIMB_230_CH7111_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7131_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7141_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSIMB_230_CH7119_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7139_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7149_S.s') == 'Estado do ponto digital:on'):
        
        config['IMB'] = 0

    elif (status.get('MSIMB_230_CH7221_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7241_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSIMB_230_CH7229_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7249_S.s') == 'Estado do ponto digital:on'):
        
        config['IMB'] = 0

    elif (status.get('MSIMB_230_CH7211_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7151_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSIMB_230_CH7219_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIMB_230_CH7159_S.s') == 'Estado do ponto digital:on'):
        
        config['IMB'] = 0

    else:
        config['IMB'] = 1

    # INOCÊNCIA
    if (status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSINO_230_CH7019_S.s') == 'Estado do ponto digital:on'):
        
        config['INO'] = 0

# ISO2 C1 e C2 CAO C1 / ISO2 C3 CAO C2 e C3
    elif((status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C1 e C2 CAO C2 / ISO2 C3 CAO C1 e C3
    elif((status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C1 e C2 CAO C3 / ISO2 C3 CAO C2 e C3
    elif((status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C1 e C3 CAO C1 / ISO2 C2 CAO C2 e C3
    elif((status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C1 e C3 CAO C2 / ISO2 C2 CAO C1 e C3
    elif((status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C1 e C3 CAO C3 / ISO2 C2 CAO C2 e C3
    elif((status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C2 e C3 CAO C1 / ISO2 C1 CAO C2 e C3
    elif((status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C2 e C3 CAO C2 / ISO2 C1 CAO C1 e C3
    elif((status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

# ISO2 C2 e C3 CAO C3 / ISO2 C1 CAO C2 e C3
    elif((status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on')) or \
        ((status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on') and \
         (status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on')):
        
        config['INO'] = 0

    elif (status.get('MSINO_230_CH7043_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7023_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7083_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSINO_230_CH7047_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7027_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7087_S.s') == 'Estado do ponto digital:on'):
        
        config['INO'] = 0

    elif (status.get('MSINO_230_CH7013_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7033_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7053_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSINO_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7037_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSINO_230_CH7057_S.s') == 'Estado do ponto digital:on'):
        
        config['INO'] = 0

    else:
        config['INO'] = 1

    # IVINHEMA 2
    if (status.get('MSIVI2_230_CH7489_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIVI2_230_CH7509_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIVI2_230_CH7519_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIVI2_230_CH7539_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIVI2_230_CH7549_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSIVI2_230_CH7569_S.s') == 'Estado do ponto digital:on'):
        
        config['IVI2'] = 0

    elif (status.get('MSIVI2_230_CH7513_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIVI2_230_CH7533_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSIVI2_230_CH7517_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIVI2_230_CH7537_S.s') == 'Estado do ponto digital:on'):
        
        config['IVI2'] = 0

    elif (status.get('MSIVI2_230_CH7503_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIVI2_230_CH7563_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSIVI2_230_CH7507_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIVI2_230_CH7567_S.s') == 'Estado do ponto digital:on'):
        
        config['IVI2'] = 0

    elif (status.get('MSIVI2_230_CH7483_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIVI2_230_CH7543_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSIVI2_230_CH7487_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSIVI2_230_CH7547_S.s') == 'Estado do ponto digital:on'):
        
        config['IVI2'] = 0

    else:
        config['IVI2'] = 1

    # NOVA PORTO PRIMAVERA
    if (status.get('SPNPP_230_CH7005_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7015_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7035_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7105_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7115_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7125_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7135_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7145_S.s') == 'Estado do ponto digital:on' or 
        status.get('SPNPP_230_CH7205_S.s') == 'Estado do ponto digital:on'):
        
        config['NPP'] = 0

    elif (status.get('SPNPP_230_CH7001_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7011_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7031_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SPNPP_230_CH7007_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7017_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7037_S.s') == 'Estado do ponto digital:on'):
        
        config['NPP'] = 0

    elif (status.get('SPNPP_230_CH7201_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7111_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SPNPP_230_CH7207_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7117_S.s') == 'Estado do ponto digital:on'):
        
        config['NPP'] = 0

    elif (status.get('SPNPP_230_CH7101_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7121_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SPNPP_230_CH7107_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7127_S.s') == 'Estado do ponto digital:on'):
        
        config['NPP'] = 0

    elif (status.get('SPNPP_230_CH7131_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7141_S.s') == 'Estado do ponto digital:on') or \
         (status.get('SPNPP_230_CH7137_S.s') == 'Estado do ponto digital:on' and 
          status.get('SPNPP_230_CH7147_S.s') == 'Estado do ponto digital:on'):
        
        config['NPP'] = 0

    else:
        config['NPP'] = 1

    # PARAÍSO 2
    if (status.get('MSPSO2_230_CHF16_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSPSO2_230_CHJ16_S.s') == 'Estado do ponto digital:on' or
        status.get('MSPSO2_230_CHF26_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSPSO2_230_CHJ26_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSPSO2_230_CHT16_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSPSO2_230_CHT26_S.s') == 'Estado do ponto digital:on'):
        
        config['PSO2'] = 0

    elif (status.get('MSPSO2_230_CHF11_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSPSO2_230_CHF21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSPSO2_230_CHF12_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSPSO2_230_CHF22_S.s') == 'Estado do ponto digital:on'):
        
        config['PSO2'] = 0

    elif (status.get('MSPSO2_230_CHJ11_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSPSO2_230_CHJ21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSPSO2_230_CHJ12_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSPSO2_230_CHJ22_S.s') == 'Estado do ponto digital:on'):
        
        config['PSO2'] = 0

    elif (status.get('MSPSO2_230_CHT11_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSPSO2_230_CHT21_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSPSO2_230_CHT12_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSPSO2_230_CHT22_S.s') == 'Estado do ponto digital:on'):
        
        config['PSO2'] = 0

    else:
        config['PSO2'] = 1

    # RIO BRILHANTE
    if (status.get('MSRBE_230_CH7307_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSRBE_230_CH7317_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSRBE_230_CH7327_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSRBE_230_CH7367_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSRBE_230_CH7387_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSRBE_230_CH7397_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSRBE_230_CH7537_S.s') == 'Estado do ponto digital:on'):
        
        config['RBE'] = 0

    elif (status.get('MSRBE_230_CH7313_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSRBE_230_CH7533_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSRBE_230_CH7315_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSRBE_230_CH7535_S.s') == 'Estado do ponto digital:on'):
        
        config['RBE'] = 0

    elif (status.get('MSRBE_230_CH7321_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSRBE_230_CH7361_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSRBE_230_CH7325_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSRBE_230_CH7365_S.s') == 'Estado do ponto digital:on'):
        
        config['RBE'] = 0

    elif (status.get('MSRBE_230_CH7301_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSRBE_230_CH7381_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSRBE_230_CH7305_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSRBE_230_CH7385_S.s') == 'Estado do ponto digital:on'):
        
        config['RBE'] = 0

    else:
        config['RBE'] = 1

    # SIDROLÂNDIA 2
    if (status.get('MSSIA2_230_CH7433_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSSIA2_230_CH7443_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSSIA2_230_CH7453_S.s') == 'Estado do ponto digital:on' or 
        status.get('MSSIA2_230_CH7483_S.s') == 'Estado do ponto digital:on'):
        
        config['SIA2'] = 0

    elif (status.get('MSSIA2_230_CH7441_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSSIA2_230_CH7481_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSSIA2_230_CH7447_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSSIA2_230_CH7487_S.s') == 'Estado do ponto digital:on'):
        
        config['SIA2'] = 0

    elif (status.get('MSSIA2_230_CH7431_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSSIA2_230_CH7451_S.s') == 'Estado do ponto digital:on') or \
         (status.get('MSSIA2_230_CH7437_S.s') == 'Estado do ponto digital:on' and 
          status.get('MSSIA2_230_CH7457_S.s') == 'Estado do ponto digital:on'):
        
        config['SIA2'] = 0

    else:
        config['SIA2'] = 1

    print("Configurações atualizadas:", config)

atualizar_get_current_values()