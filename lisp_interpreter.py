# symbol table of the local environment variables plus a link to the symbol table of the defining environment
class Symbol_table:
    def __init__(self, parent_table):
        # this is a list of (name, value) pairs, not a dict, because names can be overwritten and the newest name is always chosen
        self.table = []
        # when there is no parent, choose None
        self.parent = parent_table
    # look up variable name
    def lookup(self, var_name):
        for (name, value) in self.table:
            if name == var_name:
                return value
        if self.parent == None:
            return None
        return self.parent.lookup(var_name)
    # add variable in symbol table
    def add(self, name, value):
        self.table.insert(0, (name, value))
    # set value of variable
    def set_value(self, var_name, new_value):
        for i, (name, old_value) in enumerate(self.table):
            if name == var_name:
                self.table[i] = (var_name, new_value)
                return
        if self.parent != None:
            self.parent.set_value(var_name, new_value)
    # clear symbol table
    def clear(self):
        del self.table
        self.table = []

# stream of characters from input
class Inputstream:
    def __init__(self):
        self.unused_chars = ''
    def read_next_char(self):
        if self.unused_chars == '':
            self.unused_chars = input() + '\n'
        return self.unused_chars[0]
    def get_next_char(self):
        ch = self.read_next_char()
        self.unused_chars = self.unused_chars[1:]
        return ch

# stream of tokens given input stream
class Tokenstream:
    def __init__(self):
        self.inputstream = Inputstream()
    def get_next_token(self):
        ch = self.inputstream.get_next_char()
        while isspace(ch):
            ch = self.inputstream.get_next_char()
        if ch == '(' or ch == ')' or is_quotechar(ch):
            return ch
        else:
            token = ch
            ch = self.inputstream.read_next_char()
            while is_normalchar(ch):
                self.inputstream.get_next_char()
                token = token + ch
                ch = self.inputstream.read_next_char()
            return token
    # extracts the tokens of one statement from the token stream
    def get_one_statement(self):
        num_parens = 0
        statement_tokens = []
        while True:
                token = self.get_next_token()
                if num_parens == 0 and token == ")":
                        # to do: report a syntax error
                        print("syntax error")
                        raise RuntimeError("syntax")

                if token == "(":
                        num_parens += 1
                if token == ")":
                        num_parens -= 1
                statement_tokens.append(token)

                if num_parens == 0 and (token == ")" or is_normalstring(token)):
                        break

        return statement_tokens

# dummy class declaration so that the class lisp_object_t can be referred to inside itself
class lisp_object_t:
    pass

# parent class for all Lisp objects
# many methods are overridden by child classes and simply return their default values here
class lisp_object_t:
        # inherits to lisp_atom_t and lisp_list_t
        # to be overridden
        def is_atom(self):
                return False
        # to be overridden
        def is_list(self):
                return False
        # to be overridden
        def is_nil(self):
                return False
        # to be overridden
        def length(self):
                return -1
        # to be overridden
        def to_bool(self):
                return True
        # to be overridden
        def built_in_name(self):
                print("Error: object {} is not a built-in function".format(self))
                raise RuntimeError("evaluation")
        # to be overridden
        def car(self):
                if self.is_nil():
                        return self
                print("Error: car can only be called on a list")
                raise RuntimeError("evaluation")
        # to be overridden
        def cdr(self):
                if self.is_nil():
                        return self
                print("Error: cdr can only be called on a list")
                raise RuntimeError("evaluation")
        # to be overridden
        def to_int(self):
                print("Error: {} is not a number".format(self))
                raise RuntimeError("evaluation")

# class for all atoms
class lisp_atom_t(lisp_object_t):
        def is_atom(self):
                return True
        # to be overridden
        def is_numeric(self):
                return False
        # to be overridden
        def is_function(self):
                return False
        # to be overridden
        def is_symbol(self):
                return False
        def length(self):
                return 0
        # returns a list of "members" of self, as a string
        # an atom has no members, so this returns the empty string if self is nil or a dotted pair description otherwise
        def members_str(self):
                if self.is_nil():
                        return ""
                else:
                        return " . " + str(self)

# class for all numeric values
class lisp_numeric_t(lisp_atom_t):
        def __init__(self, num):
                self.value = num
        def is_numeric(self):
                return True;
        def to_int(self):
                return self.value
        def name(self):
                return str(self.value)
        def __str__(self):
                return self.name()

# class for all symbols (quoted names)
# the booleans (t and nil) are the only symbols that evaluate to themselves when evaluated as code
class lisp_symbol_t(lisp_atom_t):
        def __init__(self, text):
                if is_num(text):
                        print("Error: initializing numeric object as symbol")
                        raise RuntimeError("evaluation")
                self.text = text.lower()
        def is_symbol(self):
                return True
        def is_nil(self):
                return self.text == "nil"
        def is_t(self):
                return self.text == "t"
        def is_bool(self):
                return self.is_nil() or self.is_t()
        def to_bool(self):
                return self.text != "nil"
        def name(self):
                return self.text
        def __str__(self):
                return self.name()

# class for all function objects
# class elements:
# fn_params (Lisp list of formal parameter names, or None if built-in function)
# fn_defn (function definition code, or None if built-in function)
# built_in (True if built-in function, False otherwise)
# fn_name (function name if built-in function, or None otherwise)
# symbol_table (table of variables in function environment, or None if built-in function)
class lisp_func_t(lisp_atom_t):
        # in the initializer, params, defn, and definer_vars are for user-defined functions and name is for built-in functions. Any value that isn't used is None.
        def __init__(self, params: lisp_object_t, defn: lisp_object_t, name: str, definer_vars: Symbol_table):
                self.fn_params = params
                self.fn_defn = defn
                self.built_in = (name != None)
                self.fn_name = name
                self.symbol_table = Symbol_table(definer_vars) if definer_vars != None else None
        def is_function(self):
                return True
        # built-in functions are "+", "-", "*", "/", "car", "cdr", "cons", "sqrt", "pow", ">", "<", "=", "!=", "and", "or", "not"
        def is_built_in(self):
                return self.built_in
        def params(self):
                return self.fn_params
        def defn(self):
                return self.fn_defn
        def built_in_name(self):
                return self.fn_name
        # calls function with actual parameters specified as objects in args_list
        def call(self, args_list):
                if (self.is_built_in()):
                        # evaluate built-in function by calling equivalent function in source code
                        if self.fn_name == "+":
                                return add(args_list)
                        if self.fn_name == "-":
                                return subtract(args_list)
                        if self.fn_name == "*":
                                return multiply(args_list)
                        if self.fn_name == "/":
                                return divide(args_list)
                        if self.fn_name == "car":
                                return car(args_list)
                        if self.fn_name == "cdr":
                                return cdr(args_list)
                        if self.fn_name == "cons":
                                return cons(args_list)
                        if self.fn_name == "sqrt":
                                return math_sqrt(args_list)
                        if self.fn_name == "pow":
                                return math_pow(args_list)
                        if self.fn_name == ">":
                                return greater(args_list)
                        if self.fn_name == "<":
                                return less(args_list)
                        if self.fn_name == "=":
                                return equal(args_list)
                        if self.fn_name == "!=":
                                return not_equal(args_list)
                        if self.fn_name == "and":
                                return logic_and(args_list)
                        if self.fn_name == "or":
                                return logic_or(args_list)
                        if self.fn_name == "not":
                                return logic_not(args_list)
                        if self.fn_name == "quit":
                                print("bye")                                
                                out_file.close()
                                exit()
                else:
                        # check that function call has the right number of arguments
                        if self.fn_params.length() != args_list.length():
                                print("Error: wrong number of arguments")
                                raise RuntimeError("evaluation")
                        # bind actual parameters to formal parameters; add to symbol table
                        next_params = self.fn_params
                        next_args = args_list
                        while next_params.is_list():
                                self.symbol_table.add(next_params.car().name(), next_args.car())
                                next_params = next_params.cdr()
                                next_args = next_args.cdr()
                        # evaluate function body
                        next_defn = self.fn_defn
                        while next_defn.is_list():
                                result = eval_code_object(next_defn.car(), self.symbol_table)
                                next_defn = next_defn.cdr()
                        # clear symbol table for next function call
                        self.symbol_table.clear()
                        return result

# class for all lists, except nil
class lisp_list_t(lisp_object_t):
        def car(self) -> lisp_object_t:
                return self.head
        def cdr(self) -> lisp_object_t:
                return self.tail
        def __init__(self, head: lisp_object_t, tail: lisp_object_t):
                self.head = head
                self.tail = tail
        def is_list(self):
                return True
        def set_car(self, head: lisp_object_t):
                self.head = head
        def set_cdr(self, tail: lisp_object_t):
                self.tail = tail
        # length of an atom is 0, length of a list is the number of elements
        def length(self):
                return 1 + self.cdr().length()
        # returns string representation of list
        def __str__(self):
                obj_str = '('
                obj_str += self.members_str()
                obj_str += ')'
                return obj_str
        # returns a string representation of all members of the list, separated by spaces. the list is not enclosed in parentheses
        def members_str(self):
                return str(self.car()) + ('' if self.cdr().is_atom() else ' ') + self.cdr().members_str()

# names of all built-in functions
built_in_funcs = ['+', '-', '*', '/', 'car', 'cdr', 'cons', 'sqrt', 'pow', '>', '<', '=', '!=', 'and', 'or', 'not', 'quit']

def isspace(ch):
    return ch == ' ' or ch == '\t' or ch == '\n'

def is_quotechar(ch):
    return ch == '`' or ch == '\''

# normal character is anything except space and quoting character
def is_normalchar(ch):
    return ch != '`' and ch != '\'' and ch != '(' and ch != ')' and not isspace(ch)

# normal string is a string of normal characters
def is_normalstring(string):
        if len(string) == 0:
                return True
        return is_normalchar(string[0]) and is_normalstring(string[1:])

# replace quotes in statement with the equivalent (quote ...) command
def replace_quotes(statement_tokens):
        replaced_tokens = []
        is_quoted = False
        num_parens_in_quote = 0
        for token in statement_tokens:
                if is_quoted and token == "(":
                        num_parens_in_quote += 1
                if is_quoted and token == ")":
                        num_parens_in_quote -= 1
                if is_quotechar(token) and not is_quoted:
                        is_quoted = True
                        num_parens_in_quote = 0
                        replaced_tokens.append("(")
                        replaced_tokens.append("quote")
                else:
                        replaced_tokens.append(token)
                if is_quoted and num_parens_in_quote == 0 and not is_quotechar(token):
                        is_quoted = False
                        replaced_tokens.append(")")

        return replaced_tokens

# convert token list into Lisp object representing single statement of code
# p_start_index is a list containing one member: the starting index of the statement in statement_tokens. when the function returns, p_start_index contains the starting index of the next statement.
# this is done so that the function can call itself to parse a subexpression in the same list
def make_code_object(statement_tokens, p_start_index):
        if is_normalstring(statement_tokens[p_start_index[0]]):
                text = statement_tokens[p_start_index[0]]
                p_start_index[0] += 1
                # to do: add the code for creating different objects if the string is a number etc.
                if is_num(text):
                        return lisp_numeric_t(int(text))
                return lisp_symbol_t(text)
        if (statement_tokens[p_start_index[0]] == "("):
                p_start_index[0] += 1
                if statement_tokens[p_start_index[0]] == ")":
                        p_start_index[0] += 1
                        return lisp_symbol_t("nil")
                head = make_code_object(statement_tokens, p_start_index)
                lisp_list = lisp_list_t(head, None)
                prev_lisp_list = lisp_list
                while statement_tokens[p_start_index[0]] != ")":
                        head = make_code_object(statement_tokens, p_start_index)
                        curr_lisp_list = lisp_list_t(head, None)
                        prev_lisp_list.set_cdr(curr_lisp_list)
                        prev_lisp_list = curr_lisp_list
                prev_lisp_list.set_cdr(lisp_symbol_t("nil"))
                p_start_index[0] += 1
                return lisp_list

# determines if a string represents a decimal integer
def is_num(text):
        if len(text) == 0:
                return False
        if len(text) == 1:
                return '0' <= text[0] <= '9'
        if text[0] == '-':
                return text[1] != '-' and is_num(text[1:])
        return '0' <= text[0] <= '9' and is_num(text[1:])

# evaluates Lisp code object into Lisp data object
def eval_code_object(code_object, symbol_table):
        if code_object.is_atom():
                if code_object.is_numeric():
                        return code_object
                if code_object.is_symbol():
                        if is_reserved_word(code_object.name()): # reserved word is just t or nil
                                return code_object
                        # assume symbol is variable, look up in symbol table
                        data_object = symbol_table.lookup(code_object.name())
                        if data_object == None:
                                # to do: raise error: not a variable name
                                print("Error: {} is not a variable name".format(code_object.name()))
                                raise RuntimeError("evaluation")
                        return data_object
        if code_object.is_list():
                # assume function call (or call of special form)
                # list head must evaluate to function object while list tail contains unevaluated arguments
                fn_code_object = code_object.car()
                args_code_object = code_object.cdr()
                if fn_code_object.is_symbol() and is_special_form(fn_code_object.name()):
                        # special form call
                        return special_call(fn_code_object.name(), args_code_object, symbol_table)
                else:
                        # function call
                        fn_object = eval_code_object(fn_code_object, symbol_table)
                        if not fn_object.is_function():
                                print("Error: {} is not a function name".format(fn_code_object))
                                raise RuntimeError("evaluation")
                        # evaluate arguments
                        args_list = eval_list(args_code_object, symbol_table)
                        return fn_object.call(args_list)

# evaluates Lisp list of Lisp code objects
def eval_list(code_list, symbol_table):
        if code_list.is_atom():
                # should probably be nil
                return code_list
        if code_list.is_list():
                return lisp_list_t(eval_code_object(code_list.car(), symbol_table), eval_list(code_list.cdr(), symbol_table))

# check if string represents a symbol that evaluates to itself (t or nil)
def is_reserved_word(text):
        return text == "t" or text == "nil"

# determines if a string is the name of a special form
# note: predefined functions (+, -, *, /, car, cdr, cons, sqrt, pow, >, <, =, !=, and, or, not) are not special forms.
# we need "quote" because ` and ' turn into it in the preprocessing
# we also need "if" because even though it is syntactically a function, we cannot have it evaluate both the true and false case expressions in case they have side effects
def is_special_form(text):
        return text == "if" or text == "define" or text == "set!" or text == "defun" or text == "quote"

# convert True, False to their corresponding Lisp objects
def bool_to_object(boolean):
    return lisp_symbol_t("t") if boolean else lisp_symbol_t("nil")

# evaluates a special call on Lisp code
# args_code is the list of special call arguments, unevaluated (because they override default evaluation rules)
# note: the special call may have side effects (may add or change a variable binding)
def special_call(call_name, args_code, symbol_table):
        if call_name == "if":
                numargs = args_code.length()
                if numargs != 2 and numargs != 3:
                        # to do: raise exception: wrong number of arguments
                        print("Error: wrong number of arguments to if")
                        raise RuntimeError("evaluation")
                condition_result = eval_code_object(args_code.car(), symbol_table)
                if numargs == 2:
                        if condition_result.to_bool():
                                return eval_code_object(args_code.cdr().car(), symbol_table)
                        return lisp_symbol_t("nil")
                if numargs == 3:
                        if condition_result.to_bool():
                                return eval_code_object(args_code.cdr().car(), symbol_table)
                        return eval_code_object(args_code.cdr().cdr().car(), symbol_table)
        if call_name == "define":
                # already existing variables can be redefined; a new copy is made
                numargs = args_code.length()
                if numargs != 2:
                        print("Error: wrong number of arguments to define")
                        raise RuntimeError("evaluation")
                var_name = args_code.car().name()
                var_value = eval_code_object(args_code.cdr().car(), symbol_table)
                symbol_table.add(var_name, var_value)
                return var_value
        if call_name == "set!":
                numargs = args_code.length()
                if numargs != 2:
                        print("Error: wrong number of arguments to set!")
                        raise RuntimeError("evaluation")
                var_name = args_code.car().name()
                if symbol_table.lookup(var_name) == None:
                        print("Error: {} is currently undefined".format(var_name))
                        raise RuntimeError("evaluation")
                var_value = eval_code_object(args_code.cdr().car(), symbol_table)
                symbol_table.set_value(var_name, var_value)
                return var_value
        if call_name == "defun":
                numargs = args_code.length()
                if numargs < 3:
                        print("Error: wrong number of arguments to defun")
                        raise RuntimeError("evaluation")
                fn_name = args_code.car().name()
                params = args_code.cdr().car()
                defn = args_code.cdr().cdr()
                symbol_table.add(fn_name, lisp_func_t(params, defn, None, symbol_table))
                return lisp_symbol_t(fn_name)
        if call_name == "quote":
                numargs = args_code.length()
                if numargs != 1:
                        print("Error: wrong number of arguments to quote")
                        raise RuntimeError("evaluation")
                return args_code.car()

# performs addition on Lisp objects in args_list
def add(args_list):
        # adding zero values - empty sum is 0
        if args_list.is_atom():
                return lisp_numeric_t(0)
        # adding one or more values
        else:
                total = args_list.car().to_int() + add(args_list.cdr()).to_int()
                return lisp_numeric_t(total)

# performs subtraction on Lisp objects in args_list
def subtract(args_list):
        # unlike addition, subtraction only uses 2 arguments
        # yes I know real Lisp has multi-argument subtraction but I'm low on time
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        arg1 = args_list.car()
        arg2 = args_list.cdr().car()
        return lisp_numeric_t(arg1.to_int() - arg2.to_int())

# performs multiplication on Lisp objects in args_list
def multiply(args_list):
        # multiplying zero values - empty product is 1
        if args_list.is_atom():
                return lisp_numeric_t(1)
        # multiplying one or more values
        else:
                product = args_list.car().to_int() * multiply(args_list.cdr()).to_int()
                return lisp_numeric_t(product)

# performs division on Lisp objects in args_list
# integer division because the specification didn't say how to do floating point numbers
def divide(args_list):
        # divison only uses 2 arguments
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        arg1 = args_list.car()
        arg2 = args_list.cdr().car()
        num1 = arg1.to_int()
        num2 = arg2.to_int()
        if num2 == 0:
                print("Error: division by zero")
                raise RuntimeError("evaluation")
        return lisp_numeric_t(num1 // num2)

# evaluates car on Lisp object given by args_list
def car(args_list):
        if args_list.length() != 1:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return args_list.car().car()

# evaluates cdr on Lisp object given by args_list
def cdr(args_list):
        if args_list.length() != 1:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return args_list.car().cdr()

# evaluates cons on Lisp objects given by args_list
def cons(args_list):
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return lisp_list_t(args_list.car(), args_list.cdr().car())

# evaluates the square root function on Lisp objects given by args_list
# returns only the integer part of the square root
# this is consistent with none of the rest of the instructions specifying floating point types
def math_sqrt(args_list):
        if args_list.length() != 1:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        num = args_list.car().to_int()
        if num < 0:
                print("Error: square root of negative number")
                raise RuntimeError("evaluation")
        i = 0
        while (i + 1) ** 2 <= num:
                i += 1
        return lisp_numeric_t(i)

# evaluates the exponential function on Lisp objects given by args_list
# returns integer part of base to power of exponent
def math_pow(args_list):
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        arg1 = args_list.car()
        arg2 = args_list.cdr().car()
        num1 = arg1.to_int()
        num2 = arg2.to_int()
        if num1 == 0 and num2 <= 0:
                print("Error: domain error of function")
                raise RuntimeError("evaluation")
        if num1 == 1:
                return lisp_numeric_t(1)
        if num1 == -1:
                return lisp_numeric_t(1 if (num2 % 2 == 0) else -1)
        if num2 < 0:
                return lisp_numeric_t(0)
        result = 1
        for i in range(num2):
                result *= num1
        return lisp_numeric_t(result)

# evaluates the greater-than function on Lisp objects given by args_list
def greater(args_list):
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return bool_to_object(args_list.car().to_int() > args_list.cdr().car().to_int())

# evaluates the less-than function on Lisp objects given by args_list
def less(args_list):
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return bool_to_object(args_list.car().to_int() < args_list.cdr().car().to_int())

# evaluates the equal-to function on Lisp objects given by args_list
def equal(args_list):
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return bool_to_object(args_list.car().to_int() == args_list.cdr().car().to_int())

# evaluates the not-equal-to function on Lisp objects given by args_list
def not_equal(args_list):
        if args_list.length() != 2:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return bool_to_object(args_list.car().to_int() != args_list.cdr().car().to_int())

# evaluates the logical AND function on Lisp objects given by args_list
def logic_and(args_list):
        # empty and is true
        if args_list.is_atom():
                return bool_to_object(True)
        # anding one or more values
        else:
                result = args_list.car().to_bool() and logic_and(args_list.cdr()).to_bool()
                return bool_to_object(result)

# evaluates the logical OR function on Lisp objects given by args_list
def logic_or(args_list):
        # empty or is false
        if args_list.is_atom():
                return bool_to_object(False)
        # oring one or more values
        else:
                result = args_list.car().to_bool() or logic_and(args_list.cdr()).to_bool()
                return bool_to_object(result)

# evaluates the logical NOT function on Lisp objects given by args_list
def logic_not(args_list):
        if args_list.length() != 1:
                print("Error: wrong number of args")
                raise RuntimeError("evaluation")
        return bool_to_object(not args_list.car().to_bool())

# open output file
out_file = open("results.file", "w")
# initialize token stream (containing input character stream) and main-environment symbol table
tokenstream = Tokenstream()
symbol_table = Symbol_table(None)
# add names for built-in functions to symbol table
for fn_name in built_in_funcs:
    symbol_table.add(fn_name, lisp_func_t(None, None, fn_name, None))

# main loop
print("Welcome to the fancy new Prompt LISP INTERPRETER, type in LISP commands!")
while True:
    print('> ', end='')
    try:
        tokens = tokenstream.get_one_statement()
    except RuntimeError:
        continue
    code_object = make_code_object(replace_quotes(tokens), [0])
    try:
        result = eval_code_object(code_object, symbol_table)
    except RuntimeError:
        continue
    print(result)
    out_file.write(str(result))
    out_file.write('\n')
