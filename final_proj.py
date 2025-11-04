#============================== HELPERR ==============================

def split_ip_mask(string):
    index_ip = 0
    for letters in string:
        if letters != "/": index_ip += 1
        elif letters == "/": break
    return string[:index_ip], string[index_ip + 1:]

def split_ip(ip):
    dot_index = []
    for index in range(len(ip)): 
        if ip[index] == ".": dot_index.append(index)
    return ip[:dot_index[0]], ip[dot_index[0] + 1:dot_index[1]], ip[dot_index[1] + 1:dot_index[2]], ip[dot_index[2] + 1:]

def is_between_0_255(value):
    if value >= 0 and value <=255: return True
    else: return False

def is_int_convertable(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def is_correct_format(ip, mask):
    octet1, octet2, octet3, octet4 = split_ip(ip)
    if not (is_int_convertable(octet1) and is_int_convertable(octet2) and is_int_convertable(octet3) and is_int_convertable(octet4)): return False
    octet1, octet2, octet3, octet4 = int(octet1), int(octet2), int(octet3), int(octet4)
    if not (is_between_0_255(octet1) and is_between_0_255(octet2) and is_between_0_255(octet3) and is_between_0_255(octet4)): return False

    if is_int_convertable(mask) == False : return False
    mask = int(mask)
    if mask > 32 or mask < 0: return False 
    return True

def to_u32(octet1, octet2, octet3, octet4): #convert o1, o2, o3, o4 to u32
    return octet1 << 24 | octet2 << 16 | octet3 << 8 | octet4
    
def from_u32(u32_integer): #convert to_u32 but reverse
    return (u32_integer >> 24) & 255, (u32_integer >> 16) & 255, (u32_integer >> 8) & 255, (u32_integer) & 255

def to_dotted_format(octet_tuple):
    return f"{octet_tuple[0]}.{octet_tuple[1]}.{octet_tuple[2]}.{octet_tuple[3]}"

def to_mask32(mask):
    return ((1 << mask) - 1) << (32 - mask)


#============================= CALC ==============================

def netmask(mask32):
    return mask32

def wildcard(mask32):
    return ~mask32

def network(ip32, mask32):
    return ip32 & mask32

def broadcast(ip32, mask32):
    return ip32 | ~mask32

def first_host(ip32, mask32, mask):
    if mask == 31 or mask == 32: return network(ip32, mask32)
    else: return network(ip32, mask32) + 1

def last_host(ip32, mask32, mask):
    if mask == 32: return network(ip32, mask32)
    if mask == 31: return broadcast(ip32, mask32)
    else: return broadcast(ip32, mask32) - 1

def total_address(mask):
    if mask == 32: return 1
    if mask == 31: return 2
    return 2 ** (32 - mask)


def usable_host(mask):
    if mask == 32: return 1
    if mask == 31: return 2
    return total_address(mask) -2

def ip_class(octet1):
    if 0 <= octet1 <= 127: return 'A'
    if 128 <= octet1 <= 191: return 'B'
    if 192 <= octet1 <= 223: return 'C'
    if 224 <= octet1 <= 239: return 'D'  
    return 'E'  

def ip_scope(octet1, octet2):
    if octet1 == 10: return "Private"   
    if octet1 == 172 and 16 <= octet2 <= 31: return "Private"
    if octet1 == 192 and octet2 == 168: return "Private"
    if octet1 == 127: return "Loopback"
    if octet1 == 169 and octet2 == 254: return "Link-local"
    if 224 <= octet1 <= 239: return "Multicast"
    if 240 <= octet1 <= 255: return "Reserved"
    return "Public"

#=============================== MAIN ===============================

print('''
  ██╗██████╗░██╗░░░██╗░░██╗██╗░░░░░░░██╗░░░██╗████████╗██╗██╗░░░░░██╗████████╗██╗░░░██╗
  ██║██╔══██╗██║░░░██║░██╔╝██║░░░░░░░██║░░░██║╚══██╔══╝██║██║░░░░░██║╚══██╔══╝╚██╗░██╔╝
  ██║██████╔╝╚██╗░██╔╝██╔╝░██║░░░░░░░██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░╚████╔╝░
  ██║██╔═══╝░░╚████╔╝░███████║░░░░░░░██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░░╚██╔╝░░
  ██║██║░░░░░░░╚██╔╝░░╚════██║░░░░░░░╚██████╔╝░░░██║░░░██║███████╗██║░░░██║░░░░░░██║░░░
  ╚═╝╚═╝░░░░░░░░╚═╝░░░░░░░░╚═╝░░░░░░░░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═╝░░░╚═╝░░░░░░╚═╝░░░
  ''')
print("Input IP Address in CIDR Format : <IP>/<MASK>")
ip_mask = input("> ")

ip, mask = split_ip_mask(ip_mask)
if is_correct_format(ip, mask):
    octet1, octet2, octet3, octet4 = map(int, split_ip(ip))
    mask = int(mask)
    ip32 = to_u32(octet1, octet2, octet3, octet4)
    mask32 = to_mask32(mask)

    netmask_var = to_dotted_format(from_u32(netmask(mask32)))
    wildcard_var = to_dotted_format(from_u32(wildcard(mask32)))
    network_var = f"{to_dotted_format(from_u32(network(ip32, mask32)))}/{mask}"
    broadcast_var = f"{to_dotted_format(from_u32(broadcast(ip32, mask32)))}"
    first_host_var = to_dotted_format(from_u32(first_host(ip32, mask32, mask)))
    last_host_var = to_dotted_format(from_u32(last_host(ip32, mask32, mask)))
    total_address_var = total_address(mask)
    usabel_host_var = usable_host(mask)
    class_scope_var = f"{ip_class(octet1)} / {ip_scope(octet1, octet2)}"
    binary_ip_var = to_dotted_format((f'{octet1:08b}', f'{octet2:08b}', f'{octet3:08b}', f'{octet4:08b}'))
    binary_mask_var = to_dotted_format((f'{from_u32(mask32)[0]:08b}', f'{from_u32(mask32)[1]:08b}', f'{from_u32(mask32)[2]:08b}', f'{from_u32(mask32)[3]:08b}'))
       
    print(f'''
Network         : {network_var}
Broadcast       : {broadcast_var}
First host      : {first_host_var}
Last host       : {last_host_var}
Total addresses : {total_address_var}
Usable hosts    : {usabel_host_var}
Netmask         : {netmask_var}
Wildcard        : {wildcard_var}
Class / Scope   : {class_scope_var}
Binary (IP)     : {binary_ip_var}
Binary (Mask)   : {binary_mask_var}
''')
else: print("Incorrect Format!")
