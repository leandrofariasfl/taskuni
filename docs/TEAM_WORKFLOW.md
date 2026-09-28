# TASKUNI — Workflow da Equipe

## 1. BRANCHES PRINCIPAIS

### main

Representa a versão estável do projeto.

Não desenvolver diretamente nela.

### develop

Integra as funcionalidades que estão sendo desenvolvidas.

Features nascem de `develop`.

Após uma feature ser revisada, ela volta para `develop`.

Quando uma versão estiver estável, `develop` será integrada à `main`.

---

# 2. PRIMEIRA BRANCH

Antes das features:

setup/project-base

Responsabilidade:

- estrutura de diretórios;
- arquivos iniciais;
- documentação;
- `.gitignore`;
- `requirements.txt`;
- estrutura inicial do JSON;
- arquivos Python vazios ou apenas preparados estruturalmente.

O arquivo `data/taskuni.json` deve ser versionado inicialmente com as coleções vazias. Dados pessoais usados durante testes não devem ser enviados nos commits.

Não implementar funcionalidades completas nessa branch.

Depois de revisada:

setup/project-base
↓
develop

A partir daí começa o trabalho paralelo.

---

# 3. BRANCHES DE FEATURE

Utilizar:

feature/nome-da-funcionalidade

Exemplos:

feature/disciplinas-conteudos

feature/tarefas

feature/avaliacoes-notas

feature/estudos-metas

feature/persistencia

feature/gamificacao

feature/analise

feature/dashboard

Evitar branch com nome do integrante.

A branch representa a funcionalidade, não a pessoa.

---

# 4. PRIMEIRA ONDA DE DESENVOLVIMENTO

Depois da estrutura base estar na `develop`, podem começar em paralelo:

## Frente A

Disciplinas + conteúdos.

Branch:

feature/disciplinas-conteudos

## Frente B

Tarefas.

Branch:

feature/tarefas

## Frente C

Avaliações + notas.

Branch:

feature/avaliacoes-notas

## Frente D

Estudos + metas.

Branch:

feature/estudos-metas

## Frente E

Persistência + estrutura dos dados.

Branch:

feature/persistencia

Essas cinco frentes formam a fundação do sistema.

---

# 5. SEGUNDA ONDA

Depois que dados essenciais estiverem integrados:

## Gamificação

Depende principalmente das sessões de estudo.

feature/gamificacao

## Análise

Depende principalmente de tarefas e avaliações.

feature/analise

## Dashboard

Depende dos módulos já produzirem informações.

feature/dashboard

A distribuição dessas features entre os integrantes deve considerar quem terminar primeiro a primeira onda.

Não deixar toda integração permanentemente sobre apenas uma pessoa.

---

# 6. DEPENDÊNCIAS

Disciplinas
↓
Conteúdos

Disciplinas
↓
Avaliações

Disciplinas
↓
Estudos acadêmicos

Conteúdos
↓
Avaliações

Conteúdos
↓
Estudos

Tarefas + Avaliações
↓
Análise

Estudos
↓
Metas

Estudos
↓
Gamificação

Todos os módulos
↓
Dashboard

Persistência
↔
Todos os dados

Isso significa que o modelo de dados deve ser definido ANTES do trabalho paralelo.

Antes de abrir as branches da primeira onda, a equipe deve confirmar que os contratos gerais de `PROJECT_CONTEXT.md` estão aprovados e integrados em `develop`.

A implementação de persistência pode ocorrer em paralelo, mas os demais módulos devem trabalhar apenas com o dicionário em memória e não podem criar formatos próprios nem acessar o JSON diretamente.

---

# 7. COMMITS

Padrão:

feat:

fix:

refactor:

docs:

test:

chore:

Exemplos:

feat: adiciona cadastro de disciplinas

feat: adiciona registro de sessão de estudo

fix: impede duração negativa no estudo

refactor: reutiliza validação de data

docs: documenta regras de prioridade

test: adiciona cenários manuais para tarefas

chore: cria estrutura inicial do projeto

---

# 8. TAMANHO DO COMMIT

Um commit deve representar uma ideia coerente.

Evitar:

"terminei módulo inteiro"

"várias alterações"

"final"

"update"

Preferir:

feat: adiciona criação de tarefa

feat: adiciona conclusão de tarefa

feat: adiciona filtro por status

Mesmo que as três mudanças pertençam ao mesmo módulo.

---

# 9. ANTES DE COMEÇAR UMA FEATURE

Confirmar:

- qual requisito está sendo implementado;
- quais dados serão utilizados;
- quais módulos serão importados;
- quais funções serão necessárias;
- quais outras features são dependências;
- quais campos do modelo serão acessados;
- quais casos precisam ser testados.
- se os contratos gerais do modelo já cobrem as relações e os valores utilizados.

Não alterar o modelo de dados unilateralmente.

---

# 10. DEFINITION OF DONE

Uma tarefa só está pronta quando:

- funciona no cenário normal;
- entradas inválidas foram consideradas;
- coleção vazia foi considerada;
- nomes estão claros;
- não utiliza POO;
- respeita o modelo de dados;
- não acessa JSON diretamente fora da persistência;
- não duplica lógica sem necessidade;
- foi executada manualmente;
- outro integrante consegue explicar seu funcionamento;
- possui commits claros;
- está pronta para revisão.

---

# 11. PULL REQUEST

Antes do merge, verificar:

## Funcionalidade

Funciona?

Atende ao requisito?

## Dados

Respeita PROJECT_CONTEXT.md?

Alterou algum campo compartilhado?

## Código

Funções possuem responsabilidades claras?

Existe repetição?

Nomes são compreensíveis?

## Validação

Entradas inválidas foram consideradas?

## Integração

Pode quebrar outro módulo?

## Ensino

Outro integrante consegue explicar?

---

# 12. ALTERAÇÃO DE MODELO

Exemplo:

Um integrante percebe que precisa adicionar:

`tarefa["dificuldade"]`

Não deve simplesmente adicionar.

Primeiro:

1. explicar necessidade;
2. verificar módulos afetados;
3. discutir com equipe;
4. atualizar PROJECT_CONTEXT.md;
5. só depois implementar.

---

# 13. REUNIÃO RÁPIDA DE INTEGRAÇÃO

Quando possível, fazer uma revisão curta diária:

- o que foi concluído;
- o que está em andamento;
- bloqueios;
- alteração de contrato;
- merge necessário;
- conflitos previstos.

Isso evita cinco versões diferentes do sistema.

---

# 14. REGRA DE RESPONSABILIDADE

"Eu não programei essa parte" NÃO pode significar "eu não sei explicar essa parte".

Antes da apresentação, todos devem revisar:

- fluxo principal;
- estrutura do JSON;
- relações por ID;
- persistência;
- disciplinas;
- tarefas;
- avaliações;
- estudos;
- gamificação;
- análise;
- dashboard.

---

# 15. INTEGRAÇÃO FINAL

Não deixar todas as features para integrar no último dia.

Integrar continuamente em `develop`.

Ordem aproximada:

estrutura base

↓

persistência

↓

disciplinas / conteúdos

↓

tarefas / avaliações / estudos

↓

metas / gamificação

↓

análise

↓

dashboard

↓

revisão

↓

main

---

# 16. CONGELAMENTO DO ESCOPO

Quando faltar pouco tempo para a entrega:

não adicionar funcionalidades novas.

Priorizar:

correções;

testes;

integração;

documentação;

compreensão;

simulação da apresentação.
