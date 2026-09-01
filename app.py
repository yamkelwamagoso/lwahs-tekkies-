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
    # auto resize big phone photos to small web size
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA","P"): img = img.convert("RGB")
    # max size 1000px
    img.thumbnail((1000,1000))
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=75, optimize=True)
    return out.getvalue()

@app.route('/')
def shop():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    prods = res.data or []
    html = ""
    for p in prods:
        html += f"<div style='background:white;border-radius:15px;overflow:hidden'><img src='{p['img']}' style='width:100%;height:160px;object-fit:cover' onclick=\"window.open('{p['img']}','_blank')\"><div style='padding:10px;text-align:center'><b>{p['name']}</b><br><span style='color:#ff2d78;font-weight:bold'>R {p['price']}</span><br><button onclick=\"addCart('{p['name']}',{p['price']})\" style='background:black;color:white;border:0;padding:8px 15px;border-radius:20px;margin-top:5px'>Add to Cart</button></div></div>"
    return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{margin:0;font-family:sans-serif;background:#fff0f5}}header{{background:black;color:white;padding:10px 15px;display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid #ff2d78}}.logo{{display:flex;align-items:center;gap:8px;font-weight:bold}}.logo img{{width:45px;height:45px;border-radius:50%;border:2px solid #ff2d78}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}}#cart{{position:fixed;right:10px;top:70px;background:white;padding:12px;border-radius:12px;display:none;width:280px;box-shadow:0 5px 20px #0003;z-index:10;color:black}}</style></head><body><header><div class='logo'><img src='{LOGO}'>Lwah's Tekkies</div><div onclick='toggle()' style='background:#ff2d78;padding:8px 15px;border-radius:20px'>Cart (<span id='c'>0</span>)</div></header><div style='background:linear-gradient(90deg,black,#ff2d78);color:white;text-align:center;padding:20px'><h2 style='margin:0'>Step Out. Stand Out.</h2>Tap image to view full</div><div id='cart'><h3>Cart</h3><div id='items'></div><button onclick='order()' style='background:#25D366;color:white;border:0;padding:10px;width:100%;border-radius:20px;margin-top:8px'>Order on WhatsApp</button><br><small onclick='toggle()' style='color:gray'>Close</small></div><div class='grid'>{html}</div><script>let cart=JSON.parse(localStorage.getItem('cart')||'[]');function save(){{localStorage.setItem('cart',JSON.stringify(cart));update()}}function addCart(n,p){{cart.push({{n,p}});save();alert(n+' added!')}}function del(i){{cart.splice(i,1);save()}}function update(){{document.getElementById('c').innerText=cart.length;let h='';let t=0;cart.forEach((x,i)=>{{t+=x.p;h+=x.n+' R'+x.p+' <span onclick=del('+i+') style=color:red> X</span><br>'}});h+=cart.length?'<hr>Total R'+t:'Empty';document.getElementById('items').innerHTML=h}}function toggle(){{let d=document.getElementById('cart');d.style.display=d.style.display=='none'?'block':'none'}}function order(){{if(!cart.length)return alert('Empty');let m='Hi Lwah! Order:%0A';let t=0;cart.forEach(c=>{{m+=c.n+' R'+c.p+'%0A';t+=c.p}});m+='Total R'+t;window.open('https://wa.me/{WA}?text='+m,'_blank')}}update();</script></body></html>"

@app.route('/admin')
def admin():
    res = supabase.table("products").select("*").order("id", desc=True).execute()
    prods = res.data or []
    items = "".join([f"<div style='background:white;padding:10px;margin:5px 0;border-radius:8px;display:flex;gap:8px'><img src='{p['img']}' style='width:50px;height:50px;object-fit:cover'><b>{p['name']}</b> R{p['price']} <a href='/delete/{p['id']}' style='margin-left:auto;color:red'>Delete</a></div>" for p in prods])
    return f"<body style='background:#ffe6ef;font-family:sans-serif;padding:15px'><div style='background:white;padding:15px;border-radius:12px;max-width:400px;margin:auto'><h2>Admin</h2><a href='/'>Shop</a><form action='/add' method='post' enctype='multipart/form-data'><input name='name' placeholder='Name' required style='width:100%;padding:8px;margin:5px 0'><input name='price' type='number' placeholder='Price' required style='width:100%;padding:8px'><input name='file' type='file' accept='image/*' required style='width:100%;margin:5px 0'><button style='width:100%;background:#ff2d78;color:white;border:0;padding:10px;border-radius:20px'>ADD</button></form><hr>{items}</div></body>"

@app.route('/add', methods=['POST'])
def add():
    try:
        name=request.form['name']; price=int(request.form['price']); file=request.files['file']
        raw=file.read()
        compressed = compress_image(raw)
        fname=str(uuid.uuid4())+".jpg"
        supabase.storage.from_(BUCKET).upload(fname, compressed, {"content-type":"image/jpeg","upsert":"true"})
        url=supabase.storage.from_(BUCKET).get_public_url(fname)
        supabase.table("products").insert({"name":name,"price":price,"img":url}).execute()
        return redirect('/admin')
    except Exception as e:
        return f"<h3>Error: {e}</h3><a href='/admin'>Back</a>"

@app.route('/delete/<id>')
def delete(id):
    try: supabase.table("products").delete().eq("id",id).execute()
    except: pass
    return redirect('/admin')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
