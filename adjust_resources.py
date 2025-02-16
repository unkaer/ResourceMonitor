import psutil
import time
import math
import logging
import multiprocessing
from multiprocessing import Process, Event

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# 设置目标占用范围
MIN_CPU = 15  # CPU最低占用百分比
MAX_CPU = 20  # CPU最高占用百分比
MIN_MEM = 15  # 内存最低占用百分比
MAX_MEM = 20  # 内存最高占用百分比

# 资源控制全局变量
arr = []
cpu_processes = []
stop_event = Event()

def cpu_worker(stop_event: Event, target_usage: float, core_id: int):
    """CPU密集型工作线程，绑定到指定核心"""
    try:
        p = psutil.Process()
        p.cpu_affinity([core_id])
        logging.debug(f"Process bound to core {core_id}")
    except Exception as e:
        logging.error(f"Error setting affinity: {e}")

    cycle_duration = 0.1  # 100ms周期
    compute_time = cycle_duration * target_usage / 100
    sleep_time = cycle_duration - compute_time

    while not stop_event.is_set():
        start = time.perf_counter()
        # 计算阶段
        while (time.perf_counter() - start) < compute_time:
            math.sqrt(123456789 ** 2)
        # 休眠阶段
        if sleep_time > 0:
            time.sleep(sleep_time)

def adjust_resources():
    """资源调整主循环"""
    global arr, cpu_processes, stop_event
    
    target_cpu = (MIN_CPU + MAX_CPU) / 2  # 每个核心的目标CPU占用
    physical_cores = psutil.cpu_count(logical=False)
    
    while True:
        # 获取系统资源使用情况
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        avg_cpu = sum(cpu_usage) / len(cpu_usage)
        mem = psutil.virtual_memory()
        
        logging.info(f"CPU Usage: {cpu_usage} (Avg: {avg_cpu:.1f}%) | "
                     f"Memory: {mem.percent}%")

        # CPU调整逻辑
        if avg_cpu < MIN_CPU and not cpu_processes:
            logging.info(f"Starting {physical_cores} CPU workers")
            stop_event.clear()
            for core in range(physical_cores):
                p = Process(target=cpu_worker,
                            args=(stop_event, target_cpu, core))
                p.start()
                cpu_processes.append(p)
        
        elif avg_cpu > MAX_CPU and cpu_processes:
            logging.info("Stopping CPU workers")
            stop_event.set()
            for p in cpu_processes:
                p.join()
            cpu_processes = []
            stop_event = Event()  # 重置事件

        # 内存调整逻辑
        target_mem = mem.total * (MIN_MEM + MAX_MEM) / 2 / 100
        current_mem = mem.total - mem.available
        
        if mem.percent < MIN_MEM:
            need_bytes = max(int(target_mem - current_mem), 0)
            elements = need_bytes // 8  # 64位整数占8字节
            arr.extend([0] * elements)
            logging.info(f"Added {need_bytes/(1024**2):.1f}MB memory")
        
        elif mem.percent > MAX_MEM:
            release_bytes = max(int(current_mem - target_mem), 0)
            elements = min(release_bytes // 8, len(arr))
            del arr[-elements:]
            logging.info(f"Released {release_bytes/(1024**2):.1f}MB memory")

if __name__ == "__main__":
    try:
        adjust_resources()
    except KeyboardInterrupt:
        stop_event.set()
        for p in cpu_processes:
            p.join()