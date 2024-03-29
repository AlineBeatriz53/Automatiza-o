import pandas as pd
import win32com.client as win32

# Importar a base de dados
tabela_vendas = pd.read_excel('Vendas.xlsx')

# Vizualizar a base de dados
pd.set_option('display.max_column', None)
print(tabela_vendas)

# Faturamento por loja
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)

# Quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(quantidade)
print('-' * 50)

# Ticket médio por produto em cada loja
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0:  'Ticket Médio'})
print(ticket_medio)

# Enviar um email com o relatório

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'bia.ali5353@gmail.com'
mail.Subject = 'Relatório de Cada Loja'
mail.Body = 'Message body'
mail.HTMLBody = f''' 
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}
    
<p>Quantidade Vendida:</p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Dúvidas estou à disposição:</p>

Att.,
Aline
'''

mail.Send()

print ('Email Enviado')