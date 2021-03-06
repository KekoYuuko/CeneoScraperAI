from flask import request, render_template, redirect, url_for
from app import app
from app.models.opinion import Opinion
from app.models.product import Product
from app.forms import ProductForm
from os import listdir
import pandas as pd
import requests
import json

app.config['SECRET_KEY'] = "NotSoSecretKey"

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html.jinja')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ProductForm()
    if request.method == 'POST' and form.validate_on_submit():
        product = Product(request.form['productId'])
        if (product.extractName()):
            product.extractProduct()
            product.countProductStatistics()
            product.exportProduct()
            return redirect(url_for('product', productId=product.productId))
        else:
            form.productId.errors.append("For given productId there is no product")
    return render_template('extract.html.jinja', form=form)

@app.route('/<productId>')
def product(productId):
    product = Product(productId)
    opinions = product.importProduct().opinionsToDataFrame()
    opinionBar = product.getSummaryData()
    opinionPie = product.getTruFalseOpitions()
    return render_template('product.html.jinja', tables=[opinions.to_html(classes='table table-striped table-sm table-responsive', table_id="opinions")],opinionBar=opinionBar, opinionPie=opinionPie)

@app.route('/products')
def products():
    productsList = [x.split(".")[0] for x in  listdir("app/products")]
    productsDictsList = []
    for product in productsList:
        with open("app/products/{}.json".format(product), "r", encoding="UTF-8") as jf:
            productsDictsList.append(json.load(jf))
    # products = pd.json_normalize(productsDictsList)
    return render_template('products.html.jinja', products=productsDictsList)



@app.route('/author')
def author():
    return render_template('author.html.jinja')