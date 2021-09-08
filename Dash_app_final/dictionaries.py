#function and dictionaries required to transform front-end to back-end
import pandas as pd;

def dummify(df, non_dummies, dummies):
    for dummified in dummies:
        for original in non_dummies:
            if original in dummified:
                orig_name = f'{original}_'
                value = dummified.replace(orig_name, '')
                df[dummified] = df[original].map(lambda x: 1 if x == value else 0)
    df=df.drop(non_dummies,axis=1)
    return df

dummies = [
    'Neighborhood_Blueste',
    'Neighborhood_BrDale',
    'Neighborhood_BrkSide',
    'Neighborhood_ClearCr',
    'Neighborhood_CollgCr',
    'Neighborhood_Crawfor',
    'Neighborhood_Edwards',
    'Neighborhood_Gilbert',
    'Neighborhood_Greens',
    'Neighborhood_GrnHill',
    'Neighborhood_IDOTRR',
    'Neighborhood_Landmrk',
    'Neighborhood_MeadowV',
    'Neighborhood_Mitchel',
    'Neighborhood_NAmes',
    'Neighborhood_NPkVill',
    'Neighborhood_NWAmes',
    'Neighborhood_NoRidge',
    'Neighborhood_NridgHt',
    'Neighborhood_OldTown',
    'Neighborhood_SWISU',
    'Neighborhood_Sawyer',
    'Neighborhood_SawyerW',
    'Neighborhood_Somerst',
    'Neighborhood_StoneBr',
    'Neighborhood_Timber',
    'Neighborhood_Veenker',
    'BldgType_2fmCon',
    'BldgType_Duplex',
    'BldgType_Twnhs',
    'BldgType_TwnhsE',
    'MasVnrType_None',
    'MasVnrType_Stone'
    ];

non_dummies=['Neighborhood', 'BldgType', 'MasVnrType'];

dummies_linear = [
    'Neighborhood_Blueste',
    'Neighborhood_BrDale',
    'Neighborhood_BrkSide',
    'Neighborhood_ClearCr',
    'Neighborhood_CollgCr',
    'Neighborhood_Crawfor',
    'Neighborhood_Edwards',
    'Neighborhood_Gilbert',
    'Neighborhood_Greens',
    'Neighborhood_GrnHill',
    'Neighborhood_IDOTRR',
    'Neighborhood_Landmrk',
    'Neighborhood_MeadowV',
    'Neighborhood_Mitchel',
    'Neighborhood_NAmes',
    'Neighborhood_NPkVill',
    'Neighborhood_NWAmes',
    'Neighborhood_NoRidge',
    'Neighborhood_NridgHt',
    'Neighborhood_OldTown',
    'Neighborhood_SWISU',
    'Neighborhood_Sawyer',
    'Neighborhood_SawyerW',
    'Neighborhood_Somerst',
    'Neighborhood_StoneBr',
    'Neighborhood_Timber',
    'Neighborhood_Veenker',
    'BldgType_2fmCon',
    'BldgType_Duplex',
    'BldgType_Twnhs',
    'BldgType_TwnhsE',
    'MasVnrType_None',
    'MasVnrType_Stone',
    'BSMT_HighQual_bin_500-1000',
    'BSMT_HighQual_bin_0-500',
    'BSMT_HighQual_bin_1000-1500',
    'BSMT_HighQual_bin_1500+',
    'BSMT_LowQual_bin_0-500',
    'BSMT_LowQual_bin_500-1000',
    'BSMT_LowQual_bin_1000-1500',
    'BSMT_LowQual_bin_1500+'
    ];


non_dummies_linear = ['Neighborhood', 'BldgType', 'MasVnrType', 'BSMT_HighQual_bin', 'BSMT_LowQual_bin'];

column_title_dict = {
    ### from original dataset
    'GrLivArea' : {"Category": "Continuous", "Description": 'Above-ground living area', "Select":"Major", "Actionable":True, "Range": (300,4400,10)},
    'LotArea' : {"Category": "Continuous", "Description": 'Lot area', "Select":"Major", "Actionable":False},
    'OverallQual' : {"Category": "Ordinal", "Description": 'Overall quality', "Select":"Major", "Actionable":True, "Range":(0,1,1/7)},
    'BSMT_LowQual' : {"Category": "Continuous", "Description": 'Low-quality basement area', "Select":"Major", "Actionable":True, "Range": (0,2400,10)},
    'BSMT_HighQual' : {"Category": "Continuous", "Description": 'High-quality basement area', "Select":"Major", "Actionable":True, "Range": (0,2400,10)},
    'house_age_years' : {"Category": "Continuous", "Description": 'House age in years', "Select":"Major", "Actionable":False},
    'GarageCars' : {"Category": "Discrete", "Description": 'Number of cars held by garage', "Select":"Major", "Actionable":True},
    'MasVnrType' : {"Category": "Nominal", "Description": 'Masonry veneer type', "Select":"Minor", "Actionable":True},
    'FullBath' : {"Category": "Discrete", "Description":'Number of full-bathrooms', "Select":"Major", "Actionable":True},
    'HalfBath' : {"Category": "Discrete", "Description":'Number of half-bathrooms', "Select":"Minor", "Actionable":True},
    'BsmtExposure_ord' : {"Category": "Ordinal", "Description":'Basement exposure', "Select":"Minor", "Actionable":True},
    'Neighborhood' : {"Category": "Nominal", "Description":'Neighborhood', "Select":"Minor", "Actionable":False},
    'BldgType' : {"Category": "Nominal", "Description":'Building type', "Select":"Minor", "Actionable":False},
    'PorchSF' : {"Category": "Continuous", "Description":'Porch area in sq ft', "Select":"Major", "Actionable":True, "Range": (0,1250,5)},
    'ExterQual' : {"Category": "Ordinal", "Description":'Exterior quality score', "Select":"Minor", "Actionable":True},
    'OverallCond' : {"Category": "Ordinal", "Description":'Overall condition score', "Select":"Minor", "Actionable":True},
    'KitchenQual' : {"Category": "Ordinal", "Description":'Kitchen quality score', "Select":"Minor", "Actionable":True},
    'Fireplaces' : {"Category": "Discrete", "Description":'Number of fireplaces', "Select":"Minor", "Actionable":True},
    'Pool' : {"Category": "Discrete", "Description":'Pool', "Select":"Minor", "Actionable":True},
    'BedroomAbvGr' : {"Category": "Discrete", "Description":'Number of bedrooms', "Select":"Major", "Actionable":True},
    # 'ext_Asbestos_Shingles' : {"Category": "Nominal", "Description":'Asbestos used in walls'},

    ### location features
    'graveyard' : {"Category": "Discrete", "Description":'Number graveyards within 1 mile', "Select":"Major", "Actionable":False},
    'police' : {"Category": "Discrete", "Description":'Number of police stations within 1 mile', "Select":"Major", "Actionable":False},
    'optician' : {"Category": "Discrete", "Description":'Number of opticians within 1 mile', "Select":"Major", "Actionable":False},
    'stop' : {"Category": "Discrete", "Description":'Number of stop signs within 1 mile', "Select":"Major", "Actionable":False},
    'slipway' : {"Category": "Discrete", "Description":'Number of slipways within 1 mile', "Select":"Major", "Actionable":False},
    'bar' : {"Category": "Discrete", "Description":'Number of bars within 1 mile', "Select":"Major", "Actionable":False},
    'cinema' : {"Category": "Discrete", "Description":'Number of cinemas within 1 mile', "Select":"Major", "Actionable":False},
    'supermarket' : {"Category": "Discrete", "Description":'Number of supermarkets within 1 mile', "Select":"Major", "Actionable":False},
    'hotel' : {"Category": "Discrete", "Description":'Number of hotels within 1 mile', "Select":"Major", "Actionable":False},
    'farmyard' : {"Category": "Discrete", "Description":'Number of farmyards within 1 mile', "Select":"Major", "Actionable":False},
    'water_tower' : {"Category": "Discrete", "Description":'Number of water towers within 1 mile', "Select":"Major", "Actionable":False},
    'christian_catholic' : {"Category": "Discrete", "Description":'Number of catholic churches within 1 mile', "Select":"Major", "Actionable":False},
    'jewish' : {"Category": "Discrete", "Description":'Number of synagogues within 1 mile', "Select":"Major", "Actionable":False},
    'muslim' : {"Category": "Discrete", "Description":'Number of mosques within 1 mile', "Select":"Major", "Actionable":False},
    'garden_centre' : {"Category": "Discrete", "Description":'Number of garden centers within 1 mile', "Select":"Major", "Actionable":False},
    'christian_lutheran' : {"Category": "Discrete", "Description":'Number of lutheran churches within 1 mile', "Select":"Major", "Actionable":False}
};
