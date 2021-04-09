## Brazilian E-Commerce Public Dataset by Olist
## Predict Customer Review Scores

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

print('Reading data...')
def prepare_data():
    # Read orders dataset and convert timestamp to date 
    orders = pd.read_csv('data/olist/olist_orders_dataset.csv')
    orders_datetime_columns = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for column in orders_datetime_columns:
        orders[column] = pd.to_datetime(orders[column]).dt.date 
    orders.rename(columns={"order_purchase_timestamp": "order_purchase_date", "order_approved_at": "order_approved_date"}, inplace=True)

    # Read orders_items dataset and calculate number of products/sellers per order
    order_items = pd.read_csv('data/olist/olist_order_items_dataset.csv')
    order_items = order_items.groupby('order_id') \
                              .agg(num_products=('product_id', 'count'), num_sellers=('seller_id', 'count'), total_price=('price', 'sum'),  total_freight=('freight_value', 'sum')) \
                              .reset_index() 
    
    # Read orders_items dataset and calculate number of payments per order
    order_payments = pd.read_csv('data/olist/olist_order_payments_dataset.csv')
    order_payments = order_payments.groupby('order_id') \
                               .agg(num_payment_installments=('payment_installments', 'sum')) \
                               .reset_index() 
    
    # Read order_reviews which has the label - review_score
    order_reviews = pd.read_csv('data/olist/olist_order_reviews_dataset.csv', usecols=["order_id", "review_score"])
    
    df = orders.merge(order_items, how='left') \
               .merge(order_payments, how='left') \
               .merge(order_reviews, how='left') 
    
    return df

df = prepare_data()


#################################################################################
print('Feature engineering...')
features_list = list(df.drop(['order_id', 'customer_id', 'order_status', 'review_score'], axis=1).columns)
X = df[features_list].copy()
Y = df[['order_id', 'customer_id', 'review_score']].copy()

class AttributeSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X[self.attribute_names]

class FeatureEngineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass    
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        df = X.copy()
        
        # Calculate days past since purchase date
        df['days_purchase_to_approved'] = (df.order_approved_date - df.order_purchase_date).dt.days
        df['days_purchase_to_delivered_carrier'] = (df.order_delivered_carrier_date - df.order_purchase_date).dt.days
        df['days_purchase_to_delivered_customer'] = (df.order_delivered_customer_date - df.order_purchase_date).dt.days
        df['days_purchase_to_estimated_delivery'] = (df.order_estimated_delivery_date - df.order_purchase_date).dt.days
        
        # Days from estimated delivery time to actual delivery time. Positive means delivered late.
        df['days_estimated_delivery_to_delivered_customer'] = (df.order_delivered_customer_date - df.order_estimated_delivery_date).dt.days
        df['delivered_early'] = df.order_delivered_customer_date <= df.order_estimated_delivery_date
        
        # Calculate the order freight ratio.
        df['ratio_freight'] = df.total_freight / (df.total_price + df.total_freight)
                 
        # Remove extra columns from the dataset
        cols_to_drop = ['order_purchase_date', 'order_approved_date', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date',                   ]
        df.drop(cols_to_drop , axis=1, inplace=True)
        
        # Fill NA/NaN values with 0
        df.fillna(0, inplace=True)
        
        return df

pipeline = Pipeline([('selector', AttributeSelector(features_list)),
                     ('feature_engineering', FeatureEngineering()),
                     ('std_scaller', StandardScaler())
                    ])
X_prepared = pipeline.fit_transform(X)


#################################################################################
print('Splitting train/test...')
X_train,X_test,y_train,y_test=train_test_split(X_prepared,Y,test_size=0.3,random_state=0)


#################################################################################
print('Model training...')
rf = RandomForestRegressor(random_state = 42)
rf.fit(X_train, y_train['review_score'])


############################################################
print("Generating predictions...")
X_pred = np.round(rf.predict(X_prepared) * 20).astype(int)

orders = pd.read_csv('data/olist/olist_orders_dataset.csv')
order_items = pd.read_csv('data/olist/olist_order_items_dataset.csv')
orders_with_predicted_scors = pd.concat([orders, pd.Series(X_pred)], axis=1)
orders_with_predicted_scors.rename(columns={0: "order_predicted_satisfaction"},inplace=True)
orders_with_predicted_scors = orders_with_predicted_scors.merge(order_items[['order_id', 'seller_id']])

orders_with_predicted_scors.to_csv('data/olist/order_predicted_satisfaction.csv', index=False)
