# TASKUNI — Contexto e Modelo do Projeto

## 1. Visão

TASKUNI é um sistema de terminal para gestão acadêmica e controle de estudos de estudantes universitários.

O sistema possui quatro fluxos principais:

Acadêmico  
↓  
Tarefas / Avaliações  
↓  
Estudos  
↓  
Análise + Gamificação  
↓  
Dashboard

O objetivo não é somente cadastrar informações.

Os dados cadastrados devem ser utilizados para produzir informações úteis ao estudante.

---

# 2. MVP

O MVP será considerado completo quando for possível:

1. cadastrar disciplinas;
2. cadastrar conteúdos;
3. cadastrar tarefas;
4. concluir tarefas;
5. cadastrar avaliações;
6. registrar notas;
7. registrar sessões de estudo;
8. criar metas;
9. calcular tempo estudado;
10. calcular XP e nível;
11. detectar tarefas atrasadas;
12. detectar avaliações próximas;
13. gerar prioridades básicas;
14. apresentar dashboard;
15. salvar e recuperar os dados.

---

# 3. Fonte de verdade

Informações calculadas NÃO devem ser persistidas quando puderem ser obtidas através dos dados existentes.

Exemplos:

`duracao_min` das sessões
↓
tempo total

tempo total
↓
XP

XP
↓
nível

sessões
↓
disciplina mais estudada

tarefas
↓
quantidade atrasada

metas + sessões
↓
progresso da meta

Isso evita dados contraditórios.

---

# 4. Estrutura geral do JSON

Conceitualmente:

{
    "disciplinas": [],
    "conteudos": [],
    "tarefas": [],
    "avaliacoes": [],
    "sessoes_estudo": [],
    "metas": []
}

Essa estrutura poderá sofrer pequenas alterações se o grupo identificar necessidade antes da implementação.

Depois que as features começarem, alterações estruturais devem ser discutidas com o grupo.

---

# 5. DISCIPLINA

Representa uma disciplina cursada pelo estudante.

Campos:

id  
nome  
professor  
status  
media_minima

Exemplo conceitual:

{
    "id": 1,
    "nome": "Laboratório de Programação",
    "professor": "Professor X",
    "status": "ativa",
    "media_minima": 6.0
}

Valores possíveis de status:

ativa  
concluida  
arquivada

## Regras

O ID identifica a disciplina.

Outros registros devem relacionar-se com a disciplina através de `disciplina_id`.

Não utilizar o nome da disciplina como chave de relacionamento.

Evitar excluir fisicamente uma disciplina que já possui tarefas, avaliações ou sessões vinculadas.

Preferir arquivá-la.

---

# 6. CONTEÚDO

Representa um assunto de determinada disciplina.

Campos:

id  
disciplina_id  
nome  
status

Exemplo:

{
    "id": 1,
    "disciplina_id": 1,
    "nome": "Dicionários",
    "status": "estudando"
}

Status possíveis:

nao_iniciado  
estudando  
concluido

## Regras

Todo conteúdo acadêmico deve pertencer a uma disciplina existente.

---

# 7. TAREFA

Representa algo que o estudante precisa realizar.

Campos:

id  
titulo  
descricao  
tipo  
disciplina_id  
prazo  
importancia  
status

Exemplo:

{
    "id": 1,
    "titulo": "Finalizar relatório",
    "descricao": "Finalizar relatório do projeto",
    "tipo": "academica",
    "disciplina_id": 1,
    "prazo": "2026-10-05",
    "importancia": "alta",
    "status": "pendente"
}

Tipos:

academica  
pessoal

Importância:

baixa  
media  
alta

Status:

pendente  
concluida

## Regras

Tarefa pessoal não possui vínculo com disciplina.

Toda tarefa acadêmica deve possuir `disciplina_id` com ID válido.

Toda tarefa pessoal deve possuir `disciplina_id` igual a `null`.

Tarefa concluída não deve aparecer como atrasada.

A prioridade final NÃO deve ser armazenada.

Ela será calculada.

---

# 8. PRIORIDADE DE TAREFA

A prioridade pode combinar:

IMPORTÂNCIA + URGÊNCIA.

Importância:

baixa = 1  
media = 2  
alta = 3

Urgência sugerida inicialmente:

prazo vencido = 5

vence hoje ou amanhã = 4

vence em 2 ou 3 dias = 3

vence entre 4 e 7 dias = 2

mais de 7 dias = 1

Pontuação:

importância + urgência.

Faixas iniciais:

1 até 3 → baixa atenção

4 ou 5 → média atenção

6 ou mais → alta atenção

Essa regra é propositalmente simples e explicável.

Antes de implementá-la definitivamente, o grupo deve validá-la.

---

# 9. AVALIAÇÃO

Representa prova, trabalho, seminário ou outra avaliação acadêmica.

Campos:

id  
disciplina_id  
titulo  
tipo  
data  
peso  
nota  
conteudos_ids

Exemplo:

{
    "id": 1,
    "disciplina_id": 1,
    "titulo": "Primeira avaliação",
    "tipo": "prova",
    "data": "2026-10-10",
    "peso": 2,
    "nota": null,
    "conteudos_ids": [1, 2]
}

Tipos permitidos inicialmente:

prova  
trabalho  
seminario  
projeto

## Regras

Toda avaliação pertence a uma disciplina válida.

`nota` pode permanecer sem valor até a avaliação ser corrigida.

Conteúdos relacionados devem pertencer à mesma disciplina da avaliação.

---

# 10. MÉDIA

A média deve ser calculada a partir das avaliações que possuem nota.

Caso sejam utilizados pesos:

soma(nota × peso)
-----------------
soma(pesos)

Não armazenar a média no JSON.

Calcular quando necessário.

---

# 11. SESSÃO DE ESTUDO

Representa um estudo realizado pelo aluno.

Campos:

id  
tipo  
disciplina_id  
conteudo_id  
area_pessoal  
assunto  
data  
duracao_min

Exemplo acadêmico:

{
    "id": 1,
    "tipo": "academico",
    "disciplina_id": 1,
    "conteudo_id": 1,
    "area_pessoal": null,
    "assunto": "Revisão de dicionários",
    "data": "2026-09-27",
    "duracao_min": 60
}

Exemplo pessoal:

{
    "id": 2,
    "tipo": "pessoal",
    "disciplina_id": null,
    "conteudo_id": null,
    "area_pessoal": "Python",
    "assunto": "HTTP",
    "data": "2026-09-27",
    "duracao_min": 45
}

Tipos:

academico  
pessoal

## Regras

Duração deve ser maior que zero.

Estudo acadêmico pertence a uma disciplina e pode relacionar um conteúdo.

Estudo pessoal utiliza `area_pessoal`.

Toda sessão acadêmica deve possuir `disciplina_id` com ID válido.

O `conteudo_id` de uma sessão acadêmica é opcional. Quando informado, deve existir e pertencer à mesma disciplina da sessão.

Em uma sessão acadêmica, `area_pessoal` deve ser `null`.

Toda sessão pessoal deve possuir `area_pessoal` preenchida e utilizar `disciplina_id` e `conteudo_id` iguais a `null`.

Não salvar quantidade acumulada de horas.

Calcular através das sessões.

---

# 12. META

Representa objetivo de tempo de estudo.

Campos:

id  
tipo  
alvo_minutos  
ativa

Exemplo:

{
    "id": 1,
    "tipo": "diaria",
    "alvo_minutos": 120,
    "ativa": true
}

Tipos:

diaria  
semanal

## Regra

Pode existir no máximo uma meta ativa de cada tipo.

Ao ativar uma nova meta diária ou semanal, a meta anterior do mesmo tipo deve ser desativada.

A semana será considerada de segunda-feira a domingo.

O progresso é calculado:

tempo estudado no período
-------------------------
meta

Não salvar porcentagem pronta.

---

# 13. GAMIFICAÇÃO

A gamificação utiliza inicialmente uma regra extremamente simples.

1 minuto estudado = 1 XP.

Portanto:

60 minutos = 60 XP.

XP total é calculado pelas sessões registradas.

Sessões acadêmicas e pessoais geram XP pela mesma regra.

Não precisa ser armazenado separadamente.

---

# 14. NÍVEL

Regra inicial:

cada 100 XP representa um nível.

Exemplo:

0–99 XP → nível 1

100–199 → nível 2

200–299 → nível 3

300–399 → nível 4

Essa regra pode ser modificada futuramente, mas deve permanecer simples e justificável.

---

# 15. STREAK

Streak NÃO pertence ao primeiro MVP.

Se for implementado posteriormente, deverá utilizar as datas das sessões de estudo.

Não criar campo redundante sem necessidade.

---

# 16. CONQUISTAS

Conquistas também são funcionalidades posteriores ao MVP.

Exemplos futuros:

primeira sessão;

5 horas estudadas;

10 horas estudadas;

meta cumprida;

5 dias consecutivos.

---

# 17. ALERTAS

Versão inicial deve detectar apenas situações objetivas.

Exemplos:

TAREFA ATRASADA

prazo < hoje
e
status = pendente

TAREFA PRÓXIMA

prazo dentro de X dias.

AVALIAÇÃO PRÓXIMA

avaliação dentro de X dias.

Na versão inicial, uma tarefa ou avaliação é considerada próxima quando sua data está entre hoje e os próximos 7 dias, incluindo hoje e o sétimo dia.

Datas anteriores a hoje não são consideradas próximas. Tarefas concluídas também não são consideradas próximas.

Não criar "inteligência" artificial ou regras difíceis de justificar.

---

# 18. DASHBOARD

Dashboard NÃO possui dados próprios.

Ele reúne dados produzidos pelos outros módulos.

Pode apresentar:

- nível;
- XP;
- XP necessário para próximo nível;
- tempo estudado hoje;
- meta diária;
- tempo estudado na semana;
- meta semanal;
- tarefas pendentes;
- tarefas atrasadas;
- próximas avaliações;
- disciplina mais estudada;
- prioridades.

---

# 19. PERSISTÊNCIA

Arquivo:

data/taskuni.json

Módulo responsável:

persistencia.py

Fluxo:

programa inicia

↓

persistencia carrega JSON

↓

programa trabalha com listas e dicionários em memória

↓

alteração relevante ocorre

↓

persistencia salva os dados

Nenhum outro módulo deve conhecer detalhes de leitura/escrita do arquivo.

---

# 20. VALIDAÇÕES GERAIS

Validar sempre que necessário:

IDs existentes;

campos obrigatórios;

datas;

números;

duração positiva;

nota válida;

peso positivo;

valores permitidos para status;

disciplina existente;

conteúdo existente;

relações entre entidades.

Validações repetidas devem ser candidatas a `validacoes.py`.

---

# 21. CONTRATOS GERAIS DO MODELO

Estas regras complementam os campos definidos nas seções anteriores e devem ser respeitadas por todos os módulos.

## Identificadores

- IDs são números inteiros positivos.
- Cada coleção possui sua própria sequência de IDs.
- O primeiro ID de uma coleção é 1.
- Um novo ID é obtido somando 1 ao maior ID já existente na coleção.
- IDs não devem ser alterados nem reutilizados.

## Textos

- Campos textuais obrigatórios não podem ficar vazios depois da remoção de espaços no início e no fim.
- Nomes e títulos não são identificadores.
- Registros com nomes ou títulos iguais podem existir, pois podem representar períodos ou atividades diferentes.

## Campos dos registros

- Todos os campos apresentados para cada entidade devem estar presentes em seus registros.
- Um campo só pode receber `null` quando essa possibilidade estiver indicada neste documento.
- `conteudos_ids` deve ser uma lista, pode estar vazia e não pode repetir o mesmo ID.
- `ativa` deve possuir valor booleano `true` ou `false`.
- Campos adicionais não devem ser criados sem atualização prévia deste documento.

## Valores ausentes

- A ausência intencional de um valor deve ser representada por `null` no JSON e por `None` durante a execução em Python.
- Não utilizar string vazia, zero ou textos como `"nenhum"` para substituir um valor ausente.

## Datas e períodos

- Todas as datas persistidas utilizam `YYYY-MM-DD`.
- Os cálculos utilizam a data local do computador em que o programa está sendo executado.
- Uma data de estudo não pode estar no futuro, pois a sessão representa um estudo já realizado.
- Datas passadas são permitidas para tarefas e avaliações, pois são necessárias para histórico e alertas.

## Valores numéricos

- `media_minima` e `nota` aceitam números de 0 a 10, incluindo os limites.
- `peso` deve ser um número maior que zero.
- `duracao_min` e `alvo_minutos` devem ser números inteiros maiores que zero.
- Quando nenhuma avaliação possuir nota, a disciplina deve ser apresentada como sem média calculada, e não com média zero.
- A média utiliza somente avaliações que já possuem nota e mantém a precisão do cálculo; arredondamento, quando necessário, ocorre apenas na apresentação.

## Relações

- Um ID relacionado deve existir na coleção correspondente.
- Um conteúdo relacionado a uma avaliação ou sessão deve pertencer à mesma disciplina do registro.
- IDs são imutáveis, mas campos editáveis podem mudar desde que todas as regras de relacionamento continuem válidas.
- O MVP não realiza exclusão física de registros relacionados. Disciplinas deixam de ser utilizadas por meio dos status `concluida` ou `arquivada`.

## Valores permitidos

- As listas de tipos, status e importâncias definidas neste documento são fechadas durante o MVP.
- Um novo valor só pode ser usado depois de ser discutido e documentado.

## Prioridade

- A regra de importância mais urgência definida na seção 8 fica aprovada para o MVP.
- Somente tarefas pendentes recebem análise de prioridade.
- Tarefas vencidas utilizam urgência 5 e continuam classificadas normalmente pela soma dos pontos.
- A pontuação é calculada quando necessária e nunca é armazenada.

## Metas e gamificação

- O progresso das metas considera todas as sessões, acadêmicas e pessoais, registradas no período correspondente.
- A meta diária considera apenas a data atual.
- A meta semanal considera o intervalo de segunda-feira a domingo que contém a data atual.
- XP e nível também consideram sessões acadêmicas e pessoais.

## Persistência

- O objeto principal em memória é um dicionário com exatamente as coleções oficiais do JSON.
- Se `data/taskuni.json` não existir, `persistencia.py` pode criá-lo com a estrutura inicial vazia.
- Um arquivo existente vazio, inválido ou com estrutura incompatível não deve ser sobrescrito silenciosamente. O programa deve informar o problema.
- O arquivo deve ser lido e gravado em UTF-8.
- Os dados devem ser salvos depois de cada inclusão, edição, conclusão ou mudança de status realizada com sucesso.
- Somente `persistencia.py` pode abrir ou gravar o arquivo JSON.

## Separação entre interface e lógica

- `main.py` controla menus, entradas e mensagens apresentadas no terminal.
- Os módulos de domínio recebem dados por parâmetros e devolvem resultados para quem os chamou.
- Os módulos de domínio não devem solicitar entradas com `input()` nem conhecer detalhes do arquivo JSON.
- `dashboard.py` organiza a apresentação, mas consome cálculos feitos pelos módulos responsáveis.

## Alterações seguras

- Todas as validações de uma operação devem ocorrer antes da alteração dos dados em memória.
- Uma operação inválida não pode modificar parcialmente os dados nem provocar salvamento.
- Mensagens destinadas ao usuário devem ser apresentadas pela interface, não misturadas às funções de cálculo.

## Ambiente e dependências

- O projeto deve permanecer compatível com Python 3.10 ou superior.
- A biblioteca padrão do Python é suficiente para o MVP.
- Nenhuma dependência externa será adicionada enquanto não existir uma necessidade aprovada e documentada.

---

# 22. PRINCÍPIO DE INTEGRAÇÃO

Uma feature NÃO deve inventar seu próprio formato de dados.

Exemplo:

Se `disciplina_id` foi definido desta forma, todos os módulos devem respeitá-lo.

Antes de alterar qualquer campo compartilhado, verificar impacto nos outros módulos.

---

# 23. FUNCIONALIDADES POSTERIORES

Somente depois do MVP:

- cronômetro;
- streak;
- conquistas;
- frequência;
- tarefas recorrentes;
- relatórios avançados;
- barras de progresso mais elaboradas;
- simulador de médias.

---

# 24. NÃO FAZER

Não utilizar:

POO;

classes;

banco de dados;

API;

interface gráfica;

autenticação;

IA;

arquitetura excessivamente complexa.

O objetivo é demonstrar domínio dos conteúdos estudados e boa organização do desenvolvimento.
