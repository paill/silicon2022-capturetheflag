import requests
import os

session = requests.Session()

flag = ""

while True:

    r = session.get('https://arcade.silicon-ctf.party/pacman/map')
    map_data = r.json()

    for row in map_data['posY']:
        for column in row['posX']:
            if column['type'] == 'xwall':
                character_code = f'{column["col"]}{row["row"]}'
                character = chr(int(character_code))
                flag += character
    
    if character == "}":
        break

print(flag)