from classifier import PriceRecomendation
import pandas as pd

from flask import Flask, render_template, request

FATURES_NAMES = ['accommodates', 'bedrooms', 'beds', 'security_deposit',
                 'neighbourhood_cleansed', 'property_type', 'room_type', 'cancellation_policy',
                 'require_guest_phone_verification']

app = Flask(__name__)


price_rec_model = PriceRecomendation()


@app.route("/", methods=["POST", "GET", 'OPTIONS'])
def index_page(security_deposit=0, prediction_message=""):
    if request.method == "POST":

        accommodates = int(request.form["accommodates"])
        neighbourhood_cleansed = request.form["neighbourhood_cleansed"]

        property_type = request.form["property_type"]
        room_type = request.form["room_type"]
        cancellation_policy = request.form["cancellation_policy"]
        bedrooms = int(request.form["bedrooms"])
        beds = int(request.form["beds"])
        require_guest_phone_verification = request.form["require_guest_phone_verification"]

        security_deposit = request.form["security_deposit"]

        if len(security_deposit) != 0:
            try:
                security_deposit = int(security_deposit)
            except:
                prediction_message = "Error. Deposit value must be integer"
                return render_template('main_page.html', prediction_message=prediction_message)
        else:
            security_deposit = 0

        data_list = [accommodates, bedrooms, beds, security_deposit,
                     neighbourhood_cleansed, property_type, room_type, cancellation_policy,
                     require_guest_phone_verification]

        data = create_df(data_list)

        prediction_message = str(price_rec_model.get_recommended_price(data))

    return render_template('main_page.html', prediction_message=prediction_message)


def create_df(data):
    data = pd.DataFrame([data], columns=FATURES_NAMES)
    return data


if __name__ == "__main__":
    app.run()
