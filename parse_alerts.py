from xml.dom.minidom import parseString
from datetime import datetime
import os

def get_event_type(input):
    match input:
        case "tornado":
            return ".TO"
        case "thunderstorm":
            return ".SV"
        case "snow squall":
            return ".SQ"
        case "spcl marine":
            return ".MA"
        case "flash flood":
            return ".FF"
        case "wind":
            return ".EW"
        case "air quality":
            return ".AS"
        case "fog":
            return ".MF"
        case "squall":
            return ".WI"
        case "waterspout":
            return ".LW"
        case "freeze rain":
            return ".FZ"
        case "rainfall":
            return ".FA"
        case "cold":
            return ".EC"
        case "frost":
            return ".EC"
        case "heat":
            return ".EH"

def format_lat_long(input):
    output = "LAT...LON "
    for pair in input.split(" "):
        for coord in pair.split(","):
            parsed = round(float(coord), 2)
            parsed = str(parsed).replace("-", "").split(".")
            if len(parsed[1]) == 1:
                parsed[1] += "0"
            output += parsed[0] + parsed[1] + " "
    return output

def parse_cap_file(input):
    parsed_info = []

    document = parseString(input)
    parsed_info.append(document.getElementsByTagName("source")[0].firstChild.nodeValue)

    info = document.getElementsByTagName("info")
    if info[0].getElementsByTagName("language")[0].firstChild.nodeValue == "en-CA":
        info = info[0]
    else:
        info = info[1]
    
    parsed_info.append(info.getElementsByTagName("event")[0].firstChild.nodeValue)
    parsed_info.append(info.getElementsByTagName("effective")[0].firstChild.nodeValue)
    parsed_info.append(info.getElementsByTagName("expires")[0].firstChild.nodeValue)
    parsed_info.append(info.getElementsByTagName("headline")[0].firstChild.nodeValue)
    parsed_info.append(info.getElementsByTagName("description")[0].firstChild.nodeValue)

    parsed_info.append([])
    areas = info.getElementsByTagName("area")
    for area in areas:
        area_info = []
        area_info.append(area.getElementsByTagName("areaDesc")[0].firstChild.nodeValue)
        area_info.append(area.getElementsByTagName("polygon")[0].firstChild.nodeValue)
        parsed_info[6].append(area_info)

    return parsed_info

def build_warnings_file(input, count):
    output = ""
    for area in input[6]:
        effective = datetime.strptime(input[2][:len(input[2])-6], "%Y-%m-%dT%H:%M:%S")
        expires = datetime.strptime(input[3][:len(input[3])-6], "%Y-%m-%dT%H:%M:%S")

        output += "\x01\n####018001288####\nWUUS54 ECCC "
        output += effective.strftime("%d%H%M")+ "\n\n/O.NEW.ECCC"
        output += get_event_type(input[1])
        output += ".W." + count

        effective = effective.strftime("%y%m%dT%H%MZ")
        expires = expires.strftime("%y%m%dT%H%MZ")

        output += "." + effective + "-" + expires + "/\n\n"
        output += input[4] + "\n"
        output += input[0] + "\n"
        output += effective + "\n\n"
        output += area[0] + "\n\n"
        output += input[5] + "\n\n&&\n\n"
        output += format_lat_long(area[1]) + "\n\n"
        output += "$$\n\x03"

    return output

warnings = ""
for file in os.listdir("./cap"):
    text_file = open("./cap/" + file, "r")
    text = text_file.read()
    text_file.close()
    parsed = parse_cap_file(text)
    warnings += build_warnings_file(parsed, "0001")

date = datetime.utcnow()
with open("./resources/warnings_" + date.strftime("%Y%m%d_%H") + ".txt", "w") as text_file:
    text_file.write(warnings)