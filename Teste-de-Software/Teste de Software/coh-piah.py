import re
import pytest
import pyautogui


def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra:"))
    ttr = float(input("Entre a relação Type-Token:"))
    hlr = float(input("Entre a Razão Hapax Legomana:"))
    sal = float(input("Entre o tamanho médio de sentença:"))
    sac = float(input("Entre a complexidade média da sentença:"))
    pal = float(input("Entre o tamanho medio de frase:"))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")

    return textos

def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas

def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)

def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()

def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    fator = []
    resultado = 0

    for i in range(0, len(as_a), 1):
        fator.append(abs(as_a[i] - as_b[i]))

    for i in range(0, len(fator), 1):
        resultado = resultado + fator[i]

    resultado = resultado / 6

    return resultado

def calcula_assinatura(texto):
    '''IMPLEMENTAR. Essa funcao recebe um texto e deve devolver a assinatura do texto.'''
    sentencas = []
    frases = []
    palavras = []

    caracteres = 0
    caracteres_sentenca = 0
    caracteres_frase = 0

    sentencas = separa_sentencas(texto)
    for sentenca in sentencas:
        frases.extend(separa_frases(sentenca))

    for frase in frases:
        palavras.extend(separa_palavras(frase))

    for palavra in palavras:
        caracteres = caracteres + len(palavra)

    qtd_palavras = len(palavras)
    qtd_frases = len(frases)
    qtd_sentencas = len(sentencas)

    for sentenca in sentencas:
        caracteres_sentenca = caracteres_sentenca + len(sentenca)

    for frase in frases:
        caracteres_frase = caracteres_frase + len(frase)

    qtd_palavras_unicas = n_palavras_unicas(palavras)
    qtd_palavras_diferentes = n_palavras_diferentes(palavras)

    wal = float(caracteres / qtd_palavras)
    ttr = float(qtd_palavras_diferentes / qtd_palavras)
    hlr = float(qtd_palavras_unicas / qtd_palavras)
    sal = float(caracteres_sentenca / qtd_sentencas)
    sac = float(qtd_frases / qtd_sentencas)
    pal = float(caracteres_frase / qtd_frases)


    return [wal, ttr, hlr, sal, sac, pal]

def avalia_textos(textos, ass_cp):
    '''IMPLEMENTAR. Essa funcao recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto com maior probabilidade de ter sido infectado por COH-PIAH.'''
    assinaturas = []
    grau_similaridade = []

    for texto in textos:
        assinaturas.append(calcula_assinatura(texto))

    for i in range (0, len(assinaturas), 1):
        grau_similaridade.append(compara_assinatura(ass_cp, assinaturas[i]))

    infectado = min(grau_similaridade)

    for i in range (0, len(grau_similaridade), 1):
        if grau_similaridade[i] == infectado:
            texto_infectado = i + 1

    return texto_infectado

def main():

    ass_cp = le_assinatura()
    textos = le_textos()

    resultado = "O autor do texto " + str(avalia_textos(textos, ass_cp)) + " está infectado com COH-PIAH."

    return resultado

def test_1(monkeypatch):

    responses = iter(["4.51", "0.693", "0.55", "0.0000001", "999", "1"])
    monkeypatch.setattr('builtins.input', lambda var: next(responses))

    x = le_assinatura()

    assert x == [4.51, 0.693, 0.55, 0.0000001, 999, 1]

def test_2(monkeypatch):

    enter = pyautogui.press('enter')

    responses = iter(["Agora eu sei que tenho um coração, porque ele está doendo.", "Se você não sabe para onde ir, qualquer caminho serve", "Desistir na metade é pior que nunca nem ter tentado.", "Eu tenho que sair deste lugar. Um dia eu vou pegar aquele trem.", "Um lobo de cabeça cortada ainda pode morder!", "Eu acho que um homem faz o que pode...até que seu destino lhe seja revelado!", "É apenas depois de perder tudo que somos livres para fazer qualquer coisa.", "Se você usar a sua mente, você pode fazer qualquer coisa.", "É aí que você sabe que encontrou alguém especial. Quando cala a boca por um minuto e confortavelmente aproveita o silêncio.", "Odeio quando você mente. Odeio quando me faz rir muito. Ainda mais quando me faz chorar... Odeio quando não está por perto. E o fato de não me ligar. Mas eu odeio principalmente não conseguir te odiar. Nem um pouco. Nem mesmo por um segundo. Nem mesmo só por te odiar.", enter])
    monkeypatch.setattr('builtins.input', lambda var: next(responses))

    y = le_textos()
    assert y == ["Agora eu sei que tenho um coração, porque ele está doendo.", "Se você não sabe para onde ir, qualquer caminho serve", "Desistir na metade é pior que nunca nem ter tentado.", "Eu tenho que sair deste lugar. Um dia eu vou pegar aquele trem.", "Um lobo de cabeça cortada ainda pode morder!", "Eu acho que um homem faz o que pode...até que seu destino lhe seja revelado!", "É apenas depois de perder tudo que somos livres para fazer qualquer coisa.", "Se você usar a sua mente, você pode fazer qualquer coisa.", "É aí que você sabe que encontrou alguém especial. Quando cala a boca por um minuto e confortavelmente aproveita o silêncio.", "Odeio quando você mente. Odeio quando me faz rir muito. Ainda mais quando me faz chorar... Odeio quando não está por perto. E o fato de não me ligar. Mas eu odeio principalmente não conseguir te odiar. Nem um pouco. Nem mesmo por um segundo. Nem mesmo só por te odiar."]

def test_3(monkeypatch):

    enter = pyautogui.press('enter')

    responses = iter(["4.51", "0.693", "0.55", "70.82", "1.82", "38.5", "Num fabulário ainda por encontrar será um dia lida esta fábula: A uma bordadora dum país longínquo foi encomendado pela sua rainha que bordasse, sobre seda ou cetim, entre folhas, uma rosa branca. A bordadora, como era muito jovem, foi procurar por toda a parte aquela rosa branca perfeitíssima, em cuja semelhança bordasse a sua. Mas sucedia que umas rosas eram menos belas do que lhe convinha, e que outras não eram brancas como deviam ser. Gastou dias sobre dias, chorosas horas, buscando a rosa que imitasse com seda, e, como nos países longínquos nunca deixa de haver pena de morte, ela sabia bem que, pelas leis dos contos como este, não podiam deixar de a matar se ela não bordasse a rosa branca. Por fim, não tendo melhor remédio, bordou de memória a rosa que lhe haviam exigido. Depois de a bordar foi compará-la com as rosas brancas que existem realmente nas roseiras. Sucedeu que todas as rosas brancas se pareciam exactamente com a rosa que ela bordara, que cada uma delas era exactamente aquela. Ela levou o trabalho ao palácio e é de supor que casasse com o príncipe. No fabulário, onde vem, esta fábula não traz moralidade. Mesmo porque, na idade de ouro, as fábulas não tinham moralidade nenhuma.", "Voltei-me para ela; Capitu tinha os olhos no chão. Ergueu-os logo, devagar, e ficamos a olhar um para o outro... Confissão de crianças, tu valias bem duas ou três páginas, mas quero ser poupado. Em verdade, não falamos nada; o muro falou por nós. Não nos movemos, as mãos é que se estenderam pouco a pouco, todas quatro, pegando-se, apertando-se, fundindo-se. Não marquei a hora exata daquele gesto. Devia tê-la marcado; sinto a falta de uma nota escrita naquela mesma noite, e que eu poria aqui com os erros de ortografia que trouxesse, mas não traria nenhum, tal era a diferença entre o estudante e o adolescente. Conhecia as regras do escrever, sem suspeitar as do amar; tinha orgias de latim e era virgem de mulheres.", "Senão quando, estando eu ocupado em preparar e apurar a minha invenção, recebi em cheio um golpe de ar; adoeci logo, e não me tratei. Tinha o emplasto no cérebro; trazia comigo a idéia fixa dos doidos e dos fortes. Via-me, ao longe, ascender do chão das turbas, e remontar ao Céu, como uma águia imortal, e não é diante de tão excelso espetáculo que um homem pode sentir a dor que o punge. No outro dia estava pior; tratei-me enfim, mas incompletamente, sem método, nem cuidado, nem persistência; tal foi a origem do mal que me trouxe à eternidade. Sabem já que morri numa sexta-feira, dia aziago, e creio haver provado que foi a minha invenção que me matou. Há demonstrações menos lúcidas e não menos triunfantes. Não era impossível, entretanto, que eu chegasse a galgar o cimo de um século, e a figurar nas folhas públicas, entre macróbios. Tinha saúde e robustez. Suponha-se que, em vez de estar lançando os alicerces de uma invenção farmacêutica, tratava de coligir os elementos de uma instituição política, ou de uma reforma religiosa. Vinha a corrente de ar, que vence em eficácia o cálculo humano, e lá se ia tudo. Assim corre a sorte dos homens.", enter])
    monkeypatch.setattr('builtins.input', lambda var: next(responses))

    z = main()
    assert z == 'O autor do texto 2 está infectado com COH-PIAH.'
