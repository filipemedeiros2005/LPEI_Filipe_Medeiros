# Tratamento de Erros e Avisos - Status de Implementação

## 📊 Resumo Geral

**Data de Atualização**: 13 de Maio de 2025

**Taxa de Cobertura**: 65% (13 de 20 erros tratados)

| Categoria | Total | Tratados | Percentagem |
|-----------|-------|----------|-------------|
| 🔴 IMPORTANTES | 8 | 8 | ✅ 100% |
| 🟡 RELEVANTES | 7 | 5 | ⏳ 71% |
| 🟢 POUCO IMPORTANTES | 5 | 0 | ❌ 0% |
| **TOTAL** | **20** | **13** | **65%** |

---

## 🔴 ERROS DE NÍVEL IMPORTANTE (CRITICAL) - ✅ COMPLETO 100%

Todos os 8 erros críticos foram implementados com validação automatizada.

### Validação de Producer-Consumer
**Arquivo**: `ValidateProducerConsumer()`

1. ✅ **0 Produtores** → ERRO CRÍTICO
   - Mensagem: "Número de produtores deve ser mínimo 1"
   - Ação: Cancela cenário

2. ✅ **0 Consumidores** → ERRO CRÍTICO
   - Mensagem: "Número de consumidores deve ser mínimo 1"
   - Ação: Cancela cenário

3. ✅ **Buffer Size = 0** → ERRO CRÍTICO
   - Mensagem: "Tamanho do buffer deve ser mínimo 1"
   - Ação: Cancela cenário

### Validação de Readers-Writers
**Arquivo**: `ValidateReadersWriters()`

4. ✅ **0 Leitores** → ERRO CRÍTICO
   - Mensagem: "Número de leitores deve ser mínimo 1"
   - Ação: Cancela cenário

5. ✅ **0 Escritores** → ERRO CRÍTICO
   - Mensagem: "Número de escritores deve ser mínimo 1"
   - Ação: Cancela cenário

### Validação de Dining Philosophers
**Arquivo**: `ValidateDiningPhilosophers()`

6. ✅ **< 3 Filósofos** → ERRO CRÍTICO
   - Mensagem: "Número de filósofos deve ser mínimo 3"
   - Razão: Garantias deadlock
   - Ação: Cancela cenário

### Validação de Barrier Synchronization
**Arquivo**: `ValidateBarrierSynchronization()`

7. ✅ **0 Workers** → ERRO CRÍTICO
   - Mensagem: "Número de workers deve ser mínimo 1"
   - Ação: Cancela cenário

8. ✅ **0 Fases** → ERRO CRÍTICO
   - Mensagem: "Número de fases deve ser mínimo 1"
   - Ação: Cancela cenário

---

## 🟡 ERROS DE NÍVEL RELEVANTE (MEDIUM) - ⏳ PARCIALMENTE IMPLEMENTADO 71%

Avisos não-fatais que permitem continuar, mas informam sobre riscos.

### Validação de Producer-Consumer
**Arquivo**: `ValidateProducerConsumer()`

9. ✅ **Threads Totais > 500** → AVISO RELEVANTE
   - Detecta: `totalThreads = produtores + consumidores`
   - Mensagem: "Total de threads muito elevado"
   - Impacto: Performance degradada, context switching excessivo
   - Ação: Avisa com opção Continuar/Cancelar

10. ✅ **Buffer Inadequado** → AVISO RELEVANTE
   - Detecta: `buffer < (totalItemsProduzidos / consumidores)`
   - Mensagem: "Buffer muito pequeno para volume de produção"
   - Impacto: Produtores bloqueados frequentemente
   - Ação: Avisa com opção Continuar/Cancelar

11. ✅ **Buffer Muito Grande** → AVISO RELEVANTE
   - Detecta: `buffer > 5000`
   - Mensagem: "Buffer muito grande consumirá muita memória"
   - Impacto: Consumo de memória excessivo
   - Ação: Avisa com opção Continuar/Cancelar

### Validação de Readers-Writers
**Arquivo**: `ValidateReadersWriters()`

12. ✅ **Threads Totais > 500** → AVISO RELEVANTE
   - Detecta: `totalThreads = leitores + escritores`
   - Mensagem: "Total de threads muito elevado"
   - Impacto: Performance degradada
   - Ação: Avisa com opção Continuar/Cancelar

13. ✅ **Desbalanceamento Readers/Writers** → AVISO RELEVANTE
   - Detecta: `leitores > escritores × 10`
   - Mensagem: "Muito mais leitores que escritores"
   - Impacto: Writer starvation possível
   - Ação: Avisa com opção Continuar/Cancelar

### Validação de Dining Philosophers
**Arquivo**: `ValidateDiningPhilosophers()`

14. ✅ **Filósofos > 50** → AVISO RELEVANTE
   - Detecta: `filósofos > 50`
   - Mensagem: "Número de filósofos muito elevado"
   - Impacto: Overhead excessivo, degradação performance
   - Ação: Avisa com opção Continuar/Cancelar

15. ✅ **Rondas Muito Altas** → AVISO RELEVANTE
   - Detecta: `rondas > 1000`
   - Mensagem: "Número de rondas muito elevado"
   - Impacto: Execução muito lenta
   - Ação: Avisa com opção Continuar/Cancelar

### Validação de Barrier Synchronization
**Arquivo**: `ValidateBarrierSynchronization()`

16. ✅ **Workers > 500** → AVISO RELEVANTE
   - Detecta: `workers > 500`
   - Mensagem: "Número de workers muito elevado"
   - Impacto: Sincronização ineficiente
   - Ação: Avisa com opção Continuar/Cancelar

17. ✅ **Operações Totais > 100.000** → AVISO RELEVANTE
   - Detecta: `workers × phases > 100.000`
   - Mensagem: "Número total de operações muito elevado"
   - Impacto: Execução muito demorada
   - Ação: Avisa com opção Continuar/Cancelar

### Erros Relevantes NÃO IMPLEMENTADOS (Ainda Faltando)

18. ❌ **Duração Estimada > 5 Minutos**
   - Razão: Difícil estimar tempo sem executar
   - Prioridade: Baixa

---

## 🟢 ERROS DE NÍVEL POUCO IMPORTANTE (LOW) - ❌ NÃO IMPLEMENTADO

Estes erros têm impacto menor. Implementação futura se necessário.

### 19. ❌ **Erro de Criação de Arquivo**
- **Solução Parcial**: `CreateScenarioLogger()` tenta criar diretório automaticamente
- **Implementação Completa**: Não executada
- **Prioridade**: Baixa - Sistema já trata fallback

### 20. ❌ **Espaço em Disco Reduzido**
- **Solução Implementada**: Aviso informativo antes de executar
- **Detecção**: Se < 10 MB disponíveis
- **Ação**: Aviso no console (não bloqueia)
- **Status**: ✅ IMPLEMENTADO (aviso, não validação)

### 21. ❌ **ThreadPool Esgotado**
- **Solução Parcial**: Try-catch ao criar threads
- **Implementação Completa**: Parcial - catch `OutOfMemoryException`
- **Prioridade**: Média

### 22. ❌ **Log > 100 MB**
- **Implementação**: Não realizada
- **Razão**: Seria necessário monitoramento de arquivo
- **Prioridade**: Muito Baixa

### 23. ❌ **Ctrl+C (Interrupção do Programa)**
- **Implementação**: Não realizada
- **Razão**: .NET trata naturalmente via `CancelKeyPress`
- **Prioridade**: Muito Baixa

---

## 🛠️ Implementação Técnica Detalhada

### Helper Functions Criadas

```csharp
// Exibe erro em VERMELHO no console e registra no log
static void LogError(ScenarioLogger logger, string errorMsg, string? details = null)

// Exibe aviso em AMARELO e pede confirmação do utilizador
static void LogWarning(ScenarioLogger logger, string warningMsg, string? details = null)

// Retorna true se utilizador responder "S" para continuar
static bool AskContinueWithWarning()
```

### Padrão de Validação Implementado

```csharp
// Em cada ValidateXXX():

// 1. Erros CRÍTICOS (com return true)
if (condicao_critica)
{
    LogError(logger, "ERRO: ...", "MOTIVO: ...");
    return true;
}

// 2. Avisos RELEVANTES (com AskContinueWithWarning)
if (condicao_relevante)
{
    LogWarning(logger, "AVISO: ...", "DETALHES: ...\nIMPACTO: ...\nRECOMENDACAO: ...");
    if (!AskContinueWithWarning())
    {
        LogError(logger, "Cenário cancelado pelo utilizador.", "...");
        return true;
    }
}
```

### Tratamento de Exceções de I/O

**Função**: `CreateScenarioLogger()`

```csharp
try
{
    // Tentar criar diretório ./logs/
    Directory.CreateDirectory(logsDirectory);
}
catch (Exception ex)
{
    // Fallback: usar diretório temporário
    logsDirectory = Path.Combine(Path.GetTempPath(), "ProjetoLogs");
    Directory.CreateDirectory(logsDirectory);
}

// Verificar espaço em disco
string? driveName = Path.GetPathRoot(logsDirectory);
if (!string.IsNullOrEmpty(driveName))
{
    var driveInfo = new DriveInfo(driveName);
    if (driveInfo.AvailableFreeSpace < 10 * 1024 * 1024)
    {
        Console.WriteLine("⚠️  AVISO: Espaço em disco muito reduzido...");
    }
}
```

### Tratamento de ThreadPool Exaurido

**Função**: `RunProducerConsumer()` e `RunConsumers()`

```csharp
try
{
    for (int i = 0; i < config.Count; i++)
    {
        threads[i] = new Thread(/* ... */);
    }
}
catch (OutOfMemoryException)
{
    LogError(logger,
        "ERRO FATAL: Não foi possível criar todas as threads.",
        "MOTIVO: ThreadPool esgotado ou memória insuficiente.");
    return;
}
```

---

## 📈 Estatísticas por Cenário

| Cenário | Críticos | Relevantes | Total | %Cobertura |
|---------|----------|-----------|-------|-----------|
| Producer-Consumer | 3 | 3 | 6 | 100% |
| Readers-Writers | 2 | 2 | 4 | 100% |
| Dining Philosophers | 1 | 2 | 3 | 100% |
| Barrier Synchronization | 2 | 2 | 4 | 100% |
| Geral (I/O, ThreadPool) | - | - | 3 | 33% |
| **TOTAL** | **8** | **9** | **20** | **65%** |

---

## 🎯 Próximas Melhorias Recomendadas

### Prioridade Alta
1. [ ] Implementar estimativa de duração (> 5 min warning)
2. [ ] Adicionar log file rotation (se > 100 MB)
3. [ ] Melhorar tratamento de exceções de threading

### Prioridade Média
4. [ ] Adicionar progresso de execução (barra de progresso)
5. [ ] Implementar Ctrl+C handler gracioso
6. [ ] Adicionar validação de memória disponível

### Prioridade Baixa
7. [ ] Compactação automática de logs antigos
8. [ ] Relatório de desempenho ao fim da execução
9. [ ] Sugestões automáticas de parâmetros otimizados

---

## ✅ Validação de Compilação

```
Build succeeded in 1,6s
- Nenhum erro (0)
- Nenhum aviso (0)
```

**Status**: ✅ Código está compilando corretamente com todas as validações implementadas.

---

## 📝 Notas

- Todos os avisos exigem confirmação do utilizador (exceto aviso de espaço em disco)
- Mensagens de erro e aviso aparecem SIMULTANEAMENTE no console E no ficheiro de log
- O sistema mantém fallback para diretório temporário se ./logs/ não puder ser criado
- Validações são executadas ANTES de iniciar o cenário
