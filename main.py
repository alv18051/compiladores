from infixToPostfix import *
from thompson import *
from drawAF import *
from afdAFN import *
from regexCheker import *
from subsets import *
from minimization import *
from simulation import *


if __name__ == '__main__':
    regexList = [
        "a+",                  # 0
        "ab*ab*",              # 1
        "a(a|b)*b",            # 2
    ]

    stringList = [
        "abab",              # 0
        "abbab",             # 1
        "ababab",            # 2
        
    ]

    regularExpression = RegexChecker()
    # regexInput = input("\nIngrese un regex, ex. 'a(a|b)*b': ")
    # regularExpression.regex = regexInput 
    regularExpression.regex = regexList[2]
    stringInput = stringList[2]

    regex = regularExpression.check()

    if not regularExpression.isValid:
        raise Exception(regex)

    postfix = InfixToPostfix(regex)
    postfix = InfixToPostfix.infixToPostfix(postfix)
    print("Postfix: " + postfix)

    thompson = Thompson(postfix)

    # construimos el afn
    afn = Thompson.nfaConstruction(thompson)
    afn.print_dfa()
    nfa_drawer = DrawAF(afn.transitions, afn.initial_state, [afn.final_state], 'AFN')
    nfa_drawer.draw(filename='grafos/AFN')
    # construimos el afd
    subsets = Subsets(afn)

    dfaSubsets = subsets.subAFDConstruction()
    dfaSubsets.print_afd()
    dfaSubsets_drawer = DrawAF(
        dfaSubsets.transitions, dfaSubsets.initial_state, dfaSubsets.final_states, 'AFD Subconjuntos')
    dfaSubsets_drawer.draw(filename='grafos/ADF_Subconjuntos')

    minSub = Minimization(dfaSubsets)

    # construimos el afd minimizado
    minDfaSubsets = minSub.minAFDConstruction()
    minDfaSubsets.print_afd()

    minDfaSubsets_drawer = DrawAF(
        minDfaSubsets.transitions, minDfaSubsets.initial_state, minDfaSubsets.final_states, 'AFD Minimizado')
    minDfaSubsets_drawer.draw(filename='grafos/afd_minimizado')

    #Simulamos los automatas
    nfaSim = AFNSimulation(afn, stringInput)
    print("AFN    --> " + str(nfaSim.simulate()))

    subsetsSim = AFDSimulation(dfaSubsets, stringInput)
    print("AFD S  --> " + str(subsetsSim.simulate()))

    minSubSim = AFDSimulation(minDfaSubsets, stringInput)
    print("Min S  --> " + str(minSubSim.simulate()))


