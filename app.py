from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, StackingClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from urllib.parse import urlparse
from datetime import datetime
import ipaddress
import whois
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mysql.connector
from flask import *
import pandas as pd
import requests

app = Flask(__name__)
app.secret_key = 'phishing' 
app.config['UPLOAD_FOLDER'] =r'uploads'
top_doms = pd.read_csv('Dataset/top-1m.csv', header=None)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='phishing'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT email FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email not in email_data_list:
                query = "INSERT INTO users (name, email, password, attempts) VALUES (%s, %s, %s, %s)"
                values = (name, email, password, 3)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email == "admin@gmail.com":
            if password == "admin":
                return redirect("/admin")
            return render_template('login.html', message= "Invalid Password for Admin!!")
        
        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email in email_data_list:
            query = "SELECT password FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password == password__data[0][0]:
                session['user_email'] = email

                return redirect("/home")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/purchase',methods = ["GET", "POST"])
def purchase():
    if request.method == "POST":
        package = request.form['package']
        user_email = session['user_email']

        if package == "package_1":
            values = (10, user_email)
        elif package == "package_2":
            values = (50, user_email)
        elif package == "package_3":
            values = (100, user_email)

        query = "UPDATE users SET attempts = attempts + %s WHERE email = %s"
        executionquery(query, values)
       
        return render_template('purchase.html', message = f"{package} purchased successfully!")
    return render_template('purchase.html')
   

@app.route('/prediction', methods=["POST","GET"])
def prediction():
    if request.method == "POST":
        user_email = session['user_email']
        query = "SELECT attempts FROM users WHERE email = %s"
        values = (user_email,)
        attempts = retrivequery1(query, values)

        if attempts[0][0] <= 0:
            return render_template('prediction.html', message = f"Your attempts are done. Please purchase more attempts!")

        url1 = request.form['url']

        def featureExtraction(url):

            def getDomain(url):
                domain = urlparse(url).netloc
                if re.match(r"^www.", domain):
                    domain = domain.replace("www.", "")
                return domain

            def havingIP(url):
                try:
                    ipaddress.ip_address(url)
                    ip = 1
                except:
                    ip = 0
                return ip

            def haveAtSign(url):
                if "@" in url:
                    at = 1
                else:
                    at = 0
                return at

            def getLength(url):
                if len(url) < 54:
                    length = 0
                else:
                    length = 1
                return length

            def getDepth(url):
                s = urlparse(url).path.split('/')
                depth = 0
                for j in range(len(s)):
                    if len(s[j]) != 0:
                        depth = depth + 1
                return depth

            def redirection(url):
                pos = url.rfind('//')
                if pos > 6:
                    if pos > 7:
                        return 1
                    else:
                        return 0
                else:
                    return 0

            def httpDomain(url):
                domain = urlparse(url).netloc
                if 'https' in domain:
                    return 1
                else:
                    return 0

            shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                                r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                                r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                                r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                                r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                                r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                                r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                                r"tr\.im|link\.zip\.net"

            def tinyURL(url):
                match = re.search(shortening_services, url)
                if match:
                    return 1
                else:
                    return 0

            def prefixSuffix(url):
                if '-' in urlparse(url).netloc:
                    return 1  # phishing
                else:
                    return 0  # legitimate


            def domainAge(domain_name):
                creation_date = domain_name.creation_date
                expiration_date = domain_name.expiration_date
                if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
                    try:
                        creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
                        expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                    except:
                        return 1
                if ((expiration_date is None) or (creation_date is None)):
                    return 1
                elif ((type(expiration_date) is list) or (type(creation_date) is list)):
                    return 1
                else:
                    ageofdomain = abs((expiration_date - creation_date).days)
                    if ((ageofdomain / 30) < 6):
                        age = 1
                    else:
                        age = 0
                return age

            def domainEnd(domain_name):
                expiration_date = domain_name.expiration_date
                if isinstance(expiration_date, str):
                    try:
                        expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                    except:
                        return 1
                if (expiration_date is None):
                    return 1
                elif (type(expiration_date) is list):
                    return 1
                else:
                    today = datetime.now()
                    end = abs((expiration_date - today).days)
                    if ((end / 30) < 6):
                        end = 0
                    else:
                        end = 1
                return end

            def iframe(response):
                if response == "":
                    return 1
                else:
                    if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                        return 0
                    else:
                        return 1

            def mouseOver(response):
                if response == "":
                    return 1
                else:
                    if re.findall("<script>.+onmouseover.+</script>", response.text):
                        return 1
                    else:
                        return 0

            def rightClick(response):
                if response == "":
                    return 1
                else:
                    if re.findall(r"event.button ?== ?2", response.text):
                        return 0
                    else:
                        return 1

            def forwarding(response):
                if response == "":
                    return 1
                else:
                    if len(response.history) <= 2:
                        return 0
                    else:
                        return 1
                    
            features = []
            # Address bar based features (10)
            features.append(getDomain(url))
            features.append(havingIP(url))
            features.append(haveAtSign(url))
            features.append(getLength(url))
            features.append(getDepth(url))
            features.append(redirection(url))
            features.append(httpDomain(url))
            features.append(tinyURL(url))
            features.append(prefixSuffix(url))

            # Domain based features (4)
            dns = 0
            try:
                domain_name = whois.whois(urlparse(url).netloc)
            except:
                dns = 1

            features.append(dns)
            # features.append(web_traffic(url))
            features.append(1 if dns == 1 else domainAge(domain_name))
            features.append(1 if dns == 1 else domainEnd(domain_name))

            # HTML & Javascript based features (4)
            try:
                response = requests.get(url)
            except:
                response = ""

            features.append(iframe(response))
            features.append(mouseOver(response))
            features.append(rightClick(response))
            features.append(forwarding(response))
            # features.append(label)
            return features

        data0 = pd.read_csv('Dataset/url_data_modified.csv')
        data = data0.drop(['Domain','Web_Traffic'], axis=1).copy()
        data = data.sample(frac=1).reset_index(drop=True)
        y = data['Label']
        X = data.drop('Label', axis=1)
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

        forest = RandomForestClassifier(max_depth=5)
        forest.fit(X_train, y_train)


        my_features = featureExtraction(url1)
        prob_of_doms = top_doms[1].values

        if my_features[0] in prob_of_doms:
            query = "UPDATE users SET attempts = attempts - 1 WHERE email = %s"
            values = (user_email,)
            executionquery(query, values)
            return render_template('prediction.html', prediction = 'Legitimate website')
        else:
            pred1 = forest.predict([my_features[1:]])

            if pred1==0:
                prediction="Legitimate website"
            else:
                prediction = "Phishing website"

            query = "UPDATE users SET attempts = attempts - 1 WHERE email = %s"
            values = (user_email,)
            executionquery(query, values)
            return render_template('prediction.html', result = pred1, prediction = prediction)
    return render_template('prediction.html')



@app.route('/review',methods = ["GET", "POST"])
def review():
    if request.method == "POST":
        rating = request.form['rating']
        feedback = request.form['feedback']
        user_email = session['user_email']

        query = "INSERT INTO reviews (email, rating, feedback) VALUES (%s, %s, %s)"
        values = (user_email, rating, feedback)
        executionquery(query, values)
       
        return render_template('review.html', message = "Thank you for your feedback!")
    return render_template('review.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/view_reviews')
def view_reviews():
    query = "SELECT * FROM reviews"
    reviews_data = retrivequery2(query)
    return render_template('view_reviews.html', data = reviews_data)





if __name__ == '__main__':
    app.run(debug=True)




    