#include <stdio.h>
#include <time.h>

unsigned long long sum_to_n(unsigned long long n) {
    unsigned long long total = 0;
    for (unsigned long long i = 1; i <= n; i++) {
        total += i;
    }
    return total;
}

int main() {
    unsigned long long n = 100000000;  // 100 milhões
    
    clock_t start = clock();
    unsigned long long result = sum_to_n(n);
    clock_t end = clock();
    
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    
    printf("C:\n");
    printf("Resultado: %llu\n", result);
    printf("Tempo de execução: %.4f segundos\n", time_spent);
    
    return 0;
}
