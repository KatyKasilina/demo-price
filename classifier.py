import pickle
import numpy as np
import pandas as pd


CAT_FEATURES = ['neighbourhood_cleansed', 'property_type', 'room_type', 'cancellation_policy',
                'require_guest_phone_verification']
INT_FEATURES = ['accommodates', 'bedrooms', 'beds', 'security_deposit']


class PriceRecomendation(object):
    def __init__(self):
        with open('price_model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        with open('one_hot_encoder.pkl', 'rb') as f:
            self.encoder = pickle.load(f)

    def get_recommended_price(self, data):

        data = self.prepare_data(data)

        try:
            result = np.expm1(self.model.predict(data))
            return np.round(result[0])
        except:
            return "Oops, something went wrong!"


    def prepare_data(self, data):
        cat_df = (self.encoder.transform(data[CAT_FEATURES])).toarray()
        result = pd.concat([data[INT_FEATURES], pd.DataFrame(cat_df)], axis=1, sort=False)

        return result