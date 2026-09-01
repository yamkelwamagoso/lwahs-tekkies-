from flask import Flask, request, redirect
import os, uuid
from supabase import create_client

app = Flask(__name__)
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
BUCKET = "shoes"

LOGO_URL = "https://ucnjgpmzscqvcisdkumo.supabase.co/storage/v1/object/public/shoes/IMG-20260831-WA0016.jpg"
WA_NUMBER = "27815666133"  # <<<< CHANGE TO YOUR NUMBER! e.g. 27731234567

@app.route('/')
def shop():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    products = res.data or []
    cards = ""
    for p in products:
        cards += f"""
        <div class="card">
          <img src="{p['img']}">
          <div class="info"><h3>{p['name']}</h3><p>R {p['price']}</p>
          <button onclick="addToCart('{p['name']}',{p['price']})">Add to Cart 🛒</button></div>
        </div>"""
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body{{margin:0;background:#0a0a0a;color:white;font-family:sans-serif}}
      header{{background:#000;border-bottom:3px solid #ff2d78;padding:10px 18px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:20}}
      .logo{{display:flex;align-items:center;gap:10px;font-weight:900;font-size:18px}}
      .logo img{{width:55px;height:55px;border-radius:50%;border:2px solid #ff2d78;object-fit:cover}}
      .cart{{background:#ff2d78;padding:10px 18px;border-radius:25px;font-weight:bold;cursor:pointer}}
      .hero{{text-align:center;padding:35px 20px;background:linear-gradient(135deg,#000 20%,#ff2d78 100%)}}
      .hero h1{{margin:0;font-size:30px}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px;padding:18px;background:#fff5f8}}
      .card{{background:white;color:#000;border-radius:18px;overflow:hidden;box-shadow:0 4px 12px #0002}}
      .card img{{width:100%;height:170px;object-fit:cover}} .info{{padding:11px;text-align:center}}
      .info p{{color:#ff2d78;font-weight:800;margin:6px 0;font-size:18px}} .info button{{background:#000;color:white;border:0;padding:10px;width:100%;border-radius:20px;font-weight:bold}}
      #cartBox{{position:fixed;right:12px;top:85px;background:white;color:black;width:310px;border-radius:16px;padding:14px;display:none;z-index:99;box-shadow:0 10px 30px #0006}}
      .wa{{background:#25D366!important;color:white;border:0;padding:12px;width:100%;border-radius:25px;font-weight:bold;margin-top:10px}}
    </style></head><body>
    <header><div class="logo"><img src="{LOGO_URL}"> Lwah's Tekkies</div><div class="cart" onclick="toggleCart()">🛒 <span id="count">0</span></div></header>
    <div class="hero"><h1>Step Out. Stand Out.</h1><p>Quality. Style. You. 💖 | Free Delivery in Durban 🚚</p></div>
    <div id="cartBox"><h3>🛒 Your Cart</h3><div id="cartItems"></div><button class="wa" onclick="orderWA()">Order on WhatsApp 💬</button></div>
    <div class="grid">{cards if cards else "<p style='color:black'>No shoes - add in /admin</p>"}</div>
    <script>
      let cart=JSON.parse(localStorage.getItem('cart')||'[]');
      function save(){{localStorage.setItem('cart',JSON.stringify(cart));upd()}}
      function addToCart(n,p){{cart.push({{n,p}});save();alert(n+' added!')}}
      function remove(i){{cart.splice(i,1);save()}}
      function upd(){{document.getElementById('count').innerText=cart.length;let h='';let t=0;cart.forEach((c,i)=>{{t+=c.p;h+=`<div style='display:flex;justify-content:space-between;margin:5px 0'>${{c.n}} R${{c.p}} <span style='color:red;cursor:pointer' onclick='remove(${{i}})'>x</span></div>`}});h+=cart.length?`<hr><b>Total R${{t}}</b>`:'Empty';document.getElementById('cartItems').innerHTML=h}}
      function toggleCart(){{let b=document.getElementById('cartBox');b.style.display=b.style.display=='none'?'block':'none'}}
      function orderWA(){{if(!cart.length)return alert('Cart empty');let m='Hi Lwah! I want:%0A';let t=0;cart.forEach(c=>{{m+=`- ${{c.n}} R${{c.p}}%0A`;t+=c.p}});m+=`%0ATotal R${{t}}%0A%0AName:%0AAddress:%0ASize:`;window.open('https://wa.me/{WA_NUMBER}?text='+m,'_blank')}}
      upd();
    </script></body></html>"""

@app.route('/admin')
def admin():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    prods = res.data or []
    items="".join([f"<div style='background:white;color:black;padding:10px;border-radius:10px;display:flex;gap:10px;align-items:center;margin:7px 0'><img src='{p['img']}' style='width:60px;height:60px;object-fit:cover;border-radius:8px'><b>{p['name']}</b> R{p['price']}<a href='/delete/{p['id']}' style='margin-left:auto;color:red'>Delete</a></div>" for p in prods])
    return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#ffe6ef;font-family:sans-serif;padding:20px}} .box{{background:white;padding:20px;border-radius:15px;max-width:400px;margin:auto}} input{{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #ccc}} button{{width:100%;padding:12px;background:#ff2d78;color:white;border:0;border-radius:20px;font-weight:bold}}</style></head><body><div class='box'><h2 style='color:#ff2d78'>💖 Lwah Admin</h2><a href='/'>View Shop</a><br><br><form action='/add' method='post' enctype='multipart/form-data'><input name='name' placeholder='Shoe Name' required><input name='price' type='number' placeholder='Price R' required><input name='file' type='file' accept='image/*' required><button>ADD SHOE +</button></form><hr>{items}</div></body></html>"

@app.route('/add', methods=['POST'])
def add():
    name=request.form['name']; price=int(request.form['price']); file=request.files['file']
    fname=f"{uuid.uuid4()}.jpg"
    supabase.storage.from_(BUCKET).upload(fname, file.read(), {{"content-type":"image/jpeg"}})
    url=supabase.storage.from_(BUCKET).get_public_url(fname)
    supabase.table("products").insert({{"name":name,"price":price,"img":url}}).execute()
    return redirect('/admin')

@app.route('/delete/<id>')
def delete(id):
    supabase.table("products").delete().eq("id",id).execute()
    return redirect('/admin')

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
