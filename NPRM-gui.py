import tkinter as tk
import serial
import serial.tools.list_ports as lsPorts
#import telnetlib
import time
from re import search as reSearch


#Functions

def openAndChooseConnecton():
	print("TEST")

		
def sendModemCommand(NPRcommand):
	if selectedConnection.get() == "USB":
		usbPath = input_USBpath.get()
		ser = serial.Serial(usbPath, usbSerialBPS, timeout=0.2, write_timeout=0.2)
	else:
		print("Nothing or Telnet")
	print("Port is open:", ser.is_open)
	ser.write(b'\r\n')
	time.sleep(0.002)
	s = ser.readlines(1000)
	#print(s[1].decode('ascii'))
	
	for i in range(0,len(NPRcommand)):
		ser.write(NPRcommand[i].encode('ascii'))
		time.sleep(0.002)
	ser.write(b'\r\n')
	print("NPR Command is:", NPRcommand)
	
	if NPRcommand == "reboot":
		time.sleep(6)
	if NPRcommand == "radio on":
		time.sleep(1)
	time.sleep(0.002)
	s = ser.readlines(1000)
	print("Ausgabe von S:")
	print(s)
	#for i in range(0,len(s)):
	#	print(s[i])
	#exit STATUS and WHO pages with CTRL+C	
	if NPRcommand == "status" or NPRcommand == "who":
		ser.write("\x03".encode('ascii'))
		time.sleep(0.1)
		ctrlC = ser.readlines(1000)
		print("Send Ctrl+C", ctrlC)
	ser.close()
	return s

def showRadioStatus():
	msg = sendModemCommand("status")
	if msg[1].decode('ascii').find("radio OFF") == -1:
		mRadioStatus.set(msg[1].decode('ascii')[msg[1].decode('ascii').find("status:")+8:msg[1].decode('ascii').find(" TA:")])
		mRFDistance.set(msg[1].decode('ascii')[msg[1].decode('ascii').find("TA:")+3:msg[1].decode('ascii').find("km")] + " km")
		mTemp.set(msg[1].decode('ascii')[msg[1].decode('ascii').find("Temp:")+5:msg[1].decode('ascii').find("degC")] + " °C")
		mdownDBm.set(msg[3].decode('ascii')[msg[3].decode('ascii').find("RSSI:")+5:msg[3].decode('ascii').find("ERR:")-1])
		mupDBm.set(msg[4].decode('ascii')[msg[4].decode('ascii').find("RSSI:")+5:msg[4].decode('ascii').find("ERR:")-1])
	else:
		mRadioStatus.set(msg[1].decode('ascii')[msg[1].decode('ascii').find("status:")+8:msg[1].decode('ascii').find(" TA:")])
		mRFDistance.set("")
		mTemp.set("")
		mdownDBm.set("")
		mupDBm.set("")
	infoStatus.set("Showing Radio State.")
	
def turnRadioON():
	msg = sendModemCommand("radio on")
	print(msg)
	showRadioStatus()
	infoStatus.set("Radio started.")

def turnRadioOFF():
	msg = sendModemCommand("radio off")
	print(msg)
	showRadioStatus()
	infoStatus.set("Radio stopped.")

def rebootNPR():
	msg = sendModemCommand("reboot")
	infoStatus.set("Rebooted.")
	
def readVersionAndBand():
	msg = sendModemCommand("version")
	mfw_version.set(msg[1].decode('ascii')[10:20])
	mfreq_band.set(msg[2].decode('ascii')[11:15])
	infoStatus.set("Showing Version and Frequency Band.")
	
def testConnection():
	msg = sendModemCommand("status")
	print(msg[1].decode('ascii')[13:23])
	infoStatus.set("Showing Modem Status.")

def showVARTEST():
	print(selectedConnection.get())

def readModemStatusConfig():
	print("Test")

def readModemConfig():

	msg = sendModemCommand("display config")
	
	if msg[3].decode('ascii').find("no") == -1:
		print("Modem is Master")
		moc = "m"
	else:
		moc = "c"
		print("Modem is Client")
		
	if moc == "m":
		mValues = [mCallsign,
			mIs_master,
			mMAC,
			mFrequency,
			mFreq_shift,
			mRF_power,
			mModulation,
			mRadio_netw_ID,
			mRadio_on_at_start,
			mTelnet_active,
			mTelnet_routed,
			mModem_IP,
			mNetmask,
			mMaster_FDD,
			mIP_begin,
			mMaster_IP_size,
			mDef_route_active,
			mDef_route_val,
			mDNS_active,
			mDNS_value
			]
		mDHCP_active.set("BLANK")
		mClient_req_size.set("BLANK")
		mClient_static_IP.set("BLANK")
		mClient_static_IP.set("BLANK")
		
		msgStart = 2
		for i in mValues:
			i.set(msg[msgStart].decode('ascii')[msg[msgStart].decode('ascii').find(":"[:])+2:(int(len(msg[msgStart]))-2)])
			msgStart += 1

	if moc == "c":
		mValues = [mCallsign,
			mIs_master,
			mMAC,
			mFrequency,
			mFreq_shift,
			mRF_power,
			mModulation,
			mRadio_netw_ID,
			mRadio_on_at_start,
			mTelnet_active,
			mTelnet_routed,
			mModem_IP,
			mNetmask,
			mIP_begin,
			mClient_req_size,
			mDHCP_active
			]
		mMaster_IP_size.set("BLANK")
		mDef_route_active.set("BLANK")
		mDef_route_val.set("BLANK")
		mDNS_active.set("BLANK")
		mDNS_value.set("BLANK")
		mMaster_FDD.set("BLANK")
		mClient_static_IP.set("BLANK")
		
		msgStart = 2
		for i in mValues:
			i.set(msg[msgStart].decode('ascii')[msg[msgStart].decode('ascii').find(":"[:])+2:(int(len(msg[msgStart]))-2)])
			msgStart += 1
	infoStatus.set("Showing Modem Config.")
			
		

			#mDHCP_active,
			#mClient_req_size,
			#mClient_static_IP,
			#mTelnet_active,
			#mTelnet_routed,
			#mModem_IP,
			#mNetmask,
			#mIP_begin,
			#mMaster_IP_size,
			#mDef_route_active,
			#mDef_route_val,
			#mDNS_active,
			#mDNS_value
			
	

def writeModemConfig():
	
	#input.get into separate variable and:
	
    #check yes no variable
    yes_no_List = [
            [input_Is_master.get(),Is_master2m],
            [input_Radio_on_at_start.get(),Radio_on_at_start2m],
            [input_DHCP_active.get(),DHCP_active2m],
            [input_Client_static_IP.get(),Client_static_IP2m],
            [input_Telnet_active.get(),Telnet_active2m],
            [input_Telnet_routed.get(),Telnet_routed2m],
            [input_Def_route_active.get(),Def_route_active2m],
            [input_DNS_active.get(),DNS_active2m]
            ]
    for i in yes_no_List:
        if i[0] == "yes" or i[0] == "no":
            i[1] = i[0]
            #print("YES NO variale set")
            #print(type(i[0]))
            print(i[1])
        else:
            i[1] = "NULL"
            #print("YES NO NOT SET")
    #print("YesNoList is:",yes_no_List)
    #IP field check
    IPvalueList = [
            [input_Modem_IP.get(),Modem_IP2m],
            [input_Netmask.get(),Netmask2m],
            [input_DNS_value.get(),DNS_value2m],
            [input_Def_route_val.get(),Def_route_val2m],
            [input_IP_begin.get(),IP_begin2m]
            ]
    
    regexIP = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)"
    
    for i in IPvalueList:
        if reSearch(regexIP, i[0]) and i[0] != "":
            i[1] = i[0]
            #print("Valid IP set")
        else:
            i[1] = "NULL"
            #print("No Valid ip")
    #other checks
    
    #callsign check
    if len(input_Callsign.get()) <= 13 and input_Callsign.get() != "":
        Callsign2m = input_Callsign.get()
        print("Callsign set to:",Callsign2m)
    else:
        Callsign2m = "NULL"
        print("Callsign not Set or too long")
        
    #frequency check 420 zu 450.
    regexFreq = "^(4[2-4][0-9])\.([0-9][0-9][0-9])$"
    if reSearch(regexFreq, input_Frequency.get()) and len(input_Frequency.get()) == 7 and input_Frequency.get() != "420.000" or input_Frequency.get() == "450.000":
        Frequency2m = input_Frequency.get()
        print("Freq set to", Frequency2m)
    else:
        Frequency2m = "NULL"
        print("Freq to high, to low or wrong input")
    
    
    
    f0t9 = "0,1,2,3,4,5,6,7,8,9"
	#Freq Shift check
    fSvar = input_Freq_shift.get()
    wrongchars = 0
    sFsigns = "-."+f0t9
    for i in range(len(fSvar)):
        if sFsigns.find(fSvar[i-1]) == -1:
            wrongchars += 1
            print("Wrongchars: ", wrongchars)
    if fSvar.count("-") == 1 and fSvar[0] != "-":
        wrongchars += 1
        
    if wrongchars == 0 and fSvar.find(".") != -1 and int(fSvar[:fSvar.find(".")]) in range(-9,10) and len(fSvar[fSvar.find(".")+1:]) == 3 and f0t9.find(fSvar[fSvar.find(".")+1:fSvar.find(".")+2]) != -1 and f0t9.find(fSvar[fSvar.find(".")+2:fSvar.find(".")+3]) != -1 and f0t9.find(fSvar[fSvar.find(".")+3:fSvar.find(".")+4]) != -1:
        Freq_shift2m = input_Freq_shift.get()
    elif fSvar == "-10.000" or fSvar == "10.000":
        Freq_shift2m = input_Freq_shift.get()
    else:
        Freq_shift2m = "NULL"
        print("Freq-Shift to high, to low or wrong input")

    #RF_power2m = input_RF_power.get()
    RF_powerListString = "2,3,4,5,6,7,8,9,10,11,12,14,16,20"
    if len(input_RF_power.get()) <= 2 and len(input_RF_power.get()) >= 1 and RF_powerListString.find(input_RF_power.get()) != -1:
        RF_power2m = input_RF_power.get()
        print("RF Power set to:", RF_power2m)
    else:
        RF_power2m = "NULL"
        print("Wrong RF_power value.")
    #Modulation2m = input_Modulation.get()
    ModulationListString = "11, 12, 13, 14, 20, 21, 22, 23, 24"
    if len(input_Modulation.get()) == 2 and ModulationListString.find(input_Modulation.get()) != -1:
        Modulation2m = input_Modulation.get()
        print("Modulation set to:", Modulation2m)
    else:
        Modulation2m = "NULL"
        print("Wrong Modulaton Value")
	#Radio_netw_ID2m = input_Radio_netw_ID.get()
    rnwIDListString = "0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15"
    if len(input_Radio_netw_ID.get()) <= 2 and len(input_Radio_netw_ID.get()) >= 1 and rnwIDListString.find(input_Radio_netw_ID.get()) != -1:
        Radio_netw_ID2m = input_Radio_netw_ID.get()
        print("Radio NW ID set to: ", Radio_netw_ID2m)
    else:
        Radio_netw_ID2m = "NULL"
        print("Wrong Radio Network ID input.")
	#Client_req_size2m = input_Client_req_size.get()
	#Master_IP_size2m = input_Master_IP_size.get()
		
	#valuesListForCheck = [Callsign2m,Is_master2m,MAC2m,Frequency2m,Freq_shift2m,RF_power2m,Modulation2m,Radio_netw_ID2m,Radio_on_at_start2m,DHCP_active2m,Client_req_size2m,Client_static_IP2m,Telnet_active2m,Telnet_routed2m,Modem_IP2m,Netmask2m,IP_begin2m,Master_IP_size2m,Def_route_active2m,Def_route_val2m,DNS_active2m,DNS_value2m]
	#print(valuesListForCheck)
	
	#push values to NPR modem
    cmd_set = "set"
    cmd_and_val2mList = [
            [Callsign2m,"callsign"],
            [Frequency2m,"frequency"],
            [Freq_shift2m,"freq_shift"],
            [RF_power2m,"RF_power"],
            [Modulation2m,"modulation"],
            [Radio_netw_ID2m,"radio_netw_ID"],
            
            [yes_no_List[0][1],"is_master"],
            [yes_no_List[1][1],"radio_on_at_start"],
            [yes_no_List[2][1],"DHCP_active"],
            [yes_no_List[4][1],"telnet_active"],
            [yes_no_List[5][1],"telnet_routed"],
            [yes_no_List[6][1],"def_route_active"],
            [yes_no_List[7][1],"DNS_active"],
            
            ["NULL","client_req_size"],
            
            [IPvalueList[0][1],"modem_IP"],
            [IPvalueList[1][1],"netmask"],
            [IPvalueList[2][1],"DNS_value"],
            [IPvalueList[3][1],"def_route_val"],
            [IPvalueList[4][1],"IP_begin"],
            ]
    #print(cmd_and_val2mList)
    
    for i in cmd_and_val2mList:
        if i[0] != "NULL":
            cmd2m = str(cmd_set + " " + i[1] + " " + i[0])
            mfeedback = sendModemCommand(cmd2m)
            time.sleep(0.1)
            print("Feedback from CMD send: ", mfeedback)
            print(type(cmd2m), cmd2m)
        else:
            nothing = "nothing"
    readModemConfig()
        
	#print("BLANK.")

def saveModemConfig():
	msg = sendModemCommand("save")
	infoStatus.set("Configuration saved on NPR-Chip.")

def FACTORYRESET():
	msg = sendModemCommand("reset_to_default")
	time.sleep(6)
	readVersionAndBand()
	readModemConfig()
	infoStatus.set("Modem was set to FACTORY DEFAULTS")
	
def selectUSB():
	selectedConnection.set("USB")
	return selectedConnection
	
def selectTELNET():
	selectedConnection.set("TELNET")
	return selectedConnection
	
def exitTool():
	print("Exiting Tool.")
	time.sleep(0.1)
	rootF.destroy()
	
#serial config
#Parameters for serial over USB connection
usbSerialBPS = 921600
usbSerialBITS = "8"
usbSerialFlowControl = "NO"
telnetPort = 23

moc = "NULL"

rootF = tk.Tk()
rootF.title("NewPacketRadioModem - GUI")
rootF.geometry('720x760')
#vars
tool_started = 0
usbAutoConfig = 0
autoUSBpath = ""
#fix values (user cant't edit)
mfw_version = tk.StringVar()
mfreq_band = tk.StringVar()
#status values
mRadioStatus = tk.StringVar()
mTemp = tk.StringVar()
mdownDBm = tk.StringVar()
mupDBm = tk.StringVar()
mRFDistance = tk.StringVar()

#own messages
infoStatus = tk.StringVar()

#changeable values (user can edit)
selectedConnection = tk.StringVar()

if tool_started == 0:
	lsSerialDevices = lsPorts.comports()
	serialDevicesInfo = []
	serialDIcounter = -1
	for i in lsSerialDevices:
		serialDevicesInfo.append(i.device)
		serialDevicesInfo.append(i.description)

	if len(serialDevicesInfo) >= 2:
		for i in serialDevicesInfo:
			if i.find("STM32 STLink") != -1:
				autoUSBpath = str(serialDevicesInfo[serialDIcounter])
				print("USB auto-config set to: ", autoUSBpath)
			serialDIcounter += 1
	else:
		autoUSBpath = ""
		print("USB Auto-Config Failed")
	selectedConnection.set("USB")
	tool_started = 1
	
	
mConnectionStatus = tk.StringVar()
mCallsign = tk.StringVar()
mIs_master = tk.StringVar()
mMAC = tk.StringVar()
mFrequency = tk.StringVar()
mFreq_shift = tk.StringVar()
mRF_power = tk.StringVar()
mModulation = tk.StringVar()
mRadio_netw_ID = tk.StringVar()
mRadio_on_at_start = tk.StringVar()
mDHCP_active = tk.StringVar()
mClient_req_size = tk.StringVar()
mClient_static_IP = tk.StringVar()
mTelnet_active = tk.StringVar()
mTelnet_routed = tk.StringVar()
mModem_IP = tk.StringVar()
mNetmask = tk.StringVar()
mIP_begin = tk.StringVar()
mMaster_IP_size = tk.StringVar()
mDef_route_active = tk.StringVar()
mDef_route_val = tk.StringVar()
mDNS_active = tk.StringVar()
mDNS_value = tk.StringVar()
mMaster_FDD = tk.StringVar()

Callsign2m = tk.StringVar()
Is_master2m = tk.StringVar()
MAC2m = tk.StringVar()
Frequency2m = tk.StringVar()
Freq_shift2m = tk.StringVar()
RF_power2m = tk.StringVar()
Modulation2m = tk.StringVar()
Radio_netw_ID2m = tk.StringVar()
Radio_on_at_start2m = tk.StringVar()
DHCP_active2m = tk.StringVar()
Client_req_size2m = tk.StringVar()
Client_static_IP2m = tk.StringVar()
Telnet_active2m = tk.StringVar()
Telnet_routed2m = tk.StringVar()
Modem_IP2m = tk.StringVar()
Netmask2m = tk.StringVar()
IP_begin2m = tk.StringVar()
Master_IP_size2m = tk.StringVar()
Def_route_active2m = tk.StringVar()
Def_route_val2m = tk.StringVar()
DNS_active2m = tk.StringVar()
DNS_value2m = tk.StringVar()
Master_FDD2m = tk.StringVar()
#Buttons
ButtonUSBConnection = tk.Button(rootF, text="USB", command=selectUSB)
ButtonTELNETConnection = tk.Button(rootF, text="Telnet", command=selectTELNET)
ButtonUsbTelnetTest = tk.Button(rootF, text="USB/TELNET Test", command=showVARTEST)
fw_versionAndFreq_BandButton = tk.Button(rootF, text="Show FW and Freq Band", command=readVersionAndBand)
readModemStatusButton = tk.Button(rootF, text="Get NPR Status", command=readModemStatusConfig)
readModemConfigButton = tk.Button(rootF, text="Get NPR Values", command=readModemConfig)
ButtonRadioStatus = tk.Button(rootF, text="Radio Status", command=showRadioStatus)
radioOnButton = tk.Button(rootF, text="Turn Radio On", command=turnRadioON)
radioOffButton = tk.Button(rootF, text="Turn Radio Off", command=turnRadioOFF)
rebootButton = tk.Button(rootF, text="Reboot NPR70", command=rebootNPR)
FACTORYRESETButton = tk.Button(rootF, text="!!!FACTORY RESET!!!", command=FACTORYRESET)
config2ModemButton = tk.Button(rootF, text="Settings -> Modem", command=writeModemConfig)
saveConfigToChipButton = tk.Button(rootF, text="Save Config on NPR", command=saveModemConfig)
exitButton = tk.Button(rootF, text="Close", command=exitTool)

#Labels
fw_versionLabel = tk.Label(rootF, width=15, anchor="w", text="Firmware Version:")
freq_bandLabel = tk.Label(rootF, width=15, anchor="w", text="Frequency Band:")
setConnectionLabel = tk.Label(rootF, width=20, anchor="w", text="Selected Connection:")
USBportPathLabel = tk.Label(rootF, width=20, anchor="w", text="Set USB Path:")
TelnetIPLabel = tk.Label(rootF, width=20, anchor="w", text="Set Telnet IP:")

testConnection2ModemLabel = tk.Label(rootF, width=16, anchor="w", text="USB / TELNET:")

downDBmLabel = tk.Label(rootF, text="DOWNLINK (rssi):")
upDBmLabel = tk.Label(rootF, text="UPLINK (rssi):")
modemTempLabel = tk.Label(rootF, text="MODEM Temp:")
RFDistanceLabel = tk.Label(rootF, text="Connection Distance:")

radioStatusLabel = tk.Label(rootF, width=6, anchor="w", text="Status:")


#connectionStatusLabel = tk.Label(rootF,bg="red", textvariable=connectionStatus)
infoBoxLabel = tk.Label(rootF, bg="black", fg= "white", anchor="w", width=14, text="Info and Errors:")
showInfoLabel = tk.Label(rootF, bg="black", fg= "white", anchor="w", width=40, textvariable=infoStatus)

#just the Labels from settings fertig
settingsLabelWidth = 18
CallsignLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Callsign:")
Is_masterLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="is Master:")
MACLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="MAC:")
FrequencyLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Frequency:")
Freq_shiftLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Freq-Shift:")
RF_powerLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Output Power Value:")
ModulationLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Modulation Value:")
Radio_netw_IDLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Radio Network ID:")
Radio_on_at_startLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Radio on at Start:")
DHCP_activeLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="DHCP active:")
Client_req_sizeLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Client req size:")
Client_static_IPLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Client static IP:")
Telnet_activeLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Telnet active:")
Telnet_routedLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Telnet route:")
Modem_IPLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Modem IP:")
NetmaskLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Netmask:")
IP_beginLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="IP begin:")
Master_IP_sizeLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Master IP size:")
Def_route_activeLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Def route active:")
Def_route_valLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Def route val:")
DNS_activeLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="DNS active:")
DNS_valueLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="DNS value:")
Master_FDDLabel = tk.Label(rootF, width=settingsLabelWidth, bg="light grey", anchor="w", text="Master FDD:")
#|
#V
#show the values from modem fertig
svWidth = 19
scvWidth = 5
show_selectedConnection = tk.Label(rootF, bg="light grey", anchor="w", width=6, textvariable=selectedConnection)
show_mConnectionStatus = tk.Label(rootF, bg="light grey", anchor="w", width=4, textvariable=mConnectionStatus)
show_fw_version = tk.Label(rootF, bg="light grey", anchor="w", width=10, textvariable=mfw_version)
show_freq_band = tk.Label(rootF, bg="light grey", anchor="w", width=10, textvariable=mfreq_band)
show_downDBm = tk.Label(rootF, bg="light grey", anchor="w", width=5, textvariable=mdownDBm)
show_upDBm = tk.Label(rootF, bg="light grey", anchor="w", width=5, textvariable=mupDBm)
show_mTemp = tk.Label(rootF, bg="light grey", anchor="w", width=5, textvariable=mTemp)
show_mRFDistance = tk.Label(rootF, bg="light grey", anchor="w", width=9, textvariable=mRFDistance)
show_mRadioStatus = tk.Label(rootF, bg="light grey", anchor="w", width=19, textvariable=mRadioStatus)

show_mCallsign = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mCallsign)
show_mIs_master = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mIs_master)
show_mMAC = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mMAC)
show_mFrequency = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mFrequency)
show_mFreq_shift = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mFreq_shift)
show_mRF_power = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mRF_power)
show_mModulation = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mModulation)
show_mRadio_netw_ID = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mRadio_netw_ID)
show_mRadio_on_at_start = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mRadio_on_at_start)
show_mDHCP_active = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mDHCP_active)
show_mClient_req_size = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mClient_req_size)
show_mClient_static_IP = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mClient_static_IP)
show_mTelnet_active = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mTelnet_active)
show_mTelnet_routed = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mTelnet_routed)
show_mModem_IP = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mModem_IP)
show_mNetmask = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mNetmask)
show_mIP_begin = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mIP_begin)
show_mMaster_IP_size = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mMaster_IP_size)
show_mDef_route_active = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mDef_route_active)
show_mDef_route_val = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mDef_route_val)
show_mDNS_active = tk.Label(rootF, bg="light grey", anchor="w", width=scvWidth, textvariable=mDNS_active)
show_mDNS_value = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mDNS_value)
show_mMaster_FDD = tk.Label(rootF, bg="light grey", anchor="w", width=svWidth, textvariable=mMaster_FDD)
#|
#V
#Text-Input fertig
input_USBpath = tk.Entry(rootF, width=14)
#try to set usb-autodetect-path
if usbAutoConfig == 0:
	input_USBpath.insert(0, autoUSBpath)
	usbAutoConfig = 1
input_TelnetIP = tk.Entry(rootF, width=15)

input_Callsign = tk.Entry(rootF)
input_Is_master = tk.Entry(rootF)
input_MAC = tk.Entry(rootF)
input_Frequency = tk.Entry(rootF)
input_Freq_shift = tk.Entry(rootF)
input_RF_power = tk.Entry(rootF)
input_Modulation = tk.Entry(rootF)
input_Radio_netw_ID = tk.Entry(rootF)
input_Radio_on_at_start = tk.Entry(rootF)
input_DHCP_active = tk.Entry(rootF)
input_Client_req_size = tk.Entry(rootF)
input_Client_static_IP = tk.Entry(rootF)
input_Telnet_active = tk.Entry(rootF)
input_Telnet_routed = tk.Entry(rootF)
input_Modem_IP = tk.Entry(rootF)
input_Netmask = tk.Entry(rootF)
input_IP_begin = tk.Entry(rootF)
input_Master_IP_size = tk.Entry(rootF)
input_Def_route_active = tk.Entry(rootF)
input_Def_route_val = tk.Entry(rootF)
input_DNS_active = tk.Entry(rootF)
input_DNS_value = tk.Entry(rootF)
input_Master_FDD = tk.Entry(rootF)

#Layout
fw_versionAndFreq_BandButton.place(x=495, y=5)
fw_versionLabel.place(x=495, y=40)
freq_bandLabel.place(x=495, y=60)

setConnectionLabel.place(x=10, y=10)
show_selectedConnection.place(x=155,y=10)
ButtonUSBConnection.place(x=220, y=5)
ButtonTELNETConnection.place(x=280, y=5)

USBportPathLabel.place(x=10, y=40)
TelnetIPLabel.place(x=245, y=40)
input_USBpath.place(x=105, y=40)
input_TelnetIP.place(x=335, y=40)

testConnection2ModemLabel.place(x=10, y=70)
show_mConnectionStatus.place(x=125, y=70)
ButtonUsbTelnetTest.place(x=180, y=65)

downDBmLabel.place(x=10, y=135)
upDBmLabel.place(x=10, y=160)
show_downDBm.place(x=135, y=135)
show_upDBm.place(x=135, y=160)
RFDistanceLabel.place(x=200, y=135)
modemTempLabel.place(x=200, y=160)
show_mRFDistance.place(x=350, y=135)
show_mTemp.place(x=350, y=160)
radioStatusLabel.place(x=10, y=105)
show_mRadioStatus.place(x=60, y=105)
ButtonRadioStatus.place(x=240, y=100)
radioOnButton.place(x=360, y=100)
radioOffButton.place(x=490, y=100)

readModemConfigButton.place(x=545, y=205)
config2ModemButton.place(x=545, y=245)
saveConfigToChipButton.place(x=545, y=285)
rebootButton.place(x=545, y=330)
FACTORYRESETButton.place(x=545, y=380)
exitButton.place(x=575, y=640)

#Inputs
###Create Value-Name Lable Column
lableColumnList = [
        CallsignLabel,
        Is_masterLabel,
        MACLabel,
        FrequencyLabel,
        Freq_shiftLabel,
        RF_powerLabel,
        ModulationLabel,
        Radio_netw_IDLabel,
        Radio_on_at_startLabel,
        
        Client_req_sizeLabel,
        DHCP_activeLabel,
        Client_static_IPLabel,
        Telnet_activeLabel,
        Telnet_routedLabel,
        Modem_IPLabel,
        NetmaskLabel,
        IP_beginLabel,
        Master_IP_sizeLabel,
        Def_route_activeLabel,
        Def_route_valLabel,
        DNS_activeLabel,
        DNS_valueLabel,
        Master_FDDLabel
        ]

lableColumnY = 180
lableColumnX = 10
for i in lableColumnList:
	lableColumnY += 23
	i.place(x = lableColumnX, y = lableColumnY)

##Create show Value Column
show_fw_version.place(x = 620, y = 40)
show_freq_band.place(x = 620, y = 60)

showColumnList = [
        show_mCallsign,
        show_mIs_master,
        show_mMAC,
        show_mFrequency,
        show_mFreq_shift,
        show_mRF_power,
        show_mModulation,
        show_mRadio_netw_ID,
        show_mRadio_on_at_start,
        
        show_mClient_req_size,
        show_mDHCP_active,
        show_mClient_static_IP,
        show_mTelnet_active,
        show_mTelnet_routed,
        show_mModem_IP,
        show_mNetmask,
        show_mIP_begin,
        show_mMaster_IP_size,
        show_mDef_route_active,
        show_mDef_route_val,
        show_mDNS_active,
        show_mDNS_value,
        show_mMaster_FDD
        ]

showColumnY = 180
showColumnX = 165
for i in showColumnList:
	showColumnY += 23
	i.place(x = showColumnX, y = showColumnY)
	
###Create input Value Column
inputColumnList = [
        input_Callsign,
        input_Is_master,
        input_MAC,
        input_Frequency,
        input_Freq_shift,
        input_RF_power,
        input_Modulation,
        input_Radio_netw_ID,
        input_Radio_on_at_start,
        
        input_Client_req_size,
        input_DHCP_active,  
        input_Client_static_IP,
        input_Telnet_active,
        input_Telnet_routed,
        input_Modem_IP,
        input_Netmask,
        input_IP_begin,
        input_Master_IP_size,
        input_Def_route_active,
        input_Def_route_val,
        input_DNS_active,
        input_DNS_value,
        input_Master_FDD
        ]

inputColumnY = 180
inputColumnX = 345
for i in inputColumnList:
	inputColumnY += 23
	i.place(x = inputColumnX, y = inputColumnY)

infoBoxLabel.place(x = 10, y = 735)
showInfoLabel.place(x = 190, y = 735)
   
rootF.mainloop()
