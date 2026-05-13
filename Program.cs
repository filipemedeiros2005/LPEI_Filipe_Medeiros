using System.Collections.Concurrent;
using System.Threading;
using System.Text;

while (true)
{
    Console.Clear();
    Console.WriteLine("Menu de cenarios concorrentes");
    Console.WriteLine("1 - Producer-Consumer");
    Console.WriteLine("2 - Readers-Writers");
    Console.WriteLine("3 - Dining Philosphers");
    Console.WriteLine("4 - Barrier Synchronization / Thread Coordination");
    Console.WriteLine("0 - sair");
    Console.Write("Escolha uma opcao: ");

    string? choice = Console.ReadLine();

    switch (choice)
    {
        case "1":
            RunProducerConsumer();
            break;
        case "2":
            RunReadersWriters();
            break;
        case "3":
            RunDiningPhilosophers();
            break;
        case "4":
            RunBarrierSynchronization();
            break;
        case "0":
            return;
        default:
            Console.WriteLine("Opcao invalida.");
            Pause();
            break;
    }
}

static void RunProducerConsumer()
{
    Console.Clear();
    Console.WriteLine("Producer-Consumer (1 produtor, 1 consumidor, buffer limitado)");

    const int bufferLimit = 5;
    const int totalItems = 10;

    var buffer = new Queue<int>();
    // mutex protege o acesso exclusivo a estrutura do buffer. Só aceita um item
    var mutex = new SemaphoreSlim(1, 1);
    // emptySlots e filledSlots modelam o numero de posicoes livres/ocupadas.
    var emptySlots = new SemaphoreSlim(bufferLimit, bufferLimit);
    var filledSlots = new SemaphoreSlim(0, bufferLimit);

    using var logger = CreateScenarioLogger("Producer-Consumer");
    logger.Log("=== Inicio do cenario Producer-Consumer ===");
    logger.Log("Arquitetura do sistema:");
    logger.Log("- Componente Produtor: gera itens e tenta inseri-los no buffer limitado.");
    logger.Log("- Componente Consumidor: remove itens do buffer e processa-os.");
    logger.Log("- Buffer partilhado: fila FIFO com capacidade fixa.");
    logger.Log("- Sincronizacao: mutex para exclusao mutua + semaforos de slots vazios/ocupados.");
    logger.Log("Algoritmo de sincronizacao:");
    logger.Log("1) Produtor espera em emptySlots antes de escrever no buffer.");
    logger.Log("2) Consumidor espera em filledSlots antes de ler do buffer.");
    logger.Log("3) O mutex garante que apenas uma thread altera a fila por vez.");
    logger.Log($"Estado inicial do buffer: {RenderBufferBoxes(buffer, bufferLimit)}");

    void LogBufferState(string actor, string action, int item)
    {
        logger.Log($"[{actor}] {action} item={item} | ocupacao={buffer.Count}/{bufferLimit} | buffer={RenderBufferBoxes(buffer, bufferLimit)}");
    }

    Thread producer = new(() =>
    {
        for (int i = 1; i <= totalItems; i++)
        {
            // So produz quando existe pelo menos um slot livre.
            logger.Log($"[Produtor] tentativa de produzir item={i}. Aguardando slot vazio...");
            emptySlots.Wait();
            logger.Log($"[Produtor] slot vazio reservado para item={i}. Aguardando mutex...");
            mutex.Wait();

            buffer.Enqueue(i);
            LogBufferState("Produtor", "produziu", i);

            mutex.Release();
            logger.Log($"[Produtor] mutex libertado apos inserir item={i}. Sinalizando filledSlots.");
            filledSlots.Release();
            Thread.Sleep(200);
        }

        logger.Log("[Produtor] terminou a producao de todos os itens.");
    });

    Thread consumer = new(() =>
    {
        for (int i = 1; i <= totalItems; i++)
        {
            // So consome quando existe pelo menos um item no buffer.
            logger.Log("[Consumidor] tentativa de consumir. Aguardando item disponivel...");
            filledSlots.Wait();
            logger.Log("[Consumidor] item disponivel confirmado. Aguardando mutex...");
            mutex.Wait();

            int item = buffer.Dequeue();
            LogBufferState("Consumidor", "consumiu", item);

            mutex.Release();
            logger.Log($"[Consumidor] mutex libertado apos remover item={item}. Sinalizando emptySlots.");
            emptySlots.Release();
            Thread.Sleep(300);
        }

        logger.Log("[Consumidor] terminou o consumo de todos os itens.");
    });

    logger.Log("Inicializacao de threads: produtor e consumidor vao arrancar em paralelo.");
    producer.Start();
    consumer.Start();
    logger.Log("Threads iniciadas. A sincronizacao agora depende dos semaforos e mutex.");
    producer.Join();
    consumer.Join();

    logger.Log($"Estado final do buffer: {RenderBufferBoxes(buffer, bufferLimit)}");
    logger.Log("=== Fim do cenario Producer-Consumer ===");
    Console.WriteLine("Fim do cenario Producer-Consumer.");
    Console.WriteLine($"Log guardado em: {logger.LogPath}");
    logger.PresentLogsInteractively();
}

static void RunReadersWriters()
{
    Console.Clear();
    Console.WriteLine("Readers-Writers (2 leitores, 1 escritor)");

    int sharedValue = 0;
    int readersCount = 0;
    // Protege a variavel readersCount para atualizacoes atomicas.
    var readersCountMutex = new SemaphoreSlim(1, 1);
    // Controla acesso ao recurso partilhado: escritor exclusivo ou leitores em grupo.
    var resourceAccess = new SemaphoreSlim(1, 1);

    using var logger = CreateScenarioLogger("Readers-Writers");
    logger.Log("=== Inicio do cenario Readers-Writers ===");
    logger.Log("Arquitetura do sistema:");
    logger.Log("- Um escritor atualiza o estado partilhado com acesso exclusivo.");
    logger.Log("- Dois leitores consultam o estado de forma concorrente.");
    logger.Log("- readersCount rastreia quantos leitores estao ativos no momento.");
    logger.Log("- readersCountMutex protege a contabilizacao de leitores ativos.");
    logger.Log("- resourceAccess representa o lock do recurso partilhado.");
    logger.Log("Algoritmo usado:");
    logger.Log("1) O primeiro leitor bloqueia o recurso para impedir escrita concorrente.");
    logger.Log("2) Leitores seguintes entram sem bloquear uns aos outros.");
    logger.Log("3) O ultimo leitor liberta o recurso para permitir ao escritor continuar.");

    Thread writer = new(() =>
    {
        for (int i = 1; i <= 5; i++)
        {
            logger.Log($"[Escritor] ciclo={i}: aguardando acesso exclusivo ao recurso...");
            resourceAccess.Wait();
            sharedValue++;
            logger.Log($"[Escritor] ciclo={i}: escreveu valor={sharedValue}.");
            Thread.Sleep(250);
            resourceAccess.Release();
            logger.Log($"[Escritor] ciclo={i}: libertou acesso exclusivo ao recurso.");

            Thread.Sleep(200);
        }

        logger.Log("[Escritor] terminou todas as escritas.");
    });

    Thread reader1 = new(() => ReaderTask("Leitor 1"));
    Thread reader2 = new(() => ReaderTask("Leitor 2"));

    void ReaderTask(string name)
    {
        for (int i = 1; i <= 5; i++)
        {
            logger.Log($"[{name}] ciclo={i}: a solicitar entrada na secao de leitores...");
            readersCountMutex.Wait();
            readersCount++;
            logger.Log($"[{name}] ciclo={i}: readersCount incrementado para {readersCount}.");
            // Primeiro leitor bloqueia o escritor enquanto houver leitores ativos.
            if (readersCount == 1)
            {
                logger.Log($"[{name}] ciclo={i}: primeiro leitor, a bloquear resourceAccess.");
                resourceAccess.Wait();
            }
            readersCountMutex.Release();

            logger.Log($"[{name}] ciclo={i}: leu valor={sharedValue}.");
            Thread.Sleep(150);

            readersCountMutex.Wait();
            readersCount--;
            logger.Log($"[{name}] ciclo={i}: readersCount decrementado para {readersCount}.");
            // Ultimo leitor liberta o recurso para o escritor prosseguir.
            if (readersCount == 0)
            {
                logger.Log($"[{name}] ciclo={i}: ultimo leitor, a libertar resourceAccess.");
                resourceAccess.Release();
            }
            readersCountMutex.Release();

            Thread.Sleep(180);
        }

        logger.Log($"[{name}] terminou todas as leituras.");
    }

    logger.Log("Inicializacao: escritor e leitores vao arrancar em paralelo.");
    writer.Start();
    reader1.Start();
    reader2.Start();

    writer.Join();
    reader1.Join();
    reader2.Join();

    logger.Log($"Estado final partilhado: sharedValue={sharedValue}, readersCount={readersCount}.");
    logger.Log("=== Fim do cenario Readers-Writers ===");
    Console.WriteLine("Fim do cenario Readers-Writers.");
    Console.WriteLine($"Log guardado em: {logger.LogPath}");
    logger.PresentLogsInteractively();
}

static void RunDiningPhilosophers()
{
    Console.Clear();
    Console.WriteLine("Dining Philosophers (versao simples)");

    const int philosopherCount = 5;
    object[] forks = Enumerable.Range(0, philosopherCount).Select(_ => new object()).ToArray();
    Thread[] philosophers = new Thread[philosopherCount];

    using var logger = CreateScenarioLogger("Dining-Philosophers");
    logger.Log("=== Inicio do cenario Dining Philosophers ===");
    logger.Log("Arquitetura do sistema:");
    logger.Log("- 5 filosofos (threads) alternam entre pensar e comer.");
    logger.Log("- 5 garfos (locks) representam recursos exclusivos partilhados.");
    logger.Log("- Cada filosofo precisa de 2 garfos adjacentes para comer.");
    logger.Log("Estrategia de prevencao de deadlock:");
    logger.Log("- Filosofos 0..3 apanham primeiro o garfo esquerdo e depois o direito.");
    logger.Log("- O ultimo filosofo (id=4) inverte a ordem para quebrar espera circular.");

    for (int i = 0; i < philosopherCount; i++)
    {
        int id = i;
        philosophers[i] = new Thread(() =>
        {
            int leftFork = id;
            int rightFork = (id + 1) % philosopherCount;

            for (int round = 1; round <= 3; round++)
            {
                logger.Log($"[Filosofo {id}] ronda={round}: estado=PENSAR.");
                Thread.Sleep(200);

                // O ultimo filosofo pega os garfos em ordem inversa para evitar deadlock.
                if (id == philosopherCount - 1)
                {
                    logger.Log($"[Filosofo {id}] ronda={round}: tenta bloquear garfo direito={rightFork}.");
                    lock (forks[rightFork])
                    {
                        logger.Log($"[Filosofo {id}] ronda={round}: bloqueou garfo direito={rightFork}; tenta esquerdo={leftFork}.");
                        lock (forks[leftFork])
                        {
                            logger.Log($"[Filosofo {id}] ronda={round}: estado=COMER (garfos {rightFork} e {leftFork}).");
                            Thread.Sleep(200);
                        }
                    }
                }
                else
                {
                    logger.Log($"[Filosofo {id}] ronda={round}: tenta bloquear garfo esquerdo={leftFork}.");
                    lock (forks[leftFork])
                    {
                        logger.Log($"[Filosofo {id}] ronda={round}: bloqueou garfo esquerdo={leftFork}; tenta direito={rightFork}.");
                        lock (forks[rightFork])
                        {
                            logger.Log($"[Filosofo {id}] ronda={round}: estado=COMER (garfos {leftFork} e {rightFork}).");
                            Thread.Sleep(200);
                        }
                    }
                }

                logger.Log($"[Filosofo {id}] ronda={round}: terminou e libertou ambos os garfos.");
            }

            logger.Log($"[Filosofo {id}] terminou todas as rondas.");
        });
    }

    logger.Log("Inicializacao: todos os filosofos vao arrancar em paralelo.");
    foreach (Thread philosopher in philosophers)
    {
        philosopher.Start();
    }

    foreach (Thread philosopher in philosophers)
    {
        philosopher.Join();
    }

    logger.Log("=== Fim do cenario Dining Philosophers ===");
    Console.WriteLine("Fim do cenario Dining Philosophers.");
    Console.WriteLine($"Log guardado em: {logger.LogPath}");
    logger.PresentLogsInteractively();
}

static void RunBarrierSynchronization()
{
    Console.Clear();
    Console.WriteLine("Barrier Synchronization / Thread Coordination");

    const int workers = 3;

    using var logger = CreateScenarioLogger("Barrier-Synchronization");
    logger.Log("=== Inicio do cenario Barrier Synchronization ===");
    logger.Log("Arquitetura do sistema:");
    logger.Log("- 3 workers executam o trabalho em duas fases.");
    logger.Log("- Uma Barrier coordena o ponto de encontro ao fim de cada fase.");
    logger.Log("- Nenhuma thread avanca para a proxima fase sem sincronizacao global.");
    logger.Log("Algoritmo de coordenacao por fases:");
    logger.Log("1) Cada worker executa fase 1 e chama SignalAndWait().");
    logger.Log("2) A ultima thread a chegar desbloqueia todas para a fase seguinte.");
    logger.Log("3) O processo repete-se para a fase 2.");

    // A barrier permite que todas as threads avancem em "fases" sincronizadas.
    using Barrier barrier = new(workers, phase =>
    {
        logger.Log($"--- Todas as threads terminaram a fase {phase.CurrentPhaseNumber}. ---");
    });

    Thread[] threads = new Thread[workers];

    for (int i = 0; i < workers; i++)
    {
        int id = i + 1;
        threads[i] = new Thread(() =>
        {
            logger.Log($"[Thread {id}] fase 1: inicio de processamento.");
            Thread.Sleep(Random.Shared.Next(200, 600));
            logger.Log($"[Thread {id}] fase 1: concluida, a aguardar sincronizacao.");
            // Todas bloqueiam aqui ate a ultima thread chegar ao ponto de sincronizacao.
            barrier.SignalAndWait();

            logger.Log($"[Thread {id}] fase 2: inicio de processamento.");
            Thread.Sleep(Random.Shared.Next(200, 600));
            logger.Log($"[Thread {id}] fase 2: concluida, a aguardar sincronizacao final.");
            barrier.SignalAndWait();

            logger.Log($"[Thread {id}] terminou todas as fases e saiu.");
        });
    }

    logger.Log("Inicializacao: workers vao arrancar em paralelo e sincronizar por fases.");
    foreach (Thread thread in threads)
    {
        thread.Start();
    }

    foreach (Thread thread in threads)
    {
        thread.Join();
    }

    logger.Log("=== Fim do cenario Barrier Synchronization ===");
    Console.WriteLine("Fim do cenario Barrier Synchronization.");
    Console.WriteLine($"Log guardado em: {logger.LogPath}");
    logger.PresentLogsInteractively();
}

static string RenderBufferBoxes(Queue<int> buffer, int limit)
{
    int[] snapshot = buffer.ToArray();
    var sb = new StringBuilder();

    for (int i = 0; i < limit; i++)
    {
        if (i < snapshot.Length)
        {
            sb.Append($"[{snapshot[i],2}]");
        }
        else
        {
            sb.Append("[  ]");
        }

        if (i < limit - 1)
        {
            sb.Append(' ');
        }
    }

    return sb.ToString();
}

static ScenarioLogger CreateScenarioLogger(string scenarioName)
{
    string logsDirectory = ResolveLogsDirectory();
    Directory.CreateDirectory(logsDirectory);

    string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
    string fileName = $"{scenarioName}_{timestamp}.txt";
    string path = Path.Combine(logsDirectory, fileName);

    return new ScenarioLogger(path);
}

static string ResolveLogsDirectory()
{
    string[] startPoints = [
        Directory.GetCurrentDirectory(),
        AppContext.BaseDirectory
    ];

    foreach (string startPoint in startPoints)
    {
        DirectoryInfo? current = new(Path.GetFullPath(startPoint));

        while (current is not null)
        {
            bool hasSolution = current.GetFiles("*.sln").Length > 0;
            bool hasProject = current.GetFiles("*.csproj").Length > 0;

            if (hasSolution || hasProject)
            {
                return Path.Combine(current.FullName, "logs");
            }

            current = current.Parent;
        }
    }

    // Fallback se nao for possivel detetar a raiz do projeto.
    return Path.Combine(Directory.GetCurrentDirectory(), "logs");
}

static void Pause()
{
    Console.WriteLine();
    Console.WriteLine("Prima ENTER para voltar ao menu...");
    Console.ReadLine();
}

sealed class ScenarioLogger : IDisposable
{
    private sealed record LogEntry(string Message, string Line);

    private readonly object _sync = new();
    private readonly StreamWriter _writer;
    private readonly List<LogEntry> _entries = [];

    public string LogPath { get; }

    public ScenarioLogger(string logPath)
    {
        LogPath = logPath;
        _writer = new StreamWriter(LogPath, append: false, encoding: Encoding.UTF8)
        {
            AutoFlush = true
        };
    }

    public void Log(string message)
    {
        string line = $"[{DateTime.Now:HH:mm:ss.fff}] {message}";

        lock (_sync)
        {
            _entries.Add(new LogEntry(message, line));
            _writer.WriteLine(line);
        }
    }

    public void PresentLogsInteractively()
    {
        List<LogEntry> snapshot;

        lock (_sync)
        {
            snapshot = [.. _entries];
        }

        List<LogEntry> algorithmLogs = [.. snapshot.Where(static entry => IsAlgorithmInformative(entry.Message))];

        if (algorithmLogs.Count == 0)
        {
            Console.WriteLine("Nao existem logs informativos do algoritmo para apresentar.");
            return;
        }

        Console.WriteLine();
        Console.WriteLine("Apresentacao guiada de logs do algoritmo:");

        for (int i = 0; i < algorithmLogs.Count; i++)
        {
            Console.WriteLine(algorithmLogs[i].Line);

            if (i == algorithmLogs.Count - 1)
            {
                Console.WriteLine("Fim da apresentacao de logs.");
                break;
            }

            while (true)
            {
                Console.WriteLine("1. continuar");
                Console.WriteLine("0. sair");
                Console.Write("Escolha uma opcao: ");

                string? choice = Console.ReadLine()?.Trim();
                if (choice == "1")
                {
                    break;
                }

                if (choice == "0")
                {
                    Console.WriteLine("Apresentacao de logs terminada pelo utilizador.");
                    return;
                }

                Console.WriteLine("Opcao invalida.");
            }
        }
    }

    private static bool IsAlgorithmInformative(string message)
    {
        if (message.StartsWith("===", StringComparison.Ordinal))
        {
            return false;
        }

        if (message.Equals("Arquitetura do sistema:", StringComparison.Ordinal))
        {
            return false;
        }

        if (message.StartsWith("- ", StringComparison.Ordinal))
        {
            return false;
        }

        if (message.StartsWith("Algoritmo", StringComparison.Ordinal))
        {
            return false;
        }

        if (message.StartsWith("Estrategia", StringComparison.Ordinal))
        {
            return false;
        }

        if (message.StartsWith("Inicializacao:", StringComparison.Ordinal))
        {
            return false;
        }

        return true;
    }

    public void Dispose()
    {
        _writer.Dispose();
    }
}
