# 🔧 Detalhes Técnicos das Mudanças

## 📝 Records para Configuração

Foram criados 4 records (tipos imutáveis) para armazenar os parâmetros de cada cenário:

```csharp
record ProducerConsumerConfig(int Producers, int Consumers, int BufferSize, int ItemsPerProducer);
record ReadersWritersConfig(int Readers, int Writers, int IterationsPerThread);
record DiningPhilosophersConfig(int Philosophers, int RoundsPerPhilosopher);
record BarrierSynchronizationConfig(int Workers, int Phases);
```

### Vantagens dos Records
- Imutabilidade garantida
- Igualdade estrutural automática
- Sintaxe concisa e clara
- Type-safe

---

## 🔨 Funções de Configuração

Cada cenário tem uma função dedicada para obter parâmetros do utilizador:

```csharp
static ProducerConsumerConfig GetProducerConsumerConfig()
{
    Console.Clear();
    Console.WriteLine("=== Configuracao: Producer-Consumer ===");
    
    int producers = GetPositiveInt("Numero de produtores (padrao: 2): ", 2);
    int consumers = GetPositiveInt("Numero de consumidores (padrao: 2): ", 2);
    // ... mais parâmetros ...
    
    return new ProducerConsumerConfig(producers, consumers, bufferSize, itemsPerProducer);
}
```

### Função Auxiliar `GetPositiveInt`
```csharp
static int GetPositiveInt(string prompt, int defaultValue)
{
    while (true)
    {
        Console.Write(prompt);
        string? input = Console.ReadLine()?.Trim();

        if (string.IsNullOrEmpty(input))
            return defaultValue;

        if (int.TryParse(input, out int value) && value > 0)
            return value;

        Console.WriteLine("Entrada invalida...");
    }
}
```

**Características:**
- Validação de entrada (apenas números positivos)
- Valores por defeito quando entrada vazia
- Loop até entrada válida

---

## 📊 Producer-Consumer Melhorado

### Mudanças Principais

#### 1. **Múltiplos Produtores e Consumidores**
```csharp
Thread[] producers = new Thread[config.Producers];
for (int p = 0; p < config.Producers; p++)
{
    int producerId = p + 1;  // ID único para cada produtor
    producers[p] = new Thread(() => { ... });
}
```

#### 2. **Identificadores Únicos**
```csharp
int itemId = (producerId * 1000) + i;  // Ex: 1001, 1002 para produtor 1
logger.Log($"[Produtor {producerId}] ..."); // Identificação clara
```

#### 3. **Controle de Consumo**
```csharp
int consumedCount = 0;
while (consumedCount < totalItemsToConsume)
{
    // ... consumir item ...
    consumedCount++;  // Contar itens consumidos
}
```

### Logs Expandidos
- Antes: ~20 linhas de log
- Depois: 100-500 linhas (dependendo dos parâmetros)

**Exemplo de Log:**
```
[Produtor 1] inicializando...
[Produtor 1] tentativa de produzir item=1001. Aguardando slot vazio...
[Produtor 1] slot vazio reservado para item=1001. Aguardando mutex...
[Produtor 1] produziu item=1001 | ocupacao=1/5 | buffer=[ 1001] [   ] [   ] [   ] [   ]
[Produtor 1] mutex libertado apos inserir item=1001. Sinalizando filledSlots.
```

---

## 👥 Readers-Writers Melhorado

### Mudanças Principais

#### 1. **Múltiplos Leitores e Escritores**
```csharp
Thread[] writers = new Thread[config.Writers];
Thread[] readers = new Thread[config.Readers];
```

#### 2. **Iterações Configuráveis**
```csharp
for (int i = 1; i <= config.IterationsPerThread; i++)
{
    // ... cada iteração é registada ...
}
```

#### 3. **Logging Detalhado de Sincronização**
```csharp
if (readersCount == 1)
{
    logger.Log($"[Leitor {readerId}] PRIMEIRO LEITOR - bloqueando resourceAccess...");
    resourceAccess.Wait();
}

// ... leitura ...

if (readersCount == 0)
{
    logger.Log($"[Leitor {readerId}] ULTIMO LEITOR - libertando resourceAccess...");
    resourceAccess.Release();
}
```

---

## 🍽️ Dining Philosophers Melhorado

### Mudanças Principais

#### 1. **Filósofos Configuráveis**
```csharp
object[] forks = Enumerable.Range(0, config.Philosophers)
    .Select(_ => new object())
    .ToArray();
```

#### 2. **Rondas Configuráveis**
```csharp
for (int round = 1; round <= config.RoundsPerPhilosopher; round++)
{
    // ... cada ronda é registada em detalhe ...
}
```

#### 3. **Anti-Deadlock Estratégico**
```csharp
if (id == config.Philosophers - 1)
{
    // Último filósofo pega direito primeiro
    lock (forks[rightFork])
    {
        lock (forks[leftFork])
        {
            logger.Log($"ESTADO=COMER (garfos {rightFork} e {leftFork})");
        }
    }
}
else
{
    // Outros pegam esquerdo primeiro
    lock (forks[leftFork]) { ... }
}
```

---

## 🚧 Barrier Synchronization Melhorado

### Mudanças Principais

#### 1. **Workers Configuráveis**
```csharp
using Barrier barrier = new(config.Workers, phase =>
{
    logger.Log($"===== BARREIRA: Todas as {config.Workers} threads... =====");
});
```

#### 2. **Fases Configuráveis**
```csharp
for (int phase = 0; phase < config.Phases; phase++)
{
    logger.Log($"[Worker {id}] fase {phase}: inicio...");
    int workDuration = Random.Shared.Next(200, 600);
    Thread.Sleep(workDuration);
    logger.Log($"[Worker {id}] fase {phase}: concluida, aguardando...");
    
    barrier.SignalAndWait();  // Sincronizar
    
    logger.Log($"[Worker {id}] fase {phase}: DESBLOQUEADO!");
}
```

---

## 📝 Sistema de Logging Melhorado

### Classe `ScenarioLogger`

```csharp
sealed class ScenarioLogger : IDisposable
{
    private sealed record LogEntry(string Message, string Line);
    
    private readonly object _sync = new();
    private readonly StreamWriter _writer;
    private readonly List<LogEntry> _entries = [];
    
    public void Log(string message)
    {
        string line = $"[{DateTime.Now:HH:mm:ss.fff}] {message}";
        lock (_sync)  // Thread-safe
        {
            _entries.Add(new LogEntry(message, line));
            _writer.WriteLine(line);
        }
    }
}
```

### Características Principais

#### 1. **Thread-Safety**
```csharp
lock (_sync)  // Protege acesso simultâneo
{
    _entries.Add(new LogEntry(message, line));
    _writer.WriteLine(line);
}
```

#### 2. **Timestamps Precisos**
```csharp
string line = $"[{DateTime.Now:HH:mm:ss.fff}] {message}";
// Resultado: [14:02:36.036] === Inicio...
```

#### 3. **Apresentação Interativa**
```csharp
public void PresentLogsInteractively()
{
    // Filtra logs informativos
    List<LogEntry> algorithmLogs = [.. snapshot.Where(static entry => 
        IsAlgorithmInformative(entry.Message))];
    
    // Apresenta linha por linha com confirmação
    for (int i = 0; i < algorithmLogs.Count; i++)
    {
        Console.WriteLine(algorithmLogs[i].Line);
        // Aguarda input para próxima linha
    }
}
```

#### 4. **Filtragem de Logs**
```csharp
private static bool IsAlgorithmInformative(string message)
{
    // Filtra linhas não informativas (headers, arquitetura, etc)
    return !message.StartsWith("===") &&
           !message.StartsWith("- ") &&
           !message.StartsWith("PARAMETROS:") &&
           // ... mais condições ...
}
```

---

## 🏗️ Estrutura do Código

### Organização
```
Program.cs
├── Records (configuração)
├── Main()
│   └── Loop Menu
├── Funções Configuração
│   ├── GetProducerConsumerConfig()
│   ├── GetReadersWritersConfig()
│   ├── GetDiningPhilosophersConfig()
│   └── GetBarrierSynchronizationConfig()
├── Funções Cenários
│   ├── RunProducerConsumer()
│   ├── RunReadersWriters()
│   ├── RunDiningPhilosophers()
│   └── RunBarrierSynchronization()
├── Funções Auxiliares
│   ├── GetPositiveInt()
│   ├── RenderBufferBoxes()
│   ├── CreateScenarioLogger()
│   ├── ResolveLogsDirectory()
│   └── Pause()
└── ScenarioLogger (classe aninhada)
```

---

## 🚀 Performance e Escalabilidade

### Impacto de Parâmetros

| Cenário | Parâmetro | Linhas de Log |
|---------|-----------|--------------|
| P-C | 1P, 1C | ~50 |
| P-C | 3P, 3C | ~200 |
| P-C | 5P, 5C | ~400 |
| R-W | 2L, 2E | ~100 |
| R-W | 5L, 5E | ~300 |
| DP | 5F | ~80 |
| DP | 10F | ~200 |
| BS | 4W, 3F | ~100 |
| BS | 8W, 5F | ~300 |

### Memory Management

- Uso de `List<LogEntry>` para cache de logs em memória
- `StreamWriter` com `AutoFlush = true` para garantir escrita imediata
- `using` statements para limpeza automática de recursos

---

## 🔐 Segurança e Robustez

### Thread-Safety
- Locks para proteger `readersCount` e `buffer`
- SemaphoreSlim para coordenação
- Barrier para sincronização de fases

### Validação de Entrada
- Números positivos apenas
- Filósofos mínimo 3
- Valores por defeito sensatos

### Tratamento de Erros
- Try-catch implícito via framework
- IDisposable para limpeza automática
- Null-coalescing para strings

---

## 📊 Comparação Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Produtores | 1 (fixo) | N configurável |
| Consumidores | 1 (fixo) | N configurável |
| Leitores | 2 (fixo) | N configurável |
| Escritores | 1 (fixo) | N configurável |
| Filósofos | 5 (fixo) | 3-N configurável |
| Workers | 3 (fixo) | N configurável |
| Linhas Log | 20-100 | 100-500+ |
| Parâmetros Vistos | Não | Sim (primeira linha) |
| Customização | Nenhuma | Completa |

