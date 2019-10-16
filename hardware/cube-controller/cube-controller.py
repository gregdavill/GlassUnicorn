# -*- coding: utf-8 -*-

from skidl import *
from string import ascii_uppercase
import subprocess


def place_part_inline(pin_net, part):
    out_net = Net()
    part[1] += out_net
    part[2] += pin_net
    return out_net

def add_decopling(nets, part):
    for n in nets:
        p = part()
        p[1] += n
        p[2] += Net.get('gnd')

class CubeController():


    def __init__(self):

        #===============================================================================
        # Component templates.
        #===============================================================================

        output_connector = Part('Connector_Generic_Shielded', 'Conn_01x20_Shielded', dest=TEMPLATE, footprint='gkl_conn:FH12-20S-0.5SVA(54)', PN='FH12-20S-0.5SVA(54)', Manf='Hirose Electric Co Ltd')
        d_74lvc8t245 = Part('Logic_LevelTranslator', 'SN74AVC8T245PW', dest=TEMPLATE, footprint='Package_DFN_QFN:Texas_RGY_R-PVQFN-N24_EP2.05x3.1mm', PN='SN74AVC8T245RHLR', Manf='Texas Instruments')
        
        samd51 = Part('gkl_microchip', 'ATSAMD51G19A', dest=TEMPLATE, footprint='Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm', PN='ATSAMD51G19A-MF', Manf='Microchip Technology')
        c_100uF = Part('Device', 'CP1', dest=TEMPLATE, footprint='Capacitor_SMD:CP_Elec_5x3.9', PN='UWX1C101MCL1GB', Manf='Nichicon')
        c_100nF = Part('Device', 'C', dest=TEMPLATE, footprint='Capacitor_SMD:C_0402_1005Metric', value='100nF', PN='CL05B104KP5NNNC', Manf='Samsung Electro-Mechanics')
        cap = Part('Device', 'C', dest=TEMPLATE, footprint='Capacitor_SMD:C_0402_1005Metric')
        rgb = Part('Device', 'LED_ARGB', dest=TEMPLATE, footprint='gkl_led:led_rbag_1515', PN='MHPA1515RGBDT', Manf='Meihua')
        res = Part('Device', 'R', dest=TEMPLATE, footprint='Resistor_SMD:R_0402_1005Metric')

        ice40up5k = Part('FPGA_Lattice', 'ICE40UP5K-SG48ITR', dest=TEMPLATE, footprint='Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm', PN='ICE40UP5K-SG48I', Manf='Lattice Semiconductor Corporation')
    
        d_tps62135 = Part('gkl_misc', 'TPS62135', dest=TEMPLATE, footprint='gkl_misc:VQFN-11_3x2mm_P0.5mm', PN='TPS621351RGXR', Manf='Texas Instruments')
        d_cap_10uf_16V_0603 = Part('Device', 'C', dest=TEMPLATE, footprint='Capacitor_SMD:C_0603_1608Metric', value='10uF', PN='GRM188R61C106MAALD', Manf='Murata Electronics')
        d_cap_1uf_6_3V_0402 = Part('Device', 'C', dest=TEMPLATE, footprint='Capacitor_SMD:C_0402_1005Metric', value='1uF', PN='CL05A105MQ5NNNC', Manf='Samsung Electro-Mechanics')
        d_inductor_1uH = Part('Device', 'L', dest=TEMPLATE, footprint='Inductor_SMD:L_Coilcraft_XxL4020', value='1uH', PN='78438357010', Manf='Wurth Electronics Inc.')
        d_inductor_2_2uH = Part('Device', 'L', dest=TEMPLATE, footprint='Inductor_SMD:L_0805_2012Metric', value='2.2uH', PN='LQM21FN2R2N00D', Manf='Murata Electronics')
        d_inductor_10uH = Part('Device', 'L', dest=TEMPLATE, footprint='Inductor_SMD:L_0805_2012Metric', value='10uH', PN='LQM21FN100M70L', Manf='Murata Electronics')

        d_tps561201 = Part('gkl_pmic', 'TPS561201', dest=TEMPLATE, footprint='Package_TO_SOT_SMD:TSOT-23-6', PN='TPS561201DDCT', Manf='Texas Instruments')
        

        d_con_10P_2x5 = Part('Connector_Generic', 'Conn_02x05_Odd_Even', dest=TEMPLATE, footprint='gkl_conn:FTSH-105-XX-X-DV', PN='FTSH-105-01-F-DV-K-TR', Manf='Samtec Inc.')
        d_qspi_flash = Part('gkl_mem', 'AT25SF081', dest=TEMPLATE, footprint='Package_SO:SOIC-8_5.23x5.23mm_P1.27mm', PN='W25Q128JVSIM TR', Manf='Winbond Electronics')

        d_button = Part('Switch', 'SW_Push', dest=TEMPLATE, footprint='gkl_misc:EVQP4', PN='EVQ-P42B3M', Manf='Panasonic Electronic Components')

        d_usb = Part('Connector', 'USB_C_Receptacle_USB2.0', dest=TEMPLATE, footprint='Connector_USB:USB_C_Receptacle_Palconn_UTC16-G', PN='CX90M-16P', Manf='Hirose Electric Co Ltd')

        d_bmx160 = Part('gkl_misc', 'BMX160', dest=TEMPLATE, footprint='Package_LGA:Bosch_LGA-14_3x2.5mm_P0.5mm', PN='BMX160', Manf='Bosch Sensortec')

        d_crystal = Part('Device', 'Crystal', dest=TEMPLATE, footprint='Crystal:Crystal_SMD_2012-2Pin_2.0x1.2mm', PN='ECS-.327-9-12R-C-TR', Manf='ECS Inc.')
        d_con_JST_PA_2 = Part('Connector_Generic', 'Conn_01x02', dest=TEMPLATE, footprint='gkl_conn:SB02B-PASK-2', PN='S02B-PASK-2(LF)(SN)', Manf='JST Sales America Inc.')

        d_ltc4367 = Part('gkl_pmic', 'LTC4367', dest=TEMPLATE, footprint='Package_DFN_QFN:DFN-8-1EP_3x3mm_P0.5mm_EP1.66x2.38mm', PN='LTC4367IDD#PBF', Manf='Linear Technology/Analog Devices')
        d_aon7804 = Part('gkl_mosfet', 'AON7804', dest=TEMPLATE, footprint='gkl_housings_dfn:DFN3X3_8L_EP2_P', PN='AON7804', Manf='Alpha / Omega Semiconductor Inc.')
        
        d_fb = Part('Device', 'Ferrite_Bead_Small', dest=TEMPLATE, footprint='Inductor_SMD:L_0402_1005Metric', PN='BK1005HS102-T', Manf='Taiyo Yuden')
        d_ncp115 = Part('gkl_pmic', 'NCP167', dest=TEMPLATE, footprint='gkl_housings_son:X2SON_4_1.0x1.0mm')

        d_ltc4413_1 = Part('gkl_pmic', 'LTC4413-2', dest=TEMPLATE, footprint='Package_DFN_QFN:DFN-10-1EP_3x3mm_P0.5mm_EP1.65x2.38mm', PN='LTC4413EDD-1#PBF', Manf='Linear Technology/Analog Devices')
        

        # Battery and protection circuit 


        pp_usb = Net('5v0_usb')
        pp4v5 = Net('4v5')
        pp4v5_in = Net('4v5_in')
        pp3v3 = Net('3v3')
        pp2v5 = Net('2v5')
        pp1v2 = Net('1v2')
        pp1v2_pll = Net('1v2_pll')

        ppbatt_prot = Net('pp_batt_prot')
        ppbatt = Net('pp_batt')


        gnd = Net('gnd')
        self.pp3v3 = pp3v3
        self.gnd = gnd

        
        #===============================================================================
        # Component instantiations.
        #===============================================================================

        ## Power supplies
        
        # Battery Input
        batt_connector = d_con_JST_PA_2()
        batt_connector['1'] += ppbatt
        batt_connector['2'] += gnd

        # Voltage protection/cutoff
        ltc4367 = d_ltc4367()
        aon7804 = d_aon7804()

        # Connect MOSFOTS back to back
        aon7804[2] += aon7804[5]
        aon7804[4] += ppbatt
        aon7804[1] += ppbatt_prot

        ltc4367['VIN'] += ppbatt
        ltc4367['GATE'] += aon7804[6, 3]
        ltc4367['VOUT'] += ppbatt_prot
        ltc4367['~SHDN'] += place_part_inline(gnd, res(value='510k', PN='RC0402FR-07510KL', Manf='Yageo'))
        ltc4367['GND'] += gnd
        
        #Values calculated create UnderVoltage: 6.74v, OverVoltage: 16.01v
        ltc_r1 = res(value='25.3k',PN='RC0402FR-0725K3L', Manf='Yageo')
        ltc_r2 = res(value='34.8k',PN='RC0402FR-0734K8L', Manf='Yageo')
        ltc_r3 = res(value='750k',PN='RC0402FR-07750KL', Manf='Yageo')
        
        ppbatt +=        ltc_r3[1]
        ltc4367['OV'] += ltc_r3[2], ltc_r2[1]
        ltc4367['UV'] +=            ltc_r2[2], ltc_r1[1]
        gnd +=                                 ltc_r1[2]
        

        # 4A 4.5/5V converter
        dcdc_5v = d_tps62135()
        
        dcdc_5v['VIN', 'GND'] += ppbatt_prot, gnd
        dcdc_5v['EN'] += place_part_inline(ppbatt_prot, res(value='100k',PN='RC0402FR-07100KL', Manf='Yageo'))
        dcdc_5v['VSEL', 'MODE'] += gnd
        dcdc_5v['SW'] += place_part_inline(pp4v5_in , d_inductor_1uH())
        dcdc_5v['VOS'] += pp4v5_in
        
        # Input capacitors
        ppbatt_prot += place_part_inline(gnd, d_cap_10uf_16V_0603())

        # Bulk Output Capacitors
        pp4v5_in += place_part_inline(gnd, d_cap_10uf_16V_0603())

        # feedback resistors for 4.53V Well above the Vf of the LEDs, swap 93.1k for 82k for 5v output
        dcdc_5v['FB'] += Net('5v_fb')
        dcdc_5v['FB'] += place_part_inline(pp4v5_in , res(value='510k',PN='RC0402FR-07510KL', Manf='Yageo'))
        dcdc_5v['FB'] += place_part_inline(gnd , res(value='93.1k',PN='RC0402FR-0793K1L', Manf='Yageo'))


        # 1A 3v3 Converter
        dcdc_3v3 = d_tps561201()

        dcdc_3v3['VIN', 'GND'] += pp4v5, gnd
        dcdc_3v3['EN'] += place_part_inline(pp4v5, res(value='100k',PN='RC0402FR-07100KL', Manf='Yageo'))
        dcdc_3v3['VBST'] += place_part_inline(dcdc_3v3['SW'], c_100nF())
        dcdc_3v3['SW'] += place_part_inline(pp3v3 , d_inductor_2_2uH())
        
        # Input capacitors
        pp4v5 += place_part_inline(gnd, d_cap_10uf_16V_0603())

        # Bulk Output Capacitors
        pp3v3 += place_part_inline(gnd, d_cap_10uf_16V_0603())
        
        # feedback
        dcdc_3v3['VFB'] += Net('3v3_fb')
        dcdc_3v3['VFB'] += place_part_inline(pp3v3 , res(value='33.2k',PN='RC0402FR-0733K2L', Manf='Yageo'))
        dcdc_3v3['VFB'] += place_part_inline(gnd , res(value='10k',PN='RC0402FR-0710KL', Manf='Yageo'))
        
        # 2v5 Power supply
        ldo_2v5 = d_ncp115(name='NP115-2.5', PN='NCP115CMX250TCG', Manf='ON Semiconductor')
        ldo_2v5['IN'] += pp3v3
        ldo_2v5['EN'] += pp3v3
        ldo_2v5['OUT'] += pp2v5
        ldo_2v5['GND'] += gnd

        cap_2v5 = d_cap_1uf_6_3V_0402()
        cap_2v5[1,2] += pp2v5, gnd


        # 1v2 Power supply
        ldo_1v2 = d_ncp115(name='NP115-1.2', PN='NCP115AMX120TCG', Manf='ON Semiconductor')
        ldo_1v2['IN'] += pp3v3
        ldo_1v2['EN'] += pp3v3
        ldo_1v2['OUT'] += pp1v2
        ldo_1v2['GND'] += gnd

        cap_1v2 = d_cap_1uf_6_3V_0402()
        cap_1v2[1,2] += pp1v2, gnd


        # PLL power supply
        fb = d_fb()
        fb[1,2] += pp1v2, pp1v2_pll
        pll_1v2_c = d_cap_1uf_6_3V_0402()
        pll_1v2_c[1,2] += pp1v2_pll, gnd


        c_bulk = c_100uF(3)
        for _c in c_bulk:
            _c[1,2] += pp4v5, gnd

        led = rgb()
        led[1] += pp3v3

        # Configure our samd51
        uc = samd51()
        uc['VDDIO'] += pp3v3
        uc['VDDANA'] += pp3v3
        uc['GND'] += gnd

        for net in uc['VDDIO', 'VDDANA']:
            c = c_100nF()
            c[1,2] += net, gnd

        uc['VDDCORE'] += place_part_inline(gnd, d_cap_1uf_6_3V_0402())


        led_r = Net('led_r')
        led_r += led[2]
        led_g = Net('led_g')
        led_g += led[3]
        led_b = Net('led_b')
        led_b += led[4]

        uc['PA13'] += place_part_inline(led_r, res(value='470R',PN='RC0402FR-07470RL', Manf='Yageo'))
        uc['PA15'] += place_part_inline(led_g, res(value='470R',PN='RC0402FR-07470RL', Manf='Yageo'))
        uc['PA14'] += place_part_inline(led_b, res(value='470R',PN='RC0402FR-07470RL', Manf='Yageo'))


        crystal = d_crystal(value='32.768kHz')
        crystal['1','2'] += uc['PA00', 'PA01']
        crystal['1'] += place_part_inline(gnd, cap(value='22pF', PN='CC0402JRNPO9BN220', Manf='Yageo'))
        crystal['2'] += place_part_inline(gnd, cap(value='22pF', PN='CC0402JRNPO9BN220', Manf='Yageo'))


        # Create our ice40up5k
        ice40 = ice40up5k()
        
        # Wire in power
        ice40['VPP_2V5'] += pp2v5
        ice40['VCC'] += pp1v2
        ice40['VCCPLL'] += pp1v2_pll
        ice40['VCCIO_0', 'SPI_VCCIO1', 'VCCIO_2'] += pp3v3
        ice40['GND'] += gnd

        # Add decoupling to all power pins
        add_decopling(ice40['VCCIO_0', 'SPI_VCCIO1', 'VCCIO_2', 'VPP_2V5', 'VCCPLL', 'VCC'], c_100nF) 


        ice_led = rgb()
        ice_led[1] += pp3v3

        ice_led_r = Net('ice_led_r')
        ice_led_r += ice_led[2]
        ice_led_g = Net('ice_led_g')
        ice_led_g += ice_led[3]
        ice_led_b = Net('ice_led_b')
        ice_led_b += ice_led[4]

        ice40['RGB0'] += place_part_inline(ice_led_r, res(value='470R',PN='RC0402FR-07470RL', Manf='Yageo'))
        ice40['RGB1'] += place_part_inline(ice_led_g, res(value='470R',PN='RC0402FR-07470RL', Manf='Yageo'))
        ice40['RGB2'] += place_part_inline(ice_led_b, res(value='470R',PN='RC0402FR-07470RL', Manf='Yageo'))

        ice40_config = [Net('ice_config_miso'),
                        Net('ice_config_mosi'),
                        Net('ice_config_sck'),
                        Net('ice_config_ss'),
                        Net('ice_config_done'),
                        Net('ice_config_reset')]

        ice40[  
            'IOB_32a_SPI_SO',
            'IOB_33b_SPI_SI',
            'IOB_34a_SPI_SCK',
            'IOB_35b_SPI_SS',
            'CDONE',
            '~CRESET'] += ice40_config

        # SAMD51 SPI PAD assignments:
         # [0] : Data Output - MOSI
         # [1] : Clock - CLK
         # [2] : Slave Select - SS
         # [3] : Data Input - MISO


        # Create a Config bus from the SAMD51 side
        # SERCOM0
        uc[
            'PA07', # MUX D - PAD[3] - MISO
            'PA04', # MUX D - PAD[0] - MOSI
            'PA05', # MUX D - PAD[1] - CLK
            'PA06', # MUX D - PAD[2] - SS
            'PB08',
            'PB09'] += ice40_config

        # connect a Clock pin into the ice40
        uc['PB23'] += ice40['IOT_46b_G0'] # PA14 MUX M - GCLK/IO[0]

        # connect a CS pin used during user mode
        uc['PA02'] += ice40[23]

        ice40_panel_bus = [
            # data blank latch sclk
            ice40[2,3,4,6,19,18,20,21,13],
            ice40[12,11,10,9,47,48,46,45,44],
        ]

        # Led panel names
        led_panel_signals = [
            'dr', 'dg', 'db', 
            'sclk', 'latch', 'blank',
            'rdata', 'rlatch', 'rblank',
        ]



        led_panel_bus0 = Bus('pb0')
        led_panel_bus1 = Bus('pb1')
        panel_bus = [led_panel_bus0, led_panel_bus1]

        led_panel_bus0_ = Bus('pb0_b')
        led_panel_bus1_ = Bus('pb1_b')
        panel_bus_ = [led_panel_bus0_, led_panel_bus1_]

        for i in range(2):
            for sig in led_panel_signals:
                panel_bus[i].extend(Net(f'{panel_bus[i].name}_{sig}'))
                panel_bus_[i].extend(Net(f'{panel_bus_[i].name}_{sig}'))


        ice40_panel_bus[0] += led_panel_bus0
        ice40_panel_bus[1] += led_panel_bus1
        
        _74lvc8t245 = d_74lvc8t245(3)
        for i in range(3):
            _74lvc8t245[i]['GND','~OE'] += gnd
            _74lvc8t245[i]['VCCA','DIR'] += pp3v3
            _74lvc8t245[i]['VCCB'] += pp4v5

        def buffer(a, b, c, d):
            a[f'A{b}, B{b}'] += panel_bus[c][f'.*_{d}'],panel_bus_[c][f'.*_{d}']

        buffer(_74lvc8t245[0], 1, 0, 'dr')
        buffer(_74lvc8t245[0], 2, 0, 'dg')
        buffer(_74lvc8t245[0], 3, 0, 'db')
        buffer(_74lvc8t245[0], 4, 0, 'sclk')
        buffer(_74lvc8t245[0], 5, 0, 'blank')
        buffer(_74lvc8t245[0], 6, 0, 'latch')
        buffer(_74lvc8t245[0], 7, 0, 'rdata')
        buffer(_74lvc8t245[0], 8, 0, 'rlatch')
        buffer(_74lvc8t245[1], 1, 0, 'rblank')


        buffer(_74lvc8t245[1], 5, 1, 'dr')
        buffer(_74lvc8t245[1], 6, 1, 'dg')
        buffer(_74lvc8t245[1], 7, 1, 'db')
        buffer(_74lvc8t245[1], 8, 1, 'sclk')
        buffer(_74lvc8t245[2], 4, 1, 'blank')
        buffer(_74lvc8t245[2], 5, 1, 'latch')
        buffer(_74lvc8t245[2], 6, 1, 'rdata')
        buffer(_74lvc8t245[2], 7, 1, 'rlatch')
        buffer(_74lvc8t245[2], 8, 1, 'rblank')


        #led_panel_bus0 = Bus('led_panel0_buffered', led_panel_signals)
        #led_panel_bus1 = Bus('led_panel1_buffered', led_panel_signals)
        

        # connect LED panels out from the ice40 via buffers
        for i in range(2):
            name = f'led{i}'
            con = output_connector()
            #_74lvc8t245 = d_74lvc8t245(2)

            con['SH'] += gnd

            con[1,2,9,13,17] += gnd
            con[3,4,5,18,19,20] += pp4v5
            
            
            
            panel_bus_[i]['.*_dr'] += con[6]
            panel_bus_[i]['.*_dg'] += con[7]
            panel_bus_[i]['.*_db'] += con[8]

            panel_bus_[i]['.*_sclk'] += con[10]
            panel_bus_[i]['.*_latch'] += con[11]
            panel_bus_[i]['.*_blank'] += con[12]

            panel_bus_[i]['.*_rdata'] += con[14]
            panel_bus_[i]['.*_rlatch'] += con[15]
            panel_bus_[i]['.*_rblank'] += con[16]

            # Output Capacitors
            pp4v5 += place_part_inline(gnd, d_cap_10uf_16V_0603())
            pp4v5 += place_part_inline(gnd, c_100nF())
        
        ice40['~CRESET'] += place_part_inline(gnd, res(value='10k',PN='RC0402FR-0710KL', Manf='Yageo'))


        # Wire in SWD connection
        swdio, swdclk, swo, swdrst = Net('swdio'),Net('swdclk'),Net('swo'),Net('samd_rst')

        con_swd = d_con_10P_2x5()
        con_swd[3,5,7,9] += gnd
        con_swd[1] += pp3v3
        con_swd[2] += swdio
        con_swd[4] += swdclk
        con_swd[6] += swo
        con_swd[10] += swdrst

        swdclk += place_part_inline(pp3v3, res(value='1k',PN='RC0402FR-071KL', Manf='Yageo'))

        uc['PA30', 'PA31'] += swdclk, swdio
        uc['~RESET'] += swdrst        

        uc['~RESET'] += place_part_inline(pp3v3, res(value='10k',PN='RC0402FR-0710KL', Manf='Yageo'))
        uc['~RESET'] += place_part_inline(gnd, c_100nF())

        # Wire in Accelerometer
        imu = d_bmx160()
        imu['VDDIO', 'VDD'] += pp3v3
        imu['GND', 'GNDIO'] += gnd
        add_decopling(imu['VDDIO', 'VDD'], c_100nF)

        #imu['VDDIO'] += place_part_inline(gnd, c_100nF())
        #imu['VDD'] += place_part_inline(gnd, c_100nF())

        spi_imu_bus =   [Net('imu_miso'),
                         Net('imu_mosi'),
                         Net('imu_sck'),
                         Net('imu_cs'),
                         Net('imu_int1'),
                         Net('imu_int2')]

        # SERCOM1
        uc['PA19', 'PA16', 'PA17', 'PA18', 'PA20', 'PA21'] += spi_imu_bus
        imu['SDO', 'SDx', 'SCx', '~CS','INT1','INT2'] += spi_imu_bus

        # wire in FLASH
        qspi_flash = d_qspi_flash()
        qspi_flash['VCC', 'GND'] += pp3v3, gnd
        qspi_flash['~CS'] += place_part_inline(pp3v3, res(value='10k',PN='RC0402FR-0710KL', Manf='Yageo'))

        qspi_bus     = [Net('qspi_bus_io0'),
                        Net('qspi_bus_io1'),
                        Net('qspi_bus_io2'),
                        Net('qspi_bus_io3'),
                        Net('qspi_bus_sck'),
                        Net('qspi_bus_cs')]

        # QSPI0
        uc['PA08', 'PA09', 'PA10', 'PA11', 'PB10', 'PB11'] += qspi_bus
        qspi_flash['SI', 'SO', '~WP', '~HOLD','SCK','~CS'] += qspi_bus

        # Wire in USB
        usb_c = d_usb()

        samd_usb_n, samd_usb_p = Net('samd_usb_n'), Net('samd_usb_p')

        usb_c['VBUS'] += pp_usb
        usb_c['D-'] += samd_usb_n
        usb_c['D+'] += samd_usb_p
        usb_c['GND'] += gnd
        usb_c['SHIELD'] += gnd

        uc['PA24', 'PA25'] += samd_usb_n, samd_usb_p

        # Add Button
        button_a = d_button()
        button_a[1] += uc['PB22']
        button_a[2] += gnd

        button_b = d_button()
        button_b[1] += uc['PA22']
        button_b[2] += gnd


        uc_inductor = d_inductor_10uH()
        uc_inductor[1,2] += uc['VSW, VDDCORE']

        ltc4413 = d_ltc4413_1()
        ltc4413['GND','SGND'] += gnd
        ltc4413['ENBA','ENBB'] += gnd
        ltc4413['OUTA','OUTB'] += pp4v5

        ltc4413['INA'] += pp_usb
        ltc4413['INB'] += pp4v5_in

        c_usb = d_cap_10uf_16V_0603()
        c_usb[1,2] += pp_usb,gnd

        usb_c['CC1'] += Net('cc1')
        usb_c['CC1'] += place_part_inline(gnd, res(name='5.1k',PN='RC0402FR-075K1L', Manf='Yageo'))
        usb_c['CC2'] += Net('cc2')
        usb_c['CC2'] += place_part_inline(gnd, res(name='5.1k',PN='RC0402FR-075K1L', Manf='Yageo'))

        
        



        





#===============================================================================
# Instantiate the circuit and generate the netlist.
#===============================================================================

if __name__ == "__main__":
    CubeController()
    generate_netlist()
    generate_xml()

    # Create a BOM
    subprocess.call(['python3', '/usr/share/kicad/plugins/bom_csv_grouped_by_value.py', 'cube-controller.xml', 'bom/cube-controller.csv'])