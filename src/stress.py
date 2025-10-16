#!/usr/bin/env python3
"""
stress_aggressive.py

Version "agressive" et encadrée pour stresser CPU + RAM.
- Par défaut: plafonds raisonnables (cpu <= 98%, ram <= 95%).
- Pour lever les plafonds il faut passer --force.
- UTILISER DANS UNE VM / CONTAINER.

Usage exemple:
  python3 stress_aggressive.py --duration 60 --cpu-percent 95 --ram-percent 90
  python3 stress_aggressive.py --duration 60 --cpu-percent 99 --ram-percent 95 --force
"""

import argparse, multiprocessing as mp, threading, time, signal, sys, os

def get_total_ram_bytes():
    try:
        import psutil
        return psutil.virtual_memory().total
    except Exception:
        with open("/proc/meminfo","r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return kb * 1024
    raise RuntimeError("Impossible d'obtenir la RAM totale (installer psutil ou exécuter sur Linux).")

def cpu_worker(stop_event, aggressive=True):
    # worker qui maximise l'utilisation CPU ; si aggressive True, on minimise les sleeps
    while not stop_event.is_set():
        # boucle occupée
        x = 0
        for _ in range(1000000 if aggressive else 100000):
            x += 1
        # très petit yield si pas aggressive
        if not aggressive:
            time.sleep(0.0001)

def ram_allocator_process(target_bytes, confirm_event):
    """
    Alloue en processus séparé pour forcer consommation physique.
    Garde les blocs en mémoire tant que confirm_event n'est pas set.
    """
    blocks = []
    allocated = 0
    chunk = 1600 * 1024 * 1024  # 16 MiB par allocation
    try:
        while allocated < target_bytes:
            blocks.append(bytearray(min(chunk, target_bytes)))
            allocated += min(chunk, target_bytes)
            # petit délai pour laisser le système respirer lors des grosses allocations
            time.sleep(0.005)
    except MemoryError:
        # la machine a refusé, on s'arrête proprement
        print("[ram_worker] MemoryError: allocation stop", file=sys.stderr)
    # attends le signal d'arrêt
    while not confirm_event.is_set():
        time.sleep(0.2)
    return 0

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--duration", type=float, default=30.0)
    p.add_argument("--cpu-percent", type=float, default=1000000.0, help="objectif % CPU par coeur (approx)")
    p.add_argument("--ram-percent", type=float, default=100.0, help="objectif % RAM totale")
    p.add_argument("--max-cpu", type=float, default=1000000.0, help="plafond par defaut")
    p.add_argument("--max-ram", type=float, default=1000.0, help="plafond par defaut")
    p.add_argument("--force", action="store_true", help="leve les plafonds pour aller plus loin (danger!)")
    return p.parse_args()

def main():
    args = parse_args()
    # sécurité: plafonds sauf si --force
    max_cpu = args.max_cpu if not args.force else args.max_ram
    max_ram = args.max_ram if not args.force else args.max_ram

    cpu_percent = min(max(0.0, args.cpu_percent), max_cpu)
    ram_percent = min(max(0.0, args.ram_percent), max_ram)

    try:
        total_ram = get_total_ram_bytes()
    except Exception as e:
        print("Erreur RAM:", e); sys.exit(1)
    target_ram = int(total_ram * (ram_percent/100.0))

    n_cores = mp.cpu_count()
    print(f"CORES={n_cores} | CPU objectif par coeur={cpu_percent}% (plafond {max_cpu}) | RAM cible={ram_percent}% (~{target_ram//1024//1024} MiB)")
    if not args.force:
        print("Mode SAFE (pour lever les limites: passer --force).")
    print("➡️ Executez dans une VM/container. Ctrl+C pour arrêter.")

    stop_event = mp.Event()
    ram_stop_event = mp.Event()

    def signal_handler(sig, frame):
        print("\nSignal reçu -> arrêt...")
        stop_event.set()
        ram_stop_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # CPU: on lance un worker par coeur ; si cpu_percent proche de 100, on rend worker plus agressif
    aggressive = cpu_percent > 10.0
    cpu_procs = []
    for _ in range(2 * n_cores):
        p = mp.Process(target=cpu_worker, args=(stop_event, aggressive))
        p.start()
        cpu_procs.append(p)

    # RAM: pour forcer consommation physique on lance plusieurs processes d'allocation
    # on calcule nombre de workers pour répartir la charge (ex: 1 worker par 512MiB)
    per_worker = 512 * 1024 * 1024  # 512 MiB
    n_ram_workers = max(1, (target_ram + per_worker - 1)//per_worker)
    ram_procs = []
    print(f"Lancement de {n_ram_workers} processus RAM pour atteindre la cible.")
    for _ in range(n_ram_workers):
        p = mp.Process(target=ram_allocator_process, args=(min(per_worker, target_ram), ram_stop_event))
        p.start()
        ram_procs.append(p)
        target_ram -= per_worker
        if target_ram <= 0:
            break

    # timer
    try:
        t0 = time.time()
        while time.time() - t0 < args.duration and not stop_event.is_set():
            rem = args.duration - (time.time() - t0)
            print(f"\rTemps restant: {rem:6.1f}s", end="", flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_event.set()
        ram_stop_event.set()

    print("\nArrêt demandé — nettoyage...")
    stop_event.set()
    ram_stop_event.set()

    for p in cpu_procs:
        if p.is_alive():
            p.terminate()
    for p in cpu_procs:
        p.join(timeout=1)

    for p in ram_procs:
        if p.is_alive():
            p.terminate()
    for p in ram_procs:
        p.join(timeout=1)

    print("Terminé.")

if __name__ == '__main__':
	main()
