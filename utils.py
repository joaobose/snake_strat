
# image of lamda: (lamda,R) -> set of pair that have lamda as its base currency
def get_adjacencies_of_currency(currency,relationship):
    return [x for x in relationship if x.base_currency == currency]

# a class that stores information of a pair of exchange
class Pair:
    base_currency = ''
    dependent_currency = ''
    price = 0
    fee = 0

    def __init__(self,base,dependent,price,fee):
        self.base_currency = base
        self.dependent_currency = dependent
        self.price = price
        self.fee = fee

    # this method print the pair in a "human readable" way
    def stringify_pair(self):
        return '<' + self.base_currency + ',' + self.dependent_currency  + '>'

# a class that supports rate_snake_strategy (it helps saving the "stack path" of the snake)
class RateSnakeReturn:
    stack = []
    rate = 0
    pair = None

    def __init__(self,rate,stack,pair):
        self.stack = stack
        self.rate = rate
        self.pair = pair

# a method that prints a RateSnakeReturn pairs stack in a "human readable" way
def stringify_stack(stack):
    result = ''
    for pair in stack:
        result += pair.stringify_pair()
    return result


# a method that prints a RateSnakeReturn pairs stack in a "human readable" way without consecutive reapeating pairs
def stack_to_ordered_set(stack):
    result = ''
    for i in range(0,len(stack) - 1):
        if stack[i].stringify_pair() != stack[i + 1].stringify_pair():
            result += stack[i].stringify_pair()
    result += stack[len(stack) - 1].stringify_pair()
    return result
