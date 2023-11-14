#Oleksander Turchyn
#300174825
#CSI 3120 Assignment 2
#Simple Syntax Analyzer written in Python

import sys



class SyntaxAnalyzer:
    def __init__(self):
        self.stack = []

    def analyze_syntax(self, code, file_name):
        if not code:
            print(f'The file {file_name} is empty.')
            return False

        for line_count, line in enumerate(code.split('\n'), start=2):
            line = line.strip()

            for char in line:
                if char in '({[':
                    self.stack.append((char, line_count))
                elif char in ')}]':
                    if not self.stack:
                        self.report_error(line_count, f'Unmatched closing {char}', file_name)
                        return False

                    last_open, _ = self.stack.pop()
                    if not self.is_matching_pair(last_open, char):
                        self.report_error(line_count, f'Unmatched closing {char}', file_name)
                        return False

            if line.endswith(';'):
                pass  
            elif '=' in line:
                self.check_assignment(line, line_count, file_name)

        if self.stack:
            last_open, line = self.stack.pop()
            self.report_error(line, f'Missing closing {self.get_matching_pair(last_open)}', file_name)
            return False

        return True

    def check_assignment(self, line, line_count, file_name):
        # Split the line into parts around the '=' symbol
        parts = line.split('=')

        # Check if there are exactly two parts and the second part is not empty
        if len(parts) == 2 and parts[1].strip():
            # Check if the second part contains an arithmetic expression
            if any(op in parts[1] for op in {'+', '-', '*', '/'}):
                # Check if the arithmetic expression contains an operator without an operand
                if '*' in parts[1] and parts[1].count('*') == 1:
                    self.report_error(line_count, 'Missing operand before operator', file_name)
                    return False
                else:
                    self.check_arithmetic_expression(parts[1], line_count, file_name)
        else:
            self.report_error(line_count, 'Missing semicolon', file_name)

    def check_arithmetic_expression(self, expression, line_count, file_name):
        operators = set('+-*/')
        operands = set('0123456789')

        i = 0
        while i < len(expression):
            char = expression[i]

            if char in operators:
                if i == 0 or i == len(expression) - 1 or expression[i - 1] not in operands or expression[i + 1] not in operands:
                    self.report_error(line_count, 'Missing operand before or after operator', file_name)
            elif char not in operands and char not in ' \t':
                self.report_error(line_count, f'Invalid character "{char}" in arithmetic expression', file_name)

            i += 1

    def is_matching_pair(self, open_char, close_char):
        pairs = {'(': ')', '{': '}', '[': ']'}
        return pairs[open_char] == close_char

    def get_matching_pair(self, char):
        pairs = {')': '(', '}': '{', ']': '['}
        return pairs[char]

    def report_error(self, line, message, file_name):
        print(f'Syntax analysis failed.\nsyntax_analyzer_error - {message} at line {line}')
        return False


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f'The file {file_path} was not found.')
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python syntax_analyzer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    code = read_file(file_path)

    analyzer = SyntaxAnalyzer()
    result = analyzer.analyze_syntax(code, file_path)
    if result:
        print(f'Syntax analysis succeeded')
