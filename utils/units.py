from os import environ

def env(key:str)->str:
    return environ[key] if key in environ else None