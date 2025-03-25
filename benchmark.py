import time

def sum_to_n(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def main():
    n = 100_000_000  # 100 milhões
    
    start_time = time.time()
    result = sum_to_n(n)
    end_time = time.time()
    
    print(f"Python:")
    print(f"Resultado: {result}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()