from flask import Flask, request, redirect
import os, uuid, io
from supabase import create_client
from PIL import Image

app = Flask(__name__)
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
BUCKET = "shoes"
LOGO = "https://ucnjgpmzscqvcisdkumo.supabase.co/storage/v1/object/public/shoes/IMG-20260831-WA0016.jpg"
WA = "27815666133"

def compress_image(data):
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA","P"): img = img.convert("RGB")
    img.thumbnail((1000,1000))
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=75, optimize=True)
    return out.getvalue()

@app.route('/')
def shop():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    prods = res.data or []
    cards = ""
    for p in prods:
        cards += f"""
        <div class="card">
          <div class="img-wrap" onclick="openView('{p['img']}')">
            <img src='{p['img']}' loading="lazy">
            <div class="view-badge">👁️ Tap to view</div>
          </div>
          <div class="info">
            <div class="name">{p['name']}</div>
            <div class="price">R {p['price']}</div>
            <button class="add-btn" onclick="addCart('{p['name']}',{p['price']})">Add to Cart 🛒</button>
            <a class="wa-mini" href="https://wa.me/{WA}?text=Hi Lwah! I want {p['name']} R {p['price']}" target="_blank">WhatsApp to order 💬</a>
          </div>
        </div>
        """
    return f"""
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lwah's Tekkies</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
*{{font-family:Poppins,sans-serif}}
body{{margin:0;background:#fff0f5}}
header{{background:black;color:white;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:20;border-bottom:3px solid #ff2d78}}
.logo{{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:.5px}}
.logo img{{width:48px;height:48px;border-radius:50%;border:2px solid #ff2d78;object-fit:cover}}
.cart-btn{{background:#ff2d78;color:white;padding:9px 18px;border-radius:25px;font-weight:600;cursor:pointer;position:relative}}
.cart-count{{background:white;color:#ff2d78;border-radius:50%;padding:0 7px;margin-left:6px;font-weight:700}}
.banner{{background:linear-gradient(90deg,black,#ff2d78);color:white;text-align:center;padding:22px 10px}}
.banner h2{{margin:0;font-size:22px}} .banner p{{margin:5px 0 0;opacity:.9}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:14px;max-width:900px;margin:auto}}
.card{{background:white;border-radius:18px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,.08);border:1px solid #ffe0ea}}
.img-wrap{{position:relative;cursor:zoom-in}} .img-wrap img{{width:100%;height:180px;object-fit:cover;display:block}}
.view-badge{{position:absolute;bottom:8px;right:8px;background:rgba(0,0,0,.7);color:white;font-size:11px;padding:4px 8px;border-radius:12px}}
.info{{padding:12px;text-align:center}} .name{{font-weight:600;font-size:14px;min-height:20px}} .price{{color:#ff2d78;font-weight:700;margin:6px 0}}
.add-btn{{background:black;color:white;border:0;width:100%;padding:10px;border-radius:22px;font-weight:600;margin-top:4px;cursor:pointer}}
.wa-mini{{display:block;margin-top:7px;font-size:11px;color:#25D366;text-decoration:none;font-weight:600}}
#cart-drawer{{position:fixed;right:12px;top:75px;background:white;width:320px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:14px;display:none;z-index:30;color:black;border:2px solid #ff2d78}}
.cart-item{{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #eee;font-size:14px}}
.remove{{color:white;background:red;border-radius:50%;width:22px;height:22px;display:grid;place-items:center;cursor:pointer;font-weight:700}}
.wa-order{{background:#25D366;color:white;border:0;width:100%;padding:12px;border-radius:25px;font-weight:700;margin-top:10px;cursor:pointer;font-size:15px;display:block;text-align:center;text-decoration:none}}
#lightbox{{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;place-items:center;z-index:100}} #lightbox img{{max-width:92%;max-height:92%;border-radius:12px}}
</style></head><body>
<header><div class="logo"><img src="{LOGO}">Lwah's Tekkies 👑</div><div class="cart-btn" onclick="toggleCart()">Cart <span class="cart-count" id="c">0</span></div></header>
<div class="banner"><h2>Step Out. Stand Out. 👑</h2><p>Durban's Luxury Tekkies • Delivery Available</p></div>
<div id="cart-drawer"><h3 style="margin:0 0 8px">🛒 Your Cart</h3><div id="items"></div><div id="total" style="font-weight:700;margin-top:8px"></div><a id="waLink" class="wa-order" target="_blank">WhatsApp to Order 💬</a><div style="text-align:center;margin-top:8px;color:gray;cursor:pointer" onclick="toggleCart()">Close</div></div>
<div class="grid">{cards if cards else "<p style='grid-column:1/3;text-align:center'>No shoes yet - add in /admin</p>"}</div>
<div id="lightbox" onclick="this.style.display='none'"><img id="lightImg"></div>
<script>
let cart=JSON.parse(localStorage.getItem('cart')||'[]');
function save(){{localStorage.setItem('cart',JSON.stringify(cart));update()}}
function addCart(n,p){{cart.push({{n,p}});save();let d=document.getElementById('cart-drawer');d.style.display='block';}}
function removeItem(i){{cart.splice(i,1);save()}}
function update(){{
 document.getElementById('c').innerText=cart.length;
 let h='';let t=0;
 cart.forEach((x,i)=>{{t+=x.p;h+=`<div class=cart-item><span>${{x.n}} - R${{x.p}}</span><span class=remove onclick=removeItem(${{i}})>×</span></div>`}});
 if(!cart.length)h='<p style=color:gray>Cart empty</p>';
 document.getElementById('items').innerHTML=h;
 document.getElementById('total').innerText=cart.length?'Total: R'+t:'';
 let m='Hi Lwah! I want to order:%0A'; cart.forEach(c=>{{m+=c.n+' - R'+c.p+'%0A'}}); m+='%0ATotal R'+t;
 let link='https://wa.me/{WA}?text='+m;
 document.getElementById('waLink').href=link;
 document.getElementById('waLink').style.display=cart.length?'block':'none';
}}
function toggleCart(){{let d=document.getElementById('cart-drawer');d.style.display=d.style.display=='none'?'block':'none';}}
function openView(src){{document.getElementById('lightImg').src=src;document.getElementById('lightbox').style.display='grid';}}
update();
</script>
<footer style="text-align:center;padding:25px;color:gray;font-size:12px">© 2026 Lwah's Tekkies • WhatsApp 081 566 6133</footer>
</body></html>
"""

@app.route('/admin')
def admin():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    prods = res.data or []
    items = "".join([f"<div style='background:white;padding:10px;margin:6px 0;border-radius:10px;display:flex;gap:10px;align-items:center'><img src='{p['img']}' style='width:55px;height:55px;object-fit:cover;border-radius:8px'><b>{p['name']}</b> R{p['price']} <a href='/delete/{p['id']}' style='margin-left:auto;color:red;text-decoration:none;background:#ffe0ea;padding:5px 10px;border-radius:15px'>Delete</a></div>" for p in prods])
    return f"<body style='background:#fff0f5;font-family:sans-serif;padding:15px'><div style='background:white;padding:18px;border-radius:16px;max-width:420px;margin:auto;box-shadow:0 5px 20px #0001'><h2>👑 Lwah Admin</h2><a href='/' style='color:#ff2d78'>← View Shop</a><form action='/add' method='post' enctype='multipart/form-data' style='margin-top:12px'><input name='name' placeholder='Shoe name (e.g. Nike Air R1500)' required style='width:100%;padding:10px;margin:6px 0;border-radius:10px;border:1px solid #ddd'><input name='price' type='number' placeholder='Price' required style='width:100%;padding:10px;border-radius:10px;border:1px solid #ddd'><input name='file' type='file' accept='image/*' required style='width:100%;margin:10px 0'><button style='width:100%;background:#ff2d78;color:white;border:0;padding:12px;border-radius:25px;font-weight:700'>ADD SHOE</button></form><hr style='margin:16px 0'>{items}</div></body>"

@app.route('/add', methods=['POST'])
def add():
    try:
        name=request.form['name']; price=int(request.form['price']); file=request.files['file']
        compressed = compress_image(file.read())
        fname=str(uuid.uuid4())+".jpg"
        supabase.storage.from_(BUCKET).upload(fname, compressed, {"content-type":"image/jpeg","upsert":"true"})
        url=supabase.storage.from_(BUCKET).get_public_url(fname)
        supabase.table("products").insert({"name":name,"price":price,"img":url}).execute()
        return redirect('/admin')
    except Exception as e:
        return f"<h3>Upload failed: {e}</h3><a href='/admin'>Back</a>"

@app.route('/delete/<id>')
def delete(id):
    try: supabase.table("products").delete().eq("id",id).execute()
    except: pass
    return redirect('/admin')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
