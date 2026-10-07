# TASKUNI

Sistema acadêmico desenvolvido em Python para auxiliar estudantes na organização de disciplinas, conteúdos, tarefas, avaliações e estudos.

O projeto está sendo desenvolvido como atividade da disciplina de **Laboratório de Programação**, utilizando programação estruturada, organização modular, persistência em JSON e Git/GitHub para desenvolvimento colaborativo.

---

# Funcionalidades atuais

## Disciplinas

O sistema permite:

- cadastrar disciplinas;
- listar disciplinas;
- atualizar disciplinas;
- remover disciplinas;
- informar professor opcionalmente.

Exemplo de exibição:

```text
[1] Estatística | Professor: Carlos
[2] Cálculo I | Professor: Não informado
```

---

## Conteúdos

O sistema permite:

- cadastrar conteúdos vinculados a uma disciplina;
- listar conteúdos;
- atualizar conteúdos;
- remover conteúdos.

Exemplo:

```text
[1] Distribuição de frequência | Disciplina: Estatística
[2] Probabilidade | Disciplina: Estatística
```

Um conteúdo obrigatoriamente deve estar associado a uma disciplina existente.

---

## Tarefas

O sistema permite:

- cadastrar tarefas acadêmicas;
- cadastrar tarefas pessoais;
- vincular opcionalmente uma tarefa acadêmica a uma disciplina;
- listar tarefas;
- filtrar tarefas por status;
- editar tarefas;
- concluir tarefas;
- reabrir tarefas;
- calcular prioridades;
- identificar tarefas atrasadas;
- identificar tarefas próximas do prazo.

Uma tarefa acadêmica **não é obrigada a possuir uma disciplina vinculada**.

Exemplo:

```text
[3] Estudar Estatística | Estatística | Prazo: 10/10/2026 | Importância: alta | Status: pendente
```

ou:

```text
[4] Organizar documentos da faculdade | Acadêmica | Prazo: 12/10/2026 | Importância: media | Status: pendente
```

---

## Prioridade de tarefas

A prioridade não é armazenada no JSON.

Ela é calculada com base em:

- importância;
- proximidade do prazo;
- atraso da tarefa.

A pontuação combina importância e urgência.

Exemplo:

```text
[ALTA atenção | 7 pts] [3] Estudar Estatística | ...
```

O sistema também identifica:

- tarefas atrasadas;
- tarefas com prazo próximo;
- tarefas pendentes.

---

# Avaliações

O sistema possui controle de notas por unidade.

Cada disciplina pode possuir:

```text
UP1
├── ME
└── Avaliação principal

UP2
├── ME
└── Avaliação principal
```

## ME

A **Medida de Eficiência (ME)** pode valer:

```text
0 até 2 pontos
```

## Avaliação principal

A avaliação principal pode valer:

```text
0 até 8 pontos
```

Ela pode representar, dependendo da disciplina:

- prova;
- trabalho;
- projeto;
- outra avaliação equivalente.

O TASKUNI não precisa registrar individualmente cada atividade que compõe a ME.

O usuário informa diretamente:

```text
ME
Avaliação principal
```

---

## Nota da unidade

A nota da unidade é calculada automaticamente:

```text
Nota da unidade = ME + Principal
```

Exemplo:

```text
ME: 1.8
Principal: 6.5

UP1 = 8.3
```

A nota da unidade **não é armazenada**, pois pode ser calculada a partir das notas registradas.

---

## Média geral

Após o registro da UP1 e da UP2, o sistema calcula a média geral da disciplina:

```text
Média = (UP1 + UP2) / 2
```

Exemplo:

```text
UP1 = 8.0
UP2 = 9.0

Média = 8.5
```

A média também não é armazenada no JSON.

Ela é calculada sempre que necessário, evitando duplicação e inconsistência de dados.

---

## Regras das avaliações

Cada disciplina pode possuir:

```text
1 registro de UP1
1 registro de UP2
```

Não é permitido cadastrar duas UP1 ou duas UP2 para a mesma disciplina.

Validações:

```text
Unidade:
1 ou 2

ME:
0 <= nota <= 2

Principal:
0 <= nota <= 8
```

Exemplo de exibição:

```text
[1] Estatística | UP1 | ME: 1.8/2 | Principal: 6.5/8 | Total: 8.3/10
```

---

# Organização do projeto

```text
TASKUNI/
│
├── main.py
│
├── src/
│   │
│   ├── academico/
│   │   ├── __init__.py
│   │   ├── disciplinas.py
│   │   ├── conteudos.py
│   │   ├── tarefas.py
│   │   └── avaliacoes.py
│   │
│   ├── estudos/
│   │   ├── __init__.py
│   │   ├── sessoes.py
│   │   ├── metas.py
│   │   └── gamificacao.py
│   │
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── menu_principal.py
│   │   ├── menu_disciplinas.py
│   │   ├── menu_conteudos.py
│   │   ├── menu_tarefas.py
│   │   └── menu_avaliacoes.py
│   │
│   ├── persistencia/
│   │   ├── __init__.py
│   │   ├── _armazenamento.py
│   │   ├── disciplinas.py
│   │   ├── conteudos.py
│   │   ├── tarefas.py
│   │   ├── avaliacoes.py
│   │   ├── sessoes_estudo.py
│   │   └── metas.py
│   │
│   └── sistema/
│       ├── __init__.py
│       ├── analise_tarefas.py
│       └── validacoes.py
│
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Responsabilidade das camadas

A aplicação foi dividida em módulos para evitar concentração de responsabilidades em arquivos grandes.

## `main.py`

É o ponto de entrada da aplicação.

Sua responsabilidade é apenas iniciar o TASKUNI e chamar o menu principal.

Fluxo:

```text
main.py
   ↓
menu_principal.py
```

---

## `src/interface`

Responsável pela interação com o usuário.

Contém:

- menus;
- `input()`;
- `print()`;
- leitura de opções;
- formatação de resultados;
- mensagens de sucesso, aviso e erro.

A interface não deve manipular arquivos JSON diretamente.

Também deve evitar implementar regras de negócio.

---

## `src/academico`

Contém as regras relacionadas à vida acadêmica.

Atualmente inclui:

```text
disciplinas.py
conteudos.py
tarefas.py
avaliacoes.py
```

Responsabilidades:

- validações;
- criação de registros;
- edição;
- regras específicas;
- consultas;
- cálculos acadêmicos.

---

## `src/estudos`

Responsável pelas funcionalidades relacionadas à rotina de estudos.

Funcionalidades previstas:

- sessões de estudo;
- metas;
- gamificação.

---

## `src/persistencia`

Responsável por armazenar e recuperar os dados.

Os módulos dessa pasta possuem operações como:

```text
adicionar
listar
buscar
atualizar
remover
```

Exemplo:

```text
persistencia/tarefas.py
persistencia/disciplinas.py
persistencia/avaliacoes.py
```

---

## `_armazenamento.py`

É o núcleo comum da persistência.

Responsável por:

- localizar os arquivos JSON;
- carregar dados;
- gravar dados;
- gerar IDs;
- criar a pasta de dados quando necessário.

Fluxo:

```text
persistencia/disciplinas.py
        ↓
persistencia/_armazenamento.py
        ↓
disciplinas.json
```

---

## `src/sistema`

Contém funcionalidades compartilhadas e análises.

Atualmente:

```text
analise_tarefas.py
validacoes.py
```

`analise_tarefas.py` é responsável por:

- calcular urgência;
- calcular prioridade;
- identificar tarefas atrasadas;
- identificar tarefas próximas.

Essas informações são calculadas em tempo de execução e não são armazenadas.

---

# Fluxo da aplicação

A estrutura principal segue:

```text
Usuário
   ↓
Interface
   ↓
Domínio
   ↓
Persistência
   ↓
JSON
```

Exemplo com tarefas:

```text
menu_tarefas.py
        ↓
academico/tarefas.py
        ↓
persistencia/tarefas.py
        ↓
persistencia/_armazenamento.py
        ↓
tarefas.json
```

Exemplo com avaliações:

```text
menu_avaliacoes.py
        ↓
academico/avaliacoes.py
        ↓
persistencia/avaliacoes.py
        ↓
persistencia/_armazenamento.py
        ↓
avaliacoes.json
```

---

# Dados armazenados

Os dados são persistidos em arquivos JSON.

Exemplos:

```text
disciplinas.json
conteudos.json
tarefas.json
avaliacoes.json
metas.json
sessoes_estudo.json
```

Esses arquivos são dados gerados durante a utilização do sistema e não devem ser versionados no Git.

---

# Dados armazenados x dados calculados

O projeto evita armazenar informações que podem ser derivadas de outros dados.

## Armazenados

Exemplos:

```text
nota ME
nota principal
prazo da tarefa
importância
status
disciplina_id
```

## Calculados

Exemplos:

```text
nota da UP
média geral
prioridade
urgência
atraso
proximidade do prazo
```

Isso reduz duplicação e risco de inconsistência.

---

# Interface

O TASKUNI utiliza interface de terminal.

Menu principal:

```text
========================
        TASKUNI
========================

1 - Disciplinas
2 - Conteúdos
3 - Tarefas
4 - Avaliações
0 - Sair

Escolha uma opção:
```

Os submenus seguem o mesmo padrão visual.

Exemplo:

```text
------------------------
       AVALIAÇÕES
------------------------

1 - Registrar notas
2 - Listar notas
3 - Atualizar notas
4 - Remover registro
5 - Ver média da disciplina
0 - Voltar
```

---

# Padrão de mensagens

A interface utiliza mensagens padronizadas.

## Sucesso

```text
[OK] Operação realizada com sucesso.
```

## Aviso

```text
[AVISO] Nenhum registro encontrado.
```

## Erro

```text
[ERRO] Não foi possível concluir a operação.
```

Esse padrão ajuda a manter a interface consistente.

---

# Executando o projeto

Na raiz do projeto:

```bash
python main.py
```

---

# Tecnologias utilizadas

- Python
- JSON
- Git
- GitHub

O projeto prioriza recursos compatíveis com os conteúdos estudados na disciplina.

Não são utilizadas tecnologias como:

- banco de dados;
- API;
- framework web;
- interface gráfica;
- orientação a objetos.

---

# Desenvolvimento colaborativo

A branch de integração do projeto é:

```text
develop
```

A branch:

```text
main
```

é reservada para a versão final/estável.

Antes de iniciar uma funcionalidade:

```bash
git switch develop
git pull origin develop
git switch -c feature/nome-da-funcionalidade
```

---

# Padrão de branches

Exemplos:

```text
feature/avaliacoes
feature/metas
feature/gamificacao
feature/dashboard
feature/sessoes-estudo
```

Outros tipos podem ser utilizados quando necessário:

```text
refactor/nome
fix/nome
chore/nome
```

---

# Padrão de commits

Exemplos:

```text
feat: adiciona controle de avaliacoes

fix: corrige validacao de notas

refactor: organiza camadas da aplicacao

refactor: padroniza menus e mensagens da interface

test: adiciona testes de tarefas

docs: atualiza documentacao do projeto

chore: ignora arquivos locais de dados
```

---

# Regras para colaboração

Ao desenvolver novas funcionalidades:

- atualizar a `develop` antes de criar uma branch;
- criar uma branch específica para a funcionalidade;
- evitar commits diretamente na `main`;
- manter as responsabilidades das pastas;
- não colocar regras de negócio dentro dos menus;
- não acessar arquivos JSON diretamente fora da persistência;
- evitar alterar módulos de outros integrantes sem necessidade;
- testar a funcionalidade antes da integração;
- utilizar commits descritivos;
- integrar funcionalidades na `develop`.

---

# Status atual

## Implementado

- estrutura modular do projeto;
- persistência em JSON;
- disciplinas;
- conteúdos;
- tarefas acadêmicas;
- tarefas pessoais;
- vínculo opcional entre tarefa acadêmica e disciplina;
- filtros de tarefas;
- conclusão e reabertura;
- prioridade de tarefas;
- alertas de prazo;
- avaliações;
- UP1;
- UP2;
- ME;
- avaliação principal;
- cálculo da nota da unidade;
- cálculo da média geral;
- interface padronizada.

## Próximas funcionalidades

- sessões de estudo;
- metas;
- gamificação;
- dashboard;
- análises acadêmicas adicionais;
- testes automatizados adicionais.

---

# Objetivo acadêmico

O projeto não tem como objetivo apenas funcionar.

A equipe deve compreender:

- organização dos módulos;
- fluxo da aplicação;
- funções utilizadas;
- estruturas de dados;
- persistência;
- validações;
- regras de negócio;
- decisões de arquitetura;
- integração entre os módulos.

Todos os integrantes devem conseguir explicar as partes principais do sistema durante a apresentação e avaliação do projeto.