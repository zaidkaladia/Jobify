from flask import Flask, request
from scrappers import scrape
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "home"
@app.route("/post", methods=["POST"])
def data():
    # naukriDotComData = scrapeNaukriDotCom("web developer", 0, "vadodara")
    # internShalaData = scrapeInternshala("web developer", "vadodara")
    # print(internShalaData)
    # return {naukriDotComData, internShalaData}
    info = json.loads(request.data.decode())
    return scrape(info)

if __name__ == "__main__":
    app.run(debug=True)