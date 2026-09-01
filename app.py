from flask import Flask, render_template_string
app = Flask(__name__)

# SHOES SAVED FOREVER INSIDE CODE - NEVER DELETE!
PRODUCTS = [
 {"id":1,"name":"Nike Air Max 90 - White","price":850,"img":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"},
 {"id":2,"name":"Adidas Samba - Black/White","price":900,"img":"https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=800"},
 {"id":3,"name":"New Balance 550 - White/Green","price":1200,"img":"https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=800"},
 {"id":4,"name":"Puma RS-X - Pink","price":950,"img":"https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800"},
]

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lwah's Tekkies - Saves Forever</title>
<style>
body{margin:0;font-family:Arial;background:#fff5f8}
.header{display:flex;justify-content:space-between;align-items:center;padding:12px 15px;background:white;position:sticky;top:0;z-index:100;border-bottom:2px solid #ffe0eb}
.logo{color:#ff1493;font-weight:bold;font-size:20px;text-decoration:none}
.cart-btn{background:#ff1493;color:white;padding:8px 15px;border-radius:20px;border:none;font-weight:bold;cursor:pointer}
.banner{background:linear-gradient(90deg,#ff1493,#ff69b4);color:white;text-align:center;padding:15px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.card{background:white;border-radius:15px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);text-align:center;padding-bottom:10px}
.card img{width:100%;height:150px;object-fit:cover;cursor:pointer}
.card h4{margin:8px 5px;font-size:12px;height:30px}
.price{color:#ff1493;font-weight:bold;margin:2px}
.btn{border:none;padding:8px 10px;border-radius:20px;margin:3px;font-size:11px;font-weight:bold;cursor:pointer;width:90%}
.btn-view{background:#f0f0f0;color:#333}
.btn-cart{background:#222;color:white}
.btn-wa{background:#25D366;color:white}
/* CART PAGE */
#cartPage{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:white;z-index:200;overflow:auto;padding:15px}
.cart-item{display:flex;gap:10px;align-items:center;border-bottom:1px solid #eee;padding:10px 0}
.cart-item img{width:60px;height:60px;border-radius:10px;object-fit:cover}
.checkout{background:#25D366;color:white;padding:15px;border:none;border-radius:25px;width:100%;font-size:16px;font-weight:bold;margin-top:15px;cursor:pointer}
/* IMAGE VIEWER */
#imgViewer{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:300;justify-content:center;align-items:center;flex-direction:column;padding:20px}
#imgViewer img{max-width:95%;max-height:70%;border-radius:15px}
#imgViewer h3{color:white;margin-top:15px}
</style></head><body>

<div class="header">
<a class="logo" href="/">💖 Lwah's Tekkies</a>
<button class="cart-btn" onclick="openCart()">🛒 Cart (<span id="cartCount">0</span>)</button>
</div>

<div class="banner"><b>Step Out. Stand Out. 👑</b><br><small>Tap picture to VIEW • Add to Cart • Saves Forever</small></div>

<div class="grid">
{% for p in products %}
<div class="card">
<img src="{{p.img}}" onclick="viewImage('{{p.img}}','{{p.name}} - R{{p.price}}')">
<h4>{{p.name}}</h4>
<div class="price">R{{p.price}}</div>
<button class="btn btn-view" onclick="viewImage('{{p.img}}','{{p.name}}')">👁️ View Picture</button>
<button class="btn btn-cart" onclick="addToCart({{p.id}},'{{p.name}}',{{p.price}},'{{p.img}}')">+ Add to Cart</button>
<button class="btn btn-wa" onclick="buyNow('{{p.name}}',{{p.price}})">Order via WhatsApp</button>
</div>
{% endfor %}
</div>

<!-- CART PAGE -->
<div id="cartPage">
<h2>🛒 Your Cart</h2><button onclick="closeCart()" style="position:absolute;top:15px;right:15px;background:#ff1493;color:white;border:none;border-radius:50%;width:35px;height:35px;font-weight:bold">X</button>
<div id="cartItems" style="margin-top:20px"></div>
<h3 style="border-top:2px solid #ff1493;padding-top:10px">Total: R<span id="cartTotal">0</span></h3>
<button class="checkout" onclick="checkoutWA()">✅ Checkout via WhatsApp</button>
<button onclick="clearCart()" style="background:#eee;border:none;padding:12px;width:100%;border-radius:20px;margin-top:10px;cursor:pointer">🗑️ Clear Cart</button>
</div>

<!-- IMAGE VIEWER -->
<div id="imgViewer" onclick="closeImg()">
<img id="viewerImg" src="">
<h3 id="viewerName"></h3>
<p style="color:#ccc;font-size:12px">Tap anywhere to close</p>
</div>

<script>
// FOREVER SAVE: Cart uses localStorage - stays even if phone off!
let cart = JSON.parse(localStorage.getItem('lwahs_cart_forever')||'[]');
updateCount();

function viewImage(img,name){
 document.getElementById('viewerImg').src=img;
 document.getElementById('viewerName').innerText=name;
 document.getElementById('imgViewer').style.display='flex';
}
function closeImg(){document.getElementById('imgViewer').style.display='none';}

function addToCart(id,name,price,img){
 cart.push({id,name,price,img});
 localStorage.setItem('lwahs_cart_forever',JSON.stringify(cart));
 updateCount();
 alert('✅ '+name+' added to cart!\\nCart: '+cart.length+' items');
}
function updateCount(){
 document.getElementById('cartCount').innerText=cart.length;
 let total=0; cart.forEach(i=>total+=i.price);
 document.getElementById('cartTotal').innerText=total;
}
function openCart(){
 document.getElementById('cartPage').style.display='block';
 let html=''; 
 if(cart.length==0) html='<p style="text-align:center;padding:30px">Cart empty 😔<br>Add some tekkies!</p>';
 else cart.forEach((item,idx)=>{
  html+=`<div class="cart-item">
   <img src="${item.img}">
   <div style="flex:1"><b>${item.name}</b><br>R${item.price}</div>
   <button onclick="removeItem(${idx})" style="background:#ff1493;color:white;border:none;border-radius:10px;padding:8px 10px;cursor:pointer">Remove</button>
  </div>`;
 });
 document.getElementById('cartItems').innerHTML=html;
 updateCount();
}
function closeCart(){document.getElementById('cartPage').style.display='none';}
function removeItem(i){
 cart.splice(i,1);
 localStorage.setItem('lwahs_cart_forever',JSON.stringify(cart));
 openCart(); updateCount();
}
function clearCart(){
 if(confirm('Clear all cart?')){cart=[];localStorage.setItem('lwahs_cart_forever','[]');openCart();updateCount();}
}
function buyNow(name,price){
 let msg=`Hi Lwah! 💖 I want:\\n👟 ${name} - R${price}\\n\\nSize: [type]\\nAddress: [type]`;
 window.open("https://wa.me/27815666133?text="+encodeURIComponent(msg),"_blank");
}
function checkoutWA(){
 if(cart.length==0){alert('Cart empty!');return;}
 let msg="Hi Lwah! 💖 My Order:\\n\\n";
 let total=0;
 cart.forEach((item,i)=>{msg+=`${i+1}. ${item.name} - R${item.price}\\n`; total+=item.price;});
 msg+=`\\n💰 TOTAL: R${total}\\n\\nMy sizes: [type]\\nMy address: [type]\\n`;
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
