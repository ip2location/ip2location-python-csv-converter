import os, sys, re, csv, socket, struct, ipaddress, binascii
import time
from io import open

# if sys.version < '3':
    # def u(x):
        # return x.decode('utf-8')
    # def b(x):
        # return str(x)
# else:
    # def u(x):
        # if isinstance(x, bytes):
            # return x.decode()
        # return x
    # def b(x):
        # if isinstance(x, bytes):
            # return x
        # return x.encode('ascii')

# Windows version of Python does not provide it
#          for compatibility with older versions of Windows.
if not hasattr(socket, 'inet_pton'):
    import win_inet_pton

# def writetofile(filename, row):
    # new_file = open(filename, 'a')
    # if sys.version < '3':
        # new_file.write(new_row.decode('utf-8') + '\n')
    # else:
        # new_file.write(new_row + '\n')
    # new_file.close()

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

conversion_mode = 'range'
write_mode = 'replace'

chunk_size = 1000

# startTime = time.time()

if (len(sys.argv) > 2):
    # print (sys.argv)
    if (len(sys.argv) == 3):
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif (len(sys.argv) == 4):
        param1 = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    elif (len(sys.argv) == 5):
        param1 = sys.argv[1]
        param2 = sys.argv[2]
        input_file = sys.argv[3]
        output_file = sys.argv[4]
    
    if ((os.path.isfile(input_file)) is False):
        print ("File doesn't exist! Please check again.")
        sys.exit(1)
    else:
        if (check_data_validity(input_file)  is False):
            print ("Please make sure the columns had comma as separator.")
            sys.exit(1)
    regex1 = r"^\-(range|cidr|hex)$"
    regex2 = r"^\-(replace|append)$"
    if (re.search(regex1, param1) != None):
        conversion_mode = re.findall(regex1, param1)[0]
    elif (re.search(regex2, param1) != None):
        write_mode = re.findall(regex2, param1)[0]
    if (re.search(regex1, param2) != None):
        conversion_mode = re.findall(regex1, param2)[0]
    elif (re.search(regex2, param2) != None):
        write_mode = re.findall(regex2, param2)[0]
    # print (conversion_mode,write_mode)
    if (conversion_mode == 'range'):
        # my_list = []
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

                # Process the current chunk of data (e.g., print it)
                for row in chunk:
                    # print(row)
                    if ((re.search(r"^[0-9]+$", row[0]) == None) or (re.search(r"^[0-9]+$", row[0]) == None)):
                        continue
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
                        # print (new_row)

                    if sys.version < '3':
                        my_list.append(new_row.decode('utf-8'))
                    else:
                        my_list.append(new_row)
                
                # print(len(chunk))
                
                # sys.exit()
                
                with open(output_file, 'a') as myWrite:
                    myWrite.writelines("{}\n".format(x) for x in my_list)

                my_list = []

                # Stop the loop if there are no more rows
                if not chunk:
                    break
    
    elif (conversion_mode == 'cidr'):
        # my_list = []
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

                # Process the current chunk of data (e.g., print it)
                for row in chunk:
                    if ((re.search(r"^[0-9]+$", row[0]) == None) or (re.search(r"^[0-9]+$", row[0]) == None)):
                        continue
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
                        if sys.version < '3':
                            my_list.append(new_row.decode('utf-8'))
                        else:
                            my_list.append(new_row)
                    except:
                        print ("Skipped invalid (range) data record")
                
                with open(output_file, 'a') as myWrite:
                    myWrite.writelines("{}\n".format(x) for x in my_list)

                my_list = []

                # Stop the loop if there are no more rows
                if not chunk:
                    break

    elif (conversion_mode == 'hex'):
        my_list = []
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

                # Process the current chunk of data (e.g., print it)
                for row in chunk:
                    if ((re.search(r"^[0-9]+$", row[0]) == None) or (re.search(r"^[0-9]+$", row[0]) == None)):
                        continue
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
                        # print (new_row)
                    if sys.version < '3':
                        my_list.append(new_row.decode('utf-8'))
                    else:
                        my_list.append(new_row)
                
                with open(output_file, 'a') as myWrite:
                    myWrite.writelines("{}\n".format(x) for x in my_list)

                my_list = []

                # Stop the loop if there are no more rows
                if not chunk:
                    break

else :
    print ("You must enter at least 2 parameters.")
    sys.exit(1)

# print ('The script took {0} second !'.format(time.time() - startTime))