from flask import Flask, render_template_string, request, redirect, url_for
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

PRODUCTS_FILE = 'products.json'
if not os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, 'w') as f: json.dump([], f)

def load_products():
    with open(PRODUCTS_FILE) as f: return json.load(f)
def save_products(p): 
    with open(PRODUCTS_FILE, 'w') as f: json.dump(p,f)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lwah's Tekkies - Step Out. Stand Out.</title>
<style>
body{font-family:Arial;margin:0;background:#fff0f6}
.header{background:#fff;padding:15px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px #ffb6d9}
.logo{font-family:cursive;font-size:28px;color:#ff1493;font-weight:bold}
.nav a{margin:10px;color:#ff1493;text-decoration:none;font-weight:bold}
.banner{background:linear-gradient(135deg,#ff1493,#ff69b4);color:white;text-align:center;padding:40px 20px}
.banner h1{font-size:36px;margin:0}
.products{display:grid;grid-template-columns:1fr 1fr;gap:15px;padding:20px}
.card{background:white;border-radius:15px;padding:15px;text-align:center;box-shadow:0 4px 10px rgba(255,20,147,0.2)}
.card img{width:100%;height:150px;object-fit:cover;border-radius:10px}
.price{color:#ff1493;font-weight:bold;font-size:18px}
.btn{background:#ff1493;color:white;padding:10px 15px;border:none;border-radius:20px;width:100%;margin-top:8px;font-weight:bold}
.footer{background:#ff1493;color:white;text-align:center;padding:15px;margin-top:20px}
</style>
</head>
<body>
<div class="header">
<div class="logo">💖 Lwah's Tekkies</div>
<div class="nav"><a href="/">Shop</a> <a href="/upload">Upload</a> <a href="#">Cart (0)</a></div>
</div>
<div class="banner">
<h1>Step Out. Stand Out. 👑</h1>
<p>Durban's Hottest Tekkies | 081 566 6133</p>
</div>
<div class="products">
{% for p in products %}
<div class="card">
<img src="{{p.image}}">
<h3>{{p.name}}</h3>
<div class="price">R{{p.price}}</div>
<p>{{p.desc}}</p>
<button class="btn" onclick="alert('Order {{p.name}} via WhatsApp 081 566 6133')">Add to Cart</button>
</div>
{% endfor %}
{% if not products %}
<div class="card"><h3>Welcome Queen!</h3><p>Upload your first tekkie in Upload!</p><a href="/upload"><button class="btn">Go Upload</button></a></div>
{% endif %}
</div>
<div class="footer">© 2026 Lwah's Tekkies | 081 566 6133 | Durban & PMB Delivery 💖</div>
</body>
</html>
"""

UPLOAD_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;background:#fff0f6;padding:20px}input,textarea{width:100%;padding:12px;margin:8px 0;border:2px solid #ffb6d9;border-radius:10px}
.btn{background:#ff1493;color:white;padding:12px;border:none;border-radius:20px;width:100%;font-weight:bold;font-size:18px}</style>
</head><body>
<h2 style="color:#ff1493">💖 Upload New Tekkie - Lwah's Tekkies</h2>
<form method="post" enctype="multipart/form-data">
<input name="name" placeholder="Tekkie Name: eg Nike Air Pink" required>
<input name="price" placeholder="Price: eg 1200" required>
<textarea name="desc" placeholder="Description: eg Size 3-8, Durban delivery"></textarea>
<p>Product Image:</p><input type="file" name="image" accept="image/*" required>
<p>Logo (optional):</p><input type="file" name="logo" accept="image/*">
<button class="btn" type="submit">Upload Tekkie 👑</button>
</form>
<br><a href="/">← Back to Shop</a>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, products=load_products())

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        name=request.form['name']; price=request.form['price']; desc=request.form['desc']
        file=request.files['image']
        filename=secure_filename(file.filename)
        path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        products=load_products()
        products.append({"name":name,"price":price,"desc":desc,"image":f"/{path}"})
        save_products(products)
        return redirect('/')
    return render_template_string(UPLOAD_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
