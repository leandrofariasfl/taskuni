# Regras de Negócio — TASKUNI

Este documento registra as principais regras de negócio do sistema.

O objetivo é garantir que todos os integrantes compreendam o comportamento esperado das funcionalidades e evitem implementar regras diferentes para a mesma entidade.

---

# 1. Disciplinas

Uma disciplina representa uma matéria cadastrada pelo estudante.

## Dados principais

```text
id
nome
professor
```

## Regras

- o nome é obrigatório;
- não devem existir disciplinas duplicadas pelo nome;
- professor é opcional;
- o ID é gerado automaticamente;
- o usuário não escolhe o ID.

## Remoção

Ao remover uma disciplina, seus conteúdos vinculados também são removidos.

Os relacionamentos utilizam `disciplina_id`.

---

# 2. Conteúdos

Um conteúdo representa um assunto pertencente a uma disciplina.

## Dados

```text
id
disciplina_id
titulo
```

## Regras

- título obrigatório;
- disciplina obrigatória;
- a disciplina informada deve existir;
- a relação é armazenada através de `disciplina_id`.

Um conteúdo não pode existir sem disciplina.

---

# 3. Tarefas

Uma tarefa representa uma obrigação acadêmica ou pessoal.

## Dados principais

```text
id
titulo
descricao
tipo
disciplina_id
prazo
importancia
status
```

## Tipos

```text
academica
pessoal
```

## Importância

```text
baixa
media
alta
```

## Status

```text
pendente
concluida
```

## Tarefa pessoal

Uma tarefa pessoal deve possuir:

```text
tipo = pessoal
disciplina_id = None
```

Ela não pode estar vinculada a disciplina.

## Tarefa acadêmica

Pode possuir:

```text
disciplina_id = None
```

ou:

```text
disciplina_id = ID de uma disciplina existente
```

O vínculo é opcional porque existem obrigações acadêmicas que não pertencem diretamente a uma matéria.

## Prazo

Formato:

```text
AAAA-MM-DD
```

Exemplo:

```text
2026-10-15
```

---

# 4. Prioridade das tarefas

A prioridade não é armazenada.

Ela é calculada usando importância e urgência.

## Importância

```text
baixa = 1
media = 2
alta = 3
```

## Urgência

```text
atrasada       = 5
hoje/amanhã    = 4
até 3 dias     = 3
até 7 dias     = 2
mais de 7 dias = 1
```

## Cálculo

```text
pontuação = importância + urgência
```

Depois a tarefa é classificada em faixa de atenção.

## Atraso

Uma tarefa só é considerada atrasada quando:

```text
status = pendente
```

e o prazo já passou.

Tarefas concluídas não são classificadas como atrasadas.

---

# 5. Avaliações

Cada disciplina pode possuir duas unidades:

```text
UP1
UP2
```

Cada unidade possui duas notas:

```text
ME
Principal
```

## ME

Intervalo:

```text
0 até 2
```

## Principal

Intervalo:

```text
0 até 8
```

## Nota da unidade

```text
UP = ME + Principal
```

Exemplo:

```text
ME = 1.8
Principal = 6.5

UP = 8.3
```

## Média geral

Quando UP1 e UP2 existem:

```text
Média = (UP1 + UP2) / 2
```

## Duplicidade

Uma disciplina pode possuir apenas:

```text
1 UP1
1 UP2
```

Para corrigir uma nota, o registro existente deve ser atualizado.

## Dados derivados

Não são armazenados:

```text
nota total da unidade
média geral
```

Esses valores são calculados quando necessários.

---

# 6. Sessões de estudo

Uma sessão representa um período de estudo já realizado.

## Dados principais

```text
id
tipo
disciplina_id
assunto
duracao_min
data
```

## Tipos

```text
academica
pessoal
```

## Sessão pessoal

```text
tipo = pessoal
disciplina_id = None
```

Sessão pessoal não pode possuir disciplina.

Exemplos:

```text
Inglês
Leitura
Programação pessoal
```

## Sessão acadêmica

Pode existir sem disciplina:

```text
tipo = academica
disciplina_id = None
```

ou vinculada:

```text
disciplina_id = ID válido
```

## Assunto

É obrigatório.

Não são aceitos:

```text
""
"   "
```

## Duração

É registrada em minutos.

A duração deve:

- ser inteira;
- ser maior que zero.

Exemplos:

```text
30
60
90
120
```

## Data

Formato:

```text
AAAA-MM-DD
```

A data:

- deve ser válida;
- é obrigatória;
- não pode estar no futuro.

Uma sessão representa estudo já realizado.

Planejamento futuro deve ser tratado por outra funcionalidade.

---

# 7. IDs

Os registros usam IDs numéricos positivos.

O próximo ID é calculado como:

```text
maior ID existente + 1
```

Se não houver dados:

```text
ID inicial = 1
```

IDs não devem ser alterados durante atualização.

---

# 8. Relacionamentos

As entidades se relacionam através de IDs.

Exemplo:

```text
conteudo.disciplina_id
tarefa.disciplina_id
avaliacao.disciplina_id
sessao.disciplina_id
```

O nome da disciplina não é armazenado novamente nessas entidades.

Isso reduz duplicação.

---

# 9. `None`

`None` representa ausência de valor.

Exemplo:

```text
disciplina_id = None
```

significa que nenhum vínculo foi definido.

Não deve ser substituído por:

```text
0
""
```

quando a intenção for ausência de relacionamento.

---

# 10. Interface

A interface é responsável por:

- apresentar menus;
- receber entrada do usuário;
- converter entradas simples;
- mostrar mensagens;
- formatar dados.

A interface não deve definir regras acadêmicas.

Exemplo:

```text
"abc" não é ID
```

pode ser identificado pela interface.

Mas:

```text
ID 50 não corresponde a nenhuma disciplina
```

é uma validação do domínio.

---

# 11. Domínio

O domínio concentra as decisões do sistema.

Exemplos:

```text
ME não pode passar de 2
tarefa pessoal não pode possuir disciplina
data de sessão não pode ser futura
conteúdo precisa de disciplina
```

Essas regras não devem ficar apenas no menu.

---

# 12. Persistência

A persistência é responsável por:

```text
adicionar
listar
buscar
atualizar
remover
salvar
```

Ela não deve decidir regras acadêmicas.

## `_armazenamento.py`

Centraliza:

- leitura dos JSONs;
- gravação;
- caminhos;
- criação da pasta;
- geração de IDs.

---

# 13. Dados armazenados e derivados

## Armazenados

Exemplos:

```text
prazo
importancia
status
ME
principal
duracao_min
data
```

## Derivados

Exemplos:

```text
prioridade
atraso
nota total da UP
média geral
```

Regra geral:

> Se um valor pode ser obtido com segurança a partir de outros dados armazenados, deve-se avaliar se realmente precisa ser persistido.

---

# 14. Convenções do projeto

## Interface

```text
src/interface/
```

## Regras acadêmicas

```text
src/academico/
```

## Regras de estudos

```text
src/estudos/
```

## Persistência

```text
src/persistencia/
```

## Análises compartilhadas

```text
src/sistema/
```

---

# 15. Regra para novas funcionalidades

Antes de implementar, perguntar:

1. Quais dados precisam ser armazenados?
2. Quais dados podem ser calculados?
3. Quais campos são obrigatórios?
4. Quais relacionamentos existem?
5. Quais entradas são inválidas?
6. Qual módulo deve conter a regra?
7. O menu está apenas coletando e apresentando informações?
8. A persistência está apenas salvando e recuperando dados?

Isso ajuda a evitar mistura de responsabilidades.