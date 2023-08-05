# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

# File holds the abbreviations for age, region and helper function

EONS = {
    'MCz': 'Mesozoic to Cenozoic',
    'Pz': 'Paleozoic',
    'lPt': 'Late Paleozoic',
    'mPt': 'Middle Paleozoic',
    'ePt': 'Early Paleozoic',
    'Ar': 'Archean'
}


PROVINCES = {
    'AFRICA-': 'AFRICA - ',
    'AFC-AB': 'AFRICA - Atlantic Border',
    'AFC-AF': 'AFRICA - Afar Depression',
    'AFC-AT': 'AFRICA - Atlas Mountains',
    'AFC-CA': 'AFRICA - Cape Ranges',
    'AFC-CH': 'AFRICA - Chad basin',
    'AFC-CO': 'AFRICA - Congo (Zaire) Basin',
    'AFC-ET': 'AFRICA - Ethiopian Highlands',
    'AFC-GH': 'AFRICA - Guinea Highlands',
    'AFC-GU': 'AFRICA - Guinea Coastal Lowlands',
    'AFC-HV': 'AFRICA - Highveld',
    'AFC-KA': 'AFRICA - Karoo',
    'AFC-KL': 'AFRICA - Kalahari basin',
    'AFC-LI': 'AFRICA - Libyan Plateau',
    'AFC-MA': 'AFRICA - Madagascar',
    'AFC-ME': 'AFRICA - Mediterranean Coastal Lowlands',
    'AFC-MO': 'AFRICA - Mozambique Lowland',
    'AFC-MS': 'AFRICA - Mauritanian-Senegal Basin',
    'AFC-NA': 'AFRICA - Namib Desert',
    'AFC-NG': 'AFRICA - Niger Basin',
    'AFC-NI': 'AFRICA - Nile Basin',
    'AFC-OR': 'AFRICA - Orange Basin',
    'AFC-RE': 'AFRICA - Red Sea highlands',
    'AFC-SA': 'AFRICA - Sahara Lowlands',
    'AFC-SH': 'AFRICA - Saharan Highlands',
    'AFC-SO': 'AFRICA - Somali Peninsula',
    'AFC-TA': 'AFRICA - Tablelands',
    'AFC-TN': 'AFRICA - Tanganyi Shield',
    'AFC-ZI': 'AFRICA - (Zimbabwe) Rhodesian Shield',
    'ANC-AM': 'ANTARCTICA - Amery Basin',
    'ANC-AN': 'ANTARCTICA - Antarctic (Palmer) Peninsula',
    'ANC-EN': 'ANTARCTICA - Enderby Land',
    'ANC-PO': 'ANTARCTICA - Polar Plateau',
    'ANC-QU': 'ANTARCTICA - Queen Maud Land',
    'ANC-RN': 'ANTARCTICA - Ronne (Filchner) Ice shelf',
    'ANC-RO': 'ANTARCTICA - Ross Ice shelf',
    'ANC-TR': 'ANTARCTICA - Trans-Antarctic Mountains',
    'ANC-WE': 'ANTARCTICA - West Antarctica',
    'ANC-WI': 'ANTARCTICA - Wilkes Land',
    'ARO-AL': 'ARCTIC OCEAN - Alpha Cordillera',
    'ARO-CA': 'ARCTIC OCEAN - Canadian Basin',
    'ARO-CH or CP': 'ARCTIC OCEAN - Chukchi Plateau',
    'ARO-FR': 'ARCTIC OCEAN - Fram Basin',
    'ARO-LO': 'ARCTIC OCEAN - Lomonobov Ridge',
    'ARO-MA': 'ARCTIC OCEAN - Makarov Basin',
    'ARO-MI': 'ARCTIC OCEAN - (Arctic) Mid-Ocean Ridge (Nansen Cordillera)',
    'ARO-NA': 'ARCTIC OCEAN - Nansen Basin',
    'ASC-AH': 'ASIA - Armenian Highlands',
    'ASC-AL': 'ASIA - Altai Mountains',
    'ASC-AM': 'ASIA - Amur Basin/Valley',
    'ASC-AN': 'ASIA - Anatolian Plateau',
    'ASC-AR': 'ASIA - Arabian Shield',
    'ASC-AS': 'ASIA - Andaman Sea Shelf',
    'ASC-BA': 'ASIA - Baluchistani Ranges',
    'ASC-BO': 'ASIA - Borneo',
    'ASC-BS': 'ASIA - Bering Sea Shelf',
    'ASC-CA': 'ASIA - Central Arabian Lowlands',
    'ASC-CE': 'ASIA - Central Highlands',
    'ASC-CH': 'ASIA - Chersky Range',
    'ASC-CL': 'ASIA - Celebes',
    'ASC-CS': 'ASIA - Chukchi Sea',
    'ASC-DE': 'ASIA - Deccan Plateau',
    'ASC-DZ': 'ASIA - Dzungarian Basin',
    'ASC-EA': 'ASIA - East Siberia Sea',
    'ASC-EC': 'ASIA - East China Sea Shelf',
    'ASC-EL': 'ASIA - Elburs (Alberz) Mountains',
    'ASC-GH': 'ASIA - Ghats',
    'ASC-GT': 'ASIA - Gulf of Thailand (Siam)',
    'ASC-GU': 'ASIA - Persian (Arabian) Gulf',
    'ASC-HA': 'ASIA - Hainan',
    'ASC-HD': 'ASIA - Hadhramawt (The Jol)',
    'ASC-HI': 'ASIA - Himalayas',
    'ASC-HK': 'ASIA - Hindu ush',
    'ASC-IL': 'ASIA - Indochinese Lowland',
    'ASC-IN': 'ASIA - Indo-Gangetic Plain',
    'ASC-IP': 'ASIA - Iranian Plateau',
    'ASC-IR': 'ASIA - Irrawaddy Valley (Erawad, Myit)',
    'ASC-JA': 'ASIA - Japan',
    'ASC-JS': 'ASIA - Java Sea',
    'ASC-JV': 'ASIA - Java',
    'ASC-KA': 'ASIA - Kazakh Uplands',
    'ASC-KD': 'ASIA - Koppch-Dagh (Kopet Dagh)',
    'ASC-KH': 'ASIA - Great Khingan Mountains (Da Hinggan Ling)',
    'ASC-KL': 'ASIA - Kolyma Highlands',
    'ASC-KO': 'ASIA - Korea',
    'ASC-KP': 'ASIA - Kamchatka Peninsula',
    'ASC-KS': 'ASIA - Kara Sea',
    'ASC-KU': 'ASIA - Kuen Lun Mountains',
    'ASC-LA': 'ASIA - Laptev Sea',
    'ASC-LE': 'ASIA - Levantine',
    'ASC-LN': 'ASIA - Lena-Alden Plateau',
    'ASC-LS': 'ASIA - Lesser Sunda Islands',
    'ASC-MA': 'ASIA - Manchurian Plain',
    'ASC-ME': 'ASIA - Mesopotamia',
    'ASC-MI': 'ASIA - North Molucca Islands',
    'ASC-ML': 'ASIA - Malay Peninsula',
    'ASC-MO': 'ASIA - Mongolian Plateau',
    'ASC-NA': 'ASIA - Nan Shan',
    'ASC-NC': 'ASIA - North China Plain',
    'ASC-NS': 'ASIA - North Siberia Lowland',
    'ASC-OK': 'ASIA - Okhotsk Sea Shelf',
    'ASC-OM': 'ASIA - Oman Mountains',
    'ASC-PA': 'ASIA - Pamirs',
    'ASC-PH': 'ASIA - Philippine Islands',
    'ASC-PO': 'ASIA - Pontic Mountains (Karadeniz Daglari)',
    'ASC-QA': 'ASIA - Qaidam Basin',
    'ASC-RU': 'ASIA - Rub-al-Khali (Empty Quarter)',
    'ASC-RY': 'ASIA - Ryukyu Islands',
    'ASC-SA': 'ASIA - Sakhalin Island',
    'ASC-SC': 'ASIA - South Chinese Highlands',
    'ASC-SI': 'ASIA - Sikhote Alin Range',
    'ASC-SM': 'ASIA - Strait of Malacoa',
    'ASC-SP': 'ASIA - (Central) Siberian Plateau',
    'ASC-SR': 'ASIA - Sri Lanka (Ceylon)',
    'ASC-SS': 'ASIA - South China Sea Shelf',
    'ASC-ST': 'ASIA - Stanovoy Range',
    'ASC-SU': 'ASIA - Sumatra',
    'ASC-SY': 'ASIA - Sayan Mountains',
    'ASC-SZ': 'ASIA - Szechuan (Red) Basin',
    'ASC-TA': 'ASIA - Taurus Mountains',
    'ASC-TB': 'ASIA - Tarim Basin',
    'ASC-TI': 'ASIA - Tibetan Plateau',
    'ASC-TL': 'ASIA - Tsin Lin Shan (Qin Lin Shan)',
    'ASC-TM': 'ASIA - Taimyr Peninsula',
    'ASC-TR': 'ASIA - Transcaucasus Lowlands',
    'ASC-TS': 'ASIA - Tien Shan',
    'ASC-TU': 'ASIA - Turan Plain (Low Land)',
    'ASC-TW': 'ASIA - Taiwan',
    'ASC-US': 'ASIA - Ustyurt Plateau',
    'ASC-VE': 'ASIA - Verkhoyansk Range',
    'ASC-VH': 'ASIA - Vitim Highlands (Upland)',
    'ASC-VI': 'ASIA - Vilyuy Plain (Yaket Lowland)',
    'ASC-WE': 'ASIA - West Siberia Plain',
    'ASC-YA': 'ASIA - Yablonovy Range',
    'ASC-YE': 'ASIA - Yellow Sea',
    'ASC-YU': 'ASIA - Yunnan Highlands',
    'ASC-ZA': 'ASIA - Zagros Mountains',
    'ASC-ZE': 'ASIA - Zeya-Bureya Depression',
    'AUC-AR': 'AUSTRALIA - Arafura Sea',
    'AUC-BA': 'AUSTRALIA - Bass Straight',
    'AUC-EH': 'AUSTRALIA - Easterm Highlands',
    'AUC-GB': 'AUSTRALIA - Great Barrier Reef',
    'AUC-LO': 'AUSTRALIA - Interior Lowlands',
    'AUC-NG': 'AUSTRALIA - New Guinea',
    'AUC-NO': 'AUSTRALIA - North Island New Zealand',
    'AUC-NU': 'AUSTRALIA - Nullarbor Plain',
    'AUC-SO': 'AUSTRALIA - South Island New Zealand',
    'AUC-TA': 'AUSTRALIA - Tasmania',
    'AUC-TI': 'AUSTRALIA - Timor Sea Shelf',
    'AUC-WP': 'AUSTRALIA - Western Plateau',
    'CGM-AV': 'CARIBBEAN SEA/GULF OF MEXICO - Aves Ridge',
    'CGM-BE': 'CARIBBEAN SEA/GULF OF MEXICO - Beata Ridge',
    'CGM-CA': 'CARIBBEAN SEA/GULF OF MEXICO - Cayman Trench',
    'CGM-CO': 'CARIBBEAN SEA/GULF OF MEXICO - Columbian Basin',
    'CGM-GR': 'CARIBBEAN SEA/GULF OF MEXICO - Grenada Basin',
    'CGM-GU': 'CARIBBEAN SEA/GULF OF MEXICO - Gulf of Mexico',
    'CGM-LA': 'CARIBBEAN SEA/GULF OF MEXICO - Lesser Antilles',
    'CGM-VE': 'CARIBBEAN SEA/GULF OF MEXICO - Venezuela Basins',
    'CGM-YU': 'CARIBBEAN SEA/GULF OF MEXICO - Yucatan Basin',
    'EUC-AE': 'EUROPE - Aegean Sea',
    'EUC-AL': 'EUROPE - Alps',
    'EUC-AP': 'EUROPE - Appenines',
    'EUC-AR': 'EUROPE - Arctic Lowlands',
    'EUC-BA': 'EUROPE - Baltic Shield',
    'EUC-BE': 'EUROPE - Baetic Mountains',
    'EUC-BK': 'EUROPE - Balkan Mountains',
    'EUC-BL': 'EUROPE - Black Sea Basin',
    'EUC-BR': 'EUROPE - Barents Sea Shelf',
    'EUC-BS': 'EUROPE - Baltic Sea',
    'EUC-CA': 'EUROPE - Caledonians',
    'EUC-CC': 'EUROPE - Causcaus Mountains',
    'EUC-CD': 'EUROPE - Caspian Depression',
    'EUC-CP': 'EUROPE - Caspian Sea',
    'EUC-CR': 'EUROPE - Capathian Mountains',
    'EUC-CS': 'EUROPE - (Atlantic) Continental Shelf',
    'EUC-FA': 'EUROPE - Faroe-Iceland Ridge',
    'EUC-HE': 'EUROPE - Hercynian (Central European)',
    'EUC-HU': 'EUROPE - Hungarian Plain',
    'EUC-IC': 'EUROPE - Iceland',
    'EUC-NO': 'EUROPE - Northern European Plain',
    'EUC-NS': 'EUROPE - North Sea',
    'EUC-PO': 'EUROPE - Po (Basin) Valley',
    'EUC-PY': 'EUROPE - Pyrennees',
    'EUC-RU': 'EUROPE - Russian (Eastern European)',
    'EUC-SC': 'EUROPE - Sardinia Corsica',
    'EUC-SI': 'EUROPE - Sicily',
    'EUC-TH': 'EUROPE - Thracian Basin',
    'EUC-UK': 'EUROPE - Ukranian Shield',
    'EUC-UR': 'EUROPE - Ural Mountains',
    'EUC-WA': 'EUROPE - Wallachan Plains',
    'INO-AD': 'INDIAN OCEAN - Gulf of Aden',
    'INO-AG': 'INDIAN OCEAN - Agulhas Basin',
    'INO-AI': 'INDIAN OCEAN - Atlantic Indian Basin',
    'INO-AN': 'INDIAN OCEAN - Andaman Sea',
    'INO-AP': 'INDIAN OCEAN - Agulhas Plateau',
    'INO-AR': 'INDIAN OCEAN - Arabian Basin',
    'INO-AT': 'INDIAN OCEAN - Atlantic-Indian Ridge',
    'INO-BE': 'INDIAN OCEAN - Bay of Bengal',
    'INO-BR': 'INDIAN OCEAN - Broken Ridge',
    'INO-CA': 'INDIAN OCEAN - Carlsberg Ridge',
    'INO-CE': 'INDIAN OCEAN - Central Indian Basin',
    'INO-CL': 'INDIAN OCEAN - Chagos-Laccadive Plateau',
    'INO-CR': 'INDIAN OCEAN - Crozet Basin',
    'INO-EX': 'INDIAN OCEAN - Exmouth Plateau',
    'INO-JT': 'INDIAN OCEAN - Java Trench',
    'INO-KE': 'INDIAN OCEAN - Kerguelan Plateau',
    'INO-MA': 'INDIAN OCEAN - Madagascar Basin',
    'INO-MD': 'INDIAN OCEAN - Madagascar Plateau/Ridge',
    'INO-MI': 'INDIAN OCEAN - Mid Indian Ridge',
    'INO-MO': 'INDIAN OCEAN - Mozambique Plateau/Ridge',
    'INO-MS': 'INDIAN OCEAN - Mascarene Plateau',
    'INO-NA': 'INDIAN OCEAN - Natal (Mozambique) Basin',
    'INO-NI': 'INDIAN OCEAN - Ninety East Ridge',
    'INO-NO': 'INDIAN OCEAN - North Australian Basin',
    'INO-NW': 'INDIAN OCEAN - Northwest Australian Basins',
    'INO-PE': 'INDIAN OCEAN - Perth Basin',
    'INO-PR': 'INDIAN OCEAN - Princess Elizabeth Trough',
    'INO-RE': 'INDIAN OCEAN - Red Sea Basin/Rift',
    'INO-SA': 'INDIAN OCEAN - South Australian Basin',
    'INO-SE': 'INDIAN OCEAN - Southeast Indian Ridge',
    'INO-SI': 'INDIAN OCEAN - South Indian Basin',
    'INO-SO': 'INDIAN OCEAN - Somali Basin',
    'INO-SW': 'INDIAN OCEAN - Southwest Indian Ridge',
    'MDS-AB': 'MEDITERRANEAN SEA - Alboran Sea',
    'MDS-AD': 'MEDITERRANEAN SEA - South Adriatic Basin',
    'MDS-AL': 'MEDITERRANEAN SEA - Algerian Basin',
    'MDS-AN': 'MEDITERRANEAN SEA - Antalya Basin',
    'MDS-BL': 'MEDITERRANEAN SEA - Black Sea Basin',
    'MDS-GE': 'MEDITERRANEAN SEA - Gela Basin',
    'MDS-HT': 'MEDITERRANEAN SEA - Hellenic Trench',
    'MDS-IO': 'MEDITERRANEAN SEA - Ionian Basin/Sea',
    'MDS-LE': 'MEDITERRANEAN SEA - Levantine Basin',
    'MDS-ME': 'MEDITERRANEAN SEA - Mediterranean Ridge',
    'MDS-TY': 'MEDITERRANEAN SEA - Tyrrhenian Basin/Sea',
    'NAC-AL': 'NORTH AMERICA - (Central) Alaska',
    'NAC-AP': 'NORTH AMERICA - Appalachian Province',
    'NAC-AR': 'NORTH AMERICA - Arctic Coastal Plain',
    'NAC-BA': 'NORTH AMERICA - Bahama Platform/Banks',
    'NAC-BE': 'NORTH AMERICA - Bear Province',
    'NAC-BR': 'NORTH AMERICA - Basin and Range Province',
    'NAC-BS': 'NORTH AMERICA - Bering Sea Shelf',
    'NAC-CA': 'NORTH AMERICA - Cascade Mountains',
    'NAC-CE': 'NORTH AMERICA - Central America',
    'NAC-CH': 'NORTH AMERICA - Churchill Province',
    'NAC-CI': 'NORTH AMERICA - Canadian (Arctic) Islands',
    'NAC-CO': 'NORTH AMERICA - Coastal Plain',
    'NAC-CP': 'NORTH AMERICA - Colorado Plateau',
    'NAC-CR': 'NORTH AMERICA - Cordillera',
    'NAC-GA': 'NORTH AMERICA - Greater Antilles',
    'NAC-GL': 'NORTH AMERICA - Greenland',
    'NAC-GP': 'NORTH AMERICA - Great Plains',
    'NAC-GR': 'NORTH AMERICA - Grenville Province',
    'NAC-HP': 'NORTH AMERICA - Hudson Platform',
    'NAC-MC': 'NORTH AMERICA - Midcontinent',
    'NAC-ME': 'NORTH AMERICA - Mexican Highlands',
    'NAC-NA': 'NORTH AMERICA - Nain Province',
    'NAC-PB': 'NORTH AMERICA - Pacific Border',
    'NAC-RM': 'NORTH AMERICA - Rocky Mountains',
    'NAC-SL': 'NORTH AMERICA - Slave Province',
    'NAC-SN': 'NORTH AMERICA - Sierra Nevada',
    'NAC-SU': 'NORTH AMERICA - Superior Province',
    'NAO-BA': 'NORTH ATLANTIC - Baffin Basin',
    'NAO-BL': 'NORTH ATLANTIC - Blake Plateau',
    'NAO-CA': 'NORTH ATLANTIC - Canary Basin',
    'NAO-CE': 'NORTH ATLANTIC - Ceara Abyssal Plain',
    'NAO-CV': 'NORTH ATLANTIC - Cape Verde Basin',
    'NAO-GR': 'NORTH ATLANTIC - Greenland Basin',
    'NAO-GU': 'NORTH ATLANTIC - Guiana Basin',
    'NAO-IB': 'NORTH ATLANTIC - Iberian Basin',
    'NAO-IC': 'NORTH ATLANTIC - Iceland Basin',
    'NAO-IP': 'NORTH ATLANTIC - Icelandic Plateau',
    'NAO-IR': 'NORTH ATLANTIC - Irminger Basin',
    'NAO-LA': 'NORTH ATLANTIC - Labrador Basin',
    'NAO-LO': 'NORTH ATLANTIC - Lofoten Basin',
    'NAO-MI': 'NORTH ATLANTIC - Mid-Atlantic Ridge',
    'NAO-MO': 'NORTH ATLANTIC - Mohns Ridge',
    'NAO-NA': 'NORTH ATLANTIC - North American Basin',
    'NAO-NE': 'NORTH ATLANTIC - Newfoundland Basin',
    'NAO-NO': 'NORTH ATLANTIC - Norwegian Basin',
    'NAO-PT': 'NORTH ATLANTIC - Puerto RicoTrench',
    'NAO-RC': 'NORTH ATLANTIC - Rockall Trough',
    'NAO-RE': 'NORTH ATLANTIC - Reykjanes Ridge',
    'NAO-RO': 'NORTH ATLANTIC - Rockall Plateau/Rise',
    'NAO-SI': 'NORTH ATLANTIC - Sierra Leone Basin',
    'NAO-SL': 'NORTH ATLANTIC - Sierra Leone Rise',
    'NAO-TO': 'NORTH ATLANTIC - Tobago Basin',
    'NAO-VO': 'NORTH ATLANTIC - Voring Plateau',
    'NAO-VT': 'NORTH ATLANTIC - Cape Verde Terrace/Plateau',
    'NAO-WE': 'NORTH ATLANTIC - West European Basin',
    'NPO-AB': 'NORTH PACIFIC - Aleutian Basin',
    'NPO-AI': 'NORTH PACIFIC - Aleutian Islands',
    'NPO-AT': 'NORTH PACIFIC - Aleutian Trench',
    'NPO-BA': 'NORTH PACIFIC - Banda and Flores Seas',
    'NPO-CA': 'NORTH PACIFIC - Caroline Ridge',
    'NPO-CE': 'NORTH PACIFIC - Celebes Basin',
    'NPO-CH': 'NORTH PACIFIC - Christmas Ridge',
    'NPO-CL': 'NORTH PACIFIC - Clipperton-Clarion Crustal Block',
    'NPO-CO': 'NORTH PACIFIC - Colon-Cocos Ridge',
    'NPO-CP': 'NORTH PACIFIC - Central Pacific Basin',
    'NPO-CR': 'NORTH PACIFIC - Clarion-Molokai Crustal Block',
    'NPO-EA': 'NORTH PACIFIC - East Pacific Rise',
    'NPO-EC': 'NORTH PACIFIC - East Caroline Basin',
    'NPO-EM': 'NORTH PACIFIC - Emperor Seamounts',
    'NPO-EP': 'NORTH PACIFIC - East Pacific Basin',
    'NPO-GC': 'NORTH PACIFIC - Gulf of Califonia Basin',
    'NPO-GL': 'NORTH PACIFIC - Galapagos-Clipperton Crustal Block',
    'NPO-GU': 'NORTH PACIFIC - Guatamala Basin',
    'NPO-HI': 'NORTH PACIFIC - Hawaiian Islands',
    'NPO-IT': 'NORTH PACIFIC - Izu-Ogasawara (Bonin) Trench',
    'NPO-JA': 'NORTH PACIFIC - Sea of Japan Basin',
    'NPO-JT': 'NORTH PACIFIC - Japan Trench',
    'NPO-JU': 'NORTH PACIFIC - Juan de Fuca Ridge',
    'NPO-KA': 'NORTH PACIFIC - Kamchatka (Komandorskiye) Basin',
    'NPO-KT': 'NORTH PACIFIC - Kuril-Kamchatka Trench',
    'NPO-KU': 'NORTH PACIFIC - Kuril Islands',
    'NPO-MA': 'NORTH PACIFIC - East Mariana Basin',
    'NPO-MD': 'NORTH PACIFIC - Middle American Trench',
    'NPO-ME': 'NORTH PACIFIC - Mendocino-Aleutian Crustal Block',
    'NPO-MG': 'NORTH PACIFIC - Marshall (Kiribati)-Gilbert Ridges',
    'NPO-MI': 'NORTH PACIFIC - Mariana Islands/ Trough',
    'NPO-ML': 'NORTH PACIFIC - Melanesian Basin',
    'NPO-MO': 'NORTH PACIFIC - Molokai-Murray Crustal Block',
    'NPO-MP': 'NORTH PACIFIC - Mid-Pacific Mountains',
    'NPO-MT': 'NORTH PACIFIC - Mariana Trench',
    'NPO-MU': 'NORTH PACIFIC - Murray-Mendocino Crustal Block',
    'NPO-NW': 'NORTH PACIFIC - Northwest Pacific Basin',
    'NPO-OK': 'NORTH PACIFIC - Sea of Okhotsk',
    'NPO-ON': 'NORTH PACIFIC - Ontong-Java Plateau',
    'NPO-PA': 'NORTH PACIFIC - Parece Vela (West Mariana) Basin',
    'NPO-PC': 'NORTH PACIFIC - Peru-Chile Trench',
    'NPO-PH': 'NORTH PACIFIC - Phillipine Basin',
    'NPO-PN': 'NORTH PACIFIC - Panama Basin',
    'NPO-PT': 'NORTH PACIFIC - Philippine Trench',
    'NPO-RT': 'NORTH PACIFIC - Ryukyu Trench',
    'NPO-SC': 'NORTH PACIFIC - South China Sea Basin',
    'NPO-SH': 'NORTH PACIFIC - South Honshu Ridge',
    'NPO-SU': 'NORTH PACIFIC - Sulu Basin',
    'NPO-WC': 'NORTH PACIFIC - West Caroline Basin',
    'SAC-AB': 'SOUTH AMERICA - (North) Atlantic Border',
    'SAC-AL': 'SOUTH AMERICA - Altiplano',
    'SAC-AM': 'SOUTH AMERICA - Amazon Basin',
    'SAC-AN': 'SOUTH AMERICA - Andes',
    'SAC-BH': 'SOUTH AMERICA - Brazilian Highlands',
    'SAC-BR': 'SOUTH AMERICA - Intermontain Basin and Range',
    'SAC-CH': 'SOUTH AMERICA - Chaco',
    'SAC-CS': 'SOUTH AMERICA - (South Atlantic) Continental Shelf',
    'SAC-GH': 'SOUTH AMERICA - Guiana Highlands',
    'SAC-LL': 'SOUTH AMERICA - Llanos (Orinoco Basin)',
    'SAC-MA': 'SOUTH AMERICA - Maracaibo Lowland/Basin',
    'SAC-MC': 'SOUTH AMERICA - Magdalena-Cauca Lowland/Basin',
    'SAC-PA': 'SOUTH AMERICA - Pampas',
    'SAC-PB': 'SOUTH AMERICA - Pacific Border',
    'SAC-PT': 'SOUTH AMERICA - Patagonia',
    'SAO-AA': 'SOUTH ATLANTIC - American-Antarctic Ridge',
    'SAO-AG': 'SOUTH ATLANTIC - Agulhas Basin',
    'SAO-AI': 'SOUTH ATLANTIC - Atlantic-Indian (Antarctic) Basin',
    'SAO-AN': 'SOUTH ATLANTIC - Angola Basin',
    'SAO-AR': 'SOUTH ATLANTIC - Argentine Basin',
    'SAO-BR': 'SOUTH ATLANTIC - Brazil Basin',
    'SAO-CA': 'SOUTH ATLANTIC - Cape Basin',
    'SAO-FA': 'SOUTH ATLANTIC - Falkland Plateau',
    'SAO-FT': 'SOUTH ATLANTIC - Falkland Trough',
    'SAO-GB': 'SOUTH ATLANTIC - Guinea Basin',
    'SAO-MI': 'SOUTH ATLANTIC - Mid-Atlantic Ridge',
    'SAO-RG': 'SOUTH ATLANTIC - Rio Grande Rise',
    'SAO-SC': 'SOUTH ATLANTIC - Scotia Basin',
    'SAO-SG': 'SOUTH ATLANTIC - South Georgia Basin',
    'SAO-SH': 'SOUTH ATLANTIC - Shona-Agulhas Ridges (Cape Rise)',
    'SAO-SR': 'SOUTH ATLANTIC - Scotia Ridge',
    'SAO-ST': 'SOUTH ATLANTIC - South Sandwich Trench',
    'SAO-WA': 'SOUTH ATLANTIC - Walvis Ridge',
    'SPO-BA': 'SOUTHERN PACIFIC - Banda Sea Basin',
    'SPO-BI': 'SOUTHERN PACIFIC - Bismarck Sea',
    'SPO-BO': 'SOUTHERN PACIFIC - Bounty Trough',
    'SPO-BT': 'SOUTHERN PACIFIC - New Britain Trench',
    'SPO-CH': 'SOUTHERN PACIFIC - Chile Basin',
    'SPO-CL': 'SOUTHERN PACIFIC - Chile Rise',
    'SPO-CM': 'SOUTHERN PACIFIC - Campbell Plateau',
    'SPO-CO': 'SOUTHERN PACIFIC - Coral Sea Basin',
    'SPO-CR': 'SOUTHERN PACIFIC - Carnegie Ridge',
    'SPO-CT': 'SOUTHERN PACIFIC - Chatham Rise',
    'SPO-EA': 'SOUTHERN PACIFIC - East Pacific Rise',
    'SPO-EC': 'SOUTHERN PACIFIC - East Coral Sea Basin',
    'SPO-EM': 'SOUTHERN PACIFIC - Emerald Basin',
    'SPO-FP': 'SOUTHERN PACIFIC - Fiji Plateau (North Fiji Basin)',
    'SPO-GA': 'SOUTHERN PACIFIC - Gazelle Basin',
    'SPO-GL': 'SOUTHERN PACIFIC - Galapagos Rise',
    'SPO-HT': 'SOUTHERN PACIFIC - New Hebrides Trench',
    'SPO-KE': 'SOUTHERN PACIFIC - Kermadec-Lau-Tonga Ridges',
    'SPO-KT': 'SOUTHERN PACIFIC - Kermadec Trench',
    'SPO-LA': 'SOUTHERN PACIFIC - Lau Basin',
    'SPO-LH': 'SOUTHERN PACIFIC - Lord Howe Rise',
    'SPO-MA': 'SOUTHERN PACIFIC - Macquarie Ridge Complex',
    'SPO-MG': 'SOUTHERN PACIFIC - Marquesas-Galapagos Crustal Block',
    'SPO-MP': 'SOUTHERN PACIFIC - Manihiki Plateau',
    'SPO-MQ': 'SOUTHERN PACIFIC - Marquesas Islands',
    'SPO-NA': 'SOUTHERN PACIFIC - Nazca Ridge',
    'SPO-NC': 'SOUTHERN PACIFIC - New Caledonia Trough/Basin',
    'SPO-NO': 'SOUTHERN PACIFIC - Norfork Ridge',
    'SPO-ON': 'SOUTHERN PACIFIC - Ontong-Java Plateau',
    'SPO-PA': 'SOUTHERN PACIFIC - Pacific-Antarctic Ridge',
    'SPO-PC': 'SOUTHERN PACIFIC - Peru-Chile Trench',
    'SPO-PE': 'SOUTHERN PACIFIC - Peru Basin',
    'SPO-PN': 'SOUTHERN PACIFIC - Penrhyn Basin',
    'SPO-QU': 'SOUTHERN PACIFIC - Queensland Plateau',
    'SPO-RO': 'SOUTHERN PACIFIC - Roggeveen Basin',
    'SPO-SA': 'SOUTHERN PACIFIC - Samoa Basin',
    'SPO-SC': 'SOUTHERN PACIFIC - Santa Cruz Basin',
    'SPO-SE': 'SOUTHERN PACIFIC - Southeast Pacific Basin',
    'SPO-SF': 'SOUTHERN PACIFIC - South Fiji Basin',
    'SPO-SG': 'SOUTHERN PACIFIC - Sala-y-Gomez Ridge',
    'SPO-SI': 'SOUTHERN PACIFIC - Solomon Islands',
    'SPO-SL': 'SOUTHERN PACIFIC - Solomon Sea Basin',
    'SPO-SO': 'SOUTHERN PACIFIC - Society Ridge',
    'SPO-SS': 'SOUTHERN PACIFIC - South Shetland Trough',
    'SPO-ST': 'SOUTHERN PACIFIC - South Tasman Rise/Plateau',
    'SPO-SW': 'SOUTHERN PACIFIC - Southwest Pacific Basin',
    'SPO-TA': 'SOUTHERN PACIFIC - Tasman Basin',
    'SPO-TI': 'SOUTHERN PACIFIC - Tiki Basin',
    'SPO-TT': 'SOUTHERN PACIFIC - Tonga Trench',
    'SPO-TU': 'SOUTHERN PACIFIC - Tuamotu Ridge',
    'SPO-TV': 'SOUTHERN PACIFIC - Tuvalu (Ellice) Ridge'
}


PROVINCE_KEYS = PROVINCES.keys()


def provinceKey(province):
    if province.upper() in PROVINCE_KEYS:
        return PROVINCES[province.upper()]
    return 'Undefined'


def ageKey(age):
    for key, value in EONS.items():
        if age.strip().lower() == key.lower():
            return value
    return 'Undefined'


def referenceKey(ref):
    if int(ref[:2]) > 50:
        y_prefix = '19'
    else:
        y_prefix = '20'
    return 'Year %s%s - %s. Author %s.' % (
        y_prefix, ref[:2], ref[4], ref[2])


def pubYear(ref):
    try:
        if int(ref[:2]) > 50:
            y_prefix = '19'
        else:
            y_prefix = '20'
        year = '%s%s' % (y_prefix, ref[:2])
        return int(year)
    except ValueError:
        return None
