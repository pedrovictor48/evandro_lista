import pandas as pd
import math


def entropy(df, tab_number=0, printar=True):
    somatorio = 0
    if printar:
        print("\t"*tab_number + "Entropia = ", end="")
        for value in df['Risco'].unique():
            print(f"- p_{value}*log2(p_{value}) ", end="")
        print()
    if printar:
        print("\t"*tab_number + "Entropia = ", end="")
    for value in df['Risco'].unique():
        numerador = len(df[df.Risco == value])
        denominador = len(df)
        p_i = len(df[df.Risco == value]) / len(df)
        somatorio += p_i * math.log2(p_i)
        if printar:
            print(f"- {numerador}/{denominador}*log2({numerador}/{denominador}) ", end="")
    if printar:
        print()
        print("\t"*tab_number + f"Entropia = {-somatorio}")
    return -somatorio


def info_gain(df, colum, tab_number=0):
    print("\t"*tab_number + "Calculando Entropia(S):")
    entropia_S = entropy(df, tab_number+1)
    print("\t"*tab_number + f"Agora, calculando a entropia para cada valor da coluna '{colum}'")
    for value in df[colum].unique():
        print("\t"*tab_number + f"Para {colum} == {value}: ")
        novo_S = df[df[colum] == value]
        entropia = entropy(novo_S, tab_number+1)
        print("\t"*tab_number + f"Entropia(S_{value}) = {entropia}")
    somatorio = 0
    print("\t"*tab_number + f"IG(S, {colum}) = ", end='')
    for value in df[colum].unique():
        novo_S = df[df[colum] == value]
        somatorio += (len(novo_S) / len(df)) * entropy(novo_S, tab_number+1, False)
        print(f"- {len(novo_S)}/{len(df)} * {entropy(novo_S, tab_number+1, False)} ", end='')
    print()
    resultado = entropia_S - somatorio
    print("\t"*tab_number + f"IG(S, {colum}) = {resultado}")
    return resultado


rule_set = []


def print_df(df, tab_num):
    print("\t"*tab_num, end="")
    print([x for x in df.columns])
    for index, row in df.iterrows():
        print("\t"*tab_num, end="")
        print([x for x in row])


def print_se_entao(list_ands, result, tab_num):
    print("Se", end="")
    for expr in list_ands:
        print(f" {expr} e", end="")
    print(f"ntao o risco e {result}")


def split_info(df, col, tab_num):
    print("\t"*tab_num, end='')
    print(f"SplitInfo(S,{col}) = ", end="")
    for value in df[col].unique():
        n_ti = len(df[col][df[col] == value])
        n = len(df[col])
        print(f"- {n_ti}/{n}*log2({n_ti}/{n}) ", end="")
    print()
    print("\t"*tab_num, end='')
    print(f"SplitInfo(S,{col}) = ", end="")
    somatorio = 0
    for value in df[col].unique():
        n_ti = len(df[col][df[col] == value])
        n = len(df[col])
        print(f"- {n_ti}/{n}*({math.log2(n_ti/n)}) ", end="")
        somatorio -= (n_ti/n)*math.log2(n_ti/n)
    print()
    print("\t"*tab_num, end='')
    print(f"SplitInfo(S,{col}) = {somatorio}")
    return somatorio


def gain_ratio(df, col, tab_num):
    print("\t"*tab_num, end='')
    print(f"Calculando o ganho de informacao para {col}:")
    ig = info_gain(df, col, tab_num+1)
    print("\t"*tab_num, end='')
    print(f"Calculando o SplitInfo para {col}")
    split = split_info(df, col, tab_num+1)
    print("\t"*tab_num, end='')
    if ig != 0:
        print(f"Dessa forma, GainRatio para {col} = {ig}/{split} = {ig/split}")
        return ig/split
    else:
        print(f"Dessa forma, GainRatio para {col} = 0")
        return 0


def walk_tree(df, tab_num, list_ands):
    print("\t"*tab_num + "Nesse no, a tabela fica assim:")
    print_df(df, tab_num)
    # print(df)
    if len(df['Risco'].unique()) == 1:
        valor_unico = df['Risco'].unique()[0]
        print("\t"*tab_num + f"Como a tabela tem entropia 0, temos uma folha de valor {valor_unico}")
        print("\t"*tab_num + "Entao, entra na lista a regra ", end="")
        print_se_entao(list_ands, valor_unico, tab_num)
        rule_set.append(([x for x in list_ands], valor_unico))
        return
    # escolhe o cara de maior ganho
    max_ratio = -1e6
    chose = str()
    for col in df.columns:
        if col == "Risco":
            continue
        print("\t"*tab_num + f"Ganho de info. para o campo {col}")
        atual = gain_ratio(df, col, tab_num+1)
        if atual > max_ratio:
            max_ratio = atual
            chose = col
    print("\t"*tab_num + f"O campo escolhido foi {chose}, com ganho {max_ratio}")
    for ramos in df[chose].unique():
        print("\t"*tab_num + f"Para a escolha {chose} == {ramos}, a subarvore segue:")
        list_ands.append(f"'{chose}'=={ramos}")
        walk_tree(df[df[chose] == ramos], tab_num+1, list_ands)
        list_ands.pop()


def main():
    df = pd.read_csv("./data_risk.csv")
    walk_tree(df, 0, [])

    print("------")
    for (rule, res) in rule_set:
        print_se_entao(rule, res, 0)
        print()


main()
