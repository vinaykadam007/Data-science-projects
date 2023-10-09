import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

user_basket = []


def encode_units(x):
    return 1 if x > 0 else 0


def find_frequent_datasets(basket, support, metric='support', min_threshold=0.8):

    # now find out frequeny sets of items
    # min_support = 5%
    # these itemsets come at least 3% of all transactions in the database
    frequent_itemsets = apriori(
        basket, min_support=support, use_colnames=True)

    # now apply association rules over the frequent items
    # frequent itemsets should have support and itemsets colums
    # Minimal threshold for the evaluation metric to decide whether a candidate rule is of interest.
    rules = association_rules(
        frequent_itemsets, metric=metric, min_threshold=min_threshold)

    return (frequent_itemsets, rules)


# def fill_basket(item):
#     global user_basket
#     user_basket.append(item)

# df1 = pd.read_excel('./data/mcd.xlsx', index_col=None, header=None)
# df = df.fillna("")

# df = df1.drop([0], axis=1)

# dataset = [['Chocolate', 'Popcorn', 'Soda', 'Bread', 'Butter', 'Nutella'],
#            ['Bread', 'Butter', 'Nutella', 'Jam'],
#            ['Soda', 'Lentils', 'Pizza', 'Burger'],
#            ['Popcorn', 'Bread', 'Nutella', 'Pizza'],
#            ['Nutella', 'Jam', 'Bread', 'Butter']]

dataset = [["Bread", "Milk", "Beer"],
           ["Bread", "Diapers", "Eggs"],
           ["Milk", "Diapers", "Beer", "Cola"],
           ["Bread", "Milk", "Diapers", "Beer"],
           ["Bread", "Milk", "Cola"]]


def get_baskets():

    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df


def get_all_items(dataset):
    d = list(set([j for i in dataset for j in i]))
    return d


def get_consequent(antecedant_item, rules):

    # return list(set([list(i)[0] for i in rules[rules['antecedants'].apply(lambda x: antecedant_item in list(x))]['consequents'].tolist()]))
    new_rows = rules[rules["antecedants"].apply(lambda x: set([antecedant_item]).issubset(set(x)))].sort_values(["support"])['consequents'].tolist()
    return list(set([j for i in new_rows for j in list(i)]))


if __name__ == '__main__':

    user_metric = 'confidence'
    user_min_threshold = 0.5
    user_metric_thresh = 0.5
    df = get_baskets()
    (baskets_obtained, rules_obtained) = find_frequent_datasets(
        df, user_metric_thresh, user_metric, user_min_threshold)

    all_items = get_all_items(dataset)
    # print(rules_obtained)
    # print(get_all_items(dataset))
    # input_item = 'Nutella'
    # consequent_items = get_consequent(input_item, rules_obtained)
    # print(consequent_items)

    print("-----------------Cart Addition App-------------------\nPRESS EXIT TO LEAVE")
    print("Items which can be bought:", all_items)
    first_input = input("Enter first item:\n").capitalize()

    cart = []
    cart.append(first_input)
    remaining_items = all_items[:]
    remaining_items.remove(first_input)

    # remove cart item from suggestions
    # put stop purchase code

    while 1:
        if not remaining_items:
            print("All items taken! Leaving..")
            break

        suggestions = get_consequent(first_input, rules_obtained)

        if list(set(suggestions) ^ set(cart)):
            print("Available suggestions:", list(set(suggestions) - set(cart)))

        print("Remaining items in store", list(set(
            remaining_items) - set(cart) - set(suggestions)))

        next_item = input("\n")

        if next_item.lower() == 'exit':
            break

        if next_item not in all_items:
            print("Item doesn't exist! Try again! Type exit to leave")

        if next_item in cart:
            print("Oops! Item already in cart!")
        else:
            cart.append(next_item)
            first_input = next_item
            remaining_items.remove(next_item)

        print("*" * 30, "\nYour cart is", cart, "\n", "*" * 30)

    print("*" * 30, "\nYour Final cart is", cart, "\n", "*" * 30)
