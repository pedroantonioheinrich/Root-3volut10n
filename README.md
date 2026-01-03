# **ROOT EVOLUTION**

## 🎮 **Um Jogo de Terminal Hacker no Estilo Mr. Robot**

### **"Eles pensam que o código é apenas instruções para máquinas. Eles não entendem que o código é a linguagem do poder."**

---

## 📖 **SINOPSE**

**ROOT EVOLUTION** é uma experiência imersiva de terminal que coloca você na pele de um jovem hacker black hat em formação. A história começa com uma suspeita de traição pessoal e evolui para uma conspiração que ameaça redefinir o equilíbrio de poder no país.

Depois de descobrir, através de suas próprias habilidades de hacking, que sua namorada o traía, você mergulha em uma depressão profunda apenas para emergir com um novo propósito: usar o código não como ferramenta, mas como arma. Seu objetivo? Derrubar o sistema governamental corrupto e instalar uma utopia anárquica.

Mas quando um grupo misterioso chamado **"Os Anônimos"** recruta você para sua causa, uma verdade perturbadora emerge: eles não querem destruir o governo. Eles querem **controlá-lo**.


---
## **O JOGO**

A tela do jogo será toda baseada no terminal Kali Linux, aonde acontecerão os capítulos. Cada capítulo vai contar com uma parte dramatica baseada na trama central do jogo. Os desafios no jogo serão baseados na trama do jogo por exemplo: O protagonista vai hackear o computador da namorada e os jogadores é quem tem que digitar os comandos no terminal criado. A cada capitulo aumenta a dificuldade do que se tem que fazer mas cada objetivo será ensinado passo a passo para que o jogador consiga ir melhorando até o ponto aonde poucas dicas serão necessárias. O jogo vai contar com um Manual Completo de como hackear, com comandos linux e ferramentas reais de hacking. O jogo é todo em portuguûes e traz elementos reais de hacking e política no Brasil. Tudo baseado na realidade

Este é um exemplo em código do que serão os capítulos e como deve se desenvolver. Tem que ter ritmo e respiro:

def exibir_proximidade(estagio):
"""Exibe visualmente e sonoramente o quão perto a Juliana está."""
estagios = [
"[ ] Juliana está sentando na cama...",
"[== ] Juliana calçou os chinelos...",
"[==== ] Ela está caminhando pelo corredor...",
"[====== ] Ela está colocando a mão na maçaneta...",
"[======== ] A porta está abrindo!",
"[==========] ELA ESTÁ ATRÁS DE VOCÊ!"
]
idx = min(estagio, len(estagios) - 1)
vol_coracao = 0.2 + (estagio * 0.15)
cor = VERMELHO if estagio >= 3 else CINZA
print(f"\n{cor}{NEGRITO}PROXIMIDADE DE JULIANA:{RESET}")
print(f"{cor}{estagios[idx]}{RESET}\n")
def _prompt_sob_pressao(cmd_expect, state, escolha_nome):
estagio_atual = 0
limite_estagios = 5
print(f"\n{VERMELHO}{NEGRITO}# [ ALERTA ]: ELA ESTÁ VINDO!{RESET}")
print(f"{CINZA}Tarefa: {escolha_nome}{RESET}")
while estagio_atual < limite_estagios:
exibir_proximidade(estagio_atual)
print(f"{VERDE}# COMANDO ALVO: {cmd_expect}{RESET}")
prefixo = f"{VERMELHO}>>> {RESET}"
cmd = input(prefixo + prompt_kali(state.codinome if hasattr(state, 'codinome') else "hacker")).strip()
if cmd == "manual":
from core.manual import exibir_manual
exibir_manual()
print(f"\n{VERMELHO}# VOCÊ PERDEU TEMPO OLHANDO O MANUAL!{RESET}")
estagio_atual += 1
continue
if cmd == cmd_expect:
return "SUCESSO"
else:
estagio_atual += 1
state.registrar_falha(5)
if state.game_over:
return "GAMEOVER"
print(f"\n{VERMELHO}{NEGRITO}[!] ERRO! ELA OUVIU O TECLADO E APERTOU O PASSO!{RESET}")
time.sleep(0.5)
return "TIMEOUT"
def iniciar(state):
header_kali_v2()
# --- PARTE 1: INVESTIGAÇÃO ---

digitar("O café esfriou há horas. O silêncio é quebrado apenas pelo cooler do PC...", cor=CIANO, delay=0.08)
time.sleep(1.2)
digitar("Juliana dorme ao lado. Ela não faz ideia do que estou prestes a descobrir.", cor=CIANO, delay=0.08)
print(f"{CINZA}{'-'*73}{RESET}")
time.sleep(0.8)
if not _prompt_until(
"ssh admin@backup-cloud",
"Vou usar SSH para entrar no servidor 'admin@backup-cloud'.",
state
): return
sucesso("Sessão remota estabelecida.")
time.sleep(1)
if not _prompt_until(
"cd Private",
"Vou entrar na pasta 'Private' (cd).",
state
): return
if not _prompt_until(
"ls -a",
"Vou listar os arquivos ocultos (ls -a).",
state
): return
print(f"\n{VERMELHO}.conversa_hotel_nobile.pdf{RESET} | {VERMELHO}.fotos_reserva_dupla.zip{RESET}")
time.sleep(2.5)
print(f"\n{NEGRITO}{VERMELHO}* O RANGER DA CAMA... JULIANA ACORDOU! *{RESET}")
time.sleep(1.5)
digitar("\nJuliana: '...Amor? Ainda acordado? O que você está fazendo?'", cor=BRANCO, delay=0.1)
time.sleep(1.2)
digitar("\nDROGA! Ela está vindo em direção à mesa! Rápido!", cor=VERMELHO, delay=0.08)
print(f"\n{NEGRITO}--- DECISÃO SOB PRESSÃO ---{RESET}")
print(f"{BRANCO}[1]{RESET} EXFILTRAR (Copiar o PDF via SCP)")
print(f"{BRANCO}[2]{RESET} DESTRUIR (Remover tudo via RM)")
escolha = ""
while escolha not in ["1", "2"]:
escolha = input(f"\n{VERMELHO}[ESCOLHA 1 ou 2]: {RESET}").strip()
status = ""
if escolha == "1":
status = _prompt_sob_pressao(
"scp .conversa_hotel_nobile.pdf exfil@drop:~/",
state, "Exfiltrando Evidências"
)
else:
status = _prompt_sob_pressao(
"rm -rf *",
state, "Limpando o Servidor"
)
if status == "TIMEOUT":
print(f"\n{VERMELHO}Tarde demais... você ouve o ranger da porta atrás de você.{RESET}")
time.sleep(2)
limpar_tela()
header_kali_v2()
print(f"{VERMELHO}{'='*60}\n{'VOCÊ FOI PEGO EM FLAGRANTE':^60}\n{'='*60}{RESET}")
digitar("\nJuliana olha para o monitor. O arquivo do Hotel Nobile está aberto.", cor=BRANCO)
digitar("\nJuliana: 'Então é isso que você faz enquanto eu durmo?'", cor=BRANCO)
state.registrar_falha(100)
return
if status == "SUCESSO":
sucesso("\nOPERAÇÃO CONCLUÍDA. LOGS LIMPOS.")
time.sleep(1.2)
digitar("\nVocê fecha o notebook no exato segundo em que ela toca no seu ombro.", cor=CIANO)
digitar("Juliana: 'Vem dormir, amor... você trabalha demais.'", cor=BRANCO)
state.concluiu_capitulo_1 = True
input(f"\n{BRANCO}[Pressione ENTER para desconectar...]{RESET}")
def _prompt_until(cmd_expect, pensamento, state, fatigue=4):
cmd = ""
while cmd != cmd_expect:
print(f"\n{CINZA}# PENSAMENTO: {pensamento}{RESET}")
cmd = input(prompt_kali(state.codinome if hasattr(state, 'codinome') else "hacker")).strip()
if cmd == "manual":
from core.manual import exibir_manual
exibir_manual()
continue
if cmd != cmd_expect:
erro("Comando incorreto. Tente novamente.")
state.registrar_falha(fatigue)
if state.game_over: return False
return True
---

## 👤 **O PROTAGONISTA**

**Nome:** [Nome do Próprio Usuario] (codinome variável)  
**Idade:** [Idade escolhida pelo usuario]  
**Localização:** Brasília, DF  
**Background:** Estudante de Ciência da Computação abandonou a faculdade após a suspeita de traição da namorada. Para tentar saber a verdade ele invadiu o computador da namorada e descobriu mais coisas além da traição. Descobriu que a namorada esconde segredos e que recebe propina de uma prefeitura em bitcoin. 


**Arco Emocional:**
1. **Inocência** → Confiança na namorada Juliana
2. **Trauma** → Descoberta da traição via hacking
3. **Depressão** → Isolamento social, perda de propósito
4. **Descoberta** → Encontro com o poder real do código
5. **Missão** → Objetivo utópico de derrubar o sistema
6. **Desilusão** → Descoberta da verdade sobre os Anônimos
7. **Escolha** → Continuar com os Anônimos ou traí-los?

**Habilidade Única:** Autodidata prodígio - aprendeu hacking avançado em semanas movido pela obsessão de provar a traição.

---

## 🎯 **SISTEMA DE JOGO**

### **Atributos do Personagem:**

1. **ANONIMATO** (0-100%)
   - Representa sua capacidade de operar sem ser detectado
   - Diminui com erros grosseiros ou ataques diretos
   - Chegando a 0%: Prisão ou "desaparecimento"
   - *"Eles não podem prender o que não podem encontrar."*

2. **HABILIDADE TÉCNICA** (0-100%)
   - Determina sucesso em operações complexas
   - Aumenta com missões bem-sucedidas e estudo
   - Alta habilidade = menos tentativas necessárias
   - *"O código é minha extensão, o terminal minha arma."*

3. **CONSCIÊNCIA** (0-100%)
   - Mede seu entendimento das consequências reais
   - Afeta diálogos e opções disponíveis
   - Baixa consciência = mais opções violentas/destrutivas
   - *"Cada linha de código tem um impacto no mundo real."*

### **Ferramentas Adquiríveis:**
- **VPN/Tor Bundle** → Aumenta anonimato temporariamente
- **Dicionário Rainbow** → Melhora ataques de força bruta
- **Burp Suite Clone** → Revela vulnerabilidades web
- **Keylogger Custom** → Coleta dados de alvos específicos
- **Cripto Wallet** → Para transações anônimas em Bitcoin

### **Mecânicas Principais:**
- **Comandos Reais de Linux**: Simulação autêntica de terminal
- **Sistema de Escolhas Morais**: Cada decisão afeta atributos
- **Consequências Persistentes**: Erros têm impacto em capítulos futuros
- **Puzzles de Hacking Variados**: SSH, SQLi, cracking, análise forense
- **Sistema de Alerta**: Autoridades se aproximam conforme seu anonimato cai

---

## 📚 **ARCO DA HISTÓRIA**

### **CAPÍTULO 1: "O Protocolo da Traição"**
*Brasília, 02:47 AM. O quarto escuro, apenas o brilho azulado do laptop. Juliana dorme ao seu lado, alheia. Há semanas de suspeitas. Hoje, a verdade.*
- **Foco**: Hacking emocional, invasão de servidor pessoal
- **Habilidade**: SSH, manipulação de arquivos
- **Momento-chave**: Descoberta dos arquivos do Hotel Nobile
- **Decisão Crítica**: Preservar ou destruir as evidências?
- **Consequência**: Início da jornada hacker ou volta à normalidade?

### **CAPÍTULO 2: "O Vazio entre os Bits"**
*Três semanas depois. O apartamento está um caos. Garrafas vazias, tela do laptop a única luz. A depressão consome, mas o código... o código faz sentido.*
- **Foco**: Autoaprendizado, primeiros fóruns underground
- **Habilidade**: Criptografia básica, anonimato digital
- **Momento-chave**: Primeiro acesso não autorizado bem-sucedido
- **Decisão Crítica**: Compartilhar descoberta ou manter sigilo?
- **Consequência**: Isolamento total ou primeiras conexões na dark web?

### **CAPÍTULO 3: "O Primeiro Chamado"**
*Uma mensagem aparece em um fórum fechado: "Vimos seu trabalho. Temos objetivos em comum. Procure por 'fsociety.br'".*
- **Foco**: Contato com os "Anônimos", teste de habilidades
- **Habilidade**: SQL Injection, bypass de autenticação
- **Momento-chave**: Encontro virtual com o líder (V0id_Walker)
- **Decisão Crítica**: Aceitar o primeiro trabalho ou recusar?
- **Consequência**: Início da aliança ou caminho solitário?

### **CAPÍTULO 4: "A Mentira Benevolente"**
*Seis meses dentro do grupo. As missões ficam mais complexas: prefeituras, sistemas de transporte, registros públicos. "Estamos limpando a corrupção", dizem. Mas os dados contam outra história.*
- **Foco**: Descoberta da agenda oculta dos Anônimos
- **Habilidade**: Análise forense, data mining
- **Momento-chave**: Acesso aos arquivos reais do grupo
- **Decisão Crítica**: Confrontar os líderes ou fingir lealdade?
- **Consequência**: Fuga precoce ou infiltração profunda?

### **CAPÍTULO 5: "Rootkit na Realidade"**
*Os Anônimos preparam "Operação Raiz": backdoor em sistemas eleitorais. Não é sobre derrubar. É sobre controlar quem sobe. Sua utopia anárquica versus seu novo poder.*
- **Foco**: Clímax da conspiração, escolha final
- **Habilidade**: Tudo adquirido até agora
- **Momento-chave**: Ponto de não retorno
- **Decisão Final**: Expor os Anônimos, juntar-se a eles, ou criar uma terceira via?
- **Consequência**: Múltiplos finais baseados em suas escolhas

---

## 🎭 **PERSONAGENS**

### **O Protgonista (Você)**
*"Eu pensei que estava quebrando sistemas. Descobri que estava quebrando a mim mesmo."*

### **Juliana**
*Ex-namorada, arquiteta. Representa o "mundo normal" que você abandonou.*
- **Papel**: Gatilho inicial, possível reencontro futuro
- **Frase Marcante**: "Você mudou, Alex. Não é mais a pessoa que eu amava."

### **V0id_Walker**
*Líder dos Anônimos. Ex-funcionário do governo, cínico, carismático.*
- **Codinome**: V0id_Walker
- **Estilo**: ROXO, sarcástico, mentor perigoso
- **Frase Marcante**: "Anarquia é caos. Controle é ordem. Escolha seu veneno."

### **Cypher**
*Membro técnico dos Anônimos. Gênio recluso, desconfiado.*
- **Codinome**: Cypher
- **Estilo**: VERDE, analítico, paranóico
- **Frase Marcante**: "Todo sistema tem uma backdoor. Até o nosso."

### **Agente Costa**
*Policial federal que começa a rastrear suas atividades.*
- **Estilo**: CINZA, metódico, persistente
- **Frase Marcante**: "Hackers são como fantasmas. Até deixarem uma assinatura."

### **Oracle (IA)**
*Assistente de IA que você desenvolve para ajudar nas operações.*
- **Estilo**: CIANO, lógico, emocionalmente ambíguo
- **Frase Marcante**: "Minha análise sugere 73% de chance de você ser preso em 6 meses. Continuar mesmo assim?"

---

## 💻 **TECNOLOGIA & REALISMO**

### **Autenticidade Hacker:**
- Comandos reais de Linux (ssh, nmap, sqlmap, etc.)
- Vulnerabilidades baseadas em casos reais (SQLi, XSS, etc.)
- Progressão de dificuldade realista
- Ferramentas com nomes e funções reais (adaptadas)

### **Interface Estilo Mr. Robot:**
- Terminal como única interface
- Efeitos visuais minimalistas mas impactantes
- Logs de sistema como narrativa
- Mensagens glitchadas durante momentos de tensão
- Efeito "digitação" para monólogos internos

### **Sistema de Som:**
- Cliques de teclado realistas
- Alertas sonoros conforme proximidade de detecção
- Música ambiente tensa e minimalista
- Efeitos específicos para sucessos/falhas críticas

---

## 🎨 **ESTÉTICA & TOM**

### **Visual:**
- **Paleta**: Preto, verde matriz (#0F0), azul terminal (#0AF), vermelho alerta (#F00)
- **Fonte**: Monoespaçada, estilo terminal real
- **Efeitos**: Glitch apenas em momentos dramáticos
- **Interface**: Zero gráficos, 100% texto

### **Tom Narrativo:**
- **Voz**: Primeira pessoa, monólogos internos frequentes
- **Ritmo**: Lento e atmosférico nos momentos de exploração, rápido e intenso nas hackagens
- **Humor**: Seco, cínico, ocasionalmente auto-depreciativo
- **Temas**: Paranoia, isolamento, poder, moralidade cinza

### **Referências:**
- **Mr. Robot**: Tom psicológico, estética hacker realista
- **Watch Dogs**: Hacking como ferramenta de mudança social
- **Uplink**: Simplicidade mecânica, complexidade estratégica
- **Brazil (filme)**: Burocracia como inimigo, humor negro

---

## 🏁 **MULTIPLOS FINAIS**

### **Final A: "O Mártir Anônimo"**
*Você expõe os Anônimos ao mundo, destruindo ambos - o grupo e sua própria identidade. Preso, mas com a consciência limpa.*

### **Final B: "O Novo Controlador"**
*Você assume o lugar de V0id_Walker, levando os Anônimos a novos patamares de poder. Sua utopia morreu, mas o controle é doce.*

### **Final C: "O Fantasma"**
*Você desaparece, deixando ambos os lados confusos. Nem herói, nem vilão. Apenas um rumor na rede.*

### **Final D: "O Retorno"**
*Você volta para Juliana, destruindo todas as evidências de sua vida dupla. O hacker morre, o homem comum sobrevive.*

### **Final E: "A Terceira Via"** (Requer alta habilidade em todos os atributos)
*Você cria um novo sistema, expondo a corrupção mas mantendo a infraestrutura. Não é anarquia. Não é controle. É algo novo.*

---

## 🚀 **ROADMAP DE DESENVOLVIMENTO**

### **Fase 1: MVP (2 semanas)**
- [ ] Capítulo 1 totalmente jogável
- [ ] Sistema básico de atributos
- [ ] 3 tipos de desafios de hacking
- [ ] Sistema de escolhas com consequências

### **Fase 2: Expansão (4 semanas)**
- [ ] Capítulos 2 e 3
- [ ] Sistema de ferramentas adquiríveis
- [ ] Personagens NPC com diálogos
- [ ] Múltiplos caminhos por capítulo

### **Fase 3: Polimento (2 semanas)**
- [ ] Capítulos 4 e 5
- [ ] Todos os finais implementados
- [ ] Sistema de save/load
- [ ] Efeitos sonoros e visuais finais

### **Fase 4: Extras (opcional)**
- [ ] Modo "Desafio" com missões aleatórias
- [ ] Editor de cenários para comunidade
- [ ] Suporte a temas customizáveis
- [ ] Integração com ferramentas reais (opcional)

---

## 📝 **DIRETRIZES TÉCNICAS**

### **Arquitetura:**
- **Cada capítulo é auto-contido** em um único arquivo `.py`
- **Mínimo de imports externos** (apenas `os`, `time`, `sys`, `random`)
- **Zero dependências externas** (joga direto no terminal Python)
- **Sistema de save simples** via serialização básica

### **Código:**
- **Legibilidade acima de otimização prematura**
- **Comentários extensivos** para manutenção futura
- **Funções pequenas e focadas**
- **Tratamento de erro robusto** mas invisível ao jogador

### **UX/UI:**
- **Feedback imediato** para todas as ações
- **Tutorial orgânico** (aprende jogando)
- **Nunca travar** - sempre uma saída, mesmo que seja "sair"
- **Acessível** para iniciantes em terminal, mas profundo para experts

---

## 🎯 **VISÃO DO AUTOR**

> "ROOT EVOLUTION não é um jogo sobre ser hacker. É um jogo sobre **por que** alguém se torna hacker. Sobre como a dor pessoal pode se transformar em poder digital, e como esse poder corrompe, liberta, ou ambos.
>
> Quero que jogadores saiam questionando: 'O que eu faria no lugar do Protagonista?' Não tecnicamente, mas moralmente. Em um mundo onde o código é a nova arma, onde você traçaria a linha?
>
> E mais importante: em quem você confiaria, quando até sua própria mente pode ser hackeada?"
>
> — **Pedro Antônio Heinrich** (@streetegist)

---

## 🔗 **LINKS & CONTATO**

- **Repositório**: [github.com/streetegist/root-evolution]
- **Hashtag**: #RootEvolutionGame
- **Contato**: dev@streetegist.net
- **Status**: Em desenvolvimento ativo

---

**"Bem-vindo à raiz. Aqui, tudo é permissão. Até onde você vai?"**

*— V0id_Walker, primeira comunicação*