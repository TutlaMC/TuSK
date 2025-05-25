import json,os

def get_package_config(package_name:str):
    with open(f"config.json", "r") as f:
        data = json.load(f)
        return data["packages"].get(package_name, None)
def change_settings(package_name:str, settings:dict):
    with open(f"config.json", "r") as f:
        data = json.load(f)
        if package_name in data["packages"]:
            data["packages"][package_name] = settings
            with open(f"config.json", "w") as f:
                json.dump(data, f, indent=4)
            return True
        else:
            return False
def get_config():
    with open(f"config.json", "r") as f:
        return json.load(f).copy()
def create_package_config(package_name:str, config_data:dict):
    conf = get_config()
    if not package_name in conf["packages"]:
        conf["packages"][package_name] = config_data
        print(conf)
        with open(f"config.json", "w") as f:
            json.dump(conf, f, indent=4)
        return True
    else:
        return False

    

def create_json_db(package_name:str):
    with open(f"database/{package_name}.json", "w") as f:
        json.dump({}, f, indent=4)
    return True

def get_json_db(package_name:str):
    with open(f"database/{package_name}.json", "r") as f:
        return json.load(f)
    
def change_json_db(package_name:str, data:dict):
    if not exists_json_db(package_name):
        create_json_db(package_name)
    with open(f"database/{package_name}.json", "w") as f:
        json.dump(data, f, indent=4)
    return True

def delete_json_db(package_name:str):
    with open(f"database/{package_name}.json", "w") as f:
        json.dump({}, f, indent=4)
    return True

def exists_json_db(package_name:str):
    if os.path.exists(f"database/{package_name}.json"):
        return True
    return False