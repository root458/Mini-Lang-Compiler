
from typing import NamedTuple
import re

#Each Token Tuple(like dictionary)
class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return "<{0}, {1} >".format(self.type, self.value)


code = open("code.txt", "r").read()

def tokenize(code):
    keywords = {'using', 'namespace', 'std', 'float',
                'string', 'cout', 'cin', '<<', '>>', 'if', 'else', 'return'}
    token_specification = [
        ('COMMENT',             r'//+(.*)'),                           # COMMENT
        ('STD_OUT',             r'<<'),                                # STDOUT SYMBOL
        ('STD_IN',              r'>>'),                                # STDIN SYMBOL
        ('SAME_TYPE',           r','),                                 # Comma to denote Same type
        ('BLOCK_START',         r'{'),                                 # Block start
        ('BLOCK_END',           r'}'),                                 # Block end
        ('EXPRESSION_START',    r'[(]'),                               # Exp start
        ('EXPRESSION_END',      r'[)]'),                               # Exp end
        ('FUNCTION',            r'[A-Za-z]+([A-Za-z_]*)\(\)'),         # Function
        ('STRINGLITERAL',       r'"+([^"]*)+"'),                       # String literal
        ('STARTENDSTRING',      r'"'),                                 # Start or end of string
        ('INCLUDE',             r'#include <[a-z]+.[a-z]+>'),          # Include statement
        ('NUMBER',              r'\d+(\.\d*)?'),                       # Integer or decimal number
        ('ASSIGN',              r'='),                                 # Assignment operator
        ('END',                 r';'),                                 # Statement terminator
        ('IDENTIFIERS',         r'[A-Za-z][A-Za-z_]+'),                # Identifiers
        ('OP',                  r'[+\-*/]'),                           # Arithmetic operators
        ('RELATIONALOPS',       r'[><]|(&&)'),                              # Relational operators
        # ('LOGICALOPS',          r'[(&&)]|(||)'),                      # Logical operators
        # ('LOGICALOPS',          r'&&'),                                # Logical operators
        # ('LOGICALOPS',          r'||'),                              # Logical operators
        ('NEWLINE',             r'\n'),                                # Line endings
        ('SKIP',                r'[ \t]+'),                            # Skip over spaces and tabs
        # ('MISMATCH',      r'.'),                                     # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for matched_object in re.finditer(tok_regex, code):
        kind = matched_object.lastgroup
        value = matched_object.group()
        column = matched_object.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'IDENTIFIERS' and value in keywords:
            kind = value
        elif kind == 'INCLUDE':
            kind = 'include'
        elif kind == 'STRING':
            kind = 'String'
        elif kind == 'FUNCTION':
            kind = 'Function'
        elif kind == 'NEWLINE':
            line_start = matched_object.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)


codenot = r'''
#include <iostream>
using namespace std;

int main() {

    int basic_salary, sales_made, commission, total;
    string classification;

    cout << "SALARY CALCULATOR";

    cout << "\n\nEnter basic salary\n>>> ";
    cin >> basic_salary;

    cout << "\nEnter sales made\n>>> ";
    cin >> sales_made;

    commission = 0.2 * sales_made;

    total = basic_salary + commission;

    cout << "\nTotal: " << total << "\n\n";

    // Compare & Classify
    if (total > 0 && total > 40000) {
        cout << "Seller's salary is high\n";
    }
    else {
        cout << "Seller's salary is low\n";
    }

    return 0;
}
'''

for token in tokenize(code):
    print(token)
