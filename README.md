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

Os dados são armazenados em arquivos JSON separados por entidade, na pasta `src/dados/`:

- `disciplinas.json`
- `conteudos.json`
- `tarefas.json`
- `avaliacoes.json`
- `sessoes_estudo.json`
- `metas.json`

A responsabilidade fica no pacote `src/persistencia/`:

- `_armazenamento.py`: única parte que abre e grava arquivos. Oferece `carregar`, `gravar` e `proximo_id`. A gravação é atômica (arquivo temporário + `os.replace`). Se um arquivo estiver corrompido, ele é renomeado para `<nome>.corrompido.json` e a coleção começa vazia.
- Um módulo por entidade (`disciplinas.py`, `conteudos.py`, `tarefas.py`, `avaliacoes.py`, `sessoes_estudo.py`, `metas.py`), cada um com `adicionar`, `listar`, `buscar`, `atualizar`, `remover` e `salvar`.

Regras desta camada:

- cada módulo manipula somente os próprios dados;
- não há validação de relacionamentos entre entidades (por exemplo, se um `disciplina_id` existe); essa verificação pertence à camada de domínio;
- o arquivo é salvo automaticamente após cada inclusão, alteração ou remoção;
- informações calculadas, como média, tempo total, XP, nível e quantidade de tarefas atrasadas, não são armazenadas.

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
