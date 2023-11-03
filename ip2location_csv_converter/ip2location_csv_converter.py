import os, sys, re, csv, socket, struct, ipaddress, binascii
import time
from io import open

conversion_mode = 'range'
write_mode = 'replace'

chunk_size = 1000
# chunk_size = 10000

# Windows version of Python does not provide it
#          for compatibility with older versions of Windows.
if not hasattr(socket, 'inet_pton'):
    import win_inet_pton

def no2ip(iplong):
    if (int(iplong) > 4294967295):
        if sys.version < '3':
            return ipaddress.ip_address(long(iplong)).__str__()
        else:
            return ipaddress.ip_address(int(iplong)).__str__()
    else:
        return (socket.inet_ntoa(struct.pack('!I', int(iplong))))

def check_data_validity(file):
    with open(file, newline = "") as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(4096), delimiters = ",")
            return True
        except:
            return False

def range_number_to_ip(row, write_mode):
    from_ip = no2ip(row[0])
    to_ip = no2ip(row[1])
    # print (from_ip, to_ip)
    total_row = len(row)
    remaining_columns = ''
    for i in range(2, total_row):
        if (i == (total_row - 1)):
            remaining_columns += row[i] + '"'
        else:
            remaining_columns += row[i] + '","'
    if (write_mode == 'replace'):
        # new_row = '"' + from_ip + '","' + to_ip + '","' + remaining_columns
        if remaining_columns == '':
            new_row = '"' + from_ip + '","' + to_ip + '"'
        else:
            new_row = '"' + from_ip + '","' + to_ip + '","' + remaining_columns
        # print (new_row)
    elif (write_mode == 'append'):
        # new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns
        if remaining_columns == '':
            new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '"'
        else:
            new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns
    return new_row

def number_to_cidr(row, write_mode):
    from_ip = no2ip(row[0])
    to_ip = no2ip(row[1])
    # print (from_ip, to_ip)
    total_row = len(row)
    startip = ipaddress.ip_address(from_ip)
    endip = ipaddress.ip_address(to_ip)
    try:
        ar = [ipaddr for ipaddr in ipaddress.summarize_address_range(startip, endip)]
        ar1 = []
        for i in range(len(ar)):
            ar1.append(str(ar[i]))
        # print (ar1)
        remaining_columns = ''
        for i in range(2, total_row):
            if (i == (total_row - 1)):
                remaining_columns += row[i] + '"'
            else:
                remaining_columns += row[i] + '","'
        if (write_mode == 'replace'):
            if remaining_columns == '':
                new_row = '"' + ar1[0] + '"'
            else:
                new_row = '"' + ar1[0] + '","' + remaining_columns
            # print (new_row)
        elif (write_mode == 'append'):
            if remaining_columns == '':
                new_row = '"' + row[0] + '","' + row[1] + '","' + ar1[0] + '"'
            else:
                new_row = '"' + row[0] + '","' + row[1] + '","' + ar1[0] + '","' + remaining_columns
            # print (new_row)
    except:
        print ("Skipped invalid (range) data record")
    return new_row

def number_to_hex(row, write_mode):
    from_ip = no2ip(row[0])
    to_ip = no2ip(row[1])
    total_row = len(row)
    if (int(row[0]) > 4294967295):
        # from_hex = int(binascii.hexlify(socket.inet_pton(socket.AF_INET6, from_ip)), 16).upper()
        from_hex = binascii.hexlify(socket.inet_pton(socket.AF_INET6, from_ip)).upper()
        if (len(from_hex) < 16) :
            from_hex = from_hex.zfill(16-from_hex.len())
    else:
        # from_hex = int(binascii.hexlify(socket.inet_aton(from_ip)), 8).upper()
        from_hex = binascii.hexlify(socket.inet_aton(from_ip)).upper()
        if (len(from_hex) < 8) :
            from_hex = from_hex.zfill(8-from_hex.len())
    if (int(row[1]) > 4294967295):
        # to_hex = int(binascii.hexlify(socket.inet_pton(socket.AF_INET6, to_ip)), 16).upper()
        to_hex = binascii.hexlify(socket.inet_pton(socket.AF_INET6, to_ip)).upper()
        if (len(to_hex) < 16) :
            to_hex = to_hex.zfill(16-to_hex.len())
    else:
        # to_hex = int(binascii.hexlify(socket.inet_aton(to_ip)), 8).upper()
        to_hex = binascii.hexlify(socket.inet_aton(to_ip)).upper()
        if (len(to_hex) < 8) :
            to_hex = to_hex.zfill(8-to_hex.len())
    remaining_columns = ''
    for i in range(2, total_row):
        if (i == (total_row - 1)):
            remaining_columns += row[i] + '"'
        else:
            remaining_columns += row[i] + '","'
    if (write_mode == 'replace'):
        # new_row = '"' + from_ip + '","' + to_ip + '","' + remaining_columns
        if sys.version < '3':
            if remaining_columns == '':
                new_row = '"' + from_hex + '","' + to_hex + '"'
            else:
                new_row = '"' + from_hex + '","' + to_hex + '","' + remaining_columns
        else:
            if remaining_columns == '':
                new_row = '"' + str(from_hex.decode('utf-8')) + '","' + str(to_hex.decode('utf-8')) + '"'
            else:
                new_row = '"' + str(from_hex.decode('utf-8')) + '","' + str(to_hex.decode('utf-8')) + '","' + remaining_columns
        # print (new_row)
    elif (write_mode == 'append'):
        # new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns
        if sys.version < '3':
            if remaining_columns == '':
                new_row = '"' + row[0] + '","' + row[1] + '","' + from_hex + '","' + to_hex + '"'
            else:
                new_row = '"' + row[0] + '","' + row[1] + '","' + from_hex + '","' + to_hex + '","' + remaining_columns
        else:
            if remaining_columns == '':
                new_row = '"' + row[0] + '","' + row[1] + '","' + str(from_hex.decode('utf-8')) + '","' + str(to_hex.decode('utf-8')) + '"'
            else:
                new_row = '"' + row[0] + '","' + row[1] + '","' + str(from_hex.decode('utf-8')) + '","' + str(to_hex.decode('utf-8')) + '","' + remaining_columns
    return new_row

def convert_to_csv(input_file, output_file, conversion_mode, write_mode):
    with open(input_file, 'r', encoding = 'utf-8') as f:
        mycsv = csv.reader(f)

        # Read and process the CSV file in chunks
        while True:
            chunk = []
            my_list = []
            for _ in range(chunk_size):
                try:
                    row = next(mycsv)
                    chunk.append(row)
                except StopIteration:
                    break
            
            for row in chunk:
                if ((re.search(r"^[0-9]+$", row[0]) == None) or (re.search(r"^[0-9]+$", row[0]) == None)):
                    continue
                if (conversion_mode == 'range'):
                    new_row = range_number_to_ip(row, write_mode)
                elif (conversion_mode == 'cidr'):
                    new_row = number_to_cidr(row, write_mode)
                elif (conversion_mode == 'hex'):
                    new_row = number_to_hex(row, write_mode)
                if sys.version < '3':
                    my_list.append(new_row.decode('utf-8'))
                else:
                    my_list.append(new_row)

            if (len(my_list) > 0):
                with open(output_file, 'a') as myWrite:
                    myWrite.writelines("{}\n".format(x) for x in my_list)

            my_list = []

            # Stop the loop if there are no more rows
            if not chunk:
                break
