#=============================== HELPERR ===============================
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

def to_u32(octet1, octet2, octet3, octet4):
    return octet1 << 24 | octet2 << 16 | octet3 << 8 | octet4
    
def from_u32(u32_integer):
    return (u32_integer >> 24) & 255, (u32_integer >> 16) & 255, (u32_integer >> 8) & 255, (u32_integer) & 255



#=============================== MAIN ===============================

def main():
    print('''
    ██╗██████╗░██╗░░░██╗░░██╗██╗░░░░░░░██╗░░░██╗████████╗██╗██╗░░░░░██╗████████╗██╗░░░██╗
    ██║██╔══██╗██║░░░██║░██╔╝██║░░░░░░░██║░░░██║╚══██╔══╝██║██║░░░░░██║╚══██╔══╝╚██╗░██╔╝
    ██║██████╔╝╚██╗░██╔╝██╔╝░██║░░░░░░░██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░╚████╔╝░
    ██║██╔═══╝░░╚████╔╝░███████║░░░░░░░██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░░╚██╔╝░░
    ██║██║░░░░░░░╚██╔╝░░╚════██║░░░░░░░╚██████╔╝░░░██║░░░██║███████╗██║░░░██║░░░░░░██║░░░
    ╚═╝╚═╝░░░░░░░░╚═╝░░░░░░░░╚═╝░░░░░░░░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═╝░░░╚═╝░░░░░░╚═╝░░░
    ''')
    print("FORMAT = <IP>/<PORT>")
    ip_mask = input("> ")


    ip, mask = split_ip_mask(ip_mask)
    if is_correct_format(ip, mask):
        octet1, octet2, octet3, octet4 = map(int, split_ip(ip))

    else: print("Incorrect Format!")

