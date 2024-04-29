from flask import Flask, send_file, jsonify, request
import requests
import json

app = Flask(__name__)

def read():
    with open('products.json', 'r') as file:
        data = json.load(file)
    return data

def write(product):
    with open('products.json', 'w') as file:
        json.dump(product,file, indent=2)
       
     

@app.route('/')
def index():
   return "<p>Hello, World!</p>"

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        return send_file('products.json')
    except Exception as e:
        return str(e)
    


@app.route('/api/products/<int:product_id>')
def get_products_id(product_id):

    data = read()

    for product in data['data']:
        if product['id'] == product_id:
            return f"{product}"
    return f'<p> produit non trouvé <p>'

@app.route('/api/products/add', methods=['POST'])
def add_product():

    try:
       
        # Charger les données existantes depuis le fichier JSON
        with open('products.json', 'r') as file:
            data = json.load(file)

        new_product_data = request.get_json()
    
        required_fields = ['code', 'name', 'description', 'image', 'price', 'category', 'quantity', 'inventoryStatus', 'rating']
        if not all(field in new_product_data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_product_data['id'] = len(data['data']) + 1

        data['data'].append(new_product_data)

        with open('products.json', 'w') as file:
            json.dump(data, file, indent=2)
       
        return jsonify({'message': 'product added successfully', 'data': new_product_data}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products/del/<int:id>', methods=['DELETE'])
def del_product(id):

    with open('products.json', 'r') as file:
        data = json.load(file)

    updated_data = [product for product in data['data'] if product['id'] != id]

    
    if len(updated_data) < len(data['data']):
        data['data'] = updated_data
        with open('products.json', 'w') as fp:
            json.dump(data, fp, indent=2)
        return jsonify('product deleted'), 200
    else:
        return jsonify('product not found'), 404

@app.route('/api/products/update/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    try:
    
        data = read()

        product_to_update = next((product for product in data['data'] if product['id'] == product_id), None)

        if product_to_update is None:
            return jsonify({'error': 'Product not found'}), 404

        updated_data = request.get_json()

        for key, value in updated_data.items():
            product_to_update[key] = value

        write(data)

        return jsonify({'message': 'Product updated successfully', 'data': product_to_update}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    


    
    
if __name__ == '__main__':
    app.run(debug=True)