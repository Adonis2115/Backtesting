closing_price_sum = 0

with open('Data/Custom/BANKNIFTY.csv') as f:
    content = f.readlines()[-200:]
    for line in content:
        print(line)
        tokens = line.split(",")
        close = tokens[6]
        closing_price_sum += float(close)

    print(closing_price_sum/200)