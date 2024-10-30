from flask import Flask, render_template, request
import requests
import socket

app = Flask(__name__)

IPINFO_API_KEY = '10458ae23c689b'

#Home route with the form
@app.route('/')
def index():
    return render_template('index.html')

#Route to handle form submission
@app.route('/lookup', methods=['POST'])
def lookup():
    #Get the input from the form
    domain = request.form['domain']
    
    #getting ip address for a domain
    try:
        ip_address = socket.gethostbyname(domain)
    except socket.gaierror:
        return f"Error: could not resolve Ip address for {domain}"
    
    #calling the ipinfo API to get geolocation information for the domain's ip address
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={IPINFO_API_KEY}')
        data = response.json()
        
        #Get geolocation information
        city = data.get('city')
        region = data.get('region')
        country = data.get('country')
        loc = data.get('loc')
        org = data.get('org')
        timezone = data.get('timezone')
        
        return render_template('result.html', domain=domain, ip_address=ip_address, city=city, region=region, country=country, loc=loc, org=org, timezone=timezone)

    except requests.RequestException as e:
        return f"Error: could not retrieve IP information. Details: {str(e)}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)