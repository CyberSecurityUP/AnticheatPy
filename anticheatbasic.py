import psutil
import os
import time

def find_procs_by_partial_name(name):
    "Retorna uma lista de processos cujo nome contém a substring dada."
    ls = []
    for p in psutil.process_iter(['name']):
        if name in p.info['name']:
            ls.append(p)
    return ls

def kill_proc_tree(pid, including_parent=True):  
    "Mata um processo e todos os seus filhos."
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

# substring do nome do processo a ser pesquisado
target_process_name = 'modest'

while True:
    procs = find_procs_by_partial_name(target_process_name)
    for proc in procs:
        print(f'Matando processo {proc.pid}...')
        kill_proc_tree(proc.pid)
    time.sleep(5)  # espera 5 segundos antes de procurar novamente
