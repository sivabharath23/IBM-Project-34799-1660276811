# from flask import Flask, render_template, redirect, url_for, request
# import requests

# app = Flask(__name__)

# @app.route("/", methods = ['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         arr = []
#         for i in request.form:
#             val = request.form[i]
#             if val == '' and request.form == 'Research':
#                 return redirect(url_for("demo2"))
#             arr.append(float(val))
#         # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
#         result = 0.01
#         return redirect(url_for('chance', percent=result*100))
#     else:
#         return redirect(url_for("demo2"))

# @app.route("/home")
# def demo2():
#     return render_template("demo2.html")

# @app.route("/chance/<percent>")
# def chance(percent):
#     return render_template("chance.html", content=[percent])

# @app.route("/nochance/<percent>")
# def no_chance(percent):
#     return render_template("noChance.html", content=[percent])


# if __name__ == "__main__":
#     app.run()


from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            print(request.form[0])
            if val == '':
                return redirect(url_for("demo2"))
            arr.append(float(val))
        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        arr2 = []
        for i in range(len(arr)):
            if (i < len(arr)):
                arr2[i] = arr[i]
                
        API_KEY = "0_d3yshfsnUx7b0lWqaWqM-d60Jsl9qIoUpDi22b8ZKl"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
            })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr2]
                            }]
                        }

        response_scoring = requests.post(
            'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/d9e58dfd-9f6e-416e-a5bf-51fdb49ebb80/predictions?version=2022-10-20', 
            json=payload_scoring,
            headers=header
        ).json()
        
        result = response_scoring['predictions'][0]['values'][0][0]
        if result[0][0] > 0.5:
            return redirect(url_for('chance', percent=result[0][0]*100))
        else:
            return redirect(url_for('no_chance', percent=result[0][0]*100))
    else:
        return redirect(url_for("demo2"))

@app.route("/home")
def demo2():
    return render_template("demo2.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("demo2"))

if __name__ == "__main__":
    app.run()