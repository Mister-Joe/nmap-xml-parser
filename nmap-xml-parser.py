import argparse, sys
import xml.etree.ElementTree as ET


def open_ports():
        for host in root.iter('ports'):
                ports = host.findall('port')
                for port in ports:
                        print(port.get('portid'))

def ports_per_host():
        for host in root.iter('host'):
                address = host.find('address')
                print(address.get('addr'), end=' : ')
                for ports in host.iter('ports'):
                        port_list = ports.findall('port')
                        for port in port_list:
                                print(port.get('portid'), end=',')
        print()

def alive_hosts():
        for host in root.iter('host'):
                status = host.find('status')
                address = host.find('address')
                if status.get('state') == 'up':
                        print(address.get('addr'))

parser = argparse.ArgumentParser(description='Parse nmap XML output.')
parser.add_argument('filepath', type = str, help = 'path to XML file')
parser.add_argument('--all_open_ports', action = 'store_true', help = 'display list of open ports irrespective of host')
parser.add_argument('--alive_hosts', action = 'store_true', help = 'display alive hosts (ping + ports)')
parser.add_argument('--host_port', action = 'store_true', help = 'display hosts & respective open ports')
args = parser.parse_args()

tree = ET.parse(args.filepath)
root = tree.getroot()

if len(sys.argv) > 3:
        print('Error: too many arguments.')
        exit(-1)
elif args.all_open_ports == True:
        open_ports()
elif args.alive_hosts == True:
        alive_hosts()
elif args.host_port == True:
        ports_per_host()
