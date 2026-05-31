from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_path': self.image_path,
            'price': self.price,
            'description': self.description
            }

# Define Cart model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref=db.backref('carts', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

def get_product_dict(product):
    return product.to_dict() if product else None

def get_products():
    products = Product.query.all()
    return [get_product_dict(product) for product in products]

def get_cart_dict(cart):
    return cart.to_dict() if cart else None

def add_product_from_dict(data):
    product = Product(name=data['name'], image_path=data['image_path'], price=data['price'], description=data['description'])
    db.session.add(product)
    db.session.commit()
    return get_product_dict(product)

def add_to_cart_from_dict(data):
    product_id = data['product_id']
    quantity = data['quantity']
    product = Product.query.get(product_id)
    if product:
        cart = Cart(product_id=product_id, quantity=quantity)
        db.session.add(cart)
        db.session.commit()
        return get_cart_dict(cart)
    return None

def delete_from_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if cart:
        db.session.delete(cart)
        db.session.commit()

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()

def edit_quantity(cart_id, quantity):
    cart = Cart.query.get(cart_id)
    if cart:
        cart.quantity = quantity
        db.session.commit()

def create_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
