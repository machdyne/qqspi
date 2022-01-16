# QQSPI Pmod(tm) compatible module
# Copyright (c) 2021 Lone Dynamics Corporation. All rights reserved.
#
# DESCRIPTION:
#
# Provides access to up to 4 Quad-SPI devices via a 12-pin PMOD port.
#
# PMOD CONNECTOR:
#
# 3v3 GND CLK SO1 SI0 /SS
# ------------------------
#  6   5   4   3   2   1
#  12  11  10  9   8   7
# ------------------------
# 3V3 GND CS1 CS0 SIO3 SIO2
#
# QSPI MEMORY:
#
# /CE     | 1  8 | VDD
# SO/SIO1 | 2  7 | SIO3
# SIO2    | 3  6 | SCLK
# VSS     | 4  5 | SI/SIO0
#
# 3-TO-8 DECODER (SN74HCS138PWR):
#
# A0  | 1  16 | VCC
# A1  | 2  15 | O0
# A2  | 3  14 | O1
# /E1 | 4  13 | O2
# /E2 | 5  12 | O3
# E3  | 6  11 | O4
# O7  | 7  10 | O5
# GND | 8   9 | O6
#
# FUNCTIONAL MODES:
#
# PMOD/SS PMODCS0 PMODCS1 QSPI1/CE QSPI2/CE QSPI3/CE QSPI4/CE
# H       X       X       H        H        H        H
# L       L       L       L        H        H        H
# L       H       L       H        L        H        H
# L       L       H       H        H        L        H
# L       H       H       H        H        H        L

from skidl import *

# create power
vcc3v3, gnd = Net('VCC3V3'), Net('GND')

# create the memory bus
qspi_clk = Net('CLK')
qspi_mosi = Net('MOSI') # SIO0
qspi_miso = Net('MISO') # SIO1
qspi_sio2 = Net('SIO2')
qspi_sio3 = Net('SIO3')
qspi_ss = Net('~SS')
qspi_cs0 = Net('CS0')
qspi_cs1 = Net('CS1')

# create the pmod connector
pmod = Part(lib='pmod.lib', name='PMOD-Device-x2-Type-Generic-Alt',
    footprint='pmod_pin_array_6x2')

# wire the pmod connector to the nets
qspi_ss += pmod['P1']
qspi_cs0 += pmod['P9']
qspi_cs1 += pmod['P10']
qspi_mosi += pmod['P2']
qspi_miso += pmod['P3']
qspi_clk += pmod['P4']
qspi_sio2 += pmod['P7']
qspi_sio3 += pmod['P8']

# create the 3-to-8 decoder
decoder = Part(lib='74xx.lib', name='74LS138',
    footprint='Package_SO:TSSOP-16_4.4x5mm_P0.65mm')
decoder.value = 'SN74HCS138PWR'

# create and wire the decoder decoupling capacitor
decoder_cap = Part(lib='Device.lib', name='C',
    footprint='Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder')
decoder_cap.value = '100nF'
vcc3v3 & decoder_cap & gnd

# create the memory
sram1 = Part(lib='Memory_RAM.lib', name='ESP-PSRAM32',
    footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm')
sram1.value = 'PSRAM1'

sram2 = sram1.copy()
sram2.value = 'PSRAM2'
sram3 = sram1.copy()
sram3.value = 'PSRAM3'
sram4 = sram1.copy()
sram4.value = 'PSRAM4'

# create and wire the memory decoupling capacitors
sram1_cap = decoder_cap.copy()
vcc3v3 & sram1_cap & gnd
sram2_cap = decoder_cap.copy()
vcc3v3 & sram2_cap & gnd
sram3_cap = decoder_cap.copy()
vcc3v3 & sram3_cap & gnd
sram4_cap = decoder_cap.copy()
vcc3v3 & sram4_cap & gnd

# power from host
vcc3v3 += pmod['P6']
vcc3v3 += pmod['P12']
gnd += pmod['P5']
gnd += pmod['P11']

# power the decoder
vcc3v3 += decoder['VCC']
gnd += decoder['GND']

# power the memory
vcc3v3 += sram1['VCC']
vcc3v3 += sram2['VCC']
vcc3v3 += sram3['VCC']
vcc3v3 += sram4['VCC']
gnd += sram1['VSS']
gnd += sram2['VSS']
gnd += sram3['VSS']
gnd += sram4['VSS']

# enable the decoder
vcc3v3 += decoder['E3']
gnd += decoder['E2']

# wire the chip enable/selects to the decoder inputs
qspi_ss += decoder['E1']
qspi_cs0 += decoder['A0']
qspi_cs1 += decoder['A1']
gnd += decoder['A2']

# wire the memory bus
qspi_clk += sram1['SCLK'], sram2['SCLK'], sram3['SCLK'], sram4['SCLK']
qspi_miso += sram1['SO/SIO'], sram2['SO/SIO'], sram3['SO/SIO'], sram4['SO/SIO']
qspi_mosi += sram1['SI/SIO'], sram2['SI/SIO'], sram3['SI/SIO'], sram4['SI/SIO']
qspi_sio2 += sram1['SIO2'], sram2['SIO2'], sram3['SIO2'], sram4['SIO2']
qspi_sio3 += sram1['SIO3'], sram2['SIO3'], sram3['SIO3'], sram4['SIO3']

# wire the decoder outputs to the memory chip enables
sram1['~CE'] += decoder['O0']
sram2['~CE'] += decoder['O1']
sram3['~CE'] += decoder['O2']
sram4['~CE'] += decoder['O3']

# create and wire the board decoupling capacitor
board_cap = Part(lib='Device.lib', name='C',
    footprint='Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder')
board_cap.value = '1uF'
vcc3v3 & board_cap & gnd

# generate the netlist to be imported into pcbnew
generate_netlist()
generate_svg()
