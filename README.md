# TASKUNI

Sistema acadêmico desenvolvido em Python para auxiliar estudantes na organização de disciplinas, conteúdos, tarefas, avaliações e sessões de estudo.

O projeto foi desenvolvido como atividade da disciplina de **Laboratório de Programação**, utilizando programação estruturada, persistência em JSON e Git/GitHub para colaboração.

## Funcionalidades

Atualmente o TASKUNI possui:

- gerenciamento de disciplinas;
- gerenciamento de conteúdos;
- tarefas acadêmicas e pessoais;
- prioridade e alertas de tarefas;
- avaliações com UP1 e UP2;
- cálculo de média;
- sessões de estudo acadêmicas e pessoais;
- persistência em arquivos JSON.

## Estrutura

```text
TASKUNI/
│
├── main.py
│
├── src/
│   ├── academico/
│   │   ├── disciplinas.py
│   │   ├── conteudos.py
│   │   ├── tarefas.py
│   │   └── avaliacoes.py
│   │
│   ├── estudos/
│   │   ├── sessoes.py
│   │   ├── metas.py
│   │   └── gamificacao.py
│   │
│   ├── interface/
│   │   ├── menu_principal.py
│   │   ├── menu_disciplinas.py
│   │   ├── menu_conteudos.py
│   │   ├── menu_tarefas.py
│   │   ├── menu_avaliacoes.py
│   │   └── menu_sessoes.py
│   │
│   ├── persistencia/
│   │   ├── _armazenamento.py
│   │   ├── disciplinas.py
│   │   ├── conteudos.py
│   │   ├── tarefas.py
│   │   ├── avaliacoes.py
│   │   ├── sessoes_estudo.py
│   │   └── metas.py
│   │
│   └── sistema/
│       ├── analise_tarefas.py
│       └── validacoes.py
│
├── docs/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Arquitetura

O sistema segue uma divisão simples de responsabilidades:

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

### Interface

Responsável por:

- menus;
- `input()`;
- `print()`;
- mensagens;
- apresentação dos dados.

### Domínio

Responsável pelas regras de negócio.

Os módulos ficam principalmente em:

```text
src/academico/
src/estudos/
```

### Persistência

Responsável por salvar e recuperar informações em JSON.

### Sistema

Responsável por análises e funcionalidades compartilhadas, como prioridade de tarefas.

## Menu principal

```text
========================
        TASKUNI
========================

1 - Disciplinas
2 - Conteúdos
3 - Tarefas
4 - Avaliações
5 - Sessões de estudo
0 - Sair
```

## Padrão de mensagens

```text
[OK]    operação concluída
[AVISO] informação ou ausência de registros
[ERRO]  operação inválida ou não concluída
```

## Executando

Na raiz do projeto:

```bash
python main.py
```

## Persistência

Os dados são armazenados em arquivos JSON gerados durante a execução.

Exemplos:

```text
disciplinas.json
conteudos.json
tarefas.json
avaliacoes.json
sessoes_estudo.json
```

Esses arquivos não devem ser versionados.

```gitignore
src/dados/*.json
__pycache__/
*.pyc
```

## Desenvolvimento

A branch de integração é:

```text
develop
```

A `main` é reservada para a versão estável/final.

Fluxo recomendado:

```bash
git switch develop
git pull origin develop
git switch -c feature/nome-da-funcionalidade
```

## Commits

Exemplos:

```text
feat: adiciona sessoes de estudo
fix: corrige validacao de disciplina
refactor: organiza camada de interface
docs: atualiza documentacao
chore: ignora arquivos locais de dados
```

## Documentação

As regras detalhadas do sistema estão em:

```text
docs/REGRAS_NEGOCIO.md
```

## Status

Implementado:

- disciplinas;
- conteúdos;
- tarefas;
- prioridade e alertas;
- avaliações;
- média geral;
- sessões de estudo;
- persistência;
- interface padronizada.

Próximas funcionalidades:

- metas;
- gamificação;
- dashboard;
- relatórios;
- testes adicionais.