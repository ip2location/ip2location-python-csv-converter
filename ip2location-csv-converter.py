import os, sys, re, csv, socket, struct, ipaddress

def no2ip(iplong):
    return (socket.inet_ntoa(struct.pack('!I', int(iplong))))

conversion_mode = 'range'
write_mode = 'replace'

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
    if ((input_file.lower().endswith('.csv')) and (output_file.lower().endswith('.csv'))):
        print (input_file,'and',output_file,'is valid csv file.')
        if ((os.path.isfile(input_file))):
            print ("File exist!")
        else:
            print ("File doesn't exist! Please check again.")
            sys.exit(1)
    else:
        print ("Please enter valid CSV filename")
        sys.exit(1)
    regex1 = r"^\-(range|cidr)$"
    regex2 = r"^\-(replace|append)$"
    if (re.search(regex1, param1) != None):
        conversion_mode = re.findall(regex1, param1)[0]
    elif (re.search(regex2, param1) != None):
        write_mode = re.findall(regex2, param1)[0]
    if (re.search(regex1, param2) != None):
        conversion_mode = re.findall(regex1, param2)[0]
    elif (re.search(regex2, param2) != None):
        write_mode = re.findall(regex2, param2)[0]
    print (conversion_mode,write_mode)
    if (conversion_mode == 'range'):
        with open(input_file, 'r', encoding = 'utf-8') as f:
            mycsv = csv.reader(f)
            for row in mycsv:
                if ((re.search(r"^[0-9]+$", row[0]) == None) or (re.search(r"^[0-9]+$", row[0]) == None)):
                    continue
                from_ip = no2ip(row[0])
                to_ip = no2ip(row[1])
                print (from_ip, to_ip)
                total_row = len(row)
                remaining_columns = ''
                for i in range(2, total_row):
                    if (i == (total_row - 1)):
                        remaining_columns += row[i] + '"'
                    else:
                        remaining_columns += row[i] + '","'
                if (write_mode == 'replace'):
                    new_row = '""' + from_ip + '","' + to_ip + '","' + remaining_columns
                    print (new_row)
                elif (write_mode == 'append'):
                    new_row = '""' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns
                    print (new_row)
                new_file = open(output_file, 'a')
                new_file.write(new_row + '\n')
                new_file.close()
    elif (conversion_mode == 'cidr'):
        with open(input_file, 'r', encoding = 'utf-8') as f:
            mycsv = csv.reader(f)
            for row in mycsv:
                if ((re.search(r"^[0-9]+$", row[0]) == None) or (re.search(r"^[0-9]+$", row[0]) == None)):
                    continue
                from_ip = no2ip(row[0])
                to_ip = no2ip(row[1])
                print (from_ip, to_ip)
                total_row = len(row)
                startip = ipaddress.IPv4Address(from_ip)
                endip = ipaddress.IPv4Address(to_ip)
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
                    new_row = '""' + ar1[0] + '","' + remaining_columns
                    print (new_row)
                elif (write_mode == 'append'):
                    new_row = '""' + row[0] + '","' + row[1] + '","' + ar1[0] + '","' + remaining_columns
                    print (new_row)
                new_file = open(output_file, 'a')
                new_file.write(new_row + '\n')
                new_file.close()
else :
    print ("You must enter at least 2 parameters.")
    sys.exit(1)