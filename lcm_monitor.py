from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

if __name__ == "__main__":
  # not having host='0.0.0.0' here for network security reason
  # vscode will auto forward ports from remote to local
  app.run(debug=True, port=5002)