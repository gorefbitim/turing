from flask import Flask, render_template
import shopify
from dynaconf import settings


shop_url = settings['shop_url']
api_key = settings['api_key']
password = settings['password']

app = Flask(__name__)


shopify.ShopifyResource.set_site(f"https://{api_key}:{password}@{shop_url}/admin")
SHOP_HANDLE = "f2e8c6"

API_VERSION = '2019-07'


def get_all_products(limit=100):
    get_next_page = True
    since_id = 0
    while get_next_page:
        products = shopify.Product.find(since_id=since_id, limit=limit)

        for product in products:
            yield product
            since_id = product.id

        if len(products) < limit:
            get_next_page = False



@app.route('/checkout/<product_id>')
def checkout(product_id):
    # Find the product by ID
    product = shopify.Product.find(product_id)

    # Create a new checkout with the product
    checkout = shopify.Checkout.create(line_items=[{'variant_id': product.variants[0].id, 'quantity': 1}])

    # Redirect the customer to the checkout URL
    return redirect(checkout.web_url)

@app.route('/')
def home():
    shop_url = "https://{}.myshopify.com/admin/api/{}".format(SHOP_HANDLE, API_VERSION)
    shopify.ShopifyResource.set_site(shop_url)
    shopify.ShopifyResource.set_user(api_key)
    shopify.ShopifyResource.set_password(password)
    
    products = get_all_products()
    # Do something with product
    #print(product.title)

    # Fetch products from Shopify
    #session = shopify.Session("SHOP_NAME.myshopify.com")

#    with shopify.Session.temp(shop_url, version="2023-01", token=password):
#        products = shopify.Product.find()

#    api_session = shopify.Session(shop_url, version="2023-01", token=password)
#    products = api_session.Product.find()
    return render_template('index.html', products=products)


app.run(host='0.0.0.0', port=82)
