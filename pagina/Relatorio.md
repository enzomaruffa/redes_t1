# Relatório

O projeto consiste de uma simulação do preço das ações do "Canil de Outros Reinos"!

Assim, o servidor e cliente tem os seguintes papéis:
- servidor envia mensagens com os valores da ação naquele instante
- cliente recebe e acompanha os preços das ações

Ao sair da transmissão, o cliente realiza uma regressão linear sobre os valores e determina se deve ou não comprar ações - ou seja, se ele acredita que o preço vai crescer ou cair :)

