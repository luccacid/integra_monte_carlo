## Integração Numérica com Monte Carlo utilizando Threads

### Introdução

O cálculo de integrais, especialmente em dimensões altas, pode ser extremamente difícil e demorado usando métodos tradicionais. O **Método de Monte Carlo** é uma abordagem poderosa que usa **amostragem aleatória** para estimar integrais de funções complexas. Este método pode ser ainda mais eficiente quando combinado com **execução paralela** utilizando **threads** para acelerar o processo de cálculo.

### O Problema

Deseja-se calcular a seguinte integral definida:

$$
I = \int_{0}^{1} \int_{0}^{1} \dots \int_{0}^{1} e^{-\sum_{i=1}^n x_i^2} \,dx_1 dx_2 \dots dx_n
$$

A função a ser integrada é:

$$
f(x) = e^{-\sum_{i=1}^n x_i^2}
$$

E está sendo realizada a integração no domínio $[0,1]^n$, que é um **hipercubo** $n$-dimensional com lados de comprimento 1.

![Hipercubo 3D](hipercubo_3d.png)

### Método de Monte Carlo

O método de Monte Carlo para calcular integrais segue os seguintes passos básicos:

1. **Gerar pontos aleatórios** dentro do domínio de integração. No caso, isso significa gerar valores aleatórios para $x_1, x_2, ..., x_n$ no intervalo $[0, 1]$.
2. **Avaliar a função** nesses pontos aleatórios.
3. **Calcular a média** dos valores da função nos pontos gerados.
4. Multiplicar essa média pelo **volume do domínio**. No caso do hipercubo $[0,1]^n$, o volume é 1, pois é um quadrado (ou hipercubo) com comprimento de lado 1 em cada dimensão.

Assim, a integral é aproximada pela média dos valores da função nas amostras multiplicada pelo volume do domínio.

### A Fórmula para a Integral de Monte Carlo

Se $f(x)$ for a função a ser integrada em um domínio $D$ (no caso, o hipercubo $[0]^n$), a fórmula do Método de Monte Carlo é:

$$
I \approx \frac{1}{N} \sum_{i=1}^{N} f(x_i)
$$

onde $N$ é o número de pontos amostrados, e $x_i$ são pontos aleatórios dentro do domínio $D$.

### Função a Ser Integrada

No código original, a função $f(x)$ a ser integrada foi definida da seguinte forma:

```python
def f(x):
    """Função que queremos integrar."""
    return sum(-xi**2 for xi in x)
```

Aqui, a função $f(x)$ recebe um vetor de variáveis $x = [x_1, x_2, ..., x_n]$ e retorna $-\sum_{i=1}^n x_i^2$. Essa é a forma negativa da função gaussiana que está sendo integrada. O sinal negativo é utilizado porque a função foi escrita dessa forma no código original para aproximar a integral de uma função exponencial.

### Exemplos de Outras Funções

Aqui estão alguns exemplos de outras funções que poderiam ser usadas no lugar da função $f(x)$ para calcular a integral:

#### Exemplo 1: Função $f(x) = x_1 + x_2 + \dots + x_n$

Este é um exemplo simples de uma função linear, onde está sendo somado as variáveis $x_i$:

```python
def f(x):
    """Função linear simples."""
    return sum(x)  # Soma dos componentes x_i
```

#### Exemplo 2: Função $f(x) = x_1^2 + x_2^2 + \dots + x_n^2$

Neste caso, está sendo somado os quadrados das variáveis $x_i$:

```python
def f(x):
    """Função quadrática simples."""
    return sum(xi**2 for xi in x)  # Soma dos quadrados dos componentes
```

#### Exemplo 3: Função $f(x) = \sin(x_1 + x_2 + \dots + x_n)$

Este exemplo considera uma função trigonométrica que depende da soma das variáveis:

```python
import math

def f(x):
    """Função que soma as coordenadas e aplica o seno."""
    return math.sin(sum(x))  # Seno da soma das coordenadas
```

#### Exemplo 4: Função $f(x) = \cos(x_1 + x_2 + \dots + x_n)$

Neste caso, está sendo trabalhado com a função cosseno:

```python
import math

def f(x):
    """Função que soma as coordenadas e aplica o cosseno."""
    return math.cos(sum(x))  # Cosseno da soma das coordenadas
```

#### Exemplo 5: Função $f(x) = \tan(x_1 + x_2 + \dots + x_n)$

Aqui, está sendo considerada a função tangente:

```python
import math

def f(x):
    """Função que soma as coordenadas e aplica a tangente."""
    return math.tan(sum(x))  # Tangente da soma das coordenadas
```

#### Exemplo 6: Função $f(x) = e^{-(x_1 + x_2 + \dots + x_n)}$

Agora, está sendo trabalhada com uma função exponencial, que pode ser útil em diversos problemas de modelagem e física.

```python
import math

def f(x):
    """Função exponencial decaindo com a soma das coordenadas."""
    return math.exp(-sum(x))  # Exponencial decaindo com a soma das coordenadas
```

#### Exemplo 7: Função $f(x) = \prod_{i=1}^{n} x_i$

Aqui, está sendo considerada o produto das variáveis $x_1, x_2, ..., x_n$.

```python
def f(x):
    """Função produto das coordenadas."""
    result = 1
    for xi in x:
        result *= xi
    return result
```

#### Exemplo 8: Função $f(x) = 1$ (Função Constante)

Se a função $f(x)$ for uma constante, digamos 1, tem-se:

```python
def f(x):
    """Função constante 1."""
    return 1  # A função é constante, sempre 1
```

### Explicação do Código

Agora, é possível analisar o código passo a passo.

#### Importação das Bibliotecas

```python
import threading
import random
import time
import queue
```

- **`threading`**: A biblioteca `threading` é utilizada para criar e gerenciar múltiplas threads. No código, as threads são usadas para realizar o cálculo da integral em paralelo, dividindo o trabalho entre várias threads e, assim, acelerando a execução do código.
  
- **`random`**: A biblioteca `random` é responsável por gerar números aleatórios. Em nosso caso, ela é usada para gerar as coordenadas $x_i$ aleatórias para os pontos de amostragem dentro do intervalo $[0, 1]$.
  
- **`time`**: A biblioteca `time` é utilizada para medir o tempo de execução do código. No exemplo, utiliza-se o `time.time()` para registrar o tempo antes e depois da execução, permitindo calcular o tempo total de execução da integral.
  
- **`queue`**: A biblioteca `queue` é utilizada para gerenciar o armazenamento dos resultados de cada thread. A `queue.Queue()` permite que as threads armazenem seus resultados de forma segura e eficiente, para que os mesmos possam ser agregados no final da execução.

#### Função `monte_carlo_integral`

```python
def monte_carlo_integral(num_points, dimensions, result_queue, thread_id):
    """Avalia a integral via Monte Carlo."""
    print(f"Iniciando Thread {thread_id}...")
    inside_sum = 0
    for _ in range(num_points):
        point = [random.uniform(0, 1) for _ in range(dimensions)]
        inside_sum += f(point)
    result_queue.put(inside_sum / num_points)
    print(f"Encerrando Thread {thread_id}...")
```

Aqui está o que ocorre na função `monte_carlo_integral` linha por linha:

- **`def monte_carlo_integral(num_points, dimensions, result_queue, thread_id):`**  
  Define-se a função que realiza a integração via Monte Carlo. A função recebe quatro parâmetros:
  - `num_points`: o número de pontos a serem amostrados por esta thread.
  - `dimensions`: o número de dimensões do problema (no caso, o número de variáveis $x_i$).
  - `result_queue`: uma fila onde os resultados da thread serão armazenados.
  - `thread_id`: o identificador da thread, usado para impressão.

- **`print(f"Iniciando Thread {thread_id}...")`**  
  Imprime-se uma mensagem indicando que a thread foi iniciada.

- **`inside_sum = 0`**  
  Inicializa-se a variável `inside_sum`, que será usada para acumular a soma das avaliações da função $f(x)$.

- **`for _ in range(num_points):`**  
  Um loop que itera `num_points` vezes, amostrando um ponto aleatório para cada iteração.

- **`point = [random.uniform(0, 1) for _ in range(dimensions)]`**  
  Gera-se um ponto aleatório no domínio $[0, 1]^n$, onde `n` é o número de dimensões. A função `random.uniform(0, 1)` gera um número aleatório entre 0 e 1.

- **`inside_sum += f(point)`**  
  Avalia-se a função `f(x)` no ponto gerado e adiciona-se o valor à variável `inside_sum`.

- **`result_queue.put(inside_sum / num_points)`**  
  Após a soma, calcula-se a média e coloca-se o resultado na fila `result_queue`.

- **`print(f"Encerrando Thread {thread_id}...")`**  
  Imprime-se uma mensagem indicando que a thread terminou sua execução.

A função calcula a integral usando amostragem de Monte Carlo, acumulando os resultados em cada thread.

#### Função Principal

```python
def main():
    DIMENSIONS = 5   # Número de dimensões
    TOTAL_POINTS = 10_000_000  # Total de pontos
    NUM_THREADS = 10
    points_per_thread = TOTAL_POINTS // NUM_THREADS
    result_queue = queue.Queue()
    threads = []
    
    start_time = time.time()
```

A função `main` é onde a execução do código começa. Os parâmetros principais são definidos:

- **`DIMENSIONS`**: Representa-se o número de dimensões da integral. No exemplo, trabalha-se com 5 dimensões, mas este número pode ser alterado conforme

 necessário.
- **`TOTAL_POINTS`**: O número total de pontos a serem amostrados para a integral. Aqui, está sendo usado 10 milhões de pontos.
- **`NUM_THREADS`**: Número de threads a serem usadas. Aqui, utilizam-se 10 threads.
- **`points_per_thread`**: Divide-se o número total de pontos pelo número de threads, determinando quantos pontos cada thread deve processar.
  
A função também inicializa a fila `result_queue`, onde os resultados de cada thread serão armazenados, e a lista de threads.

#### Criação e Execução das Threads

```python
for thread_id in range(NUM_THREADS):
    thread = threading.Thread(
        target=monte_carlo_integral, 
        args=(points_per_thread, DIMENSIONS, result_queue, thread_id)
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

Aqui, cria-se e inicia-se cada thread. Para cada thread, chama-se a função `monte_carlo_integral` com os parâmetros apropriados. Depois, espera-se todas as threads terminarem utilizando o `join`.

#### Agregação dos Resultados

```python
integral_result = sum(result_queue.get() for _ in range(NUM_THREADS))
integral_result /= NUM_THREADS
```

Os resultados das threads são retirados da fila e somados, com a média final sendo calculada.

#### Exibição do Resultado

```python
end_time = time.time()
print(f"Resultado da Integral: {integral_result}")
print(f"Tempo de Execução: {end_time - start_time} segundos")
```

O resultado final da integral é impresso, juntamente com o tempo de execução.
