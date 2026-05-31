# ChargeGrid Intelligence — Sprint 2

## Prova de Conceito Funcional

Este repositório contém o protótipo funcional desenvolvido para a Sprint 2 do projeto **ChargeGrid Intelligence**, uma solução de infraestrutura inteligente para recarga coletiva de veículos elétricos em condomínios.

O objetivo da prova de conceito é demonstrar, de forma simulada, a lógica principal do sistema: autenticação de usuários, gerenciamento de sessões de recarga, balanceamento dinâmico de carga, uso de energia renovável e registro de consumo por usuário.

---

## Sobre o Projeto

O ChargeGrid Intelligence propõe transformar carregadores residenciais individuais em uma rede inteligente de recarga coletiva para condomínios.

A solução foi pensada para resolver problemas como:

* sobrecarga da rede elétrica do condomínio;
* falta de controle de acesso aos carregadores;
* dificuldade na cobrança individual por morador;
* alto custo energético em horários de pico;
* baixo aproveitamento da energia solar gerada durante o dia.

---

## Objetivo da Sprint 2

Nesta Sprint, foi desenvolvido um simulador funcional em Python para comprovar a viabilidade técnica inicial da solução.

O protótipo demonstra:

* autenticação RFID simulada;
* adição e remoção de veículos em sessões de recarga;
* cálculo da energia disponível;
* balanceamento dinâmico de carga, conhecido como DLM;
* uso combinado de energia solar, bateria e rede elétrica;
* cálculo estimado de consumo, custo e CO₂ evitado;
* registro individual das sessões de recarga.

---

## Tecnologias Utilizadas

* **Python**: linguagem principal usada para desenvolver a lógica da simulação.
* **Streamlit**: biblioteca usada para criar o dashboard interativo no navegador.
* **Pandas**: biblioteca usada para organizar os dados das sessões em formato de tabela.

---

## Justificativa da Escolha do Protótipo

A solução completa do ChargeGrid envolveria carregadores reais, comunicação OCPP, autenticação RFID física, inversores solares, baterias e integração com sistemas de monitoramento energético.

Como esses equipamentos possuem alto custo e exigem uma infraestrutura física complexa, optamos por desenvolver uma simulação funcional em Python com Streamlit.

Essa escolha permite demonstrar a lógica central do sistema de forma acessível, visual e tecnicamente fundamentada. O foco da Sprint 2 foi comprovar que o sistema consegue tomar decisões de gerenciamento energético com base na quantidade de veículos conectados e na energia disponível.

---

## Funcionamento do Sistema

O simulador permite escolher diferentes cenários energéticos:

* **Pico solar**: maior geração de energia fotovoltaica.
* **Transição**: redução gradual da geração solar e maior uso de bateria.
* **Pico tarifário**: horário de maior custo da energia da rede.
* **Off-peak**: período de menor demanda e menor tarifa.

O usuário pode simular a passagem de um RFID autorizado. Quando isso acontece, um veículo é adicionado à sessão de recarga.

Caso o RFID seja inválido, o sistema bloqueia a recarga.

Quando há veículos conectados, o sistema realiza o seguinte cálculo:

1. Soma a energia disponível da fonte solar, bateria e rede elétrica.
2. Verifica se essa energia ultrapassa o limite máximo do condomínio.
3. Divide a potência disponível pela quantidade de veículos conectados.
4. Garante que nenhum carregador ultrapasse sua potência máxima.
5. Calcula consumo, custo estimado e CO₂ evitado.

---

## Relação com Sustentabilidade

O protótipo demonstra princípios de sustentabilidade e eficiência energética ao priorizar o uso de energia renovável e reduzir a dependência da rede elétrica em horários críticos.

A simulação considera o uso de energia solar e bateria como fontes prioritárias para alimentar os carregadores. Com isso, o sistema pode reduzir custos, evitar desperdício energético e diminuir emissões de CO₂ associadas ao uso da rede elétrica convencional.

---

## Como Executar o Projeto

### 1. Clonar ou baixar o repositório

Baixe os arquivos do projeto ou clone o repositório em sua máquina.

### 2. Instalar as dependências

No terminal, dentro da pasta do projeto, execute:

```bash
python -m pip install -r requirements.txt
```

### 3. Rodar o simulador

Execute:

```bash
python -m streamlit run app.py
```

### 4. Abrir no navegador

O Streamlit abrirá automaticamente o dashboard no navegador. Caso não abra, acesse o endereço exibido no terminal, geralmente:

```txt
http://localhost:8501
```

---

## Demonstração da Funcionalidade

Durante a execução, é possível:

* selecionar um cenário energético;
* adicionar veículos por RFID autorizado;
* bloquear uma tentativa com RFID inválido;
* remover veículos;
* visualizar a potência distribuída por veículo;
* acompanhar consumo, custo estimado e CO₂ evitado.

---
## Arquitetura do Sistema

A prova de conceito foi desenvolvida como uma simulação funcional do sistema ChargeGrid Intelligence.

A arquitetura simulada é composta por:

Morador
  ↓
Autenticação RFID simulada
  ↓
Dashboard / CSMS em Python com Streamlit
  ↓
Lógica de Balanceamento Dinâmico de Carga
  ↓
Distribuição de potência entre veículos conectados
  ↓
Registro de consumo, custo e CO₂ evitado


As fontes de energia consideradas na simulação são:

Energia Solar + Bateria + Rede Elétrica
              ↓
     Limite máximo do condomínio
              ↓
 Distribuição entre os carregadores


## Representação do OCPP na Prova de Conceito

Nesta prova de conceito, o protocolo OCPP não foi implementado em comunicação real com carregadores físicos. Ele foi representado de forma abstrata na lógica do simulador.

A autenticação RFID representa a etapa de `Authorize.req`.

A adição de um veículo representa o início de uma sessão de recarga, equivalente ao `StartTransaction`.

A redistribuição automática de potência representa a lógica do `SetChargingProfile`, usada para o balanceamento dinâmico de carga.

A remoção de um veículo representa o encerramento da sessão, equivalente ao `StopTransaction`.

Essa abordagem foi escolhida porque o objetivo da Sprint 2 é comprovar a lógica funcional inicial da solução, sem depender de carregadores físicos reais.


## Dados Simulados

O protótipo utiliza dados simulados para representar diferentes situações de operação do condomínio.

| Cenário | Solar | Bateria | Rede | Objetivo |
|---|---:|---:|---:|---|
| Pico solar | 22 kW | 4 kW | 4 kW | Demonstrar maior uso da energia fotovoltaica |
| Transição | 12 kW | 10 kW | 8 kW | Simular queda da geração solar e apoio da bateria |
| Pico tarifário | 2 kW | 16 kW | 12 kW | Reduzir dependência da rede em horário caro |
| Off-peak | 0 kW | 6 kW | 24 kW | Simular período de menor custo e maior uso da rede |

Esses valores foram definidos para fins de demonstração técnica e não representam uma instalação real específica.

## Conclusão

A prova de conceito demonstrou que a lógica principal do ChargeGrid Intelligence é tecnicamente viável.

Mesmo em ambiente simulado, o sistema consegue representar o funcionamento de um CSMS para condomínios, controlando sessões de recarga, distribuindo potência de forma inteligente e priorizando o uso de energia renovável.

Como melhorias futuras, o projeto poderia ser integrado a carregadores reais compatíveis com OCPP, leitores RFID físicos, APIs de monitoramento solar e sistemas reais de cobrança condominial.
