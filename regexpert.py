import parser 
import nfa
import dfa

def main():
    inp = input()
    line = input().split()
    parsed = (parser.parse(inp))
    print("PARSED:", parsed)
    n = nfa.NFA(parsed)
    ans = n.read()
    if ans != -1:
        nfa.print_nfa(n.stack[0], n.stack[1])
        d = dfa.DFA(n)
        head = d.createDFA()
        dfa.print_dfa(head)
        for words in line:
            if d.readDFA(words, head, 0):
                print(words)
    else:
        print("ERROR")

main()

#TODO: Add concatenation operator asw.... just add . between consecutive letters and add another elif in parser and nfa