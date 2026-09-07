import parser 
import nfa
import dfa
import sys

def main():
    debug = "--debug" in sys.argv
    lines = sys.stdin.readlines()
    if not lines:
        print("Parse Error", file= sys.stderr)
        return 1
    inp = lines[0].rstrip("\n")
    text = []
    for line in lines[1:]:
        text.extend(line.split())
    parsed = parser.parse(inp)
    if parsed == -1:
        print("Parse Error", file= sys.stderr)
        return 1
    n = nfa.NFA(parsed)
    ans = n.read()
    if ans == -1:
        print("Parse Error", file= sys.stderr)
        return 1      
    d = dfa.DFA(n)
    head = d.createDFA()
    if debug:
        dfa.print_dfa(head)
    for words in text:
        if d.readDFA(words, head, 0):
            print(words)
     
if __name__ == "__main__" :
    main()
