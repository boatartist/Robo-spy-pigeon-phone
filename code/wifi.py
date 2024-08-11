import os
def wifi_off():
    os.system('sudo rfkill block wifi')
    
def wifi_on():
    os.system('sudo rfkill unblock wifi')
    
def connect_to_wifi(network_name='TelstraE1908E'):
    os.system(f'wpa_cli -i wlan0 select_network $(wpa_cli -i wlan0 list_networks | grep {network_name} | cut -f 1)')

def modem_off():
    os.system('sudo ip link set usb0 down')
    
def modem_on():
    os.system('sudo ip link set usb0 up')
    
if __name__ == '__main__':
    wifi_off()
    modem_on()