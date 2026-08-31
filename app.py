from flask import Flask, render_template_string, request, redirect
import os, json
from werkzeug.utils import secure_filename
from urllib.parse import quote

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
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lwah's Tekkies - Step Out. Stand Out.</title>
<style>
body{font-family:Arial;margin:0;background:#fff0f6}
.header{background:#fff;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px #ffb6d9;position:sticky;top:0;z-index:10}
.logo{font-size:24px;color:#ff1493;font-weight:bold}
.nav a{margin:6px;color:#ff1493;text-decoration:none;font-weight:bold;font-size:14px}
.banner{background:linear-gradient(135deg,#ff1493,#ff69b4);color:white;text-align:center;padding:30px 15px}
.products{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:15px}
.card{background:white;border-radius:15px;padding:12px;text-align:center;box-shadow:0 4px 10px rgba(255,20,147,0.2)}
.card img{width:100%;height:150px;object-fit:cover;border-radius:10px}
.price{color:#ff1493;font-weight:bold;font-size:18px}
.btn-add{background:#ff1493;color:white;padding:10px;border:none;border-radius:20px;width:100%;margin-top:6px;font-weight:bold}
.btn-wa{background:#25D366;color:white;padding:10px;border:none;border-radius:20px;width:100%;margin-top:6px;font-weight:bold;display:none}
.footer{background:#ff1493;color:white;text-align:center;padding:15px;margin-top:20px}
#cartCount{background:#ff1493;color:white;border-radius:50%;padding:2px 7px;font-size:12px}
</style></head><body>
<div class="header">
<div class="logo">💖 Lwah's Tekkies</div>
<div class="nav"><a href="/">Shop</a> | <a href="/upload">Upload</a> | <a href="#" onclick="checkoutWA()">🛒 Cart (<span id="cartCount">0</span>)</a></div>
</div>
<div class="banner"><h1 style="margin:0">Step Out. Stand Out. 👑</h1><p>Durban's Hottest | 081 566 6133</p></div>
<div class="products">
{% for p in products %}
<div class="card">
<img src="{{p.image}}">
<h3>{{p.name}}</h3>
<div class="price">R{{p.price}}</div>
<p style="font-size:13px">{{p.desc}}</p>
<button class="btn-add" onclick="addToCart('{{p.name}}','{{p.price}}')">Add to Cart 🛒</button>
</div>
{% endfor %}
</div>
<div class="footer">© 2026 Lwah's Tekkies | 081 566 6133 💖</div>

<script>
let cart = JSON.parse(localStorage.getItem('lwahCart')||'[]');
updateCount();
function addToCart(name,price){
  cart.push({name,price});
  localStorage.setItem('lwahCart',JSON.stringify(cart));
  updateCount();
  alert(name+' added! Cart: '+cart.length);
}
function updateCount(){
  document.getElementById('cartCount').innerText = cart.length;
}
function checkoutWA(){
  if(cart.length==0){alert('Cart empty! Add tekkies first 👑');return;}
  let msg='Hi Lwah! 👑 I want to order:%0A';
  let total=0;
  cart.forEach((item,i)=>{
    msg+=`${i+1}. ${item.name} - R${item.price}%0A`;
    total+=parseInt(item.price)||0;
  });
  msg+=`%0ATotal: R${total}%0ADelivery: Durban`;
  window.open('https://wa.me/27815666133?text='+msg,'_blank');
}
</script>
</body></html>
"""

UPLOAD_HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;background:#fff0f6;padding:20px}input,textarea{width:100%;padding:12px;margin:8px 0;border:2px solid #ffb6d9;border-radius:10px}
.btn{background:#ff1493;color:white;padding:12px;border:none;border-radius:20px;width:100%;font-weight:bold}</style>
</head><body><h2 style="color:#ff1493">💖 Upload Tekkie</h2>
<form method="post" enctype="multipart/form-data">
<input name="name" placeholder="Name" required><input name="price" placeholder="Price: 1200" required>
<textarea name="desc" placeholder="Size / Info"></textarea>
<p>Photo:</p><input type="file" name="image" accept="image/*" required>
<button class="btn" type="submit">Upload 👑</button>
</form><br><a href="/">← Back</a></body></html>"""

@app.route('/')
def home():
    products=load_products()
    for p in products:
        p['price']=str(p['price']).replace('R','').strip()
    return render_template_string(HTML, products=products)
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        name=request.form['name']; price=str(request.form['price']).replace('R','').strip(); desc=request.form['desc']
        file=request.files['image']; filename=secure_filename(file.filename); path=os.path.join(app.config['UPLOAD_FOLDER'], filename); file.save(path)
        products=load_products(); products.append({"name":name,"price":price,"desc":desc,"image":f"/{path}"}); save_products(products); return redirect('/')
    return render_template_string(UPLOAD_HTML)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
