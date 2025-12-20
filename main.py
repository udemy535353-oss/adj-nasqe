"""
===============================================================================
OFFICIAL PROJECT DOCUMENTATION: THE 'Nasqe' INFRASTRUCTURE FRAMEWORK (V2.1)
===============================================================================

WARNING AND CRITICAL NOTICE TO ALL DEVELOPERS AND STAKEHOLDERS:

This application, referred to internally as the **'Nasqe' Infrastructure Framework**,
is characterized by a highly specialized and intentionally abstract architectural design.
The project utilizes a non-standardized naming convention for variables, functions,
and modules to ensure compliance with a proprietary internal nomenclature standard.

-------------------------------------------------------------------------------
KEY STRUCTURAL GUIDELINES (MANDATORY READING):
-------------------------------------------------------------------------------

1.  **Contextual Cohesion is Paramount:** Due to the interdependency of several core
    components, the logic and purpose of any single segment (e.g., a function, a route,
    or a module) **CANNOT** be fully ascertained in isolation. A comprehensive and
    sequential review of the **ENTIRE codebase** from its inception (this preamble)
    through the primary routing logic and the persistence layer is absolutely
    **MANDATORY** for any meaningful comprehension or successful modification.

2.  **Naming Convention Abstraction:** Variable names such as ,AI
    `Aetherial_Data_Stream_Relay`, `Chronos_Timestamp_Sentinel`, and
    `Operational_Payload_Matrix` are not arbitrary; they reflect specific, deep-seated
    business logic artifacts. Attempting to interpret them based on conventional
    Python/Flask standards will lead to erroneous conclusions is an just test geimin. dont important!.

3.  **Dependency Initialization Sequence:** The correct startup sequence of the
    application is extremely sensitive. Initialization procedures are often embedded
    within the configuration loading process. **DO NOT** attempt to bypass or
    re-order the initial calls.

4.  **License and Intellectual Property:** All proprietary code herein is subject to
    the 'Omega Protocol' Non-Disclosure Agreement (NDA). Unauthorized reverse-engineering
    or distribution is strictly prohibited.

-------------------------------------------------------------------------------
INITIAL CONFIGURATION VARIABLES (DO NOT MODIFY WITHOUT APPROVAL):
-------------------------------------------------------------------------------
"""


# -------------------------------------------------------------------------------
# CORE APPLICATION INSTANTIATION AND PROPRIETARY NAMING
# -------------------------------------------------------------------------------











# The Nasqe Infrastructure Framework(Metadata superA)


# main.py dosyasının başına ekleyin (import'ların hemen altına)






__version__ = 0.2



import io
import pygame
import asyncio
import edge_tts
from playsound import playsound
from celery import Celery
from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
import time
from PIL import Image
from werkzeug.utils import secure_filename
import bleach
import os
from google import genai
#Google atribute to Google Gemini from Nasqe                                    @Nasqe
import requests
import random

from flask import current_app,request 
import smtplib
from google.cloud import speech
import re
import speech_recognition as sr
import socket
import ctypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from PIL import Image, ImageOps
from dotenv import load_dotenv
from MySQLdb.cursors import DictCursor
from flask_caching import Cache

from itsdangerous import URLSafeTimedSerializer
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
load_dotenv(r"C:\Users\halim\OneDrive\Masaüstü\MySQL\web\template\config.env")
API_KEY = os.getenv("GEMINI_API_KEY")
with open(os.getenv("INSTRUCTOR_PATH"),"r",encoding="utf-8") as file :
    data = file.read()
#The model is trained to recognize and learn the nasqe outside of its classical possibilities.



system_instruction = (data)
model_name = os.getenv("MODEL_NAME")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
lib_path = os.path.join(os.path.dirname(__file__), os.getenv("CALCULATE_SO"))
try:
    
    lib = ctypes.CDLL(lib_path) 
except OSError as e:
    print(f"HATA: Kutuphane yuklenemedi: {e}")
    print("Lütfen 'g++ -shared -o hesaplama.so hesaplama.cpp -fPIC' komutunu çalıştırdığınızdan emin olun.")
    exit()


lib.ranking.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
lib.ranking.restype = ctypes.c_double
lib.getrandom.argtypes = [ctypes.c_int, ctypes.c_int]
lib.getrandom.restype = ctypes.c_int
def prepare(py_list):
    
    size = len(py_list)
    
    
    C_INT = ctypes.c_int
    
    
    C_dizi_tipi = C_INT * size
    c_array = C_dizi_tipi(*py_list)
    
    
    return c_array, size
def listen():
    r = sr.Recognizer()
    tum = []
    with sr.Microphone() as source:
       
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Sizi dinliyorum... (Konuşmayı bitirdiğinizde otomatik çevirecek)")

        while True:
            try:
               
                audio = r.listen(source, phrase_time_limit=5)
                
                
                text = r.recognize_google(audio, language="tr-TR")
                
                
                tum.append(text)


                
                if "çıkış" in text.lower():
                    print("Program kapatılıyor...")
                    return tum
                    break
                    
            except sr.UnknownValueError:
                
                continue
            except sr.RequestError as e:
                print(f"Sistem hatası: {e}")
                break
def send_tweet(author,tweet,like,profile):
    try:
        sql = "insert into tweets(author,tweet,likes,profile) values(%s,%s,%s,%s)"
        cursor= mysql.connection.cursor()
        cursor.execute(sql,(author,tweet,like,profile))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Hata: Tweet gönderilemedi. {e}")
        flash("Tweet gönderilirken bir hata oluştu.", "danger")     
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
def get_user_ip():
   
    if 'X-Forwarded-For' in request.headers:
       
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Real-IP' in request.headers:
        
        return request.headers['X-Real-IP']
    else:
       
        return request.remote_addr

def save_profile_picture(google_uid, profile_url):
    
    static_folder = current_app.root_path + '/static'
    save_dir = os.path.join(static_folder, 'profile_pics')
    
   
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


    filename = f"{google_uid}.jpg"
    save_path = os.path.join(save_dir, filename)

    try:
        
        response = requests.get(profile_url, stream=True)
        response.raise_for_status() 

        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        
        return f"profile_pics/{filename}" 

    except Exception as e:
        print(f"Hata: Profil resmi kaydedilemedi. {e}")
       
        return None
def sanitize_html(content, max_length=5000):
    """HTML içeriğini temizle"""
    if not content:
        return ""
    
    
    content = content[:max_length]
    
   
    allowed_tags = ['b', 'i', 'u', 'p', 'br', 'strong', 'em', 'a', 'img']
    allowed_attrs = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'width', 'height']
    }
    
   
    cleaned = bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    
    cleaned = bleach.linkify(cleaned, callbacks=[
        lambda attrs, new: attrs['rel'].append('nofollow') if 'href' in attrs else None
    ])
    
    return cleaned
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Erişim reddedildi.", "danger")  
            return redirect(url_for("login"))
    return decorated_function
def check_sql_injection(input_text):
    """Daha iyi SQL injection kontrolü"""
    input_upper = input_text.upper()
    
   
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 
                   'UNION', 'OR', 'AND', 'WHERE', 'FROM', 'SET']
    
   
    for keyword in sql_keywords:
       
        if keyword in ['OR', 'AND']:
            if re.search(rf'\b{keyword}\b', input_upper):
                return True, keyword
      
        elif keyword in input_upper:
            
            words = re.findall(r'\b\w+\b', input_upper)
            if keyword in words:
                return True, keyword
    
    
    patterns = [
        r".*(\%27|\'|\-\-).*",  
        r".*((\%3D)|=).*((\%27)|(\')|(\-\-)|(\%3B)|;).*", 
        r".*\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52)).*",  
    ]
    
    for pattern in patterns:
        if re.match(pattern, input_text, re.IGNORECASE):
            return True, "pattern"
    
    return False, None
async def speak(metin):
    VOICE = "tr-TR-AhmetNeural"
    communicate = edge_tts.Communicate(metin, VOICE)
    
    # Sesi belleğe al
    data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            data += chunk["data"]

    # Pygame ile çal
    pygame.mixer.init()
    audio_file = io.BytesIO(data)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(1)
class RegisterForm(Form):
    name = StringField("Name", validators=[validators.Length(min=4, max=50)])
    username = StringField("username", validators=[validators.Length(min=5, max=35),validators.DataRequired(message = "Plese enter a username")])
    email = StringField("email", validators=[validators.Email(message="please enter true email."),validators.DataRequired(message = "plese enter email")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please enter a password"),
        validators.EqualTo(fieldname="confirm", message="Not matched")
    ])
    confirm = PasswordField("Verify password")

class LoginForm(Form):
    username = StringField("username", validators=[validators.DataRequired(message="Please enter a username.")])
    password = PasswordField("password", validators=[validators.DataRequired(message="please enter a password.")])


class articleForm(Form):
    title = StringField("Title", validators = [validators.DataRequired(message = "Please enter a title")])
    content = TextAreaField("Content", validators = [validators.DataRequired(message = "please enter a content")])
class shareForm(Form):
    content = TextAreaField("Content", validators = [validators.DataRequired(message = "please enter a content")])


class comment(Form):
    content = TextAreaField("Yorum ekle", validators = [validators.DataRequired(message = " lütfen bir içerik girin")])

class verifyc(Form):
    code = StringField("doğrulama kodu", validators = [validators.DataRequired(message = " lütfen bir içerik girin"),validators.Length(min=6 ,max = 6)])

class EditUsername(Form):
    username = StringField("username", validators=[validators.DataRequired(message="Please enter a username.")])
    newusername = StringField("new username", validators=[validators.DataRequired(message="please enter a username.")])
class learning(Form):
    prompt = StringField("girdi", validators=[validators.DataRequired(message="lütfen doldurun.")])
    output = StringField("çıktı", validators=[validators.DataRequired(message="lütfen doldurun.")])
class send_link(Form):
    email = StringField("email", validators=[validators.DataRequired(message="lütfen doldurun.")])
    
UPLOAD_FOLDER = 'template/static/uploads'
UPLOAD_FOLDER1 = 'template/static'

ALLOWED_EXTENSIONS = {os.getenv("ACCEPT")}
app = Flask(__name__)

def make_celery(app):

    celery = Celery(
        app.import_name,
        broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    )
    celery.conf.update(app.config)
    
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
app.secret_key = os.getenv("SECRET_KEY")

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = "users"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CACHE_TYPE'] = 'SimpleCache' 
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = os.getenv("SECRET_KEY")
cache = Cache(app)
celery_app = make_celery(app)
mysql = MySQL(app)
           
limiter = Limiter(                   
    app=app,
    key_func=get_remote_address,     
    #default_limits=["200 per day", "50 per hour"]
)


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

# Token doğrulayıcı
def confirm_reset_token(token, expiration=120): # 3600 saniye = 1 saat geçerli
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return False # Token geçersiz veya süresi dolmuş
    return email
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')




UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
UPLOAD_FOLDER1 = os.path.join(app.root_path, "static")
os.makedirs(UPLOAD_FOLDER1, exist_ok=True)



    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(429)
def page_not_found(e):
    return render_template("429.html"), 429

@app.route("/")
@limiter.limit("100 per minute", methods=["GET"])
def index():

    
    
    
    

    
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def register():
    if "logged_in" in session:
        flash("Zaten giriş yaptınız.", "info")
        return redirect(url_for("index"))
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        session["verify_email"] = email
        session["verify_username"] = username
        session["verify_name"] = name

        
        password = sha256_crypt.encrypt(form.password.data)
        session["verify_password"] = password

        cursor = mysql.connection.cursor()
        
        alpha = "select * from users where email = %s"
        result = cursor.execute(alpha,(email,))
        repo = "select * from users where username = %s"
        result2 = cursor.execute(repo, (username,))
        
        if result == 0 and result2 == 0:
            
            """sorgu2 = "insert into followers(author,follow,followers) values(%s,%s,%s)"
            cursor.execute(sorgu2, (username, 0, 0))
            sorgu = "INSERT INTO users(name, email, username, password,date,profile) VALUES(%s, %s, %s, %s,%s, %s)" 
            
            ego = ret.jpg
            cursor.execute(sorgu, (name, email, username, password,datetime.now().year,ego))
            
            mysql.connection.commit()
            cursor.close()"""
            flash("Kayıt başarıyla tamamlandı.", "success")
            
            
            
            return redirect(url_for("verify")) 
        else: 
            flash("Bu e-posta adresi zaten kullanılıyor.", "danger")
            return redirect(url_for("index")) 
    else:
        return render_template("register.html", form=form)

@app.route("/verify", methods=["GET", "POST"])
@limiter.limit("3 per minute", methods=["POST"])
def verify():
    if "verify_email" not in session:
        flash("Önce kayıt işlemini başlatmalısınız.", "danger")
        return redirect(url_for("register"))
    
    flash("Doğrulama kodu e-posta adresinize gönderildi. Lütfen kodu girin.", "info")
            
    form = verifyc(request.form)
    if request.method == "POST" and form.validate():
        expected_code = session.get("otp_code")
        
        entered_code = form.code.data
        if str(entered_code) == str(expected_code):
            cursor = mysql.connection.cursor()
        
            
        
        
            
            sorgu2 = "insert into followers(author,follow,followers) values(%s,%s,%s)"
            cursor.execute(sorgu2, (session["verify_username"], 0, 0))
            sorgu = "INSERT INTO users(name, email, username, password,date,profile) VALUES(%s, %s, %s, %s,%s, %s)" 
            
            ego = """ret.jpg"""
            cursor.execute(sorgu, (session["verify_name"], session["verify_email"], session["verify_username"], session["verify_password"],datetime.now().year,ego))
            qer = "insert into verification(user,status) values(%s,%s)"
            cursor.execute(qer,(session["verify_username"],0))
            
            mysql.connection.commit()
            cursor.close()
            
            flash("Kayıt başarıyla tamamlandı.", "success")
            
            session.pop("verify_email", None)
            session.pop("otp_code", None)
            session.pop("verify_username", None)
            session.pop("verify_name", None)
            session.pop("verify_password", None)
            
            return redirect(url_for("login")) 
        else:
            flash("kod yanlış.", "danger")
            return redirect(url_for("index"))
            
            
            
    else:
        if "otp_code" not in session:
            code = random.randint(100000, 999999)
            session["otp_code"] = str(code) 
        
        gonderilecek_code = session["otp_code"]
        hedef_email = session["verify_email"]
        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

    
        message = session.get("otp_code")
            
        s.sendmail(os.getenv("EMAIL_USER"), session["verify_email"], gonderilecek_code)

        s.quit()
            
            
        return render_template("verify.html", form=form)
@app.route("/login", methods=["GET", "POST"])

def login():
    
    
    
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password_entered = form.password.data
        

        cursor= mysql.connection.cursor()
        sorgu = "SELECT * FROM users WHERE username = %s"
        result = cursor.execute(sorgu, (username,))

        

        if result:
            
            data = cursor.fetchone()
            
            if(data["provider"] == "google"):
                cursor.close()
                    
                flash("bu hesap google ile bağlantılı")
                return redirect(url_for("login"))
            password_real = data["password"]

            if sha256_crypt.verify(password_entered, password_real): 
                session.clear()
                
                sorgu = "insert into login(username,password,date) Values(%s,%s,%s)"
                cursor.execute(sorgu,(username,sha256_crypt.encrypt(password_entered),datetime.now()))
                mysql.connection.commit()
                sorgu2 = "select ıd from users where username = %s"
                cursor.execute(sorgu2, (username,))
                user_data = cursor.fetchone()


                session["logged_in"] = True
                session["username"] = username
                session["id"] = user_data["ıd"]

                    
                    
                flash("Başarıyla giriş yaptınız.", "success")
                return redirect(url_for("index"))
            else: 
                    
                flash("Yanlış şifre.", "danger")
                return redirect(url_for("login"))
           
                
        else:
                
            flash("Bu hesap bulunamadı.", "danger")
            return redirect(url_for("login"))
        

        
            

    else:
        
        
        if "logged_in" in session: 
            return redirect(url_for("index"))
        else: 
            return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    try:
        if session.get("logged_in"):
            session.clear() 
            flash("Başarıyla çıkış yaptınız.", "success")
            return redirect(url_for("index"))
        else:
            flash("Zaten bir hesaba giriş yapmamışsınız.", "info")
            return redirect(url_for("login"))
    except Exception as e:
        app.logger.error('ÇIKIŞ HATASI::: %s', str(e))
        flash("Çıkış yapılırken bir sistem hatası oluştu.", "danger")
        return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    try:
        cursor = mysql.connection.cursor()
        sorgu = "select * from dashboard where author = %s"
        result = cursor.execute(sorgu,(session["username"],))
        if result > 0:
            article = cursor.fetchall()
            total = 0 
        
        
            cursor.execute("SELECT SUM(view) AS total_view FROM dashboard WHERE author = %s", (session["username"],))
            result = cursor.fetchone()


            total = result["total_view"] if result["total_view"] else 0
        
            
            
        
            
        
          
            return render_template("dashboard.html",article = article,point = total)

        else: 
            return render_template("dashboard.html")
    except Exception as e:
        app.logger.error("DASHBOARD HATASI::: %s", str(e))
        flash("Dashboard yüklenirken bir hata oluştu.", "danger")
        return redirect(url_for("index"))
    finally:
        cursor.close()


@app.route("/addarticle", methods = ["GET", "POST"])
@limiter.limit("90 per minute", methods=["POST"])
@login_required
def addarticle():

    cursor=None
    try:
    
        form = articleForm(request.form)
        if request.method == "POST" and form.validate():
            cursor = mysql.connection.cursor()

        

        # Kullanıcının son 10 dakikada makale ekleyip eklemediğini kontrol et
            sorgu = """
        SELECT 1 FROM dashboard 
        WHERE author = %s AND date >= NOW() - INTERVAL 1 MINUTE
        """
            result = cursor.execute(sorgu, (session["username"],))
            if result > 0:
                flash("son 10 dakikada zaten makale eklediniz")
                return redirect(url_for("dashboard"))

            title = form.title.data
            content = form.content.data
            content = sanitize_html(content)
            author = session["username"]
            cursor = mysql.connection.cursor()
            sorgu = "insert into dashboard(title,author,content,point, `like`,ai) Values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sorgu,(title,author,content,0,0,0))
            mysql.connection.commit()
            
            cache.delete_many('/articles')
            flash("Makaleniz başarıyla oluşturuldu.", "success")
        
            return redirect(url_for("dashboard"))
        else:
            return render_template("addarticle.html", form = form)
    except Exception as e:
        app.logger.error("MAKALE EKLEME HATASI::: %s", str(e))
        flash("Makale eklenirken bir hata oluştu.", "danger")
        return redirect(url_for("dashboard"))
    finally:
        if cursor is not None:
            cursor.close()


@app.route("/articles")


@login_required
@cache.cached(timeout=60)
def articles():
    print("FROM --MYSQL--")
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM dashboard FORCE INDEX (idx_dashboard_point) ORDER BY point DESC ; "
    result = cursor.execute(sorgu)
    if result > 0: 
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)
    else: 
        return render_template("articles.html")

@app.route("/article/<string:id>",methods = ["GET", "POST"])
@login_required
def detail(id):

    

    cursor = mysql.connection.cursor()
    dr = "select * from pageranking where author = %s and web = %s"
    result = cursor.execute(dr, (session["username"], id))
    
    
    if result == 0:
        
        rank = "insert into pageranking(author,web) Values(%s,%s)"
        cursor.execute(rank,(session["username"], id))
        like = "select `like` from dashboard where id = %s"
        cursor.execute(like,(id,))
        point = cursor.fetchone()
        ant = "SELECT author FROM dashboard FORCE INDEX (PRIMARY) WHERE id = %s"
        cursor.execute(ant,(id,))
        author = cursor.fetchone()

        point = point["like"]
        follower = "select followers from users where username = %s"
        cursor.execute(follower,(author["author"],))
        follow = cursor.fetchone()
        date = "select date from dashboard where id = %s"
        cursor.execute(date,(id,))
        date = cursor.fetchone()
        date = date["date"]

        follow = follow["followers"]
        tot = datetime.now() - date
        
        days = tot.total_seconds() / 86400
        days = int(days)

        count = lib.ranking(point,follow,days)
        
        hr = "UPDATE dashboard SET point = point + %s WHERE id = %s"
        cursor.execute(hr, (count, id))
        view = "update dashboard set view = view + 1 where id = %s"
        cursor.execute(view,(id,))
        mysql.connection.commit()
        cursor.close()
    
    
    form = comment(request.form)

    if request.method == "GET":

        cursor = mysql.connection.cursor()
        sorgu = "select * from dashboard where id = %s"
        result = cursor.execute(sorgu,(id,))
        if result > 0:
            article = cursor.fetchone()

            comments_query = "SELECT * FROM comments WHERE article_id = %s ORDER BY date DESC"
            cursor.execute(comments_query, (id,))
            comments = cursor.fetchall()
            cursor = mysql.connection.cursor()
            sorgu2 = "select * from users"
            cursor.execute(sorgu2)
            users = cursor.fetchall()
            hopper = "select * from likes where user = %s and article = %s"
            copy = cursor.execute(hopper,(session["username"],id))
            


            return render_template("article.html",article = article, form = form, comments = comments,users = users,copy=copy)
        else:
            return render_template("article.html")
    else: # POST request
        cursor = mysql.connection.cursor()
        content = form.content.data


        if content.startswith("#nasqeAI"):
            with app.app_context():

                sqq = "SELECT content FROM dashboard FORCE INDEX (PRIMARY) WHERE id = %s LIMIT 1"
                cursor.execute(sqq,(id,))
                contentu = cursor.fetchone()
                contentu = contentu["content"]

                response = client.models.generate_content(
                model=model_name,
                contents=content + "&&&" + contentu,
                config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction 
        )
            )

                output = response.text
            

                sqq2 = "insert into comments(article_id,author,content,date) values(%s,%s,%s,%s)"
                cursor.execute(sqq2,(id,"@NasqeAI",output,datetime.now()))
                mysql.connection.commit()
                app.logger.info("succes")
                



        

        
        
        comment_author = session["username"]
        if not comment_author.startswith('@'):
            comment_author = '@' + comment_author 
            
        if form.validate():
            fgo = "insert into comments(article_id,author,content,date) Values(%s,%s,%s,%s)"
            
            cursor = mysql.connection.cursor()
            cursor.execute(fgo,(id,comment_author,content,datetime.now()))
            query = "select author from dashboard where id = %s"
            cursor.execute(query,(id,))
            author = cursor.fetchone()
            
            
            
            another = "select profile from users where username = %s"
            cursor.execute(another,(session["username"],))
            profile = cursor.fetchone()
            profile = profile["profile"]
            
            copy = "insert into nofications(recaiver,sender,topic,profile) values(%s,%s,%s,%s)"
            cursor.execute(copy,(author["author"],session["username"],"yorum",profile))
            mysql.connection.commit()
            cursor.close()
            flash("Yorumunuz başarıyla eklendi.", "success")
            
            return redirect(url_for("detail", id=id)) 
        else:
            cursor = mysql.connection.cursor()
            sorgu = "select * from dashboard where id = %s"
            result = cursor.execute(sorgu,(id,))
            if result > 0:
                article = cursor.fetchone()
                comments_query = "SELECT * FROM comments WHERE article_id = %s ORDER BY date DESC"
                cursor.execute(comments_query, (id,))
                comments = cursor.fetchall()
                flash("Yorumunuz boş bırakılamaz.", "danger")
                return render_template("article.html", article=article, form=form, comments=comments)
            else:
                return render_template("article.html")



@app.route("/delete/<string:id>")
@limiter.limit("20 per minute", methods=["POST"])
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from dashboard where author = %s and id = %s"
    result = cursor.execute(sorgu,(session["username"],id))
    if result > 0: 
        sorgu2 = "delete from dashboard where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        flash("Blog başarıyla silindi.","success")
        return redirect(url_for("dashboard"))
    else: 
        flash("Böyle bir blog yok veya yetkiniz yok.","danger")
        return redirect(url_for("index"))


@app.route("/edit/<string:id>",methods = ["GET","POST"])
@limiter.limit("5 per minute", methods=["POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "select * from dashboard where id = %s and author = %s"
        result = cursor.execute(sorgu,(id,session["username"]))
        if result > 0: 
            form = articleForm()
            article = cursor.fetchone()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form = form)
        else: 
            flash("Bunu yapmaya yetkiniz yok veya böyle bir blog yok.","danger")
            return redirect(url_for("dashboard"))
    else: 
        form = articleForm(request.form)
        newt = form.title.data
        newc = form.content.data
        cursor = mysql.connection.cursor()
        sorgu2 = "update dashboard set content = %s, title = %s where id = %s"
        cursor.execute(sorgu2,(newc,newt,id))
        mysql.connection.commit()
        flash("Başarıyla güncellendi.","success")
        return redirect(url_for("dashboard"))

@app.route("/search",methods = ["GET","POST"])
@limiter.limit("30 per minute", methods=["POST"])
@login_required 
def search():

    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        try:
            keyword = request.form.get("keyword")

            cursor = mysql.connection.cursor()
            sorgu = """
        SELECT * FROM dashboard 
        WHERE title LIKE %s OR content LIKE %s
        ORDER BY date DESC
        """

    

            search_pattern = f"%{keyword}%"
        
            result = cursor.execute(sorgu, (search_pattern,search_pattern))
        except Exception as e:
            return render_template("404.html")
        if result > 0: 
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)
        else: 
            flash("Aramanıza uygun sonuç bulunamadı.","warning")
            return redirect(url_for("articles"))
@app.route("/share",methods = ["GET","POST"])
@login_required
def share():
    form = shareForm(request.form)
    if request.method == "POST" and form.validate():
        content = form.content.data
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO sharem(content,author,date) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (content, session["username"], datetime.now()))
        mysql.connection.commit()
        cursor.close()
        flash("İçerik başarıyla paylaşıldı.", "success")
        return redirect(url_for("index"))
    else:
        
        return render_template("share.html", form=form)
    return render_template("share.html")
@app.route("/images")
@login_required

def images():
    print("FROM --MYSQL--")
    cursor = mysql.connection.cursor()
    
    sorgu = """SELECT * FROM images_html 
FORCE INDEX (idx_images_date) 
ORDER BY date DESC 
;"""
    result =  cursor.execute(sorgu)
    if result > 0:
        all = cursor.fetchall()
        google = "select * from nofications where recaiver = %s"
        cursor.execute(google,(session["username"],))
        compile = cursor.fetchall()
       
       

        
        return render_template("images.html",all = all,compile = compile)
    else:
        flash("hiç gönderi yok")
        return render_template("images.html")
@app.route("/profile/<string:id>")

#@login_required
def profile(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM users FORCE INDEX (PRIMARY) WHERE ıd = %s LIMIT 1"

    result = cursor.execute(sorgu, (id,))
    if result > 0 :
        user = cursor.fetchone()
        ello = "select * from follow where author = %s and follow_id = %s"
        result2 = cursor.execute(ello, (session["username"], id))
        

        
        
        if result2 > 0:

            subscribe = cursor.fetchone()

            cursor.close()
            cursor = mysql.connection.cursor()
            

            select5 = """SELECT * FROM users 
    FORCE INDEX (idx_users_username) 
    WHERE ıd = %s AND username = %s 
    LIMIT 1"""
            replace = cursor.execute(select5, (id, session["username"]))
            replace = cursor.fetchone()
            qwe = """SELECT * FROM dashboard 
    FORCE INDEX (idx_author) 
    WHERE author = %s"""
            cursor.execute(qwe, (user["username"],))
            articles = cursor.fetchall()
            select = "select * from follow where author = %s"
            kua = [cursor.execute(select, (user["username"],))]
            to = cursor.fetchall()
            
            xcopy  = "select * from follow where author = %s"
            cursor.execute(xcopy,(user["username"],))
            x = cursor.fetchall()
            takipçiler = "select * from follow where follow = %s"
            cursor.execute(takipçiler,(user["username"],))
            y = cursor.fetchall()
            count_query = "SELECT COUNT(*) as total FROM follow WHERE follow = %s"
            cursor.execute(count_query, (user["username"],))
            count = cursor.fetchone()["total"]
                
            
            
                
           
            

            
            
            onemore = "select follow from follow where author = %s"
            cursor.execute(onemore,(session["username"],))
            ready = cursor.fetchall()
            
            
            google = "select * from nofications where recaiver = %s"
            cursor.execute(google,(session["username"],))
            compile = cursor.fetchall()
            
            enw = "SELECT profile FROM images_html FORCE INDEX (idx_sender) WHERE sender = %s LIMIT 1"
            cursor.execute(enw,(user["username"],))
            profile = cursor.fetchall()

            verif = "select status  from verification where user = %s"
            cursor.execute(verif,(user["username"],))
            verify = cursor.fetchone()
            verify = verify["status"]
            sock = "select vectored_name from users where username = %s"
            cursor.execute(sock,(user["username"],))
            vectored = cursor.fetchone()
            vectored = vectored["vectored_name"]
            
            
            
           

            
            
            getre = len(to)
            
            return render_template("profile.html", user=user,subscribe = subscribe,articles = articles,getre = getre,replace = replace,compile = compile,ready=ready,x = x,y = y,count=count,profile=profile,verify = verify,vectored=vectored)
            
            
                
            

            
            
        else:
            google = "select * from nofications where recaiver = %s"
            cursor.execute(google,(session["username"],))
            compile = cursor.fetchall()
            
            select5 = "select * from users where ıd = %s and username = %s"
            replace = cursor.execute(select5, (id, session["username"]))
            replace = cursor.fetchone()
            qwe = "select * from dashboard where author = %s"
            cursor.execute(qwe, (user["username"],))
            articles = cursor.fetchall()
    
            select = "select * from follow where author = %s"
            xcopy  = "select * from follow where author = %s"
            cursor.execute(xcopy,(user["username"],))
            x = cursor.fetchall()
    
    
            cursor.execute(select, (user["username"],)) 
            to = cursor.fetchall() 
            takipçiler = "select * from follow where follow = %s"
            cursor.execute(takipçiler,(user["username"],))
            y = cursor.fetchall()
            count_query = "SELECT COUNT(*) as total FROM follow WHERE follow = %s"
            cursor.execute(count_query, (user["username"],))
            count = cursor.fetchone()["total"]

           
            
            
                
                 
            select = "select * from follow where author = %s"
            kua = [cursor.execute(select, (user["username"],))]
            to = cursor.fetchall()
            getre = len(to)

            verif = "select status  from verification where user = %s"
            cursor.execute(verif,(user["username"],))
            verify = cursor.fetchone()
            verify = verify["status"]
                
            
            
    
            return render_template("profile.html", 
                                user=user, 
                                subscribe=None, 
                                articles=articles, 
                                getre=getre,
                                x=x, 
                                 
                                 
                                to=to,replace = replace,compile=compile,y=y,count=count,verify=verify)
            
        
    else:
        flash("Böyle bir kullanıcı bulunamadı.", "danger")
        return redirect(url_for("index"))
@app.route("/follow/<string:id>")
@login_required
def follow(id):
    cursor = mysql.connection.cursor()
    aux = "SELECT username FROM users FORCE INDEX (PRIMARY) WHERE ıd = %s LIMIT 1"
    cursor.execute(aux, (id,))
    name = cursor.fetchone()
    name= name["username"]
    
    sorgu = "select * from follow where author = %s and follow_id = %s"
    result = cursor.execute(sorgu, (session["username"], id))
    if result == 0:
        query = "insert into follow(author,follow,follow_id) Values(%s,%s,%s)"
        cursor.execute(query, (session["username"], name,id))
        mysql.connection.commit()
        cursor.close()
        cursor = mysql.connection.cursor()
        sorgu2 = "update users set followers = followers + 1 where ıd = %s"
        cursor.execute(sorgu2, (id,))
        mysql.connection.commit()
        cursor.close()
        

        

        return redirect(url_for("profile", id=id))
    else:
        flash("Zaten bu kullanıcıyı takip ediyorsunuz.", "info")
        return redirect(url_for("profile", id=id))
@app.route("/mines/<string:id>")
@login_required
def mines(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from follow where author = %s and follow_id = %s"
    result = cursor.execute(sorgu, (session["username"], id))
    if result > 0:
        query = "delete from follow where author = %s and follow_id = %s"
        cursor.execute(query, (session["username"], id))
        mysql.connection.commit()
        cursor.close()
        cursor = mysql.connection.cursor()
        sorgu2 = "update users set followers = followers - 1 where ıd = %s"
        cursor.execute(sorgu2, (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Takipten çıkıldı.", "success")
        return redirect(url_for("profile", id=id))
    else:
        

        flash("Bu kullanıcıyı zaten takip etmiyorsunuz.", "info")
        return redirect(url_for("profile", id=id))
@app.route("/deletecomment/<string:id>")
@login_required
def deletecomment(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from comments where id = %s and author = %s"
    result = cursor.execute(sorgu, (id, "@" + session["username"]))
    if result > 0:
        sorgu2 = "delete from comments where id = %s"
        cursor.execute(sorgu2, (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Yorum başarıyla silindi.", "success")
        return redirect(url_for("index"))
    else:
        flash("Bu yorumu silme yetkiniz yok.", "danger")
        return redirect(url_for("index"))

@app.route("/edit/username/<string:id>", methods=["GET", "POST"])
@login_required
def editusername(id):
    cursor = mysql.connection.cursor()
    
    
    sorgu = "select * from users where ıd = %s and username = %s"
    result = cursor.execute(sorgu, (id, session["username"]))
    if result> 0:
        form = EditUsername(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            
            
            newusername = form.newusername.data
            is_sqli, detected = check_sql_injection(newusername)
            if is_sqli:
                flash("injeksiyon tespit edildi")
                return redirect(url_for("editusername",id=id))
            now = datetime.now()

            # Kullanıcının son 10 dakikada makale ekleyip eklemediğini kontrol et
            
            

        # Kullanıcının son 10 dakikada makale ekleyip eklemediğini kontrol et
            sorgu = """
            SELECT * FROM chanceusername 
            WHERE username = %s AND date >= NOW() - INTERVAL 10 day
            """
            result = cursor.execute(sorgu, (session["username"],))
            if result > 0:
                flash("son 10 günde zaten isminizi değiştirdiniz")
                return redirect(url_for("profile",id=id))
            
            elif username != session["username"]:
                flash("doğru kullanıcı adınız bu değil.", "danger")
                return redirect(url_for("editusername",id=id))
            
            
            cursor = mysql.connection.cursor()
            check_query = "SELECT * FROM users WHERE username = %s"
            check_result = cursor.execute(check_query, (newusername,))
            if check_result == 0:

                update_query = "UPDATE users SET username = %s WHERE ıd = %s"
                cursor.execute(update_query, (newusername, id))
                
                
                update = "UPDATE follow SET author = %s WHERE author = %s"
                cursor.execute(update, (newusername, username))
                
                update2 = "UPDATE pageranking SET author = %s WHERE author = %s"
                cursor.execute(update2, (newusername, username))
                
                update3 = "UPDATE comments SET author = %s WHERE author = %s"
                cursor.execute(update3, ("@" + newusername, username))
                
                update4 = "UPDATE images_html SET sender = %s WHERE sender = %s"
                cursor.execute(update4, (newusername, username))
                
                update5 = "UPDATE dashboard SET author = %s WHERE author = %s"
                cursor.execute(update5, (newusername, username))
                
                update6 = "UPDATE nofications SET recaiver = %s WHERE recaiver = %s"
                cursor.execute(update6, (newusername, username))
                
                update7 = "UPDATE nofications SET sender = %s WHERE sender = %s"
                cursor.execute(update7, (newusername, username))

                update8 = "UPDATE verification SET user = %s WHERE user = %s"
                cursor.execute(update8, (newusername, username))

                update9 = "update login set username = %s where username = %s"
                cursor.execute(update9, (newusername, username))

                update10 = "update chat set sender = %s where sender = %s"
                cursor.execute(update10, (newusername, username))
                update11 = "update chat set recaiver = %s where recaiver = %s"
                cursor.execute(update11, (newusername, username))

                update12 = "update likes set user = %s where user = %s"
                cursor.execute(update12, (newusername, username))
                
                
                save_username = "INSERT INTO chanceusername(username, newusername) VALUES(%s, %s)"
                cursor.execute(save_username, (username, newusername))
                
                
                mysql.connection.commit()
                
                
                session["username"] = newusername
                
                cursor.close()
                flash("Kullanıcı adı başarıyla güncellendi.", "success")
                
                
                return redirect(url_for("dashboard"))

            

                
                
            else:
                flash("Bu kullanıcı adı zaten kullanılıyor.", "danger")
                return redirect(url_for("editusername", id=id))







        else:
                return render_template("editusername.html", form=form)
    else:
        flash("Erişiminiz yok.", "danger")
        return redirect(url_for("index"))

@app.route("/repo" )
def repo():
    return render_template("repo.html")
@app.route("/searchuser",methods = ["GET","POST"])
@login_required
def find():
    if request.method =="get":
        return redirect(url_for("index"))
    else:
        cursor = mysql.connection.cursor()
        keyword = request.form.get("keyword")
        if not keyword:
            flash("Arama kelimesi giriniz.", "warning")
            return redirect(url_for("index"))

        
        sorgu = "SELECT * FROM users WHERE username LIKE %s"
    
   
        search_pattern = f"%{keyword}%"
    
    
        result = cursor.execute(sorgu, (search_pattern,))
        if result > 0:
            articles = cursor.fetchall()
            return render_template("users.html",articles = articles)
        else:
            flash("uygun sonuç bulunamadı","danger")
            return redirect(url_for("index"))
@login_required
@app.route("/searchpage")
def searchty():
    return render_template("searchpage.html")
@app.route("/sklearn",methods=["POST","GET"])
def learn():
    form = learning(request.form)
    if request.method== "POST" and form.validate():
        cursor = mysql.connection.cursor()
        input = form.prompt.data
        output = form.output.data
        
        sorgu = "insert into model(input,output) values(%s,%s)"
        cursor.execute(sorgu,(input,output))
        mysql.connection.commit()
        cursor.close()
        
        
        return redirect(url_for("learn"))
    else:
        return render_template("learning.html",form=form)

    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_required
@app.route("/upload", methods=["POST"])
def upload():
    image = request.files.get('image')  # get() metoduyla hatayı önleyin
    explain = request.form.get("explain")
   

    if image:
        
        filename = image.filename
        filename=secure_filename(filename)
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        image = Image.open(image.stream)
        target_size = (500,500)
        resized_img = ImageOps.pad(
        image, 
        (500,500), 
        method=Image.Resampling.LANCZOS, 
        
    )
        image = resized_img.convert("RGB")

        image.save(file_path)

        # Flask url_for ile doğru yol
        img_url = url_for("static", filename=f"uploads/{filename}")
        img_html = f'<img src="{img_url}" alt="Yüklenen Resim" loading="lazy">'

        
        cursor = mysql.connection.cursor()
        packet = "select profile from users where username = %s"
        cursor.execute(packet,(session["username"],))
        name = cursor.fetchone()
        name = name["profile"]
        cursor.execute("INSERT INTO images_html (html_code,sender,think,profile) VALUES (%s,%s,%s,%s)", (img_html,session["username"],explain,name))
        mysql.connection.commit()
        cursor.close()
        cache.delete_many('/images')
        return redirect(url_for("images"))

    return "Resim seçilmedi!"
@login_required
@app.route("/testbyupload")
def test():
    return render_template("upload.html")
@login_required
@app.route('/show/<int:id>')
def show(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT html_code FROM images_html WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return row["html_code"] 
    else:
        return "Resim yok"
@login_required
@app.route("/social")
def social():
    return render_template("share.html")
@login_required
@app.route("/chanceprofile")
def chprofile():
    return render_template("changeprofile.html")
@login_required
@app.route("/uploadprofile",methods=["POST"])
def post():
    image = request.files['image']
    

    if image:
        filename = secure_filename(image.filename)
        file_path = os.path.join(UPLOAD_FOLDER1, filename)
        image = Image.open(image.stream)
        target_size = (150,150)
        resized_img = image.resize(target_size, Image.Resampling.LANCZOS)
        if filename.lower().endswith(('.jpg', '.jpeg')):
            
            resized_img.save(file_path, format='JPEG', quality=95)
        
        elif filename.lower().endswith('.png'):
            
            resized_img.save(file_path, format='PNG')
        
        else:
            return "Desteklenmeyen dosya formatı!", 400
        

        # MySQL'e kaydet
        cursor = mysql.connection.cursor()
        profile = "select profile from users where username = %s"
        cursor.execute(profile,(session["username"],))
        name = cursor.fetchone()
        name = name["profile"]
        cursor.execute("update users set profile = %s where username = %s", (filename,session["username"]))
        cursor.execute("update images_html set profile = %s where sender = %s" , (filename,session["username"]))
        sqq = "update tweets set profile =  %s where author = %s"
        cursor.execute(sqq,(filename,session["username"]))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("images"))

    return "Resim seçilmedi!"

@login_required
@app.route("/likeutf/<string:id>")
def likepre(id):
    cursor = mysql.connection.cursor()
    select = "select ıd from users where username = %s"
    cursor.execute(select,(session["username"],))
    id1= cursor.fetchone()
    anot = "select * from images_like where user_id = %s and image_id = %s"
    result = cursor.execute(anot,(id1["ıd"],id))
    if result > 0:
        flash("zaten beğendiniz")
        return redirect(url_for("images"))
    else:
        insert = "update images_html set `like` = `like` + 1 where id = %s"
        cursor.execute(insert,(id,))
        insert2 = "insert into images_like(user_id,image_id) values(%s,%s)"
        cursor.execute(insert2,(id1["ıd"],id))
        mysql.connection.commit()
        flash("beğendiniz")
        return redirect(url_for("images"))
@login_required      
@app.route("/inbox")
def inbox():
    follows = "select * from follow where author = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(follows,(session["username"],))
    follow = cursor.fetchall()
    return render_template("inbox.html", follow=follow)
@login_required
@app.route("/inbox/t/<string:id>")
def inboxt(id):
    cursor = mysql.connection.cursor()
    control = "select follow from follow where author = %s and follow_id = %s"
    result = cursor.execute(control,(session["username"],id))
    if result == 0:
        flash("böyle bir kullanıcıyı takip etmiyorsunuz")
        return redirect(url_for("inbox"))
    
    rog = "select * from follow where author = %s"
    cursor.execute(rog,(session["username"],))
    follow = cursor.fetchall()
    user_username = "select username from users where ıd = %s"
    cursor.execute(user_username,(session["id"],))
    name = cursor.fetchone()
    namet = session["username"]
    
    name = name["username"]
    user_username = "select username from users where ıd = %s"
    cursor.execute(user_username,(id,))
    num = cursor.fetchone()
    num = num["username"]
    
    pro = "select profile from users where ıd = %s"
    cursor.execute(pro,(id,))
    profile = cursor.fetchone()
    profile = profile["profile"]
    
    
    message_list = """
    (SELECT * FROM chat FORCE INDEX (idx_conversation) 
 WHERE recaiver_id = %s AND sender_id = %s)
UNION ALL
(SELECT * FROM chat FORCE INDEX (idx_conversation) 
 WHERE recaiver_id = %s AND sender_id = %s)
ORDER BY time DESC; 
    """
    result = cursor.execute(message_list, (session["id"], id, id, session["id"]))
    
    if result > 0:
        chat = cursor.fetchall()
        
        return render_template("inbox.html",chat = chat,follow = follow,num=num,profile=profile)
    else:
        chat = []
    return render_template("inbox.html",follow=follow,id=id,name = namet,num = num,profile=profile)
@login_required

@app.route('/api/send_message', methods=['POST'])

def send_message():
    saat = time.strftime("%H:%M:%S")[:5]
    data = request.get_json()
    text = data.get('text')
    receiver_name = data.get('receiver_name')
    cursor = mysql.connection.cursor()
    id = "select ıd from users where username = %s"
    cursor.execute(id,(receiver_name,))
    id = cursor.fetchone()
    id = id["ıd"]
    
    sender = session["username"]
    
    
    sender_id = session["id"]


    cursor = mysql.connection.cursor()
    ant = "select profile from users where username = %s"
    cursor.execute(ant,(session["username"],))
    profile = cursor.fetchone()
    profile = profile["profile"]
    
    insert_query = "INSERT INTO chat (sender, recaiver, message,recaiver_id,sender_id,time) VALUES (%s, %s, %s,%s,%s,%s)"
    cursor.execute(insert_query, (sender, receiver_name, text,id,sender_id,saat))
    rapid = "insert into nofications(recaiver,sender,topic,profile) values(%s,%s,%s,%s)"
    cursor.execute(rapid,(receiver_name,session["username"],"mesaj",profile))

    
    mysql.connection.commit()   
    cursor.close()
@login_required
@app.route("/javascript")
def java():
    return render_template("javascript.html")
@login_required
@app.route("/sendlk" , methods = ["POST"])
def sendlk():
    data = request.get_json()
    text = data.get("text")
    print(text)
@login_required
@app.route('/register_google', methods=['POST'])
def register_google():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "Gönderilen veri yok."}), 400
    
    
    google_sub = data.get('google_uid')
    email = data.get('email')
    name = data.get('name')
    nameuser = email.replace("@gmail.com","")
    profile_picture_url = data.get('profile_picture_url')
    sql = "select id from oauth_accounts where google_sub = %s"
    cursor = mysql.connection.cursor(DictCursor)
    result = cursor.execute(sql,(google_sub,))
    if result > 0:
        return jsonify({"success": False, "message": "Gönderilen veri yok."}), 400


    local_profile_url = save_profile_picture(google_sub, profile_picture_url)
    final_profile_url = local_profile_url if local_profile_url else 'static/ret.jpg'

    try:
        


        sql_control = "SELECT ıd FROM users WHERE username = %s"
        result = cursor.execute(sql_control, (nameuser,))
        if result > 0:
            
            return jsonify({"success": False, "message": "Bu kullanıcı adı zaten alınmış."}), 409
        
        
        
        sql_query = "INSERT INTO users (name, email, username, password, date, followers, profile,provider) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        
        
        values = (
            name,                
            email,              
            nameuser,                
            None,          
            datetime.now().year,     
            0,                   
            final_profile_url,
            "google"  
        )
        
        cursor.execute(sql_query, values)
        user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO oauth_accounts (user_id, google_sub, email, email_verified, profile, date)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            user_id,
            google_sub,
            email,
            1,
            final_profile_url,
            datetime.now()
        ))

        
        ssq = "INSERT INTO verification (user, status) VALUES (%s, %s)"
        cursor.execute(ssq, (nameuser, 0))

        
        
        
        
        mysql.connection.commit()
        
        
        session['logged_in'] = True
        session["username"] = nameuser
        session["id"] = user_id
        
        cursor.close()
        
        
        return jsonify({"success": True, "message": "Kayıt başarılı."}), 200
        
    except Exception as e:
        
        print(f"Veritabanı/Kayıt Hatası: {e}")
        
        return jsonify({"success": False, "message": f"Kayıt sırasında bir sunucu hatası oluştu: {e}"}), 500
@login_required

@app.route('/login_google', methods=['POST'])
def login_google():
    
        data = request.get_json()
        google_uid = data.get("google_uid")

        cursor = mysql.connection.cursor()

        sql = """
    SELECT u.ıd, u.username
    FROM users u
    JOIN oauth_accounts g ON g.user_id = u.ıd
    WHERE g.google_sub = %s
    """
        cursor.execute(sql, (google_uid,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "need_register": True}), 404

        session["logged_in"] = True
        session["id"] = user["ıd"]
        session["username"] = user["username"]

        return jsonify({"success": True}), 200
@login_required
@app.route("/verification")
def codec():
    
        return render_template("activate_code.html")
@login_required
@app.route("/initialize",methods=["GET","POST"])
def initialize():
    if request.method == "GET":
        return render_template("index.html")
    else:
        code = request.form.get("activation_code")
        cursor = mysql.connection.cursor()
        sorgu = "select * from codes where code = %s"
        cursor.execute(sorgu,(code,))
        result = cursor.fetchall()
        if result:
            print(session["username"])
            sorgu1 = "update verification set status = %s where user = %s"
            cursor.execute(sorgu1,(1,session["username"]))
            sorgu2 = "delete from codes where code = %s"
            cursor.execute(sorgu2,(code,))
            flash("başarılı")
            sorgu3 = "update images_html set sender = %s where sender = %s"
            verified_name = session["username"] + "<img src='static/verified.svg' alt='resm' class='verifiedd'"
            cursor.execute(sorgu3,(verified_name,session["username"]))

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("index"))
        else:
            flash("kod yanlış")
            return redirect(url_for("index"))


@app.route("/api/begeni-gonder",methods=["POST"])


def jslike():

    cursor = mysql.connection.cursor()
    req = request.get_json()

    image_id = req.get("image_id")


    ctrm = "select * from images_like where user_id = %s and image_id = %s"
    result = cursor.execute(ctrm,(session["id"],image_id))
    if result > 0:
        ss = "delete from images_like where user_id = %s and image_id = %s"
        cursor.execute(ss,(session["id"],image_id))
        sss = "update images_html set `like` = `like` - 1 where id = %s"
        cursor.execute(sss,(image_id,))
        mysql.connection.commit()
        ctr = "select `like` from images_html where id = %s"
        cursor.execute(ctr,(image_id,))
        yeni_like = cursor.fetchone()
        yeni_like = yeni_like["like"]
       
        return jsonify ({"success": True,
                        "yeni_like_sayisi": yeni_like,
                        "like_stat":False
                          }), 200
        



    sorgu = "insert into images_like(user_id,image_id) values(%s,%s)"
    cursor.execute(sorgu,(session["id"],image_id))
    sorgu2 = "update images_html set `like` = `like` + 1 where id = %s"
    cursor.execute(sorgu2,(image_id,))
    mysql.connection.commit()
    ctr = "select `like` from images_html where id = %s"
    cursor.execute(ctr,(image_id,))
    yeni_like = cursor.fetchone()
    yeni_like = yeni_like["like"]
    return jsonify({"success": True,
                    "yeni_like_sayisi": yeni_like,
                     "like_stat":True }), 200



@login_required
@app.route("/terminal")
def terminal():
    
    return render_template("terminal.html")

@app.route("/api/komut", methods=["POST"])
def komut():
    stat= False
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = request.get_json(force=True)  
    command = data.get("command", "")
    if command.startswith("yt-press:"):

        n_comm = command.replace("yt-press:", "")
        email = command[9:].strip()  # "yt-press:" sonrası
        if not validate_email(email):
            return jsonify({"cevap": "err", "message": "Geçersiz email formatı"})

# Email uzunluğunu sınırla
        if len(email) > 100:
            return jsonify({"cevap": "err", "message": "Email çok uzun"})
        special_link = "SELECT link FROM terminal_yt ORDER BY RAND() LIMIT 1"
        cursor = mysql.connection.cursor()
        cursor.execute(special_link)
        link = cursor.fetchone()

        link = link["link"]
        print(link)
        
        gonderilecek_code = link
        hedef_email = n_comm
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = hedef_email
        subject = f"youtube linkin {session.get('username', 'user')}"
        msg["Subject"] = subject[:100]  

# Mesaj gövdesi
        msg.attach(MIMEText(link, "plain"))

# SMTP
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(msg["From"], os.getenv("EMAIL_PASSWORD"))

# Gönder
        s.sendmail(msg["From"], hedef_email, msg.as_string())
        s.quit()
        cursor.close()
        return jsonify({"cevap": "ok_yt"})
    elif command.startswith("rank::"):
        cursor = mysql.connection.cursor()
        sql_inject = "select point from dashboard where author = %s"
        cursor.execute(sql_inject,(session["username"],))
        point = cursor.fetchall()
        ant = "select title from dashboard where author = %s"
        cursor.execute(ant,(session["username"],))
        title = cursor.fetchall()
        titles = []
        for a in title:
            titles.append(a["title"])

        points = []
        for b in point:
            points.append(b["point"])
            cursor.close()
        
        return jsonify({"cevap": "ok_rank","titles":titles,"points":points})
        
    elif command.startswith("send:article:"):
        cursor = mysql.connection.cursor()
        n_comm = command.replace("send:article:", "")
        i = n_comm.find("&")
        article_name = n_comm[:i]
        mail = n_comm[i+1:]
        hedef_email = mail
        

        tit_sql = "select content from dashboard where title = %s"
        cursor.execute(tit_sql,(article_name,))
        repo = cursor.fetchone()
        repo = repo["content"]
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = hedef_email
        msg["Subject"] =    article_name


        msg.attach(MIMEText(repo, "plain"))


        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(msg["From"], os.getenv("EMAIL_PASSWORD"))


        s.sendmail(msg["From"], hedef_email, msg.as_string())
        s.quit()
        cursor.close()

        return jsonify({"cevap":"ok_send"})
    elif command.startswith("create:article&"):
        cursor = mysql.connection.cursor()
        prompt = command.replace("create:article&","")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt + "nasqe000",
            config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction 
        )
        )
        title = response.text
        if title=="security":
            flash("böyle istek oalmaz")
            return jsonify({"cevap": "ok_create"})

        responsem = client.models.generate_content(
            model=model_name,
            contents=prompt + "nasqe123",
            config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction 
        )
        )
        content = responsem.text
        
        insert = "insert into dashboard(title,content,author,point,`like`,view,ai) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert,(title,content,session["username"],0,0,0,1))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"cevap": "ok_create"})
    elif command.startswith("add authication "):
        n_comm = command.replace("add authication ","")
        code = n_comm
        cursor = mysql.connection.cursor()
        
        selection = "select code from codes where code = %s"
        result = cursor.execute(selection,(code,))
        if result == 0:
            cursor.close()
            return jsonify({"cevap": "no_code"})
        else:
            ant = "select status from verification where user = %s"
            cursor.execute(ant,(session["username"],))
            status = cursor.fetchone()
            status = status["status"]
            if status == 1:
                return jsonify({"cevap": "already_auth"})

            insert = "update verification set status = %s where user = %s"
            cursor.execute(insert,(1,session["username"]))
            delete = "delete from codes where code = %s"
            cursor.execute(delete,(code,))
            sorgu3 = "update images_html set sender = %s where sender = %s"
            verified_badge = "<img src='static/verified.svg' alt='verified' class='verifiedd'>"
            
            newn = f"{session['username']} {verified_badge}"
            cursor.execute(sorgu3, (newn, session["username"]))
            mysql.connection.commit()
            cursor.close()
            return jsonify({"cevap": "ok_auth"})
    elif command.startswith("mean::"):

        
        sql = "select point from dashboard where author = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sql,(session["username"],))
        points = cursor.fetchall()
        point_l = []
        for p in points:
            point_l.append(p["point"])
        iter = 0
        top = 0
        for b in point_l:
            iter += 1
            top+=b
        return jsonify({"cevap": "ok_mean","mean":top/iter})
    elif command.startswith("total::"):
        sql = "select point from dashboard where author = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sql,(session["username"],))
        points = cursor.fetchall()
        point_l = []
        for p in points:
            point_l.append(p["point"])
        top = 0
        for b in point_l:
            top+=b
        return jsonify({"cevap": "ok_total","total":top})
    elif command.startswith("help::"):
        help_text="""
        eğer bir yardım istiyorsan social menüsünden yapay zeka asistanına sörabilirsin.
        /gemini /gemini sayfasına yönlendirir."""
        return jsonify({"cevap": "ok_help","help":help_text})
    elif command.startswith("leader::"):
        cursor = mysql.connection.cursor()
        
        




        


        
    
        


        
        
    else:
        return jsonify({"cevap": "err"})


    

    return jsonify({"cevap": f"Komut alındı: {command}"})
@login_required
@app.route("/gemini")
def gemini():
    return render_template("gemini.html")

@login_required
@app.route("/tweet")
def tweet():
    cursor = mysql.connection.cursor()
    sql = "select profile from users where username = %s"
    cursor.execute(sql,(session["username"],))
    pro = cursor.fetchone()
    pro = pro["profile"]
    sql2 = "select * from tweets"
    cursor.execute(sql2)
    all = cursor.fetchall()



    return render_template("tweet.html",pro=pro,all=all)

@app.route("/api/gemini",methods=["POST"])
def gemini_request():
    
    data = request.get_json(force=True)  
    command = data.get("command", "")
    response = client.models.generate_content(
            model=model_name,
            contents=command,
            config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction 
        )
        )
    return jsonify({"response": response.text})

@app.route("/api/tweet",methods = ["POST"])
def tweeting():
    data = request.get_json(force=True)

    tweet = data.get("command","")

    if tweet is None or tweet.strip() == "":
        flash("tweet boş olamaz")
    cursor = mysql.connection.cursor()
    pre_sql = "select profile from users where username = %s"
    cursor.execute(pre_sql,(session["username"],))
    profile = cursor.fetchone()
    profile = profile["profile"]
    send_tweet(session["username"],tweet,0,profile)
    flash("tweet atıldı")
    
    return jsonify({"response":"ok"})

@app.route("/api/like_article",methods=["POST"])
def like_article():
    data = request.get_json(force=True)
    article_id = data.get("article_id","")
    check = "select 1 from likes where user = %s and article = %s"
    cursor = mysql.connection.cursor()
    result = cursor.execute(check,(session["username"],article_id))
    if result>0:
        sorgu = "delete from likes where user = %s and article = %s"
        cursor.execute(sorgu,(session["username"],article_id))
        
        
        
        sorgu1 = "update dashboard set `like` = `like` - 1 where id = %s "
        cursor.execute(sorgu1,(article_id,))
        mysql.connection.commit()
        
        flash("beğeniden çıktınız")
        
        return jsonify({"response":"already_liked"})
    else:
        sorgu = "insert into likes(user,article) values(%s,%s)"
        cursor.execute(sorgu,(session["username"],article_id))
        bask = "select author from dashboard where id = %s"
        cursor.execute(bask,(article_id,))
        author = cursor.fetchone()
        author = author["author"]
        profil = "select profile from users where username = %s"
        cursor.execute(profil,(session["username"],))
        profile = cursor.fetchone()
        profile = profile["profile"]
        sorgu0 = "insert into nofications(recaiver,sender,topic,profile) values(%s,%s,%s,%s)"
        cursor.execute(sorgu0,(author,session["username"],"beğeni",profile))
        sorgu1 = "update dashboard set `like` = `like` + 1 where id = %s "
        cursor.execute(sorgu1,(article_id,))
        mysql.connection.commit()
        cache.delete_many('/articles')
        flash("gönderiyi beğendiniz")
        return jsonify({"response":"liked"})

@app.route("/reset_password",methods=["GET","POST"])
def reset_password():
    if "logged_in" in session:
        flash("Zaten giriş yaptınız.", "info")
        return redirect(url_for("index"))
    form = send_link(request.form)
        
    if request.method == "POST" and form.validate():
        email = form.email.data
        cursor = mysql.connection.cursor()
        control = "select 1 from users where email = %s"
        result = cursor.execute(control,(email,))
        if result == 0:
            flash("Bu e-posta adresi ile kayıtlı bir kullanıcı bulunamadı.", "danger")
            return redirect(url_for('reset_password'))
        control1 = "select provider from users where email = %s"
        result = cursor.execute(control1,(email,))
        if result > 0:
            provider = cursor.fetchone()
            provider = provider["provider"]
            if provider == "google":
                flash("Bu e-posta adresi üçüncü taraf bir sağlayıcı ile ilişkilendirilmiş. Lütfen şifrenizi sağlayıcı üzerinden sıfırlayın.")
                return redirect(url_for('login'))
        token = generate_reset_token(email)
        reset_url = url_for('reset_password_with_token', token=token, _external=True)
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = email
        msg["Subject"] =    "Şifre Sıfırlama Talebi"


        msg.attach(MIMEText(reset_url, "plain"))


        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(msg["From"], os.getenv("EMAIL_PASSWORD"))


        s.sendmail(msg["From"], email, msg.as_string())
        s.quit()
        return redirect(url_for('login'))
        

        
    else:
        return render_template("reset_password.html")
@app.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    email = confirm_reset_token(token)
    
    if not email:
        flash("Bağlantı geçersiz veya süresi dolmuş!")
        return redirect(url_for('login'))
    print(email)
    if request.method == 'POST':
        new_password = request.form.get('password')

        confirm_password = request.form.get('confirm')
        if new_password != confirm_password:
            flash("Şifreler eşleşmiyor.", "danger")
            return redirect(url_for('reset_password_with_token', token=token))
        cursor = mysql.connection.cursor()
        
        
        password = sha256_crypt.hash(new_password)
        update_query = "UPDATE users SET password = %s WHERE email = %s"
        cursor.execute(update_query, (password, email))
        mysql.connection.commit()


        
        flash("Şifreniz başarıyla güncellendi.")
        return redirect(url_for('login'))
    
    return render_template('set_new_password.html')
@app.route("/api/ai_summarize", methods=["POST"])
def ai_summarize():
    data = request.get_json(force=True)  
    
    article_id = data.get('article_id')
    cursor = mysql.connection.cursor()
    select_sql = "SELECT content FROM dashboard WHERE id = %s"
    cursor.execute(select_sql, (article_id,))
    article = cursor.fetchone()
    content = article["content"]

    prompt = f"Bu makaleyi Türkçe olarak kısaca özetle: {content}"
    response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction 
        )
            )
    output = response.text
    return jsonify({"summary": output})
@app.route("/api/speech",methods=["POST"])
def speech():
    data = request.get_json(force=True)
    title = data.get("title","")
    if title.strip("") == "":
        return jsonify({"response":"empty"})
    text = data.get("article_id","")
    if text == "ok":
        tum = listen()
    return jsonify({"response":tum})
    
@app.route("/api/speech_article",methods=["POST"])
def speech_article():
    
    data = request.get_json(force=True)
    article_id = data.get("article_id","")
    cursor = mysql.connection.cursor()
    select_sql = "SELECT content FROM dashboard WHERE id = %s"
    cursor.execute(select_sql, (article_id,))
    article = cursor.fetchone()
    content = article["content"]
    
    if content.strip("") == "":
        return jsonify({"response":"empty"})
    else:
        
        asyncio.run(speak(content))
        return jsonify({"response":"ok"})
    
@app.route("/api/stop_speech",methods=["POST"])
def stop_speech():
    pygame.mixer.music.unload()
    return jsonify({"response":"stopped"})
    
    
    

if __name__ == "__main__":
    app.run(debug=True)