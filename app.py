from flask import Flask, request, redirect
import os, uuid
from supabase import create_client

app = Flask(__name__)

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)
BUCKET = "shoes"
WHATSAPP_NUMBER = "27815666133"  # <--- CHANGE TO YOUR WHATSAPP NUMBER HERE! e.g 27731234567

# ---------- CUSTOMER PAGE ----------
@app.route('/')
def shop():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    products = res.data if res.data else []
    
    cards = ""
    for p in products:
        cards += f"""
        <div class="card">
          <img src="{p['img']}">
          <h3>{p['name']}</h3>
          <p class="price">R {p['price']}</p>
          <button onclick="addToCart('{p['id']}','{p['name']}',{p['price']})">Add to Cart 🛒</button>
        </div>
        """

    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body{{font-family:sans-serif;margin:0;background:#fff5f8}}
      header{{background:#ff2d78;color:white;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0}}
      .logo{{font-weight:900;font-size:22px;letter-spacing:1px}}
      .cart{{background:white;color:#ff2d78;padding:8px 14px;border-radius:20px;font-weight:bold;cursor:pointer}}
      .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:15px;padding:20px}}
      .card{{background:white;border-radius:15px;padding:10px;box-shadow:0 2px 10px #0001;text-align:center}}
      .card img{{width:100%;height:140px;object-fit:cover;border-radius:10px}}
      .price{{font-weight:bold;color:#ff2d78}}
      button{{background:#111;color:white;border:0;padding:8px 12px;border-radius:20px;cursor:pointer;width:100%;margin-top:5px}}
      #cartBox{{position:fixed;right:10px;top:70px;background:white;width:300px;border-radius:15px;box-shadow:0 5px 20px #0003;padding:15px;display:none;z-index:99}}
      .wa{{background:#25D366 !important;margin-top:10px}}
    </style></head><body>
    
    <header>
      <div class="logo">👟 Lwah's Tekkies</div>
      <div class="cart" onclick="toggleCart()">🛒 Cart (<span id="count">0</span>)</div>
    </header>

    <div id="cartBox">
      <h3>Your Cart</h3>
      <div id="cartItems"></div>
      <button class="wa" onclick="orderWhatsApp()">Order on WhatsApp</button>
    </div>

    <div class="grid">{cards}</div>

    <script>
      let cart = JSON.parse(localStorage.getItem('cart')||'[]');
      function save(){{localStorage.setItem('cart',JSON.stringify(cart));update()}}
      function addToCart(id,name,price){{cart.push({{id,name,price}});save();alert(name+' added!');}}
      function removeFromCart(i){{cart.splice(i,1);save()}}
      function update(){{
        document.getElementById('count').innerText=cart.length;
        let html='';let total=0;
        cart.forEach((c,i)=>{{total+=c.price;html+=`<div style='display:flex;justify-content:space-between;margin:5px 0'>${{c.name}} - R${{c.price}} <span style='color:red;cursor:pointer' onclick='removeFromCart(${{i}})'>x</span></div>`}});
        html+=`<hr><b>Total: R${{total}}</b>`;
        if(cart.length==0) html='Empty';
        document.getElementById('cartItems').innerHTML=html;
      }}
      function toggleCart(){{let b=document.getElementById('cartBox');b.style.display=b.style.display=='none'?'block':'none'}}
      function orderWhatsApp(){{
        if(cart.length==0) return alert('Cart empty');
        let msg='Hi Lwah! I want to order:%0A';
        let total=0;
        cart.forEach(c=>{{msg+=`- ${{c.name}} R${{c.price}}%0A`;total+=c.price}});
        msg+=`%0ATotal: R${{total}}`;
        window.open('https://wa.me/{WHATSAPP_NUMBER}?text='+msg,'_blank');
      }}
      update();
    </script>
    </body></html>
    """

# ---------- ADMIN PAGE ----------
@app.route('/admin')
def admin():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    products = res.data if res.data else []
    items=""
    for p in products:
        items+=f"<div style='background:white;padding:10px;border-radius:10px;display:flex;gap:10px;align-items:center'><img src='{p['img']}' style='width:60px;height:60px;object-fit:cover;border-radius:8px'><b>{p['name']}</b> R{p['price']} <a href='/delete/{p['id']}' style='color:red;margin-left:auto'>Delete</a></div>"
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:sans-serif;background:#ffe6ef;padding:20px}} input{{padding:10px;width:100%;margin:5px 0;border-radius:8px;border:1px solid #ccc}} button{{background:#ff2d78;color:white;padding:12px;border:0;border-radius:20px;width:100%;font-weight:bold}} .box{{background:white;padding:20px;border-radius:15px;max-width:400px;margin:auto}}</style>
    </head><body>
    <div class="box">
      <h2 style="color:#ff2d78">💖 Lwah Admin</h2>
      <a href="/">View Shop →</a><br><br>
      <form action="/add" method="post" enctype="multipart/form-data">
        <input name="name" placeholder="Shoe Name" required>
        <input name="price" type="number" placeholder="Price R" required>
        <input name="file" type="file" accept="image/*" required>
        <button>ADD SHOE +</button>
      </form>
      <hr><div style="display:grid;gap:10px">{items}</div>
    </div></body></html>
    """

@app.route('/add', methods=['POST'])
def add():
    name=request.form['name']; price=int(request.form['price']); file=request.files['file']
    fname=f"{uuid.uuid4()}.jpg"
    supabase.storage.from_(BUCKET).upload(fname, file.read(), {"content-type":"image/jpeg"})
    url=supabase.storage.from_(BUCKET).get_public_url(fname)
    supabase.table("products").insert({{"name":name,"price":price,"img":url}}).execute()
    return redirect('/admin')

@app.route('/delete/<id>')
def delete(id):
    supabase.table("products").delete().eq("id",id).execute()
    return redirect('/admin')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
