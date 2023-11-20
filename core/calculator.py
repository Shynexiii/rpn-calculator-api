class Calculator:

    def __init__(self):
        self.stack = []

    def calculate(self, expression: str) -> float:
        """
        Calculates the result of a given expression in Reverse Polish Notation (RPN).

        This method processes an RPN expression, iterating through each token
        (either an operand or an operator). It adds operands to the stack and
        performs arithmetic operations for operators.

        Parameters
        ----------
        expression : str
            A string representing the arithmetic expression in RPN format.
            Tokens in the expression should be space-separated.

        Returns
        -------
        float
            The result of the calculated expression.

        Raises
        ------
        ValueError
            If the expression is incorrectly formatted, has insufficient operands,
            or contains invalid operands.

        Examples
        --------
        >>> calc = Calculator()
        >>> calc.calculate("3 4 +")
        7.0

        Notes
        -----
        The method relies on internal helper methods `_is_operator`, `_compute`,
        `_add_operand`, and `_get_result` for its operation.
        """
        for value in expression.split():
            if self._is_operator(value):
                self._compute(value)
            else:
                self._add_operand(value)
        return self._get_result()

    def to_rpn(self, expression: str) -> str:
        """
        Converts an infix arithmetic expression to Reverse Polish Notation (RPN).

        Parameters
        ----------
        expression : str
            The infix arithmetic expression to be converted. The expression should
            be a string where operands and operators are space-separated,
            and may include parentheses '(' and ')' for operation precedence.

        Returns
        -------
        str
            The converted expression in RPN format, where tokens are space-separated.

        Examples
        --------
        >>> calc = Calculator()
        >>> calc.to_rpn("3 + 4 * 2 / ( 1 - 5 )")
        '3 4 2 * 1 5 - / +'

        Notes
        -----
        The method assumes that the input expression is properly formatted
        and does not perform validation of the expression syntax.
        """
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        stack = []

        for token in expression.split():
            if token.isdigit():
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())

        return ' '.join(output)
    
    def format_expression(self, expression: str) -> str:
        """
        Format an arithmetic expression (infix or RPN) into individual elements.

        Parameters:
        - expression (str): The arithmetic expression to be formated.

        Returns:
        - str: A string of expression, separated by spaces.
        """
        tokens = []
        current_number = ''
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(current_number)
                    current_number = ''
                if char in '+-*/()':
                    tokens.append(char)
                elif char.strip() == '' and current_number:
                    tokens.append(current_number)
                    current_number = ''

        if current_number:
            tokens.append(current_number)

        return ' '.join(tokens)


    def _is_operator(self, token: str) -> bool:
        """
         Determines whether a given token is a valid arithmetic operator.

         Parameters
         ----------
         token : str
             The token to be checked. This should be a string representing
             a potential arithmetic operator.

         Returns
         -------
         bool
             True if the token is one of the recognized operators ('+', '-', '*', '/');
             False otherwise.
        """
        return token in ['+', '-', '*', '/']

    def _add_operand(self, operand: str):
        """
        Adds a numeric operand to the stack after converting it to a float.

        Parameters
        ----------
        operand : str
            A string representing the numeric operand to be added to the stack.
            The string should be convertible to a float.

        Raises
        ------
        ValueError
            If the input string 'operand' cannot be converted to a float,
            indicating it is not a valid numeric representation.
        """
        try:
            self.stack.append(float(operand))
        except ValueError:
            raise ValueError(f"Invalid operand: '{operand}' is not a number.")

    def _compute(self, operator: str):
        """
        Perform an arithmetic operation using the specified operator.

        Parameters
        ----------
        operator : str
            A string representing an arithmetic operator.
            Valid operators are '+', '-', '*', and '/'.

        Raises
        ------
        ValueError
            If there are fewer than two operands available on the stack,
            or if an invalid operator is provided.

        Notes
        -----
        In case of division, if the right-hand operand (divisor) is zero,
        the result is set to float('inf') to represent an infinite value.
        """
        if len(self.stack) < 2:
            raise ValueError("Insufficient operands to perform operation.")

        b, a = self.stack.pop(), self.stack.pop()
        if operator not in {'+', '-', '*', '/'}:
            raise ValueError(f"Invalid operator: '{operator}'.")

        operation = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a / b if b != 0 else float('inf'),
        }
        self.stack.append(operation[operator])

    def _get_result(self) -> float:
        """
        Retrieves the final calculation result from the stack.

        Returns
        -------
        float
            The final result of the calculation if the expression was valid.

        Raises
        ------
        ValueError
            If there is more than one or no element left on the stack,
            indicating an incorrect or incomplete expression.
        """
        if len(self.stack) != 1:
            raise ValueError("Incorrect number of operands remaining.")
        return self.stack.pop()

    def is_rpn(self, expression: str) -> bool:
        """
        Determines if a given expression is in Reverse Polish Notation (RPN).

        Parameters
        ----------
        expression : str
            The expression to be checked.

        Returns
        -------
        bool
            True if the expression is likely in RPN format, False if it's likely in infix format.

        Notes
        -----
        The function uses a heuristic based on the count of operands and operators.
        It may not be accurate for all cases, especially for more complex expressions.
        """
        operators = {'+', '-', '*', '/'}
        operand_count = 0
        operator_count = 0

        for token in expression.split():
            if token in operators:
                operator_count += 1
            else:
                operand_count += 1

        return operand_count - operator_count == 1
