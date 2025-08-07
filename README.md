# Predição de Chuva no Rio Grande do Sul

Este repositório contém os scripts utilizados para a coleta, tratamento, análise e modelagem de dados meteorológicos com o objetivo de prever se choverá no dia seguinte no estado do Rio Grande do Sul.

## Objetivo

O projeto tem como objetivo principal a criação de modelos de aprendizado de máquina capazes de prever se haverá chuva no dia seguinte com base nos dados meteorológicos do dia atual. A tarefa é formulada como um problema de classificação binária, onde considera-se que choveu se a precipitação foi maior que 1mm.

## Coleta e Processamento de Dados

- Os dados meteorológicos foram coletados do Instituto Nacional de Meteorologia (INMET), abrangendo o período de 2001 a 2024.
- Os dados brutos consistem em arquivos separados por estação e por ano, com registros horários.
- As etapas de processamento incluíram:
- Agrupamento dos dados por dia.
- Cálculo de médias, máximos, mínimos ou somatórios, dependendo da natureza da coluna.
- Tratamento de dados faltantes e correção de registros inválidos (valores -9999).
- Criação da variável alvo: se choverá no próximo dia.

## Pré-processamento

Diversas técnicas de pré-processamento foram aplicadas e avaliadas:

### Tratamento de Dados Faltantes
- Exclusão de linhas sem o valor alvo.
- Preenchimento de valores faltantes com a média da respectiva coluna.

### Normalização
- Uso do `RobustScaler` do Scikit-Learn.
- Tratamento especial para a coluna de precipitação total, com `quantile_range` ajustado para melhor normalização.

### Detecção e Tratamento de Outliers
- Utilização do Z-score para identificação de outliers.
- Criação de abordagens diferentes para atributos com distribuição altamente concentrada como a precipitação.
- Após avaliação, optou-se por **não aplicar tratamento de outliers** nas etapas seguintes.

### Balanceamento de Classes
- Teste de diversas técnicas para lidar com o desbalanceamento entre os dias com e sem chuva.
- O método escolhido foi o **Random OverSampler**, por apresentar os melhores resultados nas métricas Recall e F1.

### Redução de Dimensionalidade
- Teste do uso de **PCA** com 21 componentes principais.
- PCA foi descartado por piorar o desempenho dos modelos.

### Seleção de Features
- Avaliação de métodos como `SelectKBest` e `SelectFromModel`.
- Optou-se por **não utilizar seleção de features**, pois a maioria dos testes indicou perda de desempenho.

## Definição do Problema e Avaliação

- O problema foi formalizado como uma tarefa de **classificação supervisionada**.
- Foram utilizadas as métricas: **acurácia**, **precisão**, **recall** e **F1-score**, com prioridade para recall e F1.
- Foi utilizado o método **holdout (80% treino, 20% teste)** para avaliação durante as etapas iniciais.
- Todo o pré-processamento foi realizado **após** a separação dos dados de treino e teste.

## Spot-Checking

Foram avaliados diversos algoritmos com os dados tratados:

- MLP (Multi-Layer Perceptron)
- Random Forest
- AdaBoost
- Regressão Logística
- Bagging
- SVC Linear
- Ensemble por Votação
- SGD
- KNN
- Bernoulli Naive Bayes
- LDA

O MLP foi o algoritmo com melhor desempenho nas métricas priorizadas (recall e F1). Também se destacaram o AdaBoost e a Regressão Logística.

## Conclusão

O projeto permitiu explorar em profundidade técnicas de pré-processamento e avaliação de modelos para um problema real, baseado em dados públicos brasileiros. Embora o problema tenha sido simplificado em relação à previsão completa de enchentes, o trabalho construiu uma base sólida para análises futuras mais complexas, com foco em modelos promissores como o MLP, Regressão Logística e AdaBoost.
