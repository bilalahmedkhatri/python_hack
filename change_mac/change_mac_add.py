import optparse
import random
import re
from subprocess import run, check_output


def random_mac_address():
    generated_mac = ""
    for x in range(6):
        generated_mac += f"{random.randint(0,9)}{random.randint(0,9)}:"
    generated_mac = generated_mac[:-1]
    return generated_mac


def inline_parser_option():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='add mac address option which is open')
    parser.add_option('-m', '--mac', dest='mac', help='New Mac address')
    (options, argument) = parser.parse_args()
    if not options.interface:
        parser.error("[*] please specify interface to change mac")
    return options


def get_current_mac():
    option = inline_parser_option()
    ifconfig_result = str(check_output(['ifconfig', option.interface]))
    print(ifconfig_result)
    search_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
    if not search_mac:
        print(f"[*] MAC address is not found in {option.interface}")
    else:
        print('mac address found: => ', search_mac.group(0))


def change_mac_address():
    run(['ifconfig', inline_parser_option().interface, 'down']).returncode
    # if get_current_mac()
    if not inline_parser_option().mac:
        change_mac = run(['ifconfig', inline_parser_option().interface, 'hw', 'ether', random_mac_address()], capture_output=True)
    else:
        change_mac = run(['ifconfig', inline_parser_option().interface, 'hw', 'ether', inline_parser_option().mac], capture_output=True)
    print('test', random_mac_address())
    run(['ifconfig', inline_parser_option().interface, 'up'])
    # run(['ifconfig', option_.interface])

    print('test0', change_mac.returncode)
    print("test1", change_mac.stdout.decode())
    print("test2", change_mac.stderr.decode())


get_current_mac()
change_mac_address()
