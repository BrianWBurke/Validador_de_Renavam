# Imports
import pandas as pd

# Ignorando mensagem de erro "FutureWarning"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Verificar se o CNPJ é válido e preencher com 14 caracteres
def verificar_renavam(renavam):
    if len(renavam) == 11:
        return renavam      
    else:
        len(renavam) <= 9 or len(renavam) == 10
        return renavam.zfill(11)

def validar_renavam(renavam):
    '''
    No caso do RENAVAM, o DV (dígito verificador)
    módulo 11 é calculado multiplicando cada dígito
    do número base pela sequência de multiplicadores
    2, 3, 4, 5, 6, 7, 8, 9, 2 e 3, posicionados da
    direita para a esquerda.
    O somatório destas multiplicações é
    multiplicado por 10 e depois dividido
    por 11, e o resto desta divisão é o DV.
    Porém, sempre que o resto da divisão for
    10, o DV será 0.
    '''

    # remove ultimo digito (verificador)
    renavam_sem_digito = renavam[:-1]

    # inverte
    renavam_sem_digito = renavam_sem_digito[::-1]

    # Multiplica as strings reversas do renavam pelos numeros multiplicadores
    # para apenas os primeiros 8 digitos de um total de 10
    # Exemplo: renavam reverso sem digito = 69488936
    # 6, 9, 4, 8, 8, 9, 3, 6
    # *  *  *  *  *  *  *  *
    # 2, 3, 4, 5, 6, 7, 8, 9 (numeros multiplicadores - sempre os mesmos [fixo])
    soma = 0
    for i, digito in enumerate(renavam_sem_digito[:8]):
        soma += int(digito) * (i + 2)

    # Multiplica os dois ultimos digitos e soma
    soma += int(renavam_sem_digito[8]) * 2
    soma += int(renavam_sem_digito[9]) * 3

    # mod11 = 284 % 11 = 9 (resto da divisao por 11)
    mod11 = soma % 11

    # Faz-se a conta 11 (valor fixo) - mod11 = 11 - 9 = 2
    ultimo_digito_calculado = 11 - mod11

    # ultimoDigito = Caso o valor calculado anteriormente seja 10 ou 11,
    # transformo ele em 0. caso contrario, eh o proprio numero
    if ultimo_digito_calculado >= 10:
        ultimo_digito_calculado = 0

    # Pego o ultimo digito do renavam original (para confrontar com o calculado)
    # Comparo os digitos calculado e informado
    if ultimo_digito_calculado == int(renavam[-1]):
        return True
    return False

def validar_renavams():
    csv = pd.read_csv('renavam.csv')

    tamCSV = len(csv)

    colunas = ['renavam',
               'validacao']

    df = pd.DataFrame(columns=colunas)

    for i in csv.itertuples():
        renavams = verificar_renavam(str(i[1]))
        renavam_verificado = validar_renavam(renavams)

        if renavam_verificado:
            renavam_verificado = 'Renavam valido'
        else:
            renavam_verificado = 'Renavam inválido'
        df = df.append({'renavam': renavams,
                        'validacao': renavam_verificado}, ignore_index = True)

    if tamCSV == len(df):
        print('Gerando CSV...')
        df.to_csv("Renavam_validado.csv", encoding='utf-8', index=False, sep=',')
        print("Arquivo unidades.csv criado com sucesso!")

# Iniciando o programa
print('Deseja realizar validação simples ou de mais de 1 renavam?')
print('1- Validação simples')
print('2- Validação de mais de um renavam')
resp = input('Digite sua resposta: ')

if resp == '1':
    renavam = input('Insira um renavam: ')
    renavam_verificado = verificar_renavam(renavam)
    validacao = validar_renavam(renavam_verificado)
    if validacao:
        print(f'O renavam {renavam_verificado} é valido')
    else:
        print(f'O renavam {renavam_verificado} é inválido')
elif resp == '2':
    print('Validando renavams...')
    validar_renavams()
else:
    print('Resposta inválida, encerrando o programa...')
