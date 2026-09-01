from flask import Flask, render_template_string
app = Flask(__name__)

# YOUR SHOES ARE HERE - SAFE!
PRODUCTS = [
 {"id":1,"name":"Nike Air Max 90 - White","price":850,"img":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500","sizes":["3","4","5","6","7"]},
 {"id":2,"name":"Adidas Samba - Black/White","price":900,"img":"https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=500","sizes":["4","5","6","7","8"]},
 {"id":3,"name":"New Balance 550 - White/Green","price":1200,"img":"https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500","sizes":["3","4","5","6"]},
 {"id":4,"name":"Puma RS-X - Pink","price":950,"img":"https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500","sizes":["5","6","7"]},
 {"id":5,"name":"Converse High - Black","price":700,"img":"https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=500","sizes":["3","4","5","6","7","8"]},
 {"id":6,"name":"Nike Dunk Low - Panda","price":1100,"img":"https://images.unsplash.com/photo-1511556532299-8f662fc26c06?w=500","sizes":["4","5","6"]},
]

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lwah's Tekkies</title>
<style>
body{margin:0;font-family:Arial;background:#fff5f8}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 15px;background:white;position:sticky;top:0;z-index:10;border-bottom:2px solid #ffe0eb}
.logo{color:#ff1493;font-weight:bold;font-size:20px;text-decoration:none}
.banner{background:linear-gradient(90deg,#ff1493,#ff69b4);color:white;text-align:center;padding:20px 10px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.card{background:white;border-radius:15px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);text-align:center}
.card img{width:100%;height:140px;object-fit:cover}
.card h4{margin:8px 5px 2px;font-size:13px;height:32px;overflow:hidden}
.price{color:#ff1493;font-weight:bold;margin:5px}
.btn{background:#ff1493;color:white;border:none;padding:8px 12px;border-radius:20px;margin:5px;font-size:12px;font-weight:bold}
.footer{background:#ff1493;color:white;text-align:center;padding:12px;margin-top:10px}
</style></head><body>
<div class="header"><a class="logo" href="/">💖 Lwah's Tekkies</a><div><a href="#shop" style="color:#ff1493;font-weight:bold;text-decoration:none">SHOP</a> <span style="margin-left:10px">🛒 (<span id="cartCount">0</span>)</span></div></div>
<div class="banner"><h2 style="margin:0">Step Out. Stand Out. 👑</h2><p style="margin:5px;font-size:13px">Tap pic to view • Cart • WhatsApp</p></div>
<div id="shop" class="grid">
{% for p in products %}
<div class="card">
<img src="{{p.img}}">
<h4>{{p.name}}</h4>
<div class="price">R{{p.price}}</div>
<button class="btn" onclick="order('{{p.name}}',{{p.price}})">Order via WhatsApp</button>
</div>
{% endfor %}
</div>
<div class="footer">© Lwah's Tekkies | 081 566 6133 💖</div>
<script>
let cart=0;
function order(name,price){
 cart++;document.getElementById('cartCount').innerText=cart;
 let msg=`Hi Lwah! I want ${name} for R${price} 👟 Size: [tell your size]`;
 window.open("https://wa.me/27815666133?text="+encodeURIComponent(msg),"_blank");
}
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, products=PRODUCTS)

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
