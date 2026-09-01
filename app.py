import os, uuid
from flask import Flask, request, redirect
from supabase import create_client

app = Flask(__name__)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        file = request.files['file']
        if file:
            filename = f"{uuid.uuid4()}_{file.filename}"
            supabase.storage.from_("shoes").upload(filename, file.read(), {"content-type": file.content_type})
            img_url = supabase.storage.from_("shoes").get_public_url(filename)
            supabase.table("products").insert({"name": name, "price": int(price), "img": img_url}).execute()
        return redirect('/')
    prods = supabase.table("products").select("*").order("id", desc=True).execute().data
    html = "<h1 style='text-align:center;font-family:Arial'>👟 Lwah's Tekkies - FOREVER SHOP ✅</h1>"
    html += "<form method='post' enctype='multipart/form-data' style='text-align:center;background:#f5f5f5;padding:20px;max-width:400px;margin:auto;border-radius:10px'><input name='name' placeholder='Shoe Name' required style='padding:10px;width:90%'><br><br><input name='price' type='number' placeholder='Price R' required style='padding:10px;width:90%'><br><br><input type='file' name='file' accept='image/*' required><br><br><button style='background:black;color:white;padding:12px 30px;border:none;border-radius:5px'>ADD SHOE +</button></form><br><div style='display:flex;flex-wrap:wrap;gap:15px;justify-content:center'>"
    for p in prods:
        html += f"<div style='border:1px solid #ddd;border-radius:10px;padding:10px;width:200px;text-align:center;font-family:Arial'><img src='{p['img']}' style='width:100%;height:150px;object-fit:cover;border-radius:8px'><h3>{p['name']}</h3><p><b>R{p['price']}</b></p><a href='/delete/{p['id']}' style='color:red'>Delete</a></div>"
    html += "</div>"
    return html

@app.route('/delete/<id>')
def delete(id):
    supabase.table("products").delete().eq("id", id).execute()
    return redirect('/')
