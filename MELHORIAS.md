# 📋 Resumo das Melhorias Implementadas

## ✅ Funcionalidades Adicionadas

### 1. **Configuração de Parâmetros Dinâmica**
Cada cenário agora permite que o utilizador configure os seus próprios parâmetros:

#### Producer-Consumer
- Número de produtores (padrão: 2)
- Número de consumidores (padrão: 2)
- Tamanho do buffer (padrão: 5)
- Items por produtor (padrão: 10)

#### Readers-Writers
- Número de leitores (padrão: 3)
- Número de escritores (padrão: 2)
- Iterações por thread (padrão: 5)

#### Dining Philosophers
- Número de filósofos (padrão: 5, mínimo: 3)
- Rondas por filósofo (padrão: 4)

#### Barrier Synchronization
- Número de workers (padrão: 4)
- Número de fases (padrão: 3)

### 2. **Exibição de Parâmetros**
- A primeira linha do output no ecrã mostra os parâmetros selecionados
- A primeira linha do log registra igualmente os parâmetros (formato: `PARAMETROS: ...`)
- Exemplo: `PARAMETROS: Produtores=2, Consumidores=2, Buffer=5, Items/Produtor=10`

### 3. **Logs Mais Detalhados**
Os logs foram consideravelmente expandidos para incluir:

- **Producer-Consumer**: Cada produtor e consumidor registam em detalhe:
  - Tentativas de produção/consumo
  - Espera por slots vazios/cheios
  - Estados do buffer após cada operação
  - Contador de itens consumidos

- **Readers-Writers**: Detalhes de:
  - Cada iteração de leitura/escrita
  - Incremento/decremento de leitores ativos
  - Estado da secção crítica
  - Bloqueios e libertações de recursos

- **Dining Philosophers**: Rastreamento de:
  - Cada transição de estado (PENSAR → COMER)
  - Tentativas de aquisição de garfos
  - Ordem de aquisição (estratégia anti-deadlock)
  - Duração do tempo de comer

- **Barrier Synchronization**: Detalhes de:
  - Duração de processamento de cada fase
  - Sincronização na barreira
  - Desbloqueio para próxima fase

### 4. **Melhorias Estruturais**
- Código refatorizado para namespaces e classes apropriadas
- Métodos estáticos bem organizados dentro da classe `Program`
- Melhor tratamento de múltiplas threads com identificadores únicos
- Classe `ScenarioLogger` encapsulada e melhorada

## 📊 Exemplo de Output de Parâmetros

```
Menu de cenarios concorrentes
...
Escolha uma opcao: 1

=== Configuracao: Producer-Consumer ===

Numero de produtores (padrao: 2): 3
Numero de consumidores (padrao: 2): 2
Tamanho do buffer (padrao: 5): 10
Items por produtor (padrao: 10): 5

Producer-Consumer (3 produtores, 2 consumidores, buffer=10)

PARAMETROS: Produtores=3, Consumidores=2, Buffer=10, Items/Produtor=5
```

## 📁 Ficheiros de Log

Os logs agora são significativamente mais longos (centenas de linhas dependendo dos parâmetros) e contêm:
- Timestamps precisos (HH:mm:ss.fff)
- Rastreamento completo do algoritmo
- Estados das estruturas de dados
- Informações de sincronização

**Localização**: `./logs/[Cenario]_[timestamp].txt`

## 🔧 Tecnologias Utilizadas

- C# 12.0 (.NET 8.0)
- `SemaphoreSlim` para sincronização
- `Barrier` para coordenação de fases
- `Thread` para execução paralela
- `StreamWriter` com locks para logging thread-safe

## 💾 Compilação e Execução

```bash
# Compilar
dotnet build

# Executar
dotnet run
```

## ✨ Benefícios

1. **Flexibilidade**: Ajuste cenários conforme necessário
2. **Rastreabilidade**: Logs detalhados para análise de comportamento
3. **Educativo**: Parâmetros visíveis facilitam compreensão
4. **Escalabilidade**: Suporte a múltiplos produtores/consumidores/leitores/escritores
