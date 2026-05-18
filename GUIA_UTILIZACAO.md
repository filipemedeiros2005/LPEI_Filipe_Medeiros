# 🚀 Guia de Utilização - Cenários Concorrentes com Parâmetros Configuráveis

## 📌 Como Utilizar

### 1. **Compilar o Projeto**
```bash
cd LPEI_Filipe_Medeiros
dotnet build
```

### 2. **Executar o Programa**
```bash
dotnet run
```

### 3. **Menu Principal**
O programa apresentará um menu com 4 opções:

```
Menu de cenarios concorrentes
1 - Producer-Consumer
2 - Readers-Writers
3 - Dining Philosphers
4 - Barrier Synchronization / Thread Coordination
0 - sair
Escolha uma opcao: 
```

---

## 📋 Configuração de Cada Cenário

### **Opção 1: Producer-Consumer**

Ao selecionar esta opção, será solicitada a configuração:

```
=== Configuracao: Producer-Consumer ===

Numero de produtores (padrao: 2): 3
Numero de consumidores (padrao: 2): 2
Tamanho do buffer (padrao: 5): 10
Items por produtor (padrao: 10): 5
```

**O que acontece:**
- O programa exibirá no ecrã: `PARAMETROS: Produtores=3, Consumidores=2, Buffer=10, Items/Produtor=5`
- Serão criadas 3 threads produtoras e 2 consumidoras
- Cada produtor criará 5 items (total: 15 items)
- O buffer pode armazenar até 10 items
- Todos os detalhes serão registrados em: `logs/Producer-Consumer_[timestamp].txt`

---

### **Opção 2: Readers-Writers**

```
=== Configuracao: Readers-Writers ===

Numero de leitores (padrao: 3): 4
Numero de escritores (padrao: 2): 3
Iteracoes por thread (padrao: 5): 7
```

**O que acontece:**
- 4 threads de leitura e 3 threads de escrita
- Cada thread realiza 7 operações
- Sincronização: leitores podem ler simultaneamente, mas escritores têm acesso exclusivo
- Log em: `logs/Readers-Writers_[timestamp].txt`

---

### **Opção 3: Dining Philosophers**

```
=== Configuracao: Dining Philosophers ===

Numero de filosofos (padrao: 5, minimo: 3): 7
Rondas por filosofo (padrao: 4): 5
```

**O que acontece:**
- 7 filósofos alternam entre PENSAR e COMER
- Cada filósofo faz 5 ciclos completos
- Implementação anti-deadlock: último filósofo pega garfos em ordem inversa
- Log em: `logs/Dining-Philosophers_[timestamp].txt`

---

### **Opção 4: Barrier Synchronization**

```
=== Configuracao: Barrier Synchronization ===

Numero de workers (padrao: 4): 6
Numero de fases (padrao: 3): 4
```

**O que acontece:**
- 6 workers executam 4 fases sincronizadas
- Cada fase completa-se quando TODOS os workers chegam à barreira
- Workers não podem avançar até todos estarem prontos
- Log em: `logs/Barrier-Synchronization_[timestamp].txt`

---

## 📊 Exemplo Completo

### Input do Utilizador:
```
1           # Escolhe Producer-Consumer
2           # 2 produtores
3           # 3 consumidores
5           # Buffer tamanho 5
8           # 8 items por produtor
1           # Continua na apresentação de logs
1           # Continua...
...
0           # Sai da apresentação
0           # Volta ao menu, depois sai
```

### Output no Ecrã:
```
Producer-Consumer (2 produtores, 3 consumidores, buffer=5)

PARAMETROS: Produtores=2, Consumidores=3, Buffer=5, Items/Produtor=8
Fim do cenario Producer-Consumer.
Log guardado em: logs/Producer-Consumer_20260513_143500.txt
```

### Ficheiro de Log Gerado:
```
[14:35:00.123] PARAMETROS: Produtores=2, Consumidores=3, Buffer=5, Items/Produtor=8

[14:35:00.124] === Inicio do cenario Producer-Consumer ===
[14:35:00.124] Arquitetura do sistema:
[14:35:00.124] - Componente Produtor: gera itens e tenta inseri-los no buffer limitado.
...
[14:35:00.201] [Produtor 1] inicializando...
[14:35:00.202] [Produtor 1] tentativa de produzir item=1001. Aguardando slot vazio...
[14:35:00.202] [Produtor 1] slot vazio reservado para item=1001. Aguardando mutex...
[14:35:00.203] [Produtor 1] produziu item=1001 | ocupacao=1/5 | buffer=[ 1001] [   ] [   ] [   ] [   ]
...
```

---

## 💡 Dicas Úteis

1. **Valores por Defeito**: Prima ENTER para aceitar o valor por defeito
2. **Visualização de Logs**: Após cada cenário, pode ver os logs de forma guiada (passe por cada linha)
3. **Ficheiros de Log**: Localizados em `./logs/` com timestamp no nome
4. **Parâmetros Grandes**: Aumentar o número de threads gera logs muito mais longos
5. **Análise**: Use os logs para compreender a ordem de sincronização das threads

---

## 🔍 Estrutura de um Ficheiro de Log

Cada log contém:

1. **Cabeçalho com Parâmetros**
   ```
   [timestamp] PARAMETROS: ...
   ```

2. **Descrição da Arquitetura** (filtrada na visualização guiada)
   ```
   === Inicio do cenario ...
   Arquitetura do sistema:
   - ...
   ```

3. **Rastreamento Detalhado** (mostrado na visualização)
   ```
   [timestamp] [Thread X] estado: ...
   [timestamp] [Thread Y] ação: ...
   ```

4. **Resumo Final**
   ```
   === Fim do cenario ...
   ```

---

## ✨ Novidades Nesta Versão

✅ **Parâmetros Configuráveis**: Customize cada cenário conforme necessário
✅ **Mais Detalhes**: Logs muito mais longos e informativos
✅ **Parâmetros Visíveis**: Primeira linha do output mostra configuração escolhida
✅ **Múltiplas Threads**: Suporte a vários produtores, consumidores, leitores, etc.
✅ **Thread-Safe Logging**: Logging sincronizado para evitar corrupção de dados

---

## 📞 Suporte

Caso tenha problemas:

1. Verifique se o .NET 8.0 está instalado: `dotnet --version`
2. Limpe e recompile: `dotnet clean && dotnet build`
3. Verifique os ficheiros de log em `./logs/` para detalhes de execução
