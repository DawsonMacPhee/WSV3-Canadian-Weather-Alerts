from xml.dom.minidom import parseString
from datetime import datetime

def get_event_type(input):
    match input:
        case "tornado":
            return ".TO"
        case "thunderstorm":
            return ".SV"
        case "snowSquall":
            return ".SQ"
        case "spclMarine":
            return ".MA"
        case "flashFlood":
            return ".FF"
        case "wind":
            return ".EW"
        case "airQuality":
            return ".AS"
        case "fog":
            return ".MF"
        case "squall":
            return ".WI"
        case "waterspout":
            return ".LW"
        case "freezeRain":
            return ".FZ"
        case "rainfall":
            return ".FA"
        case "cold":
            return ".EC"
        case "heat":
            return ".EH"

def format_lat_long(input):
    output = "LAT...LON "
    for pair in input.split(" "):
        for coord in pair.split(","):
            parsed = coord.split(".")
            output += parsed[0].replace("-", "") + parsed[1][:len(parsed[1]) - 2].replace("-", "") + " "
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
        output += "\x01\n/0.NEW.ECCC"
        output += get_event_type(input[1])
        output += ".W." + count

        effective = datetime.strptime(input[2][:len(input[2])-6], "%Y-%m-%dT%H:%M:%S")
        effective = effective.strftime("%y%m%dT%H%MZ")
        expires = datetime.strptime(input[3][:len(input[3])-6], "%Y-%m-%dT%H:%M:%S")
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

parsed = parse_cap_file("""
    <?xml version='1.0' encoding='UTF-8' standalone='no'?>
    <alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
        <identifier>urn:oid:2.49.0.1.124.1596751993.2022</identifier>
        <sender>cap-pac@canada.ca</sender>
        <sent>2022-10-10T10:40:09-00:00</sent>
        <status>Actual</status>
        <msgType>Update</msgType>
        <source>Env. Can. - Can. Met. Ctr. – Montréal</source>
        <scope>Public</scope>
        <code>profile:CAP-CP:0.4</code>
        <code>layer:SOREM:1.0</code>
        <code>layer:EC-MSC-SMC:1.0</code>
        <code>layer:WPAM:1.0</code>
        <code>layer:EC-MSC-SMC:1.1</code>
        <code>layer:SOREM:2.0</code>
        <note>Service Notice - June 2022: The Environment and Climate Change Canada (ECCC) CAP Service periodically undergoes changes and additions as the business of alerting evolves. For June 2022...1) New changes to the Wireless Public Alerting Message Layer (WPAM) to take advantage of the new UpdateX feature recently deployed in the Canadian Cell Broadcasting Environment, 2) minor improvements in the audience facing wording of messages. For more information on these changes and other additions, you are invited to subscribe to the following mailing list: http://lists.cmc.ec.gc.ca/mailman/listinfo/dd_info | Notification de service - juin 2022: Le service du PAC d’Environnement et Changement climatique Canada (ECCC) subit périodiquement des changements et ajouts à mesure que le système d’alerte évolue. Pour juin 2022... 1) Il y a de nouveaux changements à la couche du Service d’alertes sans fil au public (WPAM) afin de profiter des avantages des nouvelles fonctionnalités d’UpdateX récemment déployées dans l’environnement de diffusion sans fil canadien, 2) des améliorations mineures à la formulation de messages destinés à l’auditoire. Pour plus d’informations sur ces changements ainsi que sur d’autres ajouts, vous êtes invités à vous inscrire à la liste de diffusion suivante: http://lists.cmc.ec.gc.ca/mailman/listinfo/dd_info</note>
        <references>cap-pac@canada.ca,urn:oid:2.49.0.1.124.2075275656.2022,2022-10-10T04:49:30-00:00</references>
        <info>
            <language>en-CA</language>
            <category>Met</category>
            <event>wind</event>
            <responseType>Monitor</responseType>
            <urgency>Future</urgency>
            <severity>Moderate</severity>
            <certainty>Likely</certainty>
            <audience>general public</audience>
            <eventCode>
                <valueName>profile:CAP-CP:Event:0.4</valueName>
                <value>wind</value>
            </eventCode>
            <eventCode>
                <valueName>SAME</valueName>
                <value>HWW</value>
            </eventCode>
            <effective>2022-10-10T10:39:09-00:00</effective>
            <expires>2022-10-10T20:59:09-00:00</expires>
            <senderName>Environment Canada</senderName>
            <headline>wind warning in effect</headline>
            <description>
    Strong winds with gusts near 90 km/h will continue in wind prone areas. Winds will weaken slightly to 80 km/h by this afternoon before easing this evening.

    ###

    Damage to buildings, such as to roof shingles and windows, may occur. Loose objects may be tossed by the wind and cause injury or damage.

    Wind warnings are issued when there is a significant risk of damaging winds.

    Please continue to monitor alerts and forecasts issued by Environment Canada. To report severe weather, send an email to ABstorm@ec.gc.ca or tweet reports using #ABStorm.
    </description>
            <instruction/>
            <web>http://weather.gc.ca/warnings/index_e.html?prov=ab</web>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Type</valueName>
                <value>warning</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Broadcast_Intrusive</valueName>
                <value>no</value>
            </parameter>
            <parameter>
                <valueName>layer:SOREM:1.0:Broadcast_Immediately</valueName>
                <value>No</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Parent_URI</valueName>
                <value>msc/alert/environment/hazard/alert-3.0-ascii/consolidated-xml-2.0/20221010103909002/WW_16_76_CWWG/WDW/230107328896685796202210090501_WW_16_76_CWWG/actual/en_proper_complete_c-fr_proper_complete_c/NinJo</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:CAP_count</valueName>
                <value>A:6430 M:37378 C:64556</value>
            </parameter>
            <parameter>
                <valueName>profile:CAP-CP:0.4:MinorChange</valueName>
                <value>text</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Location_Status</valueName>
                <value>active</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Name</valueName>
                <value>wind warning</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Coverage</valueName>
                <value>Northern Alberta</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Designation_Code</valueName>
                <value>WW_16_76_CWWG</value>
            </parameter>
            <parameter>
                <valueName>layer:SOREM:2.0:WirelessImmediate</valueName>
                <value>No</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Alert_Location_Status</valueName>
                <value>active</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Newly_Active_Areas</valueName>
                <value/>
            </parameter>
            <area>
                <areaDesc>M.D. of Greenview near Grande Cache Botten and Amundson</areaDesc>
                <polygon>54.0527,-117.5282 54.0246,-117.4971 53.9975,-117.5676 53.9808,-117.6769 53.9283,-117.7606 53.9265,-117.8521 53.8937,-117.9973 53.8684,-117.9974 53.8062,-117.9999 53.7966,-118.4027 53.8055,-118.8906 53.8049,-118.9984 53.8449,-118.9977 53.8402,-119.2193 53.8467,-119.4844 53.9666,-119.4915 53.9686,-119.4916 54.0784,-119.484 54.5875,-119.484 54.5875,-119.0577 54.5875,-117.997 54.5875,-117.5267 54.0883,-117.5281 54.0527,-117.5282</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077210</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4818005</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4818015</value>
                </geocode>
            </area>
            <area>
                <areaDesc>M.D. of Greenview near Kakwa Wildland Prov. Park and Nose Lake</areaDesc>
                <polygon>53.9666,-119.4915 53.8631,-119.7212 53.8894,-120.0013 53.9374,-120.0013 53.9904,-120.0013 54.5874,-120.0013 54.5875,-119.484 54.0784,-119.484 54.0248,-119.484 53.9699,-119.4841 53.9666,-119.4915</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077220</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4818015</value>
                </geocode>
            </area>
            <area>
                <areaDesc>Yellowhead Co. near William A. Switzer Prov. Park</areaDesc>
                <polygon>53.632,-117.9433 53.6282,-117.73 53.3759,-117.73 53.3685,-117.73 53.3686,-117.764 53.3687,-117.9462 53.3686,-118.0779 53.3685,-118.0833 53.3222,-118.0682 53.2749,-118.2189 53.3537,-118.3218 53.4182,-118.2928 53.4399,-118.2932 53.4772,-118.2938 53.5423,-118.2948 53.5415,-118.1465 53.6285,-118.1462 53.632,-117.9433</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077230</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814003</value>
                </geocode>
            </area>
            <area>
                <areaDesc>Yellowhead Co. near Big Berland and the Wildhay River</areaDesc>
                <polygon>53.9175,-117.9973 53.9551,-118.0153 54.0009,-117.8014 54.0525,-117.731 54.0594,-117.6056 54.0883,-117.5281 54.0527,-117.5282 54.0246,-117.4971 53.9859,-117.4572 53.6282,-117.0859 53.6283,-117.1057 53.6282,-117.73 53.6255,-117.9485 53.6285,-118.1462 53.6295,-118.1462 53.6293,-118.2936 53.6362,-118.295 53.6437,-118.2947 53.6433,-118.4419 53.7603,-118.4441 53.7607,-118.8902 53.8055,-118.8906 53.8158,-118.4225 53.8062,-117.9999 53.9175,-117.9973</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077240</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814003</value>
                </geocode>
            </area>
            <area>
                <areaDesc>Willmore Wilderness Park</areaDesc>
                <polygon>53.9904,-120.0013 53.9601,-119.7759 54.0784,-119.484 53.9696,-119.4774 53.8467,-119.4844 53.8522,-119.2196 53.8449,-118.9977 53.8049,-118.9984 53.8055,-118.8906 53.7607,-118.8902 53.7603,-118.4441 53.6433,-118.4419 53.6437,-118.2947 53.6364,-118.2933 53.6293,-118.2936 53.6295,-118.1462 53.6285,-118.1462 53.5415,-118.1465 53.5423,-118.2948 53.4772,-118.2938 53.4399,-118.2932 53.4182,-118.2928 53.3537,-118.3218 53.3782,-118.6168 53.3868,-119.1694 53.4175,-119.3341 53.3461,-119.3097 53.3454,-119.3121 53.3072,-119.4485 53.2883,-119.5155 53.3383,-119.8079 53.6168,-120.0188 53.6685,-119.9089 53.7836,-120.0959 53.804,-120.0013 53.8162,-120.0013 53.8281,-120.0013 53.835,-120.0013 53.8698,-120.0013 53.8703,-120.0013 53.8894,-120.0013 53.9374,-120.0013 53.9904,-120.0013</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077250</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814028</value>
                </geocode>
            </area>
            <area>
                <areaDesc>Yellowhead Co. near Hinton and Obed Lake Prov. Park</areaDesc>
                <polygon>53.6282,-117.0859 53.3667,-116.814 53.3666,-117.3641 53.1857,-117.3639 53.1859,-117.592 53.1858,-117.7042 53.1527,-117.7487 53.2107,-117.8927 53.3262,-118.0305 53.3222,-118.0682 53.3685,-118.0833 53.3686,-118.0779 53.3687,-117.9462 53.3686,-117.764 53.3749,-117.7523 53.3759,-117.73 53.6282,-117.73 53.6283,-117.1057 53.6282,-117.0859</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077260</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814003</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814019</value>
                </geocode>
            </area>
        </info>
        <info>
            <language>fr-CA</language>
            <category>Met</category>
            <event>vent</event>
            <responseType>Monitor</responseType>
            <urgency>Future</urgency>
            <severity>Moderate</severity>
            <certainty>Likely</certainty>
            <audience>grand public</audience>
            <eventCode>
                <valueName>profile:CAP-CP:Event:0.4</valueName>
                <value>wind</value>
            </eventCode>
            <eventCode>
                <valueName>SAME</valueName>
                <value>HWW</value>
            </eventCode>
            <effective>2022-10-10T10:39:09-00:00</effective>
            <expires>2022-10-10T20:59:09-00:00</expires>
            <senderName>Environnement Canada</senderName>
            <headline>avertissement de vent en vigueur</headline>
            <description>
    Des vents forts soufflant en rafales à près de 90 km/h devraient persister dans les secteurs exposés aux vents. Les vents vont faiblir légèrement à 80 km/h d'ici cet après-midi avant de faiblir ce soir.

    ###

    Les bâtiments pourraient être endommagés (bardeaux de toiture, fenêtres brisées). Le vent pourrait emporter les objets non fixés à une surface et causer des blessures ou des dommages.

    Un avertissement de vent est émis lorsqu'il y a un risque important que des vents destructeurs soufflent.

    Veuillez continuer à surveiller les alertes et les prévisions émises par Environnement Canada. Pour signaler du temps violent, envoyez un courriel à meteoAB@ec.gc.ca ou publiez un gazouillis en utilisant le mot-clic #ABMeteo.
    </description>
            <instruction/>
            <web>http://meteo.gc.ca/warnings/index_f.html?prov=ab</web>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Type</valueName>
                <value>warning</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Broadcast_Intrusive</valueName>
                <value>no</value>
            </parameter>
            <parameter>
                <valueName>layer:SOREM:1.0:Broadcast_Immediately</valueName>
                <value>No</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Parent_URI</valueName>
                <value>msc/alert/environment/hazard/alert-3.0-ascii/consolidated-xml-2.0/20221010103909002/WW_16_76_CWWG/WDW/230107328896685796202210090501_WW_16_76_CWWG/actual/en_proper_complete_c-fr_proper_complete_c/NinJo</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:CAP_count</valueName>
                <value>A:6430 M:37378 C:64556</value>
            </parameter>
            <parameter>
                <valueName>profile:CAP-CP:0.4:MinorChange</valueName>
                <value>text</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Location_Status</valueName>
                <value>active</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Name</valueName>
                <value>avertissement de vent</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.0:Alert_Coverage</valueName>
                <value>nord de l'Alberta</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Designation_Code</valueName>
                <value>WW_16_76_CWWG</value>
            </parameter>
            <parameter>
                <valueName>layer:SOREM:2.0:WirelessImmediate</valueName>
                <value>No</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Alert_Location_Status</valueName>
                <value>active</value>
            </parameter>
            <parameter>
                <valueName>layer:EC-MSC-SMC:1.1:Newly_Active_Areas</valueName>
                <value/>
            </parameter>
            <area>
                <areaDesc>d.m. de Greenview près de Grande Cache Botten et Amundson</areaDesc>
                <polygon>54.0527,-117.5282 54.0246,-117.4971 53.9975,-117.5676 53.9808,-117.6769 53.9283,-117.7606 53.9265,-117.8521 53.8937,-117.9973 53.8684,-117.9974 53.8062,-117.9999 53.7966,-118.4027 53.8055,-118.8906 53.8049,-118.9984 53.8449,-118.9977 53.8402,-119.2193 53.8467,-119.4844 53.9666,-119.4915 53.9686,-119.4916 54.0784,-119.484 54.5875,-119.484 54.5875,-119.0577 54.5875,-117.997 54.5875,-117.5267 54.0883,-117.5281 54.0527,-117.5282</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077210</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4818005</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4818015</value>
                </geocode>
            </area>
            <area>
                <areaDesc>d.m. de Greenview près du Kakwa Wildland Prov. Park et du lac Nose</areaDesc>
                <polygon>53.9666,-119.4915 53.8631,-119.7212 53.8894,-120.0013 53.9374,-120.0013 53.9904,-120.0013 54.5874,-120.0013 54.5875,-119.484 54.0784,-119.484 54.0248,-119.484 53.9699,-119.4841 53.9666,-119.4915</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077220</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4818015</value>
                </geocode>
            </area>
            <area>
                <areaDesc>cté de Yellowhead près du William A. Switzer Prov. Park</areaDesc>
                <polygon>53.632,-117.9433 53.6282,-117.73 53.3759,-117.73 53.3685,-117.73 53.3686,-117.764 53.3687,-117.9462 53.3686,-118.0779 53.3685,-118.0833 53.3222,-118.0682 53.2749,-118.2189 53.3537,-118.3218 53.4182,-118.2928 53.4399,-118.2932 53.4772,-118.2938 53.5423,-118.2948 53.5415,-118.1465 53.6285,-118.1462 53.632,-117.9433</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077230</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814003</value>
                </geocode>
            </area>
            <area>
                <areaDesc>cté de Yellowhead près de Big Berland et de la riv. Wildhay</areaDesc>
                <polygon>53.9175,-117.9973 53.9551,-118.0153 54.0009,-117.8014 54.0525,-117.731 54.0594,-117.6056 54.0883,-117.5281 54.0527,-117.5282 54.0246,-117.4971 53.9859,-117.4572 53.6282,-117.0859 53.6283,-117.1057 53.6282,-117.73 53.6255,-117.9485 53.6285,-118.1462 53.6295,-118.1462 53.6293,-118.2936 53.6362,-118.295 53.6437,-118.2947 53.6433,-118.4419 53.7603,-118.4441 53.7607,-118.8902 53.8055,-118.8906 53.8158,-118.4225 53.8062,-117.9999 53.9175,-117.9973</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077240</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814003</value>
                </geocode>
            </area>
            <area>
                <areaDesc>parc sauvage de Willmore</areaDesc>
                <polygon>53.9904,-120.0013 53.9601,-119.7759 54.0784,-119.484 53.9696,-119.4774 53.8467,-119.4844 53.8522,-119.2196 53.8449,-118.9977 53.8049,-118.9984 53.8055,-118.8906 53.7607,-118.8902 53.7603,-118.4441 53.6433,-118.4419 53.6437,-118.2947 53.6364,-118.2933 53.6293,-118.2936 53.6295,-118.1462 53.6285,-118.1462 53.5415,-118.1465 53.5423,-118.2948 53.4772,-118.2938 53.4399,-118.2932 53.4182,-118.2928 53.3537,-118.3218 53.3782,-118.6168 53.3868,-119.1694 53.4175,-119.3341 53.3461,-119.3097 53.3454,-119.3121 53.3072,-119.4485 53.2883,-119.5155 53.3383,-119.8079 53.6168,-120.0188 53.6685,-119.9089 53.7836,-120.0959 53.804,-120.0013 53.8162,-120.0013 53.8281,-120.0013 53.835,-120.0013 53.8698,-120.0013 53.8703,-120.0013 53.8894,-120.0013 53.9374,-120.0013 53.9904,-120.0013</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077250</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814028</value>
                </geocode>
            </area>
            <area>
                <areaDesc>cté de Yellowhead près de Hinton et Obed Lake Prov Park</areaDesc>
                <polygon>53.6282,-117.0859 53.3667,-116.814 53.3666,-117.3641 53.1857,-117.3639 53.1859,-117.592 53.1858,-117.7042 53.1527,-117.7487 53.2107,-117.8927 53.3262,-118.0305 53.3222,-118.0682 53.3685,-118.0833 53.3686,-118.0779 53.3687,-117.9462 53.3686,-117.764 53.3749,-117.7523 53.3759,-117.73 53.6282,-117.73 53.6283,-117.1057 53.6282,-117.0859</polygon>
                <geocode>
                    <valueName>layer:EC-MSC-SMC:1.0:CLC</valueName>
                    <value>077260</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814003</value>
                </geocode>
                <geocode>
                    <valueName>profile:CAP-CP:Location:0.3</valueName>
                    <value>4814019</value>
                </geocode>
            </area>
        </info>
    <Signature xmlns="http://www.w3.org/2000/09/xmldsig#" Id="Environment Canada">
    <SignedInfo>
    <CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
    <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
    <Reference URI="">
    <Transforms>
    <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
    </Transforms>
    <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
    <DigestValue>2UvTI+FesuRVJqN9h1AYYfe+Ul0dxxhewIzfUWE7nGo=</DigestValue>
    </Reference>
    </SignedInfo>
    <SignatureValue>kodDCXSF5RrilmcOSG+yeJ8U5p8iurN9+ShGjc+exPbGAlUAJJqW++LYagep+a0z
    bsFYXcK4+MfEf1AeXu9DvydTEN2bQZ7RF5MGp+jOFd4FfIW7fEfQ7FntW8BUBiUC
    LWaHFzsNIC6FIlhUbPBOMH24K1A/ppUAd2KYgI7Ro0dRcE88ehIAKgZWvsCkWx3U
    w2ObS0I5LUC6v9bM5Ze0D8EOG9fVb75BTMPedaXtUvOnHi/YazEn36wnXnjryIpV
    aS4v6GiVv+CBVoU1vXH+UCb3Pz/3CVoXwVmnU8Vr66BwQYW7PIicev/hRmZGm5v+
    Dfp5astA1/S8ZNHy26yXIA==</SignatureValue>
    <KeyInfo>
    <X509Data>
    <X509Certificate>MIIHQDCCBiigAwIBAgIQVM83tR+H9HQcCcfTpntZ0jANBgkqhkiG9w0BAQsFADCB
    ujELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUVudHJ1c3QsIEluYy4xKDAmBgNVBAsT
    H1NlZSB3d3cuZW50cnVzdC5uZXQvbGVnYWwtdGVybXMxOTA3BgNVBAsTMChjKSAy
    MDEyIEVudHJ1c3QsIEluYy4gLSBmb3IgYXV0aG9yaXplZCB1c2Ugb25seTEuMCwG
    A1UEAxMlRW50cnVzdCBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eSAtIEwxSzAeFw0y
    MTA0MDYxNDI4NTNaFw0yMjA1MDUxNDI4NTJaMGgxCzAJBgNVBAYTAkNBMQ8wDQYD
    VQQIEwZRdWViZWMxETAPBgNVBAcTCEdhdGluZWF1MRswGQYDVQQKExJFbnZpcm9u
    bWVudCBDYW5hZGExGDAWBgNVBAMMDyoud2VhdGhlci5nYy5jYTCCASIwDQYJKoZI
    hvcNAQEBBQADggEPADCCAQoCggEBAKN11t27vPi+ux94AEGuComDkX2rZYWwyE8s
    YMdJWg4TQxTljp4R8//VI9vO0c/1hH9AnkGCafH6k/9pVxkmJUZ32isJrTPS6SJK
    fejnFqVVjMEFpOkXcSy2LJ0I/FeaMJ4Ivs6dRGDSmnYQYFYHMvWGTEMBWCi2Q2G8
    4GSLKmKkJ6RC04nfyPEHuuyoS0APXnRDb4DZjVOxXb0zrpq1FvegWzCIpZiq3kCE
    JhXL3YSplB7yk1SWqjJROvj5AogyoLFiNW+S9Q1WrQ/efjxBYPmzj9VoWtcgezJB
    B4YJLP75XneF69Hxy+6OhitniSPMEtE1R0zB4G1axTNiWviH60sCAwEAAaOCA5Ew
    ggONMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFC4sBO19G7Jk7WQDbJicDuYRIyUY
    MB8GA1UdIwQYMBaAFIKicHTdvFM/z3vU981/p2DGCky/MGgGCCsGAQUFBwEBBFww
    WjAjBggrBgEFBQcwAYYXaHR0cDovL29jc3AuZW50cnVzdC5uZXQwMwYIKwYBBQUH
    MAKGJ2h0dHA6Ly9haWEuZW50cnVzdC5uZXQvbDFrLWNoYWluMjU2LmNlcjAzBgNV
    HR8ELDAqMCigJqAkhiJodHRwOi8vY3JsLmVudHJ1c3QubmV0L2xldmVsMWsuY3Js
    MIGdBgNVHREEgZUwgZKCDyoud2VhdGhlci5nYy5jYYINd2VhdGhlci5nYy5jYYIL
    bWV0ZW8uZ2MuY2GCDSoubWV0ZW8uZ2MuY2GCFSouYWxwaGEud2VhdGhlci5nYy5j
    YYITKi5hbHBoYS5tZXRlby5nYy5jYYIUKi5iZXRhLndlYXRoZXIuZ2MuY2GCEiou
    YmV0YS5tZXRlby5nYy5jYTAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYB
    BQUHAwEGCCsGAQUFBwMCMEwGA1UdIARFMEMwNwYKYIZIAYb6bAoBBTApMCcGCCsG
    AQUFBwIBFhtodHRwczovL3d3dy5lbnRydXN0Lm5ldC9ycGEwCAYGZ4EMAQICMIIB
    fwYKKwYBBAHWeQIEAgSCAW8EggFrAWkAdwBVgdTCFpA2AUrqC5tXPFPwwOQ4eHAl
    CBcvo6odBxPTDAAAAXinlhQbAAAEAwBIMEYCIQCjOHLzIFyW41zO3lT2ZShXTc8M
    hMigKHnFLVjQJnqRkgIhALIWlaEWCK6XITu3RUxkKlXtR56NDU3L7/iVG62O+Tdj
    AHYAUaOw9f0BeZxWbbg3eI8MpHrMGyfL956IQpoN/tSLBeUAAAF4p5YUFwAABAMA
    RzBFAiEAvm6gY+CUKh7AaiqwZ5TUcN/GtcMA2aHOM+FsXRJWJHsCIHjzurWrQ0aK
    IrMJsRdzMxUGavZ0IAv21eeqbrVoB+0hAHYARqVV63X6kSAwtaKJafTzfREsQXS+
    /Um4havy/HD+bUcAAAF4p5YUdgAABAMARzBFAiBbDo4h+iE+c+IlbPLFHEhyXWe9
    7C1O7KrFf76JQ6pcRgIhANVhTgXzbVEOM9MHz9Hp9NwmHhhuQUOE7zNrVDlrs5rG
    MA0GCSqGSIb3DQEBCwUAA4IBAQBPGB3a+dTaJ+raWqJKoMauRMr8WaskBj3ra1nH
    /VFeSvobDurUW59LZwY7Q8MAFDGGqr07yGZTBcb58EBJVFT55UHTRWrMJ6pfBApJ
    oYLi9ivyS/Tc4aUU/TZo8tTRUgkuEyw0gK029JAqqUUwKL0YwcRTlop5EpsittNV
    cQS83d+l0jhp7lRSIN8P6UlrteRP5l/87SHO4FO5j86DvVaRbjjxRHTVJ1ot0HiY
    qlg44k8IzfgTn9CzImGRqSc4C0CBK7VqXF2dFca9Q41+5FPvdt/reNViL3v+lPLM
    AojtY6LH2dFDcUqfz/f44MO0PKvlApB6GyCG+EfBTW02TtJx</X509Certificate>
    </X509Data>
    </KeyInfo>
    </Signature></alert>
""".strip())

date = datetime.utcnow()
with open("./resources/warnings_" + date.strftime("%Y%m%d_%H") + ".txt", "w") as text_file:
    text_file.write(build_warnings_file(parsed, "0001"))