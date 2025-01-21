from itertools import product

# Function to convert infix to postfix
def infix_to_postfix(expression):
    precedence = {'!': 4, '&': 3, '|': 2, '->': 1}
    output = []
    stack = []
    
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isalpha():
            output.append(char)
        elif char == '!':
            stack.append(char)
        elif char == '-':
            if i+1 < len(expression) and expression[i+1] == '>':
                while stack and precedence.get('->', 0) <= precedence.get(stack[-1], 0):
                    output.append(stack.pop())
                stack.append('->')
                i += 1
        elif char in precedence:
            while stack and precedence.get(char, 0) <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            stack.pop()
        else:
            raise ValueError(f"Invalid character in expression: {char}")
        i += 1
    
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    
    return "".join(output)

# Function to evaluate postfix expression
def evaluate_postfix(expression, values):
    stack = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isalpha():
            stack.append(values[char])
        elif char == '!':
            val = stack.pop()
            stack.append(not val)
        elif char == '&':
            val2 = stack.pop()
            val1 = stack.pop()
            stack.append(val1 and val2)
        elif char == '|':
            val2 = stack.pop()
            val1 = stack.pop()
            stack.append(val1 or val2)
        elif char == '-':
            if i+1 < len(expression) and expression[i+1] == '>':
                val2 = stack.pop()
                val1 = stack.pop()
                stack.append(not val1 or val2)
                i += 1
        i += 1
    
    return stack[0]

# Function to generate truth table
def generate_truth_table(expression):
    variables = sorted(set(filter(str.isalpha, expression)))
    postfix_expr = infix_to_postfix(expression)
    combinations = list(product([False, True], repeat=len(variables)))
    
    print(f"Expression: {expression}")
    print(f"Postfix: {postfix_expr}")
    
    # Print header
    for var in variables:
        print(f"{var}\t", end="")
    print(f"{expression}")
    
    # Print truth table
    for combo in combinations:
        values = dict(zip(variables, combo))
        result = evaluate_postfix(postfix_expr, values)
        
        for val in combo:
            print(f"{'T' if val else 'F'}\t", end="")
        print(f"{'T' if result else 'F'}")

# Main loop to get valid input
while True:
    try:
        expression = input("Enter a logical expression: ").strip()
        if not expression:
            raise ValueError("Expression cannot be empty.")
        generate_truth_table(expression)
        break  # Exit the loop if input is valid
    except ValueError as e:
        print(f"Error: {e}")
        print("Please enter a valid logical expression using variables (A-Z), !, &, |, ->, and parentheses.")
