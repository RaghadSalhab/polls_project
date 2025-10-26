# _db_helpers.py
import socket, subprocess

DOCKER_AUTO_START = True

# check if a TCP port is open on a given host
# example: is_port_open('localhost',6380) for redis and is_port_open('localhost',5432) for postgres
def is_port_open(host,port,timeout=1.0):
    try: socket.create_connection((host,int(port)),timeout=timeout); return True
    except Exception: return False

def ensure_redis(host='redis', port=6379):
    if is_port_open(host, port):
        print(f"ℹ️ Redis already at {host}:{port}")
        return True
    print(f"❌ Redis not reachable at {host}:{port}")
    return False

def ensure_postgres(host='postgres', port=5432):
    if is_port_open(host, port):
        print(f"ℹ️ Postgres already at {host}:{port}")
        return True
    print(f"❌ Postgres not reachable at {host}:{port}")
    return False
