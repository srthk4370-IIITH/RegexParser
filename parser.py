def parse(s: str):
    ans = []
    stack = []
    l = len(s)
    x = 0
    while x < l:
        ch = s[x]
        if ch.isalpha() or ch.isdigit():
            ans.append(ch)
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