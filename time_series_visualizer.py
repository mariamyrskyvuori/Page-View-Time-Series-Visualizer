import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Lue data CSV-tiedostosta
df = pd.read_csv('fcc-forum-pageviews.csv')

# Aseta indeksiksi päivämäärä-sarake ja muunna se datetime-tyypiksi
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Laske kvantiilit
lower_quantile = df['value'].quantile(0.025)
upper_quantile = df['value'].quantile(0.975)

# Suodata data
df = df[(df['value'] >= lower_quantile) & (df['value'] <= upper_quantile)]


def draw_line_plot():
    # Viivakaavio
    df_line = df.copy()
    # Luo kuva ja akseli
    plt.rcParams.update({'font.size': 8}) 
    fig, ax = plt.subplots(figsize=(12, 4))

    # Piirrä viivakaavio
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)

    # Aseta otsikko ja akselien nimet
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # aseta x-akselin tikit 6 kuukauden välein (alkaa jostain syystä kesäkuusta, mallikuvassa heinäkuusta)
    ax.set_xticks(pd.date_range(start=df_line.index.min(), end=df_line.index.max(), freq='6MS'))
    ax.set_xticklabels(pd.date_range(start=df_line.index.min(), end=df_line.index.max(), freq='6MS').strftime('%Y-%m'))

    # Tallenna ja palauta
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Kopioi ja muokkaa data
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Piirrä pylväskaavio
    fig = df_bar.plot(kind='bar', figsize=(10, 6), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    plt.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'])

    # Tallenna ja palauta
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Valmistele data
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #Järjestä kuukaudet
    df_box['month'] = pd.Categorical(df_box['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

    #Luo figuurit ja akselit
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Määritä värit
    year_palette = sns.color_palette("rocket", len(df_box['year'].unique()))
    month_palette = sns.color_palette("rocket", len(df_box['month'].unique()))

    # Piirrä vuositason box plot
    sns.boxplot(x='year', y='value', hue='year', data=df_box, ax=ax1, palette=year_palette)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Piirrä kuukausitason box plot
    sns.boxplot(x='month', y='value', hue='month', data=df_box, ax=ax2, palette=month_palette)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')


    # Tallenna ja palauta
    fig.savefig('box_plot.png')
    return fig
