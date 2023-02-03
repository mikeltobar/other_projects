from utils import *

root_url = "https://www.supermarket.es"             # Get website's base URL (fictional modified name)
soup = get_soups(root_url + "/online-shop/")        # Get the initial 'soups' 
departamentos = get_dpts(soup)                      # Array with departments' URLs
final = []                                          # Array with the products and its classified prices

# Iterate over all departments except for the last
for dpt in departaments[0:-1]:
    final.append(get_products(dpt, root_url))
    print(final[-1][0])                             # Print each department's name

# Csv output writing
with open('products.csv', 'w') as f:
    f.write("Section;Description;Prices\n")         # Headings
    for cat in final:
        dep = cat[0]
        for prod in cat[1:]:
            f.write(dep + ";" + prod[0] + ";" + prod[1] + "\n")
