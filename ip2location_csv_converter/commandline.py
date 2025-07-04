import os, re, sys, time
from ip2location_csv_converter.ip2location_csv_converter import convert_to_csv, check_data_validity, csv_to_parquet

regex1 = r"^\-(range|cidr|hex)$"
regex2 = r"^\-(replace|append)$"
regex3 = r"^\-(help)$"

def print_usage():
    print(
"Usage: ip2location-csv-converter [-range | -cidr | -hex | -parquet] [-replace | -append] [database_type] INPUT_FILE OUTPUT_FILE\n"
"\n"
"  -range\n"
"  IP numbers will be converted into the first IP address and last IP address in the range.\n"
"\n"
"  -cidr\n"
"  IP numbers will be converted into CIDR format.\n"
"\n"
"  -hex\n"
"  IP numbers will be converted into hexadecimal format. (auto padding)\n"
"\n"
"  -hex4\n"
"  IP numbers will be converted into hexadecimal format. (pad IPv4)\n"
"\n"
"  -hex6\n"
"  IP numbers will be converted into hexadecimal format. (pad IPv6)\n"
"\n"
"  -replace\n"
"  The IP numbers in will be replaced to the selected format.\n"
"\n"
"  -parquet\n"
"  Convert a IP2Location/IP2Proxy CSV to a parquet file.\n"
"\n"
"  -help\n"
"  Display this guide.\n"
    )

def main():
    param1 = ''
    param2 = ''
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
        
        conversion_mode = 'range'
        write_mode = 'replace'
        
        if (re.search(regex1, input_file) != None):
            print (f"Invalid input {input_file} detected for input filename. Please check again.")
            sys.exit(1)
        if (re.search(regex2, input_file) != None):
            print (f"Invalid input {input_file} detected for input filename. Please check again.")
            sys.exit(1)
        
        if (re.search(regex1, output_file) != None):
            print (f"Invalid input {output_file} detected for input filename. Please check again.")
            sys.exit(1)
        if (re.search(regex2, output_file) != None):
            print (f"Invalid input {output_file} detected for input filename. Please check again.")
            sys.exit(1)
        
        if ((os.path.isfile(input_file)) is False):
            print ("File doesn't exist! Please check again.")
            sys.exit(1)
        else:
            if (check_data_validity(input_file)  is False):
                print ("Please make sure the columns had comma as separator.")
                sys.exit(1)
        
        if param1 == '-parquet':
            if param2 == '':
                print ("Please provide the database type of the CSV file.")
                sys.exit(1)
            elif (re.search(regex2, param2) != None):
                print ("Please provide the database type of the CSV file.")
                sys.exit(1)
            print(f'Converting {input_file} to {output_file} now...')
            csv_to_parquet(input_file, output_file, param2)
            print(f'Conversion done.')
        else:
            if (re.search(regex1, param1) != None):
                conversion_mode = re.findall(regex1, param1)[0]
            elif (re.search(regex2, param1) != None):
                write_mode = re.findall(regex2, param1)[0]
            if (re.search(regex1, param2) != None):
                conversion_mode = re.findall(regex1, param2)[0]
            elif (re.search(regex2, param2) != None):
                write_mode = re.findall(regex2, param2)[0]
            convert_to_csv(input_file, output_file, conversion_mode, write_mode)

    elif ((len(sys.argv) == 2) and (re.search(regex3, sys.argv[1]) != None)):
        print_usage()

    else :
        print ("You must enter at least 2 parameters.")
        print ("Run \"ip2location-csv-converter -help\" to learn on the available parameters.")
        sys.exit(1)