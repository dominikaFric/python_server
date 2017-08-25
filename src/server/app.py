from bottle import *
import json, requests,jwt, bottle,canister

app=bottle.default_app()
app.install(canister.Canister())#logger

secret="A)13(*&&qh2#@$!!!qq" #encrypt those tokens

#get the main page
@app.get("/")
def welcome():
    filename="index.html"
    return static_file(filename, root="static")

#cors handling
@hook('after_request')
def allow_cors():
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Access-Control-Allow-Headers']='Origin, Content-Type'

#resources
@app.route("/api/menu-bars",method=(['GET','OPTIONS']))#define routes this way or the hook won't work
def getMenuBar():
    return ({"01":"/img/menubar1.png", 
            "02":"/img/menubar2.png",
            "03":"/img/menubar3.png"})

@app.route("/api/screens",method=(['GET','OPTIONS']))
def getScreens():
    return ({"01":"/img/Home_screen_2.jpg",
            "02":"/img/HS_con_menu_ECG.jpg",
            "03":"/img/HS_con_menu_ECG_curves.jpg",
            "04":"/img/HS_con_menu_ECG_settings.jpg",
            "05":"/img/HS_con_menu_ECG_settings_speed.jpg",
            "mainMenu":"/img/HS_menu_main.jpg",
            "07":"/img/HS_menu_main_therapy.jpg",
            "08":"/img/HS_menu_main_screens.jpg"})

@app.route("/api/menus",method=(['GET','OPTIONS']))
def getMenus():
    return ({"01":"/img/menu_main.png",
           "02":"/img/menu_main_therapy.png",
           "03":"/img/menu_screens.png",
           "04":"/img/Quick_menu_patient_1.jpg",
           "05":"/img/Quick_menu_patient_2.jpg",
           "06":"/img/Quick_settings_1.jpg",
           "07":"/img/Quick_settings_volume_1.1.jpg",
           "08":"/img/Quick_settings_volume_1.2.jpg",
           "09":"/img/Quick_settings_volume_expand_1.jpg"})

#static files
@app.get("/js/<filename>")
def get_js(filename):
    return static_file(filename, root="static/js")

@app.get("/css/<filename>")
def get_css(filename):
    return static_file(filename, root="static/css")

@app.get("/img/<filename>")
def get_image(filename):
    return static_file(filename, root="static/img")

@app.get("/templates/<filename>")
def get_template(filename):
    return static_file(filename, root="static/templates")

#run
if __name__== "__main__" :
    run(host='localhost',server="gunicorn",
    workers=4, port=8088)

"""
#auth example
class Authenticator(object):#public class authenticator extends Object
    def __init__(self,user):
        self.user=user

    def authorize(self,username,password):
        if username ==self.user["username"] and password==self.user["password"]:
            token=jwt.encode({"typ":"potato","username":username},secret,algorithm='HS256')
            self.user["token"]=str(token)
            return self.user
        response.status=401
        return({"response":"you shall not pass"})

    def authenticate(token):
        userInfo=jwt.decode(token,secret,algorithm='HS256')
        if userInfo==self.user:
            return True
        return False

potato={"id":"123",
          "username":"potato",
          "password":"123potato",
          "token":""}#dummy user    

//check token sent by the user
@app.get("/api/greeting")
def returnGreeting():
    data=request.json
    if data!=None:
        if Authenticator.authenticate(data["token"]):
            return({"greeting" : "Hello!"})
    response.status=401
    return({"user":"unauthorized"})

//provide authentication token
@app.post('/api/auth/me')#input json containing usrname and pass
def authenticateUser():
    response.content_type='application/json'
    data=request.json
    r = a.authorize(data["username"],data["password"])
    return(r) 

//how to set up nginx ssl 
-gunicorn and nginx must be installed
-generate openssl cert and key, put them into nginx folder, also put them into project folder
-set certfile="security/nginx.crt" ,keyfile="security/nginx.key" in run method to use them
server {
	listen 80 default_server;
	listen 443 ssl
	server_name http://127.0.0.1:8080;
	ssl_certificate /etc/nginx/ssl/nginx.crt;
	ssl_certificate_key /etc/nginx/ssl/nginx.key;
}

location @proxy_to_app {

	proxy_pass http://127.0.0.1:8080;

}"""