from datetime import datetime

def write_logs(host,port,error_bash,error_hash,error_conn):
    with open("logs.txt",'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {host} : {port} | {error_bash} | {error_hash} | {error_conn}\n")
write_logs("localhost",3090,True,False,True)
