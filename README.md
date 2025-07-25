# IP2Location Python CSV Converter

This Python script converts IP2Location CSV data file, that contains the IP address in numeric notation, into dot-decimal notation (such as x.x.x.x) or CIDR notation (x.x.x.x/24). It supports both the IP2Location commercial edition, DB1 to DB26 database and also the free edition, IP2Location LITE database. In addition to this, this converter can also be used to convert any CSV file that contains the IP number (the numeric notation).

You can download the IP2Location CSV file at the below links:

- [IP2Location Commercial Database](https://www.ip2location.com/)
- [IP2Location LITE Database](https://lite.ip2location.com/)

Please do not use this script to convert IP2Location BIN data file. It only support the CSV format, not the binary format.

## Requirement

This script require *ipaddress* to work. For Python3 user, it is already been installed as part of Python3 standard library. For Python2 user, if you do not have the library installed, you can install the library by running the following command:

`pip install ipaddress`

For Windows user, please install this library *win_inet_pton* before using this script, you can install the library by running the following command:

`pip install win-inet-pton`

## Installation

You can install the script by using pip command:

`pip install ip2location-python-csv-converter`

For Arch Linux user, you can also install the script by using the following commands:

```bash
git clone https://aur.archlinux.org/ip2location-python-csv-converter.git && cd ip2location-python-csv-converter
makepkg -si
```

## Usage

```
ip2location-csv-converter [-range | -cidr | -hex | -parquet] [-replace | -append] [database_type] INPUT_FILE OUTPUT_FILE
```

#### Parameters

| Parameter | Description                                                  |
| --------- | ------------------------------------------------------------ |
| -range    | IP numbers will be converted into the first IP address and last IP address in the range. |
| -cidr     | IP numbers will be converted into CIDR format.               |
| -hex      | IP numbers will be converted into hexadecimal format. (auto padding)        |
| -hex4     | IP numbers will be converted into hexadecimal format. (pad IPv4)        |
| -hex6     | IP numbers will be converted into hexadecimal format. (pad IPv6)        |
| -parquet  | Convert IP2Location/IP2Proxy CSV file to a custom parquet file. |
| -replace  | The IP numbers in will be replaced to the selected format.   |
| -append   | The converted format will be appended after the IP numbers field. |

### Example:

##### Sample Input

```
"17170432","17301503","IN","India"
"17301504","17367039","CN","China"
"17367040","17432575","MY","Malaysia"
"17432576","17435135","CN","China"
"17435136","17435391","AU","Australia"
"17435392","17465343","CN","China"
"17465344","17498111","TH","Thailand"
"17498112","17563647","KR","Korea, Republic of"
"17563648","17825791","CN","China"
"17825792","17842175","KR","Korea, Republic of"
```

##### Convert into range with replace option:

Command:

```
ip2location-csv-converter -range -replace IP2LOCATION-DB1.CSV IP2LOCATION-DB1.NEW.CSV
```

Output:

```
"1.6.0.0","1.7.255.255","IN","India"
"1.8.0.0","1.8.255.255","CN","China"
"1.9.0.0","1.9.255.255","MY","Malaysia"
"1.10.0.0","1.10.9.255","CN","China"
"1.10.10.0","1.10.10.255","AU","Australia"
"1.10.11.0","1.10.127.255","CN","China"
"1.10.128.0","1.10.255.255","TH","Thailand"
"1.11.0.0","1.11.255.255","KR","Korea, Republic of"
"1.12.0.0","1.15.255.255","CN","China"
"1.16.0.0","1.16.63.255","KR","Korea, Republic of"
```

##### Convert into CIDR with replace option:

Command:

```
ip2location-csv-converter -cidr -replace IP2LOCATION-DB1.CSV IP2LOCATION-DB1.NEW.CSV
```

Output:

```
"1.6.0.0/15","IN","India"
"1.8.0.0/16","CN","China"
"1.9.0.0/16","MY","Malaysia"
"1.10.0.0/21","CN","China"
"1.10.8.0/23","CN","China"
"1.10.10.0/24","AU","Australia"
"1.10.11.0/24","CN","China"
"1.10.12.0/22","CN","China"
"1.10.16.0/20","CN","China"
"1.10.32.0/19","CN","China"
```

##### Convert into hexadecimal with replace option:

Command:

```
ip2location-csv-converter -hex -replace IP2LOCATION-DB1.CSV IP2LOCATION-DB1.NEW.CSV
```

Output:

```
"01060000","0107ffff","IN","India"
"01080000","0108ffff","CN","China"
"01090000","0109ffff","MY","Malaysia"
"010a0000","010a09ff","CN","China"
"010a0a00","010a0aff","AU","Australia"
"010a0b00","010a7fff","CN","China"
"010a8000","010affff","TH","Thailand"
"010b0000","010bffff","KR","Korea, Republic of"
"010c0000","010fffff","CN","China"
"01100000","01103fff","KR","Korea, Republic of"
```

##### Convert into range with append option:

Command:

```
ip2location-csv-converter -range -append IP2LOCATION-DB1.CSV IP2LOCATION-DB1.NEW.CSV
```

Output:

```
"17170432","17301503","1.6.0.0","1.7.255.255","IN","India"
"17301504","17367039","1.8.0.0","1.8.255.255","CN","China"
"17367040","17432575","1.9.0.0","1.9.255.255","MY","Malaysia"
"17432576","17435135","1.10.0.0","1.10.9.255","CN","China"
"17435136","17435391","1.10.10.0","1.10.10.255","AU","Australia"
"17435392","17465343","1.10.11.0","1.10.127.255","CN","China"
"17465344","17498111","1.10.128.0","1.10.255.255","TH","Thailand"
"17498112","17563647","1.11.0.0","1.11.255.255","KR","Korea, Republic of"
"17563648","17825791","1.12.0.0","1.15.255.255","CN","China"
"17825792","17842175","1.16.0.0","1.16.63.255","KR","Korea, Republic of"
```

##### Convert into CIDR with append option:

Command:

```
ip2location-csv-converter -cidr -append IP2LOCATION-DB1.CSV IP2LOCATION-DB1.NEW.CSV
```

Output:

```
"17170432","17301503","1.6.0.0/15","IN","India"
"17301504","17367039","1.8.0.0/16","CN","China"
"17367040","17432575","1.9.0.0/16","MY","Malaysia"
"17432576","17435135","1.10.0.0/21","CN","China"
"17432576","17435135","1.10.8.0/23","CN","China"
"17435136","17435391","1.10.10.0/24","AU","Australia"
"17435392","17465343","1.10.11.0/24","CN","China"
"17435392","17465343","1.10.12.0/22","CN","China"
"17435392","17465343","1.10.16.0/20","CN","China"
"17435392","17465343","1.10.32.0/19","CN","China"
"17435392","17465343","1.10.64.0/18","CN","China"
"17465344","17498111","1.10.128.0/17","TH","Thailand"
"17498112","17563647","1.11.0.0/16","KR","Korea, Republic of"
"17563648","17825791","1.12.0.0/14","CN","China"
"17825792","17842175","1.16.0.0/18","KR","Korea, Republic of"
```

##### Convert into hexadecimal with append option:

Command:

```
ip2location-csv-converter -hex -append IP2LOCATION-DB1.CSV IP2LOCATION-DB1.NEW.CSV
```

Output:

```
"01060000","0107ffff","17170432","17301503","IN","India"
"01080000","0108ffff","17301504","17367039","CN","China"
"01090000","0109ffff","17367040","17432575","MY","Malaysia"
"010a0000","010a09ff","17432576","17435135","CN","China"
"010a0a00","010a0aff","17435136","17435391","AU","Australia"
"010a0b00","010a7fff","17435392","17465343","CN","China"
"010a8000","010affff","17465344","17498111","TH","Thailand"
"010b0000","010bffff","17498112","17563647","KR","Korea, Republic of"
"010c0000","010fffff","17563648","17825791","CN","China"
"01100000","01103fff","17825792","17842175","KR","Korea, Republic of"
```

## Custom Input File

You can use this converter for a custom input file provided the input is in CSV format, with the first and second field contain the **ip from** and **ip to** information in numeric format.

## Parquet conversion

You can convert any IP2Location or IP2Proxy CSV file to a parquet file using this converter. The command will be:

```
ip2location-csv-converter -parquet <database_type> <input_csv_filename> <output_parquet_filename>
```

You can get the database type of the IP2Location or IP2Proxy CSV file from the below link:
- [https://www.ip2location.com/database/ip2location](https://www.ip2location.com/database/ip2location): Between DB1 to DB26.
- [https://www.ip2location.com/database/ip2proxy](https://www.ip2location.com/database/ip2proxy): Between PX1 to PX12.

For IPv6, due to the current limitation of the Decimal data type in parquet, the converter will encode the IPv6 number to hex string and stored as varchar. Hence, you will need to do some pre-conversion during the query time.

Below is one of the example demonstrate on the per-conversion of an IPv6 address before query:

```python
import ipaddress

# Example IPv6 address
ipv6_addr = "2001:db8::1"

# Convert to integer
ipv6_int = int(ipaddress.IPv6Address(ipv6_addr))

# Convert to zero-padded 32-character lowercase hex string
ipv6_hex = format(ipv6_int, "032x")

```

To query using the hex IPv6 address, the code can looks like this:

```python
import duckdb

result = duckdb.query(f"""
    SELECT * FROM '<ipv6_parquet_filename>'
    WHERE ipv6_hex = '{ipv6_hex}'
""").to_df()
```

## Support

URL: [https://www.ip2location.com](https://www.ip2location.com/)
