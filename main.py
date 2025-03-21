import threading
import random
import time
import queue

def f(x):
    """Função que queremos integrar."""
    return sum(-xi**2 for xi in x)

def monte_carlo_integral(num_points, dimensions, result_queue, thread_id):
    """Avalia a integral via Monte Carlo."""
    print(f"Iniciando Thread {thread_id}...")
    inside_sum = 0
    for _ in range(num_points):
        point = [random.uniform(0, 1) for _ in range(dimensions)]
        inside_sum += f(point)
    result_queue.put(inside_sum / num_points)
    print(f"Encerrando Thread {thread_id}...")

def main():
    DIMENSIONS = 5   # Número de dimensões
    TOTAL_POINTS = 10_000_000  # Total de pontos
    NUM_THREADS = 10
    
    points_per_thread = TOTAL_POINTS // NUM_THREADS
    result_queue = queue.Queue()
    threads = []
    
    start_time = time.time()
    
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=monte_carlo_integral, args=(points_per_thread, DIMENSIONS, result_queue, i+1))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    integral_estimate = sum(result_queue.get() for _ in range(NUM_THREADS)) / NUM_THREADS
    
    end_time = time.time()
    
    print(f"Estimativa da Integral: {integral_estimate:.6f}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
