import argparse, sys
import xml.etree.ElementTree as ET


def all_ports():
    for host in root.iter('ports'):
        ports = host.findall('port')
        used_ports = []
        for port in ports:
            if port.get('portid') not in used_ports:
                used_ports.append(port.get('portid'))
    for port in used_ports:
        print(port)

def host_ports():
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

def all_service_names():
    used_services = []
    for ports in root.iter('ports'):
        for port in ports.iter('port'):
            services = port.find('service')
            if services.get('product') and services.get('version'):
                if services.get('product') + ' ' + services.get('version') not in used_services:
                    used_services.append(services.get('product') + ' ' + services.get('version'))
            elif services.get('product') and not services.get('version'):
                if services.get('product') not in used_services:
                    used_services.append(services.get('product'))
    for service in used_services:
        print(service)

parser = argparse.ArgumentParser(description='Parse nmap XML output.')
parser.add_argument('filepath', type = str, help = 'path to XML file')
parser.add_argument('--all_ports', action = 'store_true', help = 'display list of open ports irrespective of host')
parser.add_argument('--alive_hosts', action = 'store_true', help = 'display alive hosts')
parser.add_argument('--host_ports', action = 'store_true', help = 'display hosts & respective open ports')
parser.add_argument('--all_service_names', action = 'store_true', help = 'display list of service names + versions (if available) irrespective of host')
args = parser.parse_args()

tree = ET.parse(args.filepath)
root = tree.getroot()

if len(sys.argv) > 3:
    print('Error: too many arguments.')
    exit(-1)
elif args.all_ports == True:
    all_ports()
elif args.alive_hosts == True:
    alive_hosts()
elif args.host_ports == True:
    host_ports()
elif args.all_service_names == True:
    all_service_names()
