import subprocess # Importing subprocess to execute system commands
import optparse #The optparse module makes it easy to write user-friendly command-line interfaces.
import re
def get_arguments():
    # Use OptionParser class to allow the use of arguments in our program
    parser = optparse.OptionParser()
    # Use arguments for user input for more secure input
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    # Parse the arguments for previous options
    (options, arguments) = parser.parse_args()
    # Check if options.interface does not hold a value than throw error
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    # Check if options.new_mac does not hold a value than throw error
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    # Return the options flag so that it can be read by the other function.
    return options


def change_mac(interface, new_mac):
    # Allow python to execute terminal commands.
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])



def get_current_mac(interface):
    #execute and read ifconfig
    result = subprocess.check_output(['ifconfig', interface])
    print(result)
    #read the mac address from output
    # '\w' is for alphanumeric digits, written with colon to print our MAC
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(result))
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Could not read MAC address")

options = get_arguments()


current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] Mac address did not get changed.")


