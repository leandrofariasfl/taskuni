# TASKUNI

Sistema de Gestão Acadêmica e Estudos Gamificados desenvolvido para a disciplina de Laboratório de Programação.

O sistema será executado pelo terminal e permitirá organizar disciplinas, conteúdos, tarefas, avaliações, sessões de estudo e metas. A partir dos dados cadastrados, também produzirá análises determinísticas, estatísticas de estudo, XP, nível e um dashboard acadêmico.

## Estado atual

O projeto está na fase de preparação da estrutura base. Os módulos Python ainda não possuem funcionalidades implementadas.

## Requisitos

- Python 3.10 ou superior;
- nenhuma dependência externa para o MVP.

As bibliotecas necessárias pertencem à biblioteca padrão do Python. O arquivo `requirements.txt` existe para deixar essa decisão explícita e permitir futuras alterações controladas.

## Estrutura

```text
TASKUNI/
├── main.py
├── disciplinas.py
├── conteudos.py
├── tarefas.py
├── avaliacoes.py
├── estudos.py
├── gamificacao.py
├── analise.py
├── dashboard.py
├── persistencia.py
├── validacoes.py
├── data/
│   └── taskuni.json
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── TEAM_WORKFLOW.md
│   └── MANUAL_TESTS.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Documentação oficial

- `docs/PROJECT_CONTEXT.md`: escopo, modelo de dados e contratos;
- `docs/TEAM_WORKFLOW.md`: branches, integração e revisão;
- `docs/MANUAL_TESTS.md`: registro dos testes manuais.

Antes de implementar uma funcionalidade, a equipe deve consultar esses documentos. Alterações em campos, tipos, relacionamentos ou valores permitidos precisam ser documentadas e aprovadas antes da implementação.

## Persistência

Os dados serão mantidos em `data/taskuni.json`. Somente `persistencia.py` poderá conhecer os detalhes de leitura e escrita desse arquivo.

Informações que podem ser calculadas, como média, tempo total, XP, nível e quantidade de tarefas atrasadas, não serão armazenadas no JSON.

## Execução

Quando o ponto de entrada estiver implementado, o programa será iniciado com:

```bash
python main.py
```

Na fase atual, `main.py` é apenas um arquivo estrutural e ainda não inicia o sistema.

## Desenvolvimento

- `main`: versão estável;
- `develop`: integração das funcionalidades;
- `feature/*`: desenvolvimento de cada funcionalidade;
- `setup/project-base`: preparação inicial do repositório.

O projeto utiliza programação procedural com funções, listas, dicionários e módulos. Orientação a objetos, banco de dados, interface gráfica, API e inteligência artificial estão fora do escopo do MVP.
