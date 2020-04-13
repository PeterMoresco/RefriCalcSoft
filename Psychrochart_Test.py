import psychrochart.equations as psc_e

# Temperatura de bulbo seco; pressao vapor
# entalpia = psc_e.enthalpy_moist_air()
# print(help(psc_e.specific_volume))
# print(help(psc_e.water_vapor_pressure))
# print(help(psc_e.enthalpy_moist_air))
# psc_e.relative_humidity_from_temps()
# print(help(psc_e.wet_bulb_temperature_empiric))
# print(help(psc_e.humidity_ratio_from_temps))
# t_bu_externo = psc_e.wet_bulb_temperature_empiric(33, 0.75)
hratio_externo = psc_e.humidity_ratio_from_temps(34,26)
t_bu_refrig = psc_e.wet_bulb_temperature_empiric(-20.5, 0.925)
hratio_refrig = psc_e.humidity_ratio_from_temps(-20.5, t_bu_refrig)
w_v_pexterno = psc_e.water_vapor_pressure(hratio_externo)
w_v_prefrig = psc_e.water_vapor_pressure(hratio_refrig)
entalpia_externa = psc_e.enthalpy_moist_air(34, w_v_pexterno)
entalpia_refrigeracao = psc_e.enthalpy_moist_air(-20.5, w_v_prefrig)
densidade_refri = psc_e.specific_volume(-20.5, w_v_prefrig)
densidade_externo = psc_e.specific_volume(34, w_v_pexterno)

print("""Relação de humidade: {} 
Pressão de vapor: {}
Entalpia do ar: {}
Volume específico: {}
Densidade: {}
""".format(hratio_externo, w_v_pexterno, entalpia_externa,
           densidade_externo, 1/densidade_externo))
