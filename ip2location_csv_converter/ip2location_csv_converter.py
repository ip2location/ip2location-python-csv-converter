import os, sys, re, csv, socket, struct, ipaddress, binascii
import time
from io import open, StringIO
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from decimal import Decimal


conversion_mode = 'range'
write_mode = 'replace'

chunk_size = 1000
# chunk_size = 10000

def no2ip(iplong):
    try:
        if (int(iplong) > 4294967295):
            if sys.version < '3':
                return ipaddress.ip_address(long(iplong)).__str__()
            else:
                return ipaddress.ip_address(int(iplong)).__str__()
        else:
            return (socket.inet_ntoa(struct.pack('!I', int(iplong))))
    except ValueError:
        print(f'Invalid IP number value {iplong} detected. Please fix it before continue.')
        sys.exit(1)

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
    print (from_ip, to_ip)
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
            new_row = '"' + from_ip + '","' + to_ip + "\"\n"
        else:
            new_row = '"' + from_ip + '","' + to_ip + '","' + remaining_columns + "\n"
        # print (new_row)
    elif (write_mode == 'append'):
        # new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns
        if remaining_columns == '':
            new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + "\"\n"
        else:
            new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns + "\n"
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
        new_row = ''
        for j in range(len(ar1)):
            if (write_mode == 'replace'):
                if remaining_columns == '':
                    new_row += '"' + ar1[j] + "\"\n"
                else:
                    new_row += '"' + ar1[j] + '","' + remaining_columns + "\n"
                # print (new_row)
            elif (write_mode == 'append'):
                if remaining_columns == '':
                    new_row += '"' + row[0] + '","' + row[1] + '","' + ar1[j] + "\"\n"
                else:
                    new_row += '"' + row[0] + '","' + row[1] + '","' + ar1[j] + '","' + remaining_columns + "\n"
                # print (new_row)
    except:
        print ("Skipped invalid (range) data record")
    return new_row

def number_to_hex(row, write_mode, conversion_mode):
    total_row = len(row)

    if (conversion_mode == 'hex6'):
        from_hex = hex(int(row[0]))[2:].zfill(32)
        to_hex = hex(int(row[1]))[2:].zfill(32)
    elif ((conversion_mode == 'hex4') or (conversion_mode == 'hex')):
        from_hex = hex(int(row[0]))[2:].zfill(16)
        to_hex = hex(int(row[1]))[2:].zfill(16)
    # else:
    if (row[0] == 4294967295) :
        from_hex = hex(int(row[0]))[2:].zfill(32)
    if (row[1] == 4294967295) :
        to_hex = hex(int(row[1]))[2:].zfill(32)
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
                new_row = '"' + from_hex + '","' + to_hex + '","' + remaining_columns + "\n"
        else:
            if remaining_columns == '':
                new_row = '"' + str(from_hex) + '","' + str(to_hex) + "\"\n"
            else:
                new_row = '"' + str(from_hex) + '","' + str(to_hex) + '","' + remaining_columns + "\n"
        # print (new_row)
    elif (write_mode == 'append'):
        # new_row = '"' + row[0] + '","' + row[1] + '","' + from_ip + '","' + to_ip + '","' + remaining_columns
        if sys.version < '3':
            if remaining_columns == '':
                new_row = '"' + row[0] + '","' + row[1] + '","' + from_hex + '","' + to_hex + "\"\n"
            else:
                new_row = '"' + row[0] + '","' + row[1] + '","' + from_hex + '","' + to_hex + '","' + remaining_columns + "\n"
        else:
            if remaining_columns == '':
                new_row = '"' + row[0] + '","' + row[1] + '","' + str(from_hex) + '","' + str(to_hex) + "\"\n"
            else:
                new_row = '"' + row[0] + '","' + row[1] + '","' + str(from_hex) + '","' + str(to_hex) + '","' + remaining_columns + "\n"
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
                elif ((conversion_mode == 'hex') or (conversion_mode == 'hex4') or (conversion_mode == 'hex6')):
                    new_row = number_to_hex(row, write_mode, conversion_mode)
                if sys.version < '3':
                    my_list.append(new_row.decode('utf-8'))
                else:
                    # detect_eol(new_row)
                    # print(repr(new_row))
                    my_list.append(new_row)

            if (len(my_list) > 0):
                with open(output_file, 'a', newline='\r\n') as myWrite:
                    myWrite.write(''.join(my_list))

            my_list = []

            # Stop the loop if there are no more rows
            if not chunk:
                break

def get_last_row(file_path):
    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Move to the second-last byte
        while f.read(1) != b'\n':
            f.seek(-2, 1)
        last_line = f.readline().decode()
    return last_line

def detect_ip_version_from_number(ip_num):
    try:
        ip = ipaddress.ip_address(int(ip_num))
        return 'IPv4' if ip.version == 4 else 'IPv6'
    except ValueError:
        return 'Invalid'

def detect_versions_from_chunk(chunk):
    versions = set()

    # Combine both start and end IP columns (col 0 and col 1)
    all_ips = pd.concat([chunk.iloc[:, 0], chunk.iloc[:, 1]], ignore_index=True)

    for ip_num in all_ips:
        try:
            version = ipaddress.ip_address(int(ip_num)).version
            versions.add(version)
            if len(versions) > 1:
                break  # early stop if we detect both v4 and v6
        except ValueError:
            continue  # skip invalid numbers

    return versions

# Scan the file in chunks
def check_ip_versions(csv_path):
    seen_versions = set()
    for chunk in pd.read_csv(csv_path, chunksize=50_000, header=None, usecols=[0, 1]):
        seen_versions.update(detect_versions_from_chunk(chunk))
        if len(seen_versions) > 1:
            break  # early exit if both found

    if seen_versions == {4, 6}:
        print(f'Your csv file {csv_path} contains mixture of IPv4 and IPv6 addresses, which will causing issue when converting to parquet file.')
        print(f'It is advisable to separate IPv4 and IPv6 addresses into two identical csv file.')
        sys.exit(1)

# Convert CSV to Parquet
def csv_to_parquet(input_file, output_file, db_type):
    column_names = ''
    csv_file = input_file
    parquet_file = output_file
    parquet_chunksize = 50_000
    parquet_writer = None
    
    # Need to determine the column names
    column_names_list = {
        'DB1': ["ip_from", "ip_to", "country_code", "country_name"],
        'DB2': ["ip_from", "ip_to", "country_code", "country_name", "isp"],
        'DB3': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name"],
        'DB4': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "isp"],
        'DB5': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude"],
        'DB6': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "isp"],
        'DB7': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "isp", "domain"],
        'DB8': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "isp", "domain"],
        'DB9': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code"],
        'DB10': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "isp", "domain"],
        'DB11': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone"],
        'DB12': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain"],
        'DB13': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "time_zone", "net_speed"],
        'DB14': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "time_zone", "net_speed"],
        'DB15': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "idd_code", "area_code"],
        'DB16': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "time_zone", "net_speed", "idd_code", "area_code"],
        'DB17': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "time_zone", "net_speed", "weather_station_code", "weather_station_name"],
        'DB18': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "time_zone", "net_speed", "idd_code", "area_code", "weather_station_code", "weather_station_name"],
        'DB19': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "isp", "domain", "mcc", "mnc", "mobile_brand"],
        'DB20': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "time_zone", "net_speed", "idd_code", "area_code", "weather_station_code", "weather_station_name", "mcc", "mnc", "mobile_brand"],
        'DB21': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "idd_code", "area_code", "elevation"],
        'DB22': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "time_zone", "net_speed", "idd_code", "area_code", "weather_station_code", "weather_station_name", "mcc", "mnc", "mobile_brand", "elevation"],
        'DB23': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "isp", "domain", "mcc", "mnc", "mobile_brand", "usage_type"],
        'DB24': ["ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "time_zone", "net_speed", "idd_code", "area_code", "weather_station_code", "weather_station_name", "mcc", "mnc", "mobile_brand", "elevation", "usage_type"],
        'DB25': [
                "ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name",
                "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "net_speed",
                "idd_code", "area_code", "weather_station_code", "weather_station_name",
                "mcc", "mnc", "mobile_brand", "elevation", "usage_type", "address_type",
                "category"
                ],
        'DB26': [
                "ip_from", "ip_to", "country_code", "country_name", "region_name", "city_name",
                "latitude", "longitude", "zip_code", "time_zone", "isp", "domain", "net_speed",
                "idd_code", "area_code", "weather_station_code", "weather_station_name",
                "mcc", "mnc", "mobile_brand", "elevation", "usage_type", "address_type",
                "category", "district", "asn", "as_name"
                ],
        'PX1': ['ip_from', 'ip_to', 'country_code', 'country_name'],
        'PX2': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name'],
        'PX3': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name'],
        'PX4': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp'],
        'PX5': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain'],
        'PX6': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type'],
        'PX7': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type', 'asn', 'as'],
        'PX8': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type', 'asn', 'as', 'last_seen'],
        'PX9': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type', 'asn', 'as', 'last_seen', 'threat'],
        'PX10': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type', 'asn', 'as', 'last_seen', 'threat'],
        'PX11': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type', 'asn', 'as', 'last_seen', 'threat', 'provider'],
        'PX12': ['ip_from', 'ip_to', 'proxy_type', 'country_code', 'country_name', 'region_name', 'city_name', 'isp', 'domain', 'usage_type', 'asn', 'as', 'last_seen', 'threat', 'provider', 'fraud_score']
    }
    if db_type != '':
        try:
            column_names = column_names_list[db_type]
        except Exception:
            print(f'Invalid db_type value foundm the valid value should be range from DB1 to DB26. Your input: {db_type}.')
            sys.exit(1)
    
    # check_ip_versions(csv_file)
    
    # Determine ipv4 or ipv6 based on the last row of the file
    # Get last line
    last_line = get_last_row(csv_file)
    
    df_last = pd.read_csv(StringIO(last_line), header=None)
    
    # Check the number of column against the header row
    if len(column_names) != df_last.shape[1]:
        print(f"Column numbers not matching, aborting now...")
        sys.exit(1)
    
    ip_value = df_last.iloc[0, 0]  # Replace with actual index
    ip_ver = detect_ip_version_from_number(ip_value)

    if column_names != '':
        try:
            schema_list = []
            for column in column_names:
                if column in ["ip_from", "ip_to"]:
                    if ip_ver == 'IPv4':
                        schema_list.append(pa.field(column, pa.uint32()))
                    elif ip_ver == 'IPv6':
                        schema_list.append(pa.field(column, pa.string()))
                elif column in ["latitude", "longitude"]:
                    schema_list.append(pa.field(column, pa.float64()))
                elif column in ['last_seen', 'fraud_score', "elevation"]:
                    schema_list.append(pa.field(column, pa.int32()))
                else:
                    schema_list.append(pa.field(column, pa.string()))
            schema = pa.schema(schema_list)
            for chunk in pd.read_csv(
                csv_file,
                names=column_names,
                header=None,
                chunksize=parquet_chunksize,
                low_memory=True,
                dtype=str  # initially read all as string to control parsing
            ):
                if ip_ver == 'IPv4':
                    chunk["ip_from"] = pd.to_numeric(chunk["ip_from"], errors="coerce").astype("uint32")
                    chunk["ip_to"] = pd.to_numeric(chunk["ip_to"], errors="coerce").astype("uint32")
                elif ip_ver == 'IPv6':
                    chunk["ip_from"] = chunk["ip_from"].apply(int)
                    chunk["ip_from"] = chunk["ip_from"].apply(lambda x: format(x, '032x'))
                    chunk["ip_to"] = chunk["ip_to"].apply(int)
                    chunk["ip_to"] = chunk["ip_to"].apply(lambda x: format(x, '032x'))
                if "latitude" in column_names:
                    chunk["latitude"] = pd.to_numeric(chunk["latitude"], errors="coerce").astype("float64")
                if "longitude" in column_names:
                    chunk["longitude"] = pd.to_numeric(chunk["longitude"], errors="coerce").astype("float64")
                if "elevation" in column_names:
                    chunk["elevation"] = pd.to_numeric(chunk["elevation"], errors="coerce")

                table = pa.Table.from_pandas(chunk, schema=schema, preserve_index=False)

                if parquet_writer is None:
                    parquet_writer = pq.ParquetWriter(parquet_file, table.schema)

                parquet_writer.write_table(table)

            if parquet_writer:
                parquet_writer.close()
        except Exception as e:
            print(f'Unexcepted error occured, will abort now...')
            print(str(e))
            sys.exit(1)

