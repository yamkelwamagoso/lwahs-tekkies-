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
<title>Lwah's Tekkies</title>
<style>
body{font-family:Arial;margin:0;background:#fff0f6}
.header{background:#fff;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px #ffb6d9;position:sticky;top:0;z-index:100}
.logo{font-size:20px;color:#ff1493;font-weight:bold}
.nav a{color:#ff1493;text-decoration:none;font-weight:bold;margin-left:10px}
.banner{background:linear-gradient(135deg,#ff1493,#ff69b4);color:white;text-align:center;padding:18px 10px}
.products{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:12px}
.card{background:white;border-radius:15px;padding:10px;text-align:center;box-shadow:0 4px 10px rgba(255,20,147,0.2)}
.card img{width:100%;height:145px;object-fit:cover;border-radius:10px;cursor:zoom-in;border:1px solid #ffe0ee}
.price{color:#ff1493;font-weight:bold}
.btn-add{background:#ff1493;color:white;padding:8px;border:none;border-radius:20px;width:100%;margin-top:5px;font-weight:bold;font-size:12px}
.btn-wa{background:#25D366;color:white;padding:8px;border:none;border-radius:20px;width:100%;margin-top:5px;font-weight:bold;font-size:12px}
.footer{background:#ff1493;color:white;text-align:center;padding:12px;margin-top:15px;font-size:12px}
.modal{display:none;position:fixed;z-index:999;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.9);justify-content:center;align-items:center;flex-direction:column}
.modal img{max-width:92%;max-height:65%;border-radius:15px;border:3px solid white}
.modal h3{color:white;margin:10px;text-align:center}
.close{color:white;font-size:40px;position:absolute;top:5px;right:20px;cursor:pointer}
/* CART MODAL */
.cart-modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.7);justify-content:center;align-items:center}
.cart-box{background:white;width:90%;max-width:350px;border-radius:20px;padding:20px;max-height:80%;overflow-y:auto}
.cart-item{display:flex;justify-content:space-between;align-items:center;background:#fff0f6;padding:8px 10px;margin:6px 0;border-radius:10px;font-size:13px}
.btn-remove{background:#ff4444;color:white;border:none;border-radius:15px;padding:4px 10px;font-size:11px;font-weight:bold}
.btn-checkout{background:#25D366;color:white;padding:12px;border:none;border-radius:20px;width:100%;margin-top:10px;font-weight:bold}
</style></head><body>
<div class="header"><div class="logo">💖 Lwah's Tekkies</div><div class="nav"><a href="/">SHOP</a> <a href="#" onclick="openCart()">🛒 (<span id="cartCount">0</span>)</a></div></div>
<div class="banner"><h3 style="margin:0">Step Out. Stand Out. 👑</h3><p style="margin:3px;font-size:12px">Tap pic to view • Cart • WhatsApp</p></div>
<div class="products">
{% for p in products %}
<div class="card">
<img src="{{p.image}}" onclick="openImgModal('{{p.image}}','{{p.name}} - R{{p.price}}')">
<div style="font-size:11px;color:#ff69b4">👁️ Tap to view</div>
<h4 style="margin:5px 0;font-size:13px">{{p.name}}</h4>
<div class="price">R{{p.price}}</div>
<p style="font-size:11px;color:#666;margin:2px">{{p.desc}}</p>
<button class="btn-add" onclick="addToCart('{{p.name}}','{{p.price}}')">Add to Cart 🛒</button>
<a href="https://wa.me/27815666133?text={{p.wa_msg}}" target="_blank"><button class="btn-wa">WhatsApp Order 📱</button></a>
</div>
{% endfor %}
</div>

<!-- BIG IMAGE MODAL -->
<div id="imgModal" class="modal" onclick="closeImgModal()"><span class="close">&times;</span><img id="modalImg"><h3 id="modalTitle"></h3><p style="color:#ffb6d9;font-size:13px">Tap to close</p></div>

<!-- CART MODAL WITH REMOVE -->
<div id="cartModal" class="cart-modal" onclick="if(event.target==this)closeCart()">
<div class="cart-box">
<h3 style="color:#ff1493;margin:0 0 10px">🛒 Your Cart (<span id="cartCount2">0</span>)</h3>
<div id="cartItems"></div>
<div id="cartTotal" style="font-weight:bold;margin-top:10px;color:#ff1493"></div>
<button class="btn-checkout" onclick="checkoutWA()">Checkout via WhatsApp 📱</button>
<button onclick="clearCart()" style="background:#ff4444;color:white;padding:8px;border:none;border-radius:20px;width:100%;margin-top:6px;font-size:12px">Clear Cart ❌</button>
<button onclick="closeCart()" style="background:#ddd;padding:8px;border:none;border-radius:20px;width:100%;margin-top:6px">Continue Shopping</button>
</div></div>

<div class="footer">© Lwah's Tekkies | 081 566 6133 💖</div>
<script>
let cart=JSON.parse(localStorage.getItem('lwahCart')||'[]');updateCount();renderCart();
function openImgModal(src,title){document.getElementById('imgModal').style.display='flex';document.getElementById('modalImg').src=src;document.getElementById('modalTitle').innerText=title;}
function closeImgModal(){document.getElementById('imgModal').style.display='none';}
function addToCart(n,p){cart.push({name:n,price:p});saveCart();alert('✅ '+n+' added!');}
function removeFromCart(index){cart.splice(index,1);saveCart();}
function clearCart(){if(confirm('Clear cart?')){cart=[];saveCart();}}
function saveCart(){localStorage.setItem('lwahCart',JSON.stringify(cart));updateCount();renderCart();}
function updateCount(){document.getElementById('cartCount').innerText=cart.length;document.getElementById('cartCount2').innerText=cart.length;}
function renderCart(){let div=document.getElementById('cartItems');let total=0;if(cart.length==0){div.innerHTML='<p style="color:#999">Cart empty 👑 Add tekkies!</p>';document.getElementById('cartTotal').innerHTML='';return;}let html='';cart.forEach((it,i)=>{total+=parseInt(it.price)||0;html+=`<div class="cart-item"><span>${it.name}<br><b>R${it.price}</b></span><button class="btn-remove" onclick="removeFromCart(${i})">Remove ❌</button></div>`});div.innerHTML=html;document.getElementById('cartTotal').innerHTML='Total: R'+total;}
function openCart(){renderCart();document.getElementById('cartModal').style.display='flex';}
function closeCart(){document.getElementById('cartModal').style.display='none';}
function checkoutWA(){if(cart.length==0){alert('Cart empty!');return;}let msg='Hi Lwah! 👑 I want to order:%0A';let total=0;cart.forEach((it,i)=>{msg+=`${i+1}. ${it.name} - R${it.price}%0A`;total+=parseInt(it.price)||0;});msg+=`%0ATotal: R${total}`;window.open('https://wa.me/27815666133?text='+msg,'_blank');}
</script></body></html>
"""

UPLOAD_HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;background:#fff0f6;padding:20px}input,textarea{width:100%;padding:12px;margin:8px 0;border:2px solid #ffb6d9;border-radius:10px}
.btn{background:#ff1493;color:white;padding:12px;border:none;border-radius:20px;width:100%;font-weight:bold}</style>
</head><body><h2 style="color:#ff1493">🔐 Secret Admin - Lwah Only</h2>
<form method="post" enctype="multipart/form-data">
<input name="name" placeholder="Product Name" required><input name="price" placeholder="Price" required>
<textarea name="desc" placeholder="Info"></textarea><input type="file" name="image" accept="image/*" required>
<button class="btn" type="submit">Upload 👑</button></form><br><a href="/">← Shop</a></body></html>"""

@app.route('/')
def home():
    products=load_products()
    for p in products:
        p['price']=str(p['price']).replace('R','').strip()
        msg=f"Hi Lwah! I want {p['name']} - R{p['price']}. Available? 👑"
        p['wa_msg']=quote(msg)
    return render_template_string(HTML, products=products)
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        name=request.form['name'];price=str(request.form['price']).replace('R','').strip();desc=request.form['desc']
        file=request.files['image'];fn=secure_filename(file.filename);path=os.path.join(app.config['UPLOAD_FOLDER'], fn);file.save(path)
        products=load_products();products.append({"name":name,"price":price,"desc":desc,"image":f"/{path}"});save_products(products);return redirect('/')
    return render_template_string(UPLOAD_HTML)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
