def parse(s: str):
    ans = []
    stack = []
    x = 1
    while x < len(s):
        if (s[x].isalpha() or s[x].isdigit()) and (s[x-1].isalpha() or s[x-1].isdigit()):
            s = s[:x] + "." + s[x:]
        x = x+1
    x = 0
    l = len(s)
    while x < l:
        ch = s[x]
        if ch.isalpha() or ch.isdigit():
            ans.append(ch)
        elif ch == ".":
            while stack and (stack[-1] != "(" and stack[-1] != "|"):
                ans.append(stack.pop())
            stack.append(ch)
        elif ch == '\\':
            if x == l-1:
                return -1
            ch += s[x+1]
            ans.append(ch)
            x = x+1
        elif ch == '[':
            while True:
                if s[x] == ']':
                    break
                if x == l-1:
                    return -1
                if s[x+1] == '\\':
                    x = x+1
                    if x == l:
                        return -1
                    ch += s[x+1]
                    x = x+1
                ch += s[x+1]
                x = x+1
            if ch == "[]":
                return -1
            ans.append(ch)
        elif ch == '+' or  ch == '?' or ch == '*':
            ans.append(ch)
        elif ch == '|' or ch == '(':
            while stack and stack[-1] != '(':
                ans.append(stack.pop())
            if ch == "(":
                ans.append(ch)
            stack.append(ch)
        elif ch == ')':
            if s[x-1] == '(':
                return -1
            while stack and stack[-1] != '(':
                ans.append(stack.pop())
            if not stack:
                return -1
            stack.pop()
            ans.append(ch)
        else:
            ans.append(ch)
        x = x+1
        
    while stack:
        ch = stack.pop()
        if ch == '(':
            return -1
        ans.append(ch)
    return ans