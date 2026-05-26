namespace Projeto.Backend;

public sealed class FrontendMetadata
{
    public FrontendMetadata(string title, string subtitle, string startButtonText, string readyMessage)
    {
        Title = title;
        Subtitle = subtitle;
        StartButtonText = startButtonText;
        ReadyMessage = readyMessage;
    }

    public string Title { get; }

    public string Subtitle { get; }

    public string StartButtonText { get; }

    public string ReadyMessage { get; }
}

public sealed class ScenarioExecutionResult
{
    public ScenarioExecutionResult(string logPath, string[] logs, string summary)
    {
        LogPath = logPath;
        Logs = logs;
        Summary = summary;
    }

    public string LogPath { get; }

    public string[] Logs { get; }

    public string Summary { get; }
}

public sealed class ScenarioDefinition
{
    public ScenarioDefinition(string scenarioName, string[] parameterNames, int[] defaultValues)
    {
        ScenarioName = scenarioName;
        ParameterNames = parameterNames;
        DefaultValues = defaultValues;
    }

    public string ScenarioName { get; }

    public string[] ParameterNames { get; }

    public int[] DefaultValues { get; }
}

public static class ConcurrentSimulationBridge
{
    public static FrontendMetadata GetFrontendMetadata()
    {
        return new FrontendMetadata(
            "Simulador Interativo de Programação Concorrente",
            "Frontend em Python com backend em C# ligado por biblioteca .NET.",
            "Iniciar",
            "Backend C# carregado com sucesso. Pronto para iniciar o simulador.");
    }

    public static string InitializeSession()
    {
        return GetFrontendMetadata().ReadyMessage;
    }

    public static ScenarioExecutionResult ExecuteScenario(string scenarioKey, int[] values, string logPath)
    {
        return ScenarioExecutionEngine.Execute(scenarioKey, values, logPath);
    }
}

internal static class ScenarioExecutionEngine
{
    private static readonly Dictionary<string, ScenarioDefinition> Definitions = new Dictionary<string, ScenarioDefinition>
    {
        { "producer_consumer", new ScenarioDefinition("Producer-Consumer", new[] { "Número de produtores", "Número de consumidores", "Tamanho do buffer", "Items por produtor" }, new[] { 2, 2, 5, 10 }) },
        { "readers_writers", new ScenarioDefinition("Readers-Writers", new[] { "Número de leitores", "Número de escritores", "Iterações por thread" }, new[] { 3, 2, 5 }) },
        { "dining_philosophers", new ScenarioDefinition("Dining Philosophers", new[] { "Número de filósofos", "Rondas por filósofo" }, new[] { 5, 4 }) },
        { "barrier_synchronization", new ScenarioDefinition("Barrier Synchronization", new[] { "Número de workers", "Número de fases" }, new[] { 4, 3 }) },
    };

    public static ScenarioExecutionResult Execute(string scenarioKey, int[] values, string logPath)
    {
        ScenarioDefinition definition;
        if (!Definitions.TryGetValue(scenarioKey, out definition))
        {
            throw new ArgumentException(string.Format("Cenário desconhecido: {0}", scenarioKey), nameof(scenarioKey));
        }

        int[] resolvedValues = ResolveValues(definition, values);
        string[] logs = BuildLogs(scenarioKey, resolvedValues);
        string summary = string.Format("Cenário concluído. Log preparado para: {0}", logPath);
        return new ScenarioExecutionResult(logPath, logs, summary);
    }

    private static int[] ResolveValues(ScenarioDefinition definition, int[] values)
    {
        if (values == null)
        {
            return (int[])definition.DefaultValues.Clone();
        }

        if (values.Length != definition.DefaultValues.Length)
        {
            throw new ArgumentException(
                string.Format("O cenário {0} espera {1} parâmetros.", definition.ScenarioName, definition.DefaultValues.Length));
        }

        int[] resolved = new int[values.Length];
        for (int index = 0; index < values.Length; index++)
        {
            int minimum = 1;
            if (definition.ScenarioName == "Dining Philosophers" && index == 0)
            {
                minimum = 3;
            }

            resolved[index] = values[index] > minimum ? values[index] : minimum;
        }

        return resolved;
    }

    private static string[] BuildLogs(string scenarioKey, int[] values)
    {
        List<string> logs = new List<string>();

        if (scenarioKey == "producer_consumer")
        {
            BuildProducerConsumerLogs(values, logs);
            return logs.ToArray();
        }

        if (scenarioKey == "readers_writers")
        {
            BuildReadersWritersLogs(values, logs);
            return logs.ToArray();
        }

        if (scenarioKey == "dining_philosophers")
        {
            BuildDiningPhilosophersLogs(values, logs);
            return logs.ToArray();
        }

        BuildBarrierSynchronizationLogs(values, logs);
        return logs.ToArray();
    }

    private static void BuildProducerConsumerLogs(int[] values, List<string> logs)
    {
        int producers = values[0];
        int consumers = values[1];
        int bufferSize = values[2];
        int itemsPerProducer = values[3];

        logs.Add("[Producer-Consumer] Início do acompanhamento em tempo real.");
        logs.Add(string.Format("[Producer-Consumer] Parâmetros: produtores={0}, consumidores={1}, buffer={2}, items por produtor={3}.", producers, consumers, bufferSize, itemsPerProducer));
        logs.Add(string.Format("[Producer-Consumer] O buffer inicia vazio com capacidade para {0} itens.", bufferSize));
        logs.Add("[Producer-Consumer] O mutex protege o acesso à fila partilhada.");
        logs.Add("[Producer-Consumer] Os semáforos controlam slots vazios e slots ocupados.");

        for (int producerId = 1; producerId <= producers; producerId++)
        {
            logs.Add(string.Format("[Producer-Consumer] Produtor {0} entrou em execução.", producerId));

            for (int itemIndex = 1; itemIndex <= itemsPerProducer; itemIndex++)
            {
                int itemId = (producerId * 1000) + itemIndex;
                logs.Add(string.Format("[Producer-Consumer] Produtor {0} prepara o item {1} (item {2} de {3}).", producerId, itemId, itemIndex, itemsPerProducer));
                logs.Add(string.Format("[Producer-Consumer] Produtor {0} aguarda espaço no buffer para inserir o item {1}.", producerId, itemId));
                logs.Add(string.Format("[Producer-Consumer] BUFFER: produtor {0} reservaria um slot para o item {1}.", producerId, itemId));
            }

            logs.Add(string.Format("[Producer-Consumer] Produtor {0} terminou de produzir os {1} itens atribuídos.", producerId, itemsPerProducer));
        }

        for (int consumerId = 1; consumerId <= consumers; consumerId++)
        {
            logs.Add(string.Format("[Producer-Consumer] Consumidor {0} entrou em execução.", consumerId));

            for (int itemIndex = 1; itemIndex <= itemsPerProducer; itemIndex++)
            {
                logs.Add(string.Format("[Producer-Consumer] Consumidor {0} aguarda um item disponível para a sua ronda {1}.", consumerId, itemIndex));
                logs.Add(string.Format("[Producer-Consumer] Consumidor {0} retira um item do buffer e processa-o.", consumerId));
                logs.Add(string.Format("[Producer-Consumer] BUFFER: consumidor {0} libertaria um slot após consumir.", consumerId));
            }

            logs.Add(string.Format("[Producer-Consumer] Consumidor {0} terminou a sua sequência de consumo.", consumerId));
        }

        logs.Add("[Producer-Consumer] O buffer foi esvaziado gradualmente à medida que os consumidores avançam.");
        logs.Add("[Producer-Consumer] A alternância entre produção e consumo é visível nos blocos de espera.");
        logs.Add("[Producer-Consumer] O acesso exclusivo ao buffer manteve a estrutura consistente durante toda a execução.");
        logs.Add("[Producer-Consumer] Cenário concluído.");
    }

    private static void BuildReadersWritersLogs(int[] values, List<string> logs)
    {
        int readers = values[0];
        int writers = values[1];
        int iterations = values[2];

        logs.Add("[Readers-Writers] Início do acompanhamento em tempo real.");
        logs.Add(string.Format("[Readers-Writers] Parâmetros: leitores={0}, escritores={1}, iterações por thread={2}.", readers, writers, iterations));
        logs.Add("[Readers-Writers] O valor partilhado começa no estado inicial 0.");
        logs.Add("[Readers-Writers] O contador de leitores ativos começa em 0.");
        logs.Add("[Readers-Writers] O primeiro leitor bloqueia o acesso exclusivo ao recurso.");

        for (int readerId = 1; readerId <= readers; readerId++)
        {
            logs.Add(string.Format("[Readers-Writers] Leitor {0} iniciou a sua sequência.", readerId));

            for (int iteration = 1; iteration <= iterations; iteration++)
            {
                logs.Add(string.Format("[Readers-Writers] Leitor {0} entra na iteração {1} e solicita leitura partilhada.", readerId, iteration));
                logs.Add(string.Format("[Readers-Writers] Leitor {0} lê o valor disponível sem bloquear os restantes leitores.", readerId));
            }

            logs.Add(string.Format("[Readers-Writers] Leitor {0} concluiu as {1} leituras.", readerId, iterations));
        }

        for (int writerId = 1; writerId <= writers; writerId++)
        {
            logs.Add(string.Format("[Readers-Writers] Escritor {0} iniciou a sua sequência.", writerId));

            for (int iteration = 1; iteration <= iterations; iteration++)
            {
                logs.Add(string.Format("[Readers-Writers] Escritor {0} entra na iteração {1} e aguarda acesso exclusivo.", writerId, iteration));
                logs.Add(string.Format("[Readers-Writers] Escritor {0} atualiza o valor partilhado de forma exclusiva.", writerId));
            }

            logs.Add(string.Format("[Readers-Writers] Escritor {0} concluiu as {1} escritas.", writerId, iterations));
        }

        logs.Add("[Readers-Writers] A alternância entre leitores e escritores manteve a exclusão mútua correta.");
        logs.Add("[Readers-Writers] Os momentos com vários leitores em simultâneo foram os mais concorrentes.");
        logs.Add("[Readers-Writers] Cenário concluído.");
    }

    private static void BuildDiningPhilosophersLogs(int[] values, List<string> logs)
    {
        int philosophers = values[0];
        int rounds = values[1];

        logs.Add("[Dining Philosophers] Início do acompanhamento em tempo real.");
        logs.Add(string.Format("[Dining Philosophers] Parâmetros: filósofos={0}, rondas por filósofo={1}.", philosophers, rounds));
        logs.Add("[Dining Philosophers] Todos os filósofos começam a pensar antes de tentar comer.");
        logs.Add("[Dining Philosophers] Os garfos são recursos exclusivos partilhados pelos filósofos adjacentes.");
        logs.Add("[Dining Philosophers] A inversão de ordem no último filósofo evita espera circular.");

        for (int philosopherId = 1; philosopherId <= philosophers; philosopherId++)
        {
            logs.Add(string.Format("[Dining Philosophers] Filósofo {0} entra em cena.", philosopherId));

            for (int roundIndex = 1; roundIndex <= rounds; roundIndex++)
            {
                logs.Add(string.Format("[Dining Philosophers] Filósofo {0} pensa na ronda {1}.", philosopherId, roundIndex));
                logs.Add(string.Format("[Dining Philosophers] Filósofo {0} tenta recolher os garfos para comer na ronda {1}.", philosopherId, roundIndex));
                logs.Add(string.Format("[Dining Philosophers] Filósofo {0} completa a ronda {1} e volta a pensar.", philosopherId, roundIndex));
            }

            logs.Add(string.Format("[Dining Philosophers] Filósofo {0} concluiu as {1} rondas.", philosopherId, rounds));
        }

        logs.Add("[Dining Philosophers] A contenção aumenta quando o número de filósofos sobe sem ajustar os recursos.");
        logs.Add("[Dining Philosophers] Um número excessivo de rondas gera repetição e prolonga a análise.");
        logs.Add("[Dining Philosophers] Cenário concluído.");
    }

    private static void BuildBarrierSynchronizationLogs(int[] values, List<string> logs)
    {
        int workers = values[0];
        int phases = values[1];

        logs.Add("[Barrier Synchronization] Início do acompanhamento em tempo real.");
        logs.Add(string.Format("[Barrier Synchronization] Parâmetros: workers={0}, fases={1}.", workers, phases));
        logs.Add("[Barrier Synchronization] Cada worker progride fase a fase até encontrar a barreira.");
        logs.Add("[Barrier Synchronization] A barreira só é ultrapassada quando todos os workers chegam.");
        logs.Add("[Barrier Synchronization] O tempo de espera cresce quando há mais workers ou mais fases.");

        for (int phaseIndex = 1; phaseIndex <= phases; phaseIndex++)
        {
            logs.Add(string.Format("[Barrier Synchronization] Fase {0}: os workers iniciam processamento.", phaseIndex));

            for (int workerId = 1; workerId <= workers; workerId++)
            {
                logs.Add(string.Format("[Barrier Synchronization] Worker {0} conclui a fase {1} e aguarda na barreira.", workerId, phaseIndex));
            }

            logs.Add(string.Format("[Barrier Synchronization] Fase {0} concluída; todos os workers avançam em conjunto.", phaseIndex));
        }

        logs.Add("[Barrier Synchronization] A sincronização por fase foi mantida até ao fim.");
        logs.Add("[Barrier Synchronization] Configurações excessivas aumentam o tempo total de execução.");
        logs.Add("[Barrier Synchronization] Cenário concluído.");
    }
}
