# Lista de Possíveis Erros - Análise de Importância

## 🔴 ERROS DE NÍVEL IMPORTANTE (Critical)

Estes erros impedirão a execução do cenário ou causarão comportamentos fatais.

### 1. **Producer-Consumer: 0 Produtores**
- **Problema**: Sem produtores, nenhum item é gerado
- **Impacto**: Buffer vazio, consumidores ficarão bloqueados indefinidamente
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de produtores deve ser minimo 1. MOTIVO: Com 0 produtores, nenhum item sera produzido e o cenario fica vazio."

### 2. **Producer-Consumer: 0 Consumidores**
- **Problema**: Sem consumidores, items não são removidos
- **Impacto**: Buffer encharca rapidamente, produtores bloqueados indefinidamente
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de consumidores deve ser minimo 1. MOTIVO: Com 0 consumidores, nenhum item sera consumido e o buffer fica cheio."

### 3. **Producer-Consumer: Buffer Size = 0**
- **Problema**: Buffer sem capacidade
- **Impacto**: Impossível armazenar qualquer item
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Tamanho do buffer deve ser minimo 1. MOTIVO: Um buffer de tamanho 0 nao permite armazenar items."

### 4. **Readers-Writers: 0 Leitores**
- **Problema**: Sem leitores, nenhuma leitura ocorre
- **Impacto**: Cenário vazio, não demonstra sincronização
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de leitores deve ser minimo 1. MOTIVO: Com 0 leitores, nenhuma leitura ocorre e o cenario fica vazio."

### 5. **Readers-Writers: 0 Escritores**
- **Problema**: Sem escritores, nenhuma escrita ocorre
- **Impacto**: Valor partilhado nunca é atualizado, cenário vazio
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de escritores deve ser minimo 1. MOTIVO: Com 0 escritores, nenhuma escrita ocorre e o cenario fica vazio."

### 6. **Dining Philosophers: < 3 Filósofos**
- **Problema**: 1 filósofo tenta fazer lock do mesmo garfo 2 vezes; 2 filósofos causam deadlock circular
- **Impacto**: DEADLOCK GARANTIDO - programa travará indefinidamente
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de filosofos deve ser minimo 3. MOTIVO: Com menos de 3 filosofos, ocorrem deadlocks garantidos."

### 7. **Barrier Synchronization: 0 Workers**
- **Problema**: Sem workers, nenhum trabalho é executado
- **Impacto**: Cenário vazio, não demonstra sincronização
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de workers deve ser minimo 1. MOTIVO: Com 0 workers, nenhuma thread executa o trabalho."

### 8. **Barrier Synchronization: 0 Fases**
- **Problema**: Sem fases, nenhum trabalho ou sincronização ocorrem
- **Impacto**: Cenário vazio e sem propósito
- **Status**: ✅ JÁ VALIDADO
- **Mensagem**: "ERRO: Numero de fases deve ser minimo 1. MOTIVO: Com 0 fases, nenhum trabalho e sincronizacao ocorrem."

---

## 🟡 ERROS DE NÍVEL RELEVANTE (Medium)

Estes erros não impedem a execução, mas causam comportamentos indesejáveis ou efeitos secundários graves.

### 9. **Producer-Consumer: Buffer Size << Produtores × Items/Produtor**
- **Problema**: Buffer muito pequeno comparado com volume de produção
- **Impacto**: Produtores ficarão bloqueados frequentemente, cenário não corre suavemente
- **Exemplo**: 10 produtores × 20 items = 200 items; buffer = 5
- **Status**: ❌ NÃO VALIDADO - Deveria avisar
- **Sugestão**: Avisar se buffer < (produtores × items/produtor) / consumidores

### 10. **Readers-Writers: Muitos mais Leitores que Escritores**
- **Problema**: Writers podem sofrer de starvation (nunca conseguem acesso exclusivo)
- **Impacto**: Escritores bloqueados indefinidamente enquanto leitores monopolizam o recurso
- **Exemplo**: 50 leitores, 1 escritor
- **Status**: ❌ NÃO VALIDADO - Deveria avisar
- **Sugestão**: Avisar se Leitores > Escritores × 10

### 11. **Threads Totais Muito Elevado (> 1000)**
- **Problema**: Excesso de context switching, degradação severa de performance
- **Impacto**: Programa muito lento, sistema operativo sobrecarregado
- **Exemplo**: 500 produtores + 500 consumidores = 1000 threads
- **Status**: ❌ NÃO VALIDADO - Deveria avisar
- **Sugestão**: Avisar se threads totais > 500

### 12. **Iterações Muito Altas com Muitas Threads**
**Status**: ✅ JÁ VALIDADO (Barrier, DiningPhil)
**Sugestão**: Avisar se (threads × iterações) > 100.000
### 13. **Buffer Muito Grande (> 10.000)**
- **Problema**: Consumo de memória excessivo
- **Impacto**: Possível OutOfMemoryException
- **Status**: ❌ NÃO VALIDADO - Deveria avisar
- **Sugestão**: Avisar se buffer > 5.000

### 14. **Dining Philosophers: Número Muito Alto (> 100)**
- **Problema**: Muitos locks simultaneamente, overhead computacional alto
- **Impacto**: Performance degradada, possível deadlock ou starvation
- **Status**: ❌ NÃO VALIDADO - Deveria avisar
- **Sugestão**: Avisar se filósofos > 50

---

## 🟢 ERROS DE NÍVEL POUCO IMPORTANTE (Low)

Estes erros são raros, causam inconvenientes menores, ou têm impacto limitado.

### 15. **Arquivo de Log Não Pode Ser Criado**
- **Problema**: Pasta `./logs/` não existe ou sem permissões de escrita
- **Impacto**: Cenário executa mas log não é guardado
- **Causa Comum**: Permissões de arquivo insuficientes
- **Status**: ❌ NÃO TRATADO - Tratamento de exceção genérica
- **Sugestão**: Tentar criar pasta automaticamente ou avisar user

### 16. **Sistema Operativo Nega Criação de Thread**
- **Problema**: ThreadPool esgotado ou limite do sistema atingido
- **Impacto**: Algumas threads não conseguem ser criadas, cenário incompleto
- **Causa Comum**: Aplicação criou muitos threads anteriormente
- **Status**: ❌ NÃO TRATADO - Exceção não-controlada
- **Sugestão**: Capturar OutOfMemoryException ou ThreadStartException

### 17. **Disco Cheio Durante Gravação de Log**
- **Problema**: Espaço em disco insuficiente
- **Impacto**: Log não pode ser gravado completamente
- **Causa Comum**: Rara, logs anteriores preenchem o disco
- **Status**: ❌ NÃO TRATADO - Exceção não-controlada
- **Sugestão**: Avisar que disco está cheio

### 18. **Cenário Demora Muito (> 5 minutos)**
- **Problema**: Parâmetros combinados causam execução muito longa
- **Impacto**: Usuário acha que programa travou
- **Exemplo**: 100 filósofos × 1000 rondas
- **Status**: ⚠️ PARCIALMENTE TRATADO - Logs mostram progresso
- **Sugestão**: Mostrar barra de progresso ou estimativa de tempo

### 19. **Arquivo de Log Muito Grande (> 100 MB)**
- **Problema**: Consumo de disco excessivo
- **Impacto**: Disco cheio, dificuldade em abrir/processar logs
- **Causa Comum**: Parâmetros muito altos geraram muitos logs
- **Status**: ❌ NÃO TRATADO - Sem limite de tamanho de log
- **Sugestão**: Rotar logs ou avisar sobre tamanho estimado

### 20. **Utilizador Interrompe Programa (Ctrl+C)**
- **Problema**: Threads não são terminadas corretamente
- **Impacto**: Possível corrupção de dados ou travamento
- **Status**: ❌ NÃO TRATADO - Sem tratamento de sinais
- **Sugestão**: Implementar GracefulShutdown

---

## 📊 Resumo por Categoria

| Categoria | Total | Validados | Não Validados | Ação Recomendada |
|-----------|-------|-----------|---------------|-----------------|
| **Importante** | 8 | 8 ✅ | 0 | Mantém como está |
| **Relevante** | 7 | 0 | 7 ❌ | ADICIONAR VALIDAÇÕES |
| **Pouco Importante** | 5 | 1 | 4 ❌ | Tratamento de exceções |
| **TOTAL** | 20 | 9 | 11 | |

---

## 🎯 Próximos Passos Recomendados

### Fase 1 (Priority: HIGH)
- [ ] Validar Buffer adequado para volume de produção
- [ ] Avisar sobre threads excessivo (> 500)
- [ ] Avisar sobre iterações × threads muito alto

### Fase 2 (Priority: MEDIUM)
- [ ] Avisar sobre Readers × Writers desbalanceado
- [ ] Avisar sobre Philosophers > 50
- [ ] Avisar sobre Buffer > 5.000
- [ ] Implementar detecção de disco cheio

### Fase 3 (Priority: LOW)
- [ ] Implementar rotação de logs
- [ ] Adicionar barra de progresso para cenários longos
- [ ] Tratamento de Ctrl+C com graceful shutdown
- [ ] Criar pasta ./logs/ automaticamente

---

## 📝 Notas

- **Erros Importantes**: Todos já validados ✅
- **Erros Relevantes**: Requerem validações adicionais ❌
- **Erros Pouco Importantes**: Melhorias de experiência do utilizador
- **Total de Erros Identificados**: 20
- **Taxa de Cobertura**: 45% (9 de 20 tratados)
