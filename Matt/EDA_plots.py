def EDA_plots(df):
    for feature in df.columns:
        if feature != 'SalePrice':
            print(feature)
            scatter = px.scatter(x = df[f'{feature}'], y = df['SalePrice'])
            scatter.update_layout(
                title={
                    'text': f'Scatterplot, {feature} vs SalePrice',
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis_title = f'{feature}',
                yaxis_title = 'SalePrice'
            )
            scatter.show()
            hist = px.histogram(x = df[f'{feature}'])
            hist.update_layout(
                title={
                    'text': f'Distribution of {feature}',
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis_title = f'{feature}',
                yaxis_title = 'Frequency'
            )
            hist.show()
            box = px.box(x = df[f'{feature}'], y = df['SalePrice'])
            box.update_layout(
                title={
                    'text': f'Boxplot, {feature} vs SalePrice',
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis_title = f'{feature}',
                yaxis_title = 'Frequency'
            )
            box.show()
            if type(df.loc[0, f'{feature}']) != str:
                price_corr = df[f'{feature}'].corr(df['SalePrice'])
                print(f'Correlation between {feature} and sale price is {price_corr}')
                temp = df[df[f'{feature}'].isna() == False]
                linreg = stats.linregress(temp[f'{feature}'], temp['SalePrice'] )
                print(linreg)
                linreg.rvalue**2