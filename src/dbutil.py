import json
import os
import aiosqlite3

# quickdb
def get_db(id: int,failsafe=False) -> dict|None:
    if not os.path.exists(f"database/quickdb/{id}.json"):
        if failsafe:
            with open(f"database/quickdb/{id}.json", "w") as f:
                json.dump({}, f)
        else:
            return None
    with open(f"database/quickdb/{id}.json", "r") as f:
        return json.load(f)

def get_data(id: int,name) -> str|None:
    return get_db(id, failsafe=True)[name]
    
def set_data(id: int, name, val) -> dict:
    db = get_db(id,failsafe=True)
    db[name] = val
    with open(f"database/quickdb/{id}.json", "w") as f:
        json.dump(db, f)
    return db

def delete_data(id: int,name) -> bool:
    db = get_db(id,failsafe=True)
    del db[name]
    with open(f"database/quickdb/{id}.json", "w") as f:
        json.dump(db, f)
    return db

def delete_db(id: int) -> bool:
    if os.path.exists(f"database/quickdb/{id}.json"):
        os.remove(f"database/quickdb/{id}.json")
        return True
    else:
        return False
    
def create_db(id: int) -> bool:
    if not os.path.exists(f"database/quickdb/{id}.json"):
        with open(f"database/quickdb/{id}.json", "w") as f:
            json.dump({}, f)
        return True
    else:
        return False
    
# MySQL
async def get_mysql_db(id: int) -> dict|None: # V1.1, coming soon
    pass