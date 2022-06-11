import requests

base_url = "https://arcade.silicon-ctf.party/pacman"
path = ""
back_at_start = False

session = requests.Session()

while True:

    r = session.get(f"{base_url}/map")
    map_data = r.json()

    for row in map_data["posY"]:
        for column in row["posX"]:
            if column["type"] == "xwall":
                print(f"posY:{column['col']}, posX:{row['row']}")
                character_code = f"{column['col']}{row['row']}"
                character = chr(int(character_code))
                
    if character == "/":
        if back_at_start:
            break
        else:
            back_at_start = True
    
    path += character

print(path)
r = session.get(f"{base_url}{path}")
print(r.json())