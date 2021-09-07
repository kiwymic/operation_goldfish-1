import pandas as pd;
import numpy as np;
import plotly.express as px;
import plotly.graph_objs as go;
import pickle;

from dictionaries import *;

from app import app
from app import server

from sklearn.preprocessing import LabelEncoder, StandardScaler;
from sklearn.svm import SVR;

### Pass me a df which is front_end without the sale price (38 columns)
housing = pd.read_csv('./data/ames_housing_price_data_final.csv', index_col = 0);
front_end = housing.drop(["Address", "price_score"], axis = 1);
y = front_end["SalePrice"];

svrg_backend_scaler = StandardScaler();
svr_price_scaler = StandardScaler();
standardized_g = False; # Whether the standard scalar of Gaussian svr is fitted

# Standardize at the beginning.
# Standardizing y
svr_price_scaler.fit(np.array(np.log10(y)).reshape(-1,1));
y_std = svr_price_scaler.transform(np.array(np.log10(y)).reshape(-1,1));

def ftb_flip(fe):
    '''
    Description:
    This is the function which construct the backend data (which directly feeds to CatBoostRegressor)
    given the frontend data. For the svg
    Input:
    fe: The frontend dataframe. Columns must be the same as those in version 6 of the housing data.
    Output: The backend dataframe. Should be ready to "regressor.fit()".
    '''
    global standardized_g;

    #elif method == "svrg":
    be = fe.copy();
    be.drop(columns = ['SalePrice'], axis =1, inplace = True);
    be['ExterQualDisc']=be['ExterQual']-be['OverallQual'];
    be['OverallCondDisc']=be['OverallCond']-be['OverallQual'];
    be['KitchenQualDisc']=be['KitchenQual']-be['OverallQual'];
    be=be.drop(['ExterQual','OverallCond','KitchenQual'],axis=1);

    be = dummify(be, non_dummies, dummies);

    be['GrLivArea_log'] = np.log10(be['GrLivArea']);
    be['LotArea_log'] = np.log10(be['LotArea']);
    be.drop(['GrLivArea', 'LotArea'], axis = 1, inplace = True);

    if not standardized_g:
        be = pd.DataFrame(svrg_backend_scaler.fit_transform(be), columns = be.columns);
        standardized_g = True;
    else:
        be = pd.DataFrame(svrg_backend_scaler.transform(be), columns = be.columns);

    return be;

with open('./data/SVR_model_g.pickle', mode = 'rb') as file:
    svrg = pickle.load(file);
back_end = front_to_back(front_end, "svrg");

def pff_flip(fe):
    '''
    Description:
    Given a frontend data frame, and a string describing a regressor, predicts.
    Input:
    fe: The frontend dataframe. Columns must be the same as those in version 6 of the housing data.
    Output: A pd.Series predicting the output.
    '''
    return 10 ** (svr_price_scaler.inverse_transform\
    (svrg.predict(ftb_flip(fe))));

back_end = front_to_back(front_end, "svrg");
print(svrg.score(back_end, y_std));
