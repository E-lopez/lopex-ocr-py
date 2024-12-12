from flask import Blueprint, jsonify, request, flash, redirect
from services.parserService import parse_document_service, parse_with_miner, show_ltitem_hierarchy
import requests

from services.extract_service import crop_doc, get_boxes, handle_multiple, parse_with_plumber

routes = Blueprint('routes', __name__, url_prefix='/ocr')

@routes.route("/")
def home():
  return "Hi there mofos"

BASE_URL = "https://dummyjson.com"
@routes.route('/products', methods=['GET'])
def get_products():
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code != 200:
        return jsonify({'error': response.json()['message']}), response.status_code
    products = []
    for product in response.json()['products']:
        product_data = {
            'id': product['id'],
            'title': product['title'],

            'price': product['price'],
            'description': product['description']
        }
        products.append(product_data)
    return jsonify({'data': products}), 200 if products else 204

@routes.post('/parse')
def parse_document():
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    return parse_document_service(file)

@routes.post('/miner')
def parse_miner():
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    return parse_with_miner(file)

@routes.post('/plumber')
def parse_plumber():
    file = request.files['file']
    return parse_with_plumber(file)
    
@routes.post('/crop')
def crop_plumber():
    file = request.files['file']
    return crop_doc(file)

@routes.post('/boxes')
def get_boxes_text():
    file = request.files.getlist('file')
    return get_boxes(file)

@routes.post('/multi')
def handle_multi():
    files = request.files.getlist('files')
    return handle_multiple(files)
    