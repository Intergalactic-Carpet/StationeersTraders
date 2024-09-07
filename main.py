from xmltodict import parse
from zlib import crc32

with open(r"C:\Program Files (x86)\Steam\steamapps\common\Stationeers\rocketstation_Data\StreamingAssets\Data\tradeables.xml", 'r') as file:
    data = file.read()


def crc(s):
    hash_ = crc32(bytes(s, "UTF-8"))
    return (hash_ ^ 0x80000000) - 0x80000000


def print_rgb(text_, r, g, b):
    color_code = f"\033[38;2;{round(r)};{round(g)};{round(b)}m"
    print(f"{color_code}{text_}\033[0m")


def warn(text_):
    print_rgb(text_, 255, 255, 0)


def get_comparison(comparison):
    comp = {
        'EqualOrGreater': '>=',
        'Equal': '',
        'Less': '<',
        'LessThan': '<',
        'Greater': '>',
        'GreaterThan': '>',
        'EqualOrLess': '<=',
    }
    if comparison in comp:
        return comp[comparison]
    warn(f"Comparison '{comparison}' unsupported")
    return comparison + ' to '


xml_dict = parse(data)
traders = xml_dict['GameData']['Trader']

temp_units = {'Celsius': 'c', 'Kelvin': 'K'}

multi_items = {}
for item in xml_dict['GameData']['Buy']:
    text = str(item['@Id'])
    if 'Name' in item:
        text = str(item['Name']['@Value'])
    if 'Required' in item:
        if '@Value' in item['Required']:
            text = text + f", Quantity: {item['Required']['@Value']}"
        else:
            text = text + f", Quantity: {item['Required']['@Min']}-{item['Required']['@Max']}"
        if '@Bulk' in item['Required']:
            text = text + f" (Bulk)"
    if 'Item' in item:
        if 'Item' in item['Item']:
            text = text + ", Contains: '"
            if type(item['Item']['Item']) is list:
                for thing in item['Item']['Item']:
                    text = text + f"{thing['@Id']}, "
                text = text[:-2]
            else:
                text = text + item['Item']['Item']['@Id']
            text = text + "'"
    elif 'Gas' in item:
        if 'Moles' in item:
            text = text + f", {item['Moles']['@Value']} Moles"
        text = text + ", Consists of: '"
        if type(item['Gas']) is list:
            for gas in item['Gas']:
                text = text + f"{get_comparison(gas['@Compare'])}{gas['@Percent']}% {gas['@Type']}, "
            text = text[:-2] + "'"
        else:
            text = text + f"{get_comparison(item['Gas']['@Compare'])}{item['Gas']['@Percent']}% {item['Gas']['@Type']}'"
        if 'TemperatureRange' in item:
            text = text + f", {item['TemperatureRange']['@Min']}-{item['TemperatureRange']['@Max']}"
            text = text + f"{temp_units[item['TemperatureRange']['@Unit']]}"
    if '@Value' in item:
        text = text + f", ${item['@Value']}"
    multi_items[item['@Id']] = text

if type(xml_dict['GameData']['Sell']) is list:
    for item in xml_dict['GameData']['Sell']:

        text = str(item['@Id'])
        if 'Name' in item:
            text = str(item['Name']['@Value'])
        if 'Required' in item:
            if '@Value' in item['Required']:
                text = text + f", Quantity: {item['Required']['@Value']}"
            else:
                text = text + f", Quantity: {item['Required']['@Min']}-{item['Required']['@Max']}"
            if '@Bulk' in item['Required']:
                text = text + f" (Bulk)"
        if 'Item' in item:
            if 'Item' in item['Item']:
                text = text + ", Contains: '"
                if type(item['Item']['Item']) is list:
                    for thing in item['Item']['Item']:
                        text = text + f"{thing['@Id']}, "
                    text = text[:-2]
                else:
                    text = text + item['Item']['Item']['@Id']
                text = text + "'"
        elif 'Gas' in item:
            if 'Moles' in item:
                text = text + f", {item['Moles']['@Value']} Moles"
            text = text + ", Consists of: '"
            if type(item['Gas']) is list:
                for gas in item['Gas']:
                    text = text + f"{get_comparison(gas['@Compare'])}{gas['@Percent']}% {gas['@Type']}, "
                text = text[:-2] + "'"
            else:
                text = text + f"{get_comparison(item['Gas']['@Compare'])}{item['Gas']['@Percent']}% {item['Gas']['@Type']}'"
            if 'TemperatureRange' in item:
                text = text + f", {item['TemperatureRange']['@Min']}-{item['TemperatureRange']['@Max']}"
                text = text + f"{temp_units[item['TemperatureRange']['@Unit']]}"
        if '@Value' in item:
            text = text + f", ${item['@Value']}"
        multi_items[item['@Id']] = text
else:
    item = xml_dict['GameData']['Sell']
    text = str(item['@Id'])
    if 'Name' in item:
        text = str(item['Name']['@Value'])
    if 'Stock' in item:
        if '@Value' in item['Stock']:
            text = text + f", Quantity: {item['Stock']['@Value']}"
        else:
            text = text + f", Quantity: {item['Stock']['@Min']}-{item['Stock']['@Max']}"
        if '@Bulk' in item['Stock']:
            text = text + f" (Bulk)"
    if 'Item' in item:
        if 'Item' in item['Item']:
            text = text + ", Contains: '"
            if type(item['Item']['Item']) is list:
                for thing in item['Item']['Item']:
                    text = text + f"{thing['@Id']}, "
                text = text[:-2]
            else:
                text = text + item['Item']['Item']['@Id']
            text = text + "'"
        else:
            text = text + f", Consists of: {item['Item']['Quantity']['@Value']} x {item['Item']['@Id']}"
    elif 'Gas' in item:
        if 'Moles' in item:
            text = text + f", {item['Moles']['@Value']} Moles"
        text = text + ", Consists of: '"
        if type(item['Gas']) is list:
            for gas in item['Gas']:
                text = text + f"{get_comparison(gas['@Compare'])}{gas['@Percent']}% {gas['@Type']}, "
            text = text[:-2] + "'"
        else:
            text = text + f"{get_comparison(item['Gas']['@Compare'])}{item['Gas']['@Percent']}% {item['Gas']['@Type']}'"
        if 'TemperatureRange' in item:
            text = text + f", {item['TemperatureRange']['@Min']}-{item['TemperatureRange']['@Max']}"
            text = text + f"{temp_units[item['TemperatureRange']['@Unit']]}"
    if '@Value' in item:
        text = text + f", ${item['@Value']}"

    multi_items[item['@Id']] = text


for trader in traders:
    print()
    print(f'{trader["@Id"]}: {crc(trader["@Id"])}')

    print(f"{' ' * 2}Companies:")
    if type(trader['Name']) is list:
        for company in trader['Name']:
            print(f"{' ' * 4}{company['@Value']}")
    else:
        print(f"{' ' * 4}{trader['Name']['@Value']}")

    print(f"{' '*2}Buying:")
    for goods in trader['Buy']:
        text = goods
        if list(goods.keys()) == ['@Id']:
            text = goods['@Id']
            if text in multi_items:
                text = multi_items[text]
            else:
                warn(f"No definition for reference '{text}'")
        elif 'Gas' in goods:
            text = goods["Name"]['@Value']
            if '@Min' in goods['Required'] and '@Max' in goods['Required']:
                if goods['Required']['@Min'] == goods['Required']['@Max']:
                    text = text + f", Quantity: {goods['Required']['@Min']}"
                else:
                    text = text + f", Quantity: {goods['Required']['@Min']}-{goods['Required']['@Max']}"
                if '@Bulk' in goods['Required']:
                    text = text + ' (Bulk)'
            text = text + f", Moles: {goods['Moles']['@Value']}, Consists of: '"
            if type(goods['Gas']) is list:
                for gas in goods['Gas']:
                    text = text + f"{get_comparison(gas['@Compare'])}{gas['@Percent']}% {gas['@Type']}, "
                text = text[:-2] + "'"
            else:
                text = text + f"{get_comparison(goods['Gas']['@Compare'])}{goods['Gas']['@Percent']}% {goods['Gas']['@Type']}'"
            if '@Tier' in goods:
                text = text + f", Range: {goods['@Tier']}"
        elif 'Select' in goods:
            text = "Cardboard Box/Package consisting of: '"
            for item in goods['Select']['Item']:
                text = text + f"{item['@Id']}, "
            text = text[:-2] + "'"
            if '@Tier' in goods:
                text = text + f", Range: {goods['@Tier']}"
        else:
            text = str(goods['Item']['@Id'])
            if '@DebugID' in goods:
                text = str(goods['@DebugID'])
            if '@Min' in goods['Required'] and '@Max' in goods['Required']:
                if goods['Required']['@Min'] == goods['Required']['@Max']:
                    text = text + f", Quantity: {goods['Required']['@Min']}"
                else:
                    text = text + f", Quantity: {goods['Required']['@Min']}-{goods['Required']['@Max']}"
                if '@Bulk' in goods['Required']:
                    text = text + ' (Bulk)'
            if '@Tier' in goods:
                text = text + f", Range: {goods['@Tier']}"
        if '@Value' in goods:
            text = text + f", ${goods['@Value']}"
        print(f"{' '*4}{text}")

    print(f"{' ' * 2}Selling:")
    for goods in trader['Sell']:
        text = goods
        if list(goods.keys()) == ['@Id']:
            text = goods['@Id']
        elif 'Gas' in goods:
            text = goods["Name"]['@Value']
            if '@Min' in goods['Stock'] and '@Max' in goods['Stock']:
                if goods['Stock']['@Min'] == goods['Stock']['@Max']:
                    text = text + f", Quantity: {goods['Stock']['@Min']}"
                else:
                    text = text + f", Quantity: {goods['Stock']['@Min']}-{goods['Stock']['@Max']}"
                if '@Bulk' in goods['Stock']:
                    text = text + ' (Bulk)'
            text = text + f", Consists of: '"
            if type(goods['Gas']) is list:
                for gas in goods['Gas']:
                    if '@Moles' in gas:
                        text = text + f"{gas['@Moles']} moles of {gas['@Type']} at {gas['@Celsius']}c, "
                    elif '@Litres' in gas:
                        text = text + f"{gas['@Litres']}L of {gas['@Type']} at {gas['@Celsius']}c, "
                    else:
                        text = text + f"{gas['@Type']} at {gas['@Celsius']}c, "
                        warn('Unknown gas unit')
                text = text[:-2] + "'"
            else:
                if '@Moles' in goods['Gas']:
                    text = text + f"{goods['Gas']['@Moles']} moles of {goods['Gas']['@Type']} at {goods['Gas']['@Celsius']}c'"
                elif '@Litres' in goods['Gas']:
                    text = text + f"{goods['Gas']['@Litres']}L of {goods['Gas']['@Type']} at {goods['Gas']['@Celsius']}c'"
                else:
                    text = text + f"{goods['Gas']['@Type']} at {goods['Gas']['@Celsius']}c, "
                    warn('Unknown gas unit')
            if '@Tier' in goods:
                text = text + f", Range: {goods['@Tier']}"
        elif 'Select' in goods:
            text = "Cardboard Box/Package consisting of: '"
            for item in goods['Select']['Item']:
                text = text + f"{item['@Id']}, "
            text = text[:-2] + "'"
            if '@Tier' in goods:
                text = text + f", Range: {goods['@Tier']}"
        else:
            text = str(goods['Item']['@Id'])
            if '@DebugID' in goods:
                text = str(goods['@DebugID'])
            if '@DebugId' in goods:
                text = str(goods['@DebugId'])
            if '@Min' in goods['Stock'] and '@Max' in goods['Stock']:
                if goods['Stock']['@Min'] == goods['Stock']['@Max']:
                    text = text + f", Quantity: {goods['Stock']['@Min']}"
                else:
                    text = text + f", Quantity: {goods['Stock']['@Min']}-{goods['Stock']['@Max']}"
                if '@Bulk' in goods['Stock']:
                    text = text + ' (Bulk)'
            if '@Tier' in goods:
                text = text + f", Range: {goods['@Tier']}"
        if '@Value' in goods:
            text = text + f", ${goods['@Value']}"
        print(f"{' ' * 4}{text}")
