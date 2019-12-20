from utils import *
import time
import ccxt
import time

exchange = ccxt.bittrex()
market = exchange.load_markets()

# selected depth
max_depth = int(input('\n >> ingrese max_depth: '))

# pairs of exchange
tickers = exchange.fetch_tickers()
pairs = tickers.keys()
relationship = []
prices = {}

for pair in pairs:
    base = pair.split('/')[0]
    quote = pair.split('/')[1]
    if not (base == 'USD' or base == 'TUSD' or quote == 'USD' or quote == 'USD'):
        if base + '/USDT' in list(pairs) or 'USDT/' + quote in list(pairs):
            ask_price = tickers[pair]['info']['Ask']
            bid_price = tickers[pair]['info']['Bid']
            bid_inverse_price = 1 / bid_price

            relationship.append(Pair(quote, base, ask_price, 0.0025))
            relationship.append(Pair(base, quote, bid_inverse_price, 0.0025))

            if(quote == 'USDT'):
                prices[base] = bid_price
            print('Pair: {} - Price: {}'.format(quote + '/' + base, ask_price))
            print('Pair: {} - Price: {}'.format(base + '/' + quote, bid_inverse_price))

USDT = Pair('USDT', 'USDT', 1, 0)
relationship.append(USDT)
prices['USDT'] = 1

# redefinition of R
real_relationship = relationship.copy()
relationship.remove(USDT)
relationship = {lamda:get_adjacencies_of_currency(lamda,relationship) for lamda in prices}
# print([x.stringify_pair() for x in relationship['USDT']])

# dinamic programmig memorization
known_paths = [{lamda.stringify_pair():None for lamda in real_relationship} for x in range(0,max_depth + 1)]

# call counts (memorization,recursive)
i,j = 0,0

def rate_snake_strategy(pair,depth) -> RateSnakeReturn:
    global relationship,i,j,prices

    # dinamic programming memorization base case
    if known_paths[depth][pair.stringify_pair()] != None:
        i += 1
        other_path = known_paths[depth][pair.stringify_pair()]
        return other_path

    if depth == 0:
        last_pairs = [p for p in relationship[pair.dependent_currency] if p.dependent_currency == 'USDT']

        # <X,USDT> case (this is to avoid the <USDT,USDT> pair)
        if len(last_pairs) == 0:
            last_pair = [Pair('USDT', 'USDT', 1, 0)]
            return RateSnakeReturn(float('-inf'),[last_pair],pair);

        last_pair = last_pairs[0]
        # print(pair.stringify_pair() + ' - ' + last_pair.stringify_pair())
        value = RateSnakeReturn((prices[pair.dependent_currency]/pair.price) * (1 - pair.fee) * (1 - last_pair.fee),[last_pair],pair);

    elif depth > 0:
        # we get all the children paths
        children = [rate_snake_strategy(lamda,depth - 1) for lamda in relationship[pair.dependent_currency]]

        # we select the one with maximum rate
        max_rate = float('-inf')
        max_child = None
        for child in children:
            if child.rate >= max_rate:
                max_rate = child.rate
                max_child = child

        # then, our path is the max child sub-path plus the actual node (pair)
        stack = max_child.stack.copy()
        stack.append(max_child.pair)

        # and then we set the result to the structure that contains profit of our path (wich is the max_profit of the children + our profit) and our path itself
        value = RateSnakeReturn((max_rate/pair.price) * (1 - pair.fee), stack, pair)

    known_paths[depth][pair.stringify_pair()] = value
    j += 1
    return value

initial_time = time.time()


result = rate_snake_strategy(Pair('USDT','USDT',1,0),max_depth)

final_time = time.time()

# we reverse the stack to see it as a path
result.stack.reverse()

print('\n >> Results:\n')
print('\tpath: ' + str(stringify_stack(result.stack)) + '\n\trate: ' + str(result.rate))
print('\ttime of execution in ms: ' + str((final_time - initial_time) * 1000))
print('\trecursive calls: ' + str(j) + ', memorization calls: ' + str(i) + '\n')
