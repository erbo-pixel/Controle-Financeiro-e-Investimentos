# Meu Norte Financeiro

Aplicativo de controle financeiro pessoal e acompanhamento básico de aportes em investimentos, feito em Python com Streamlit.

## Problema e solução

Muitas pessoas anotam receitas, despesas e investimentos em lugares diferentes e têm dificuldade para entender quanto sobra no mês. O Meu Norte Financeiro reúne esses registros, calcula um resumo simples e permite consultar o histórico.

## Público

Pessoas que querem começar a organizar as finanças pessoais e acompanhar seus aportes, sem precisar de uma ferramenta complexa.

## Três funcionalidades principais

1. Painel com receitas, despesas, total investido e saldo disponível.
2. Cadastro de movimentações com categoria, descrição, data e validação do valor.
3. Histórico filtrável por tipo, com opção de baixar os dados em CSV.

## Como iniciar

1. Instale Python 3.10 ou superior.
2. No terminal, entre na pasta `outputs`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Inicie o aplicativo: `streamlit run app.py`.

Os dados ficam em `movimentacoes.csv`, criado automaticamente na mesma pasta quando o primeiro registro é salvo.

## Respostas sobre o desenvolvimento

**O que o aplicativo consegue fazer?** Ele registra receitas, despesas e aportes; apresenta os totais e o saldo disponível; e permite filtrar ou exportar o histórico.

**Qual parte do código recebe as informações?** Os campos de formulário (`selectbox`, `text_input`, `number_input` e `date_input`) capturam os dados. O botão `form_submit_button` envia o formulário, e a função `adicionar_movimentacao` organiza e salva o novo registro.

**Como a inteligência artificial ajudou?** A IA ajudou a transformar os requisitos em uma estrutura de telas e funções, sugeriu validações e apoiou a escrita do código e das instruções de uso. As decisões e a revisão final devem ser feitas por quem apresenta o trabalho.

**O que seria necessário aprender para melhorar?** Banco de dados, autenticação e proteção de dados, testes de software, integração com APIs financeiras e conceitos de rentabilidade e diversificação. Uma versão futura também poderia comparar o valor atual dos ativos com os aportes para estimar resultados.

> O aplicativo serve para organização e acompanhamento básico. Não fornece recomendação financeira nem calcula rentabilidade dos investimentos.
