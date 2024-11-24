def run_Portfolio_Performance_Optimization(language_index):
    import streamlit as st
    import yfinance as yf
    import pandas as pd
    import numpy as np
    import scipy.optimize as sco
    import datetime
    from scipy.optimize import minimize
    import Centred_Title
    import Background_Style

    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)


    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    def get_country_abbr(ticker):
        if ticker in real_estate_germany:
            origin = 'DE'
        elif ticker in real_estate_france:
            origin = 'FR'
        elif ticker in real_estate_spain:
            origin = 'ES'
        elif ticker in real_estate_italy:
            origin = 'IT'
        elif ticker in real_estate_netherlands:
            origin = 'NL'
        elif ticker in real_estate_sweden:
            origin = 'SE'
        elif ticker in real_estate_belgium:
            origin = 'BE'
        elif ticker in real_estate_switzerland:
            origin = 'CH'
        elif ticker in real_estate_uk:
            origin = 'GB'
        elif ticker in real_estate_turkey:
            origin = 'TR'
        elif ticker in real_estate_usa:
            origin = 'US'
        elif ticker in real_estate_canada:
            origin = 'CA'
        elif ticker in real_estate_australia:
            origin = 'AU'
        elif ticker in real_estate_japan:
            origin = 'JP'
        elif ticker in real_estate_china:
            origin = 'CN'
        else:
            origin = 'Empty'
        return origin

    def make_metric(ticker, weight, tickers_count,market_caps,origin):
        distributed_weight = 1 / tickers_count

        try:

            market_cap = float(market_caps[market_caps['Ticker']==ticker]['Market Cap'])

        except:
            market_cap = 0
        # st.write(market_cap)

        # Zahl formatieren

        if market_cap >= (1000_000_000_000):  # Billionen
            market_cap = f"{market_cap / 1000_000_000_000:.2f} Bn"

        elif market_cap >= 1_000_000_000:  # Milliarden
            market_cap = f"{market_cap / 1_000_000_000:.2f} Md"


        elif market_cap >= 1_000_000:  # Millionen
            market_cap = f"{market_cap / 1_000_000:.2f} Mio"

        elif market_cap >= 1_000:  # Tausend
            market_cap = f"{market_cap / 1_000:.2f} Tsd"


        else:  # Weniger als Tausend
            market_cap = f"{market_cap:.2f}"


        #st.write(market_cap)



        weight = weight * 100
        distributed_weight = distributed_weight * 100


        # Path to your local SVG file
        svg_path = f'Images/Countries Flags/{origin}.svg'

        import urllib.parse

        # Read the SVG content
        with open(svg_path, 'r') as file:
            svg_content = file.read()

        # Encode the content to escape special characters
        svg_encoded = urllib.parse.quote(svg_content)

        if weight > distributed_weight:

            st.markdown(
                f"""
                <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                     <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                         {ticker}
                         <img src='data:image/svg+xml;utf8,{svg_encoded}' alt='SVG Image' style='width: 20px; height: 20px; vertical-align: middle;'/>
                     </h1>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'>
                        <span style='color:green; '>
                        <span style='color:green; '>↑ ‎ </span>
                        {weight:.1f} %
                        </span>
                    </h1>
                    <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{market_cap}</h1>
                </div>
                """, unsafe_allow_html=True
            )
        elif weight == distributed_weight:

            st.markdown(
                f"""
                            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                                 <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                                     {ticker}
                                     <img src='data:image/svg+xml;utf8,{svg_encoded}' alt='SVG Image' style='width: 20px; height: 20px; vertical-align: middle;'/>
                                 </h1>
                                <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'>
                                    <span style='color:#FFDF00; '>
                                    <span style='color:#FFDF00; '>↔  ‎ </span>
                                    {weight:.1f} %
                                    </span>
                                </h1>
                                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{market_cap}</h1>
                            </div>
                            """, unsafe_allow_html=True
            )


        else:

            st.markdown(
                f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                     {ticker}
                     <img src='data:image/svg+xml;utf8,{svg_encoded}' alt='SVG Image' style='width: 20px; height: 20px; vertical-align: middle;'/>
                 </h1>
                <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:red; '>
                    <span style='color:red; '>↓  ‎ </span>
                    {weight:.1f} %
                    </span>
                </h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{market_cap}</h1>
            </div>
            """, unsafe_allow_html=True
            )
        st.write('')
        st.write('')


    def calculate_performance_optimization(data,selected_optimization_method,market_caps=None):


        try:
            if selected_optimization_method == 'Mean-Variance Optimization':
                method_name, weights_df = mean_variance_optimization(data)

            if selected_optimization_method == 'Minimum Variance Portfolio':
                method_name, weights_df = minimum_variance_portfolio(data)

            if selected_optimization_method == 'Maximum Sharpe Ratio Portfolio':
                method_name, weights_df = maximum_sharpe_ratio(data)

            if selected_optimization_method == 'Equal Weight Portfolio':
                method_name, weights_df = equal_weight_portfolio(data)

            if selected_optimization_method == 'Risk Parity Portfolio':
                method_name, weights_df = risk_parity_portfolio(data)

            if selected_optimization_method == 'Inverse Variance Portfolio':
                method_name, weights_df = inverse_variance_portfolio(data)

            if selected_optimization_method == 'Maximum Diversification Portfolio':
                method_name, weights_df = maximum_diversification_portfolio(data)


            if selected_optimization_method == 'Maximum Decorrelation Portfolio':
                method_name, weights_df = maximum_decorrelation_portfolio(data)

            if selected_optimization_method == 'Black-Litterman Model Portfolio':
                method_name, weights_df = black_litterman_portfolio(data,market_caps)

            if selected_optimization_method == 'Hierarchical Risk Parity Portfolio':
                method_name, weights_df = hierarchical_risk_parity_portfolio(data)


        except Exception as e:
            method_name, weights_df = '',pd.DataFrame(columns=['Ticker','Weight'])


        return method_name, weights_df

    def create_pie_chart(data):
        import plotly.express as px


        # Erstellen des Kreisdiagramms mit Plotly
        fig = px.pie(data, values='Weight', names='Ticker',
                     title='Verteilung der Ticker-Gewichte',
                     color_discrete_sequence=px.colors.sequential.RdBu,
                     hole=0.3)  # Optional für einen Donut-Style

        # Layout des Diagramms anpassen (Titel zentrieren)
        fig.update_layout(
            height=600,  # Höhe des Diagramms
            title={
                'text': 'Verteilung der Ticker-Gewichte',
                'x': 0.5,  # Zentrieren des Titels (x=0.5 bedeutet mittig)
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font_size=24,  # Titelgröße
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),
            margin=dict(l=50, r=50, t=100, b=50)  # Ränder anpassen
        )

        # Darstellung des Diagramms mit Streamlit
        st.plotly_chart(fig,use_container_width=True)


    def create_line_chart(data):
        import plotly.express as px
        import plotly.graph_objects as go
        import pandas as pd
        import streamlit as st


        data_selected_date_from_to = pd.DataFrame(data)

        # Layout und Grunddiagramm erstellen
        fig = go.Figure()

        # Schleife über alle Spalten außer 'date'
        for col in data_selected_date_from_to.columns:
            if col != 'Date':
                fig.add_trace(
                    go.Scatter(
                        x=data_selected_date_from_to['Date'],
                        y=data_selected_date_from_to[col],
                        mode='lines',
                        name=col
                    )
                )

        # Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'Fonds-Kurse',  # Titeltext
                x=0.5,  # Zentriert den Titel
                xanchor='center',  # Verankert den Titel in der Mitte
                font=dict(size=25)  # Schriftgröße des Titels
            )
        )

        # Achsenfarben anpassen
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)

    # Daten abrufen
    st.cache
    def portfolio_performacne_fetch_data(tickers, start_date, end_date):
        try:
            selected_ticker_dummy = tickers
            selected_tickers = []
            for ticker in tickers:
                selected_tickers.append(str(ticker).upper())


            data = yf.download(selected_tickers,
                               start=start_date,
                               end=end_date,
                               interval='1d')['Adj Close']

            return data
        except:
            st.warning('Bitte andere Daten wählen')
            data = pd.DataFrame({'Date':[None],
                                 'None1':[None],
                                 'None2':[None]})

            return data

    import yfinance as yf
    import pandas as pd

    # Holt die Marktkapitalisierungen (Market Cap) für Fonds oder Unternehmen.
    def get_market_caps_funds(tickers):

        market_caps = {}
        for ticker in tickers:
            try:
                fund = yf.Ticker(ticker)
                info = fund.info

                # Versuche, 'marketCap' direkt zu holen
                market_cap = info.get("marketCap")

                # Falls 'marketCap' nicht verfügbar, versuche alternative Felder
                if not market_cap:
                    # Schätzung basierend auf Schlusskurs und einem angenommenen Wert für Aktienanzahl
                    price = info.get("regularMarketPreviousClose")
                    shares_outstanding = info.get("sharesOutstanding")  # Prüfen, ob verfügbar
                    if price and shares_outstanding:
                        market_cap = price * shares_outstanding

                market_caps[ticker] = market_cap if market_cap else None  # None, falls keine Daten verfügbar
            except Exception as e:
                print(f"Fehler bei {ticker}: {e}")
                market_caps[ticker] = None

        # Rückgabe als DataFrame
        return pd.DataFrame(list(market_caps.items()), columns=["Ticker", "Market Cap"])

    # Mean-Variance Optimization
    def mean_variance_optimization(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        avg_returns = returns.mean()
        num_assets = len(avg_returns)

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        bounds = [(0, 1) for _ in range(num_assets)]
        initial_weights = np.array([1 / num_assets] * num_assets)

        result = minimize(portfolio_volatility, initial_weights, bounds=bounds, constraints=constraints)
        weights = result.x
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Mean-Variance Optimization", weight_df


    # Minimum Variance Portfolio
    def minimum_variance_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        num_assets = len(cov_matrix)

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        bounds = [(0, 1) for _ in range(num_assets)]
        initial_weights = np.array([1 / num_assets] * num_assets)

        result = minimize(portfolio_volatility, initial_weights, bounds=bounds, constraints=constraints)
        weights = result.x
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Minimum Variance Portfolio", weight_df

    # Maximum Sharpe Ratio Portfolio
    def maximum_sharpe_ratio(df, risk_free_rate=0.01):
        # Berechnung der täglichen Renditen
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        avg_returns = returns.mean()
        num_assets = len(avg_returns)

        # Zielfunktion: Negative Sharpe Ratio
        def negative_sharpe_ratio(weights):
            portfolio_return = np.dot(weights, avg_returns)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return -(portfolio_return - risk_free_rate) / portfolio_volatility

        # Constraints: Summe der Gewichte = 1
        constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}]

        # Zusatz: Mindestgewicht für Diversifikation
        min_weight = 0  # Mindestens 5% Gewicht pro Asset
        max_weight = 1  # Maximal 50% Gewicht pro Asset
        bounds = [(min_weight, max_weight) for _ in range(num_assets)]

        # Startwerte: Gleichgewichtetes Portfolio
        initial_weights = np.array([1 / num_assets] * num_assets)

        # Optimierung
        result = minimize(
            negative_sharpe_ratio,
            initial_weights,
            bounds=bounds,
            constraints=constraints
        )

        # Überprüfung, ob die Optimierung erfolgreich war
        if not result.success:
            raise ValueError("Die Optimierung ist fehlgeschlagen: " + result.message)

        # Ergebnis: Gewichte der Assets
        weights = result.x

        # Ausgabe als DataFrame
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Maximum Sharpe Ratio Portfolio", weight_df

    # Equal Weight Portfolio
    def equal_weight_portfolio(df):
        num_assets = len(df.columns) - 1
        weights = np.full(num_assets, 1 / num_assets)
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Equal Weight Portfolio", weight_df


    # Risk Parity Portfolio
    def risk_parity_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        inv_volatility = 1 / np.sqrt(np.diag(cov_matrix))
        weights = inv_volatility / np.sum(inv_volatility)
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Risk Parity Portfolio", weight_df

    # Inverse Variance Portfolio
    def inverse_variance_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        variances = returns.var()
        weights = 1 / variances
        weights /= weights.sum()
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Inverse Variance Portfolio", weight_df


    # Maximum Diversification Portfolio
    def maximum_diversification_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        avg_returns = returns.mean()
        diversifications = np.abs(avg_returns) / np.sqrt(np.diag(cov_matrix))
        weights = diversifications / diversifications.sum()
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Maximum Diversification Portfolio", weight_df



    # Maximum Decorrelation Portfolio
    def maximum_decorrelation_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        corr_matrix = returns.corr()
        inv_correlation = 1 / np.abs(corr_matrix).sum()
        weights = inv_correlation / inv_correlation.sum()
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Maximum Decorrelation Portfolio", weight_df


    # Black-Litterman Model Portfolio
    def black_litterman_portfolio(df, market_capitalizations, tau=0.025):
        # Berechnung der historischen Renditen (Änderungen über die Zeit für jede Spalte außer Datum)
        returns = df.iloc[:, 1:].pct_change().dropna()
        avg_returns = returns.mean()

        # Sicherstellen, dass die Ticker aus 'df' und 'market_capitalizations' übereinstimmen
        tickers = df.columns[1:]
        market_capitalizations = market_capitalizations.set_index('Ticker')

        # Überprüfen, ob die Tickers in beiden DataFrames übereinstimmen und ordnen
        market_caps = market_capitalizations.reindex(tickers)['Market Cap']

        # Fehlende Werte abfangen
        if market_caps.isnull().any():
            missing_tickers = market_caps[market_caps.isnull()].index.tolist()
            raise ValueError(f"Marktkapitalisierungen fehlen für folgende Ticker: {missing_tickers}")

        # Normalisierung der Gewichte aus den Marktkapitalisierungen
        weights = market_caps.values / market_caps.sum()

        # Black-Litterman-Anpassung der erwarteten Renditen
        adjusted_returns = tau * avg_returns + (1 - tau) * weights
        weights = adjusted_returns / adjusted_returns.sum()

        # Ausgabe der Gewichtungen als DataFrame
        weight_df = pd.DataFrame({'Ticker': tickers, 'Weight': weights})

        return "Black-Litterman Model Portfolio", weight_df


    #Hierarchical Risk Parity (HRP) Portfolio
    def hierarchical_risk_parity_portfolio(df):
        from scipy.cluster.hierarchy import linkage, fcluster
        returns = df.iloc[:, 1:].pct_change().dropna()
        corr_matrix = returns.corr()
        distances = np.sqrt((1 - corr_matrix) / 2)
        clusters = linkage(distances, method='ward')
        tickers = df.columns[1:]
        cluster_assignments = fcluster(clusters, t=1.5, criterion='distance')
        unique_clusters = np.unique(cluster_assignments)
        weights = np.zeros(len(tickers))
        for cluster in unique_clusters:
            cluster_indices = np.where(cluster_assignments == cluster)[0]
            equal_weight = 1 / len(cluster_indices)
            weights[cluster_indices] = equal_weight
        weights /= weights.sum()
        weight_df = pd.DataFrame({'Ticker': tickers, 'Weight': weights})

        return "Hierarchical Risk Parity Portfolio", weight_df

    # Logo sidebar
    st.sidebar.image("Images/RB Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)


    # Market auswählen
    markt_options = ['Deutschland', 'Andere EU-Länder', 'USA', 'China', 'Japan', 'Kanada', 'Australien']
    # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
    selected_market = st.sidebar.selectbox("Markt auswählen:",
                                           options=markt_options,
                                           index=0,
                                           key='selected_market'

                                           )

    selected_ticker_col, selected_interval_col = st.sidebar.columns(2)

    with selected_ticker_col:
        # Fonds Immboilien
        ## Deutschland
        real_estate_germany = [
            "VNA.DE",  # Vonovia SE
            "LEG.DE",  # LEG Immobilien SE
            "TEG.DE",  # TAG Immobilien AG
            "DWNI.DE",  # Deutsche Wohnen SE
            "AT1.DE",  # Aroundtown SA
            "GYC.DE",  # Grand City Properties S.A.
            "AOX.DE",  # alstria office REIT-AG
            "DEQ.DE",  # Deutsche EuroShop AG
            "WCMK.DE",  # WCM Beteiligungs- und Grundbesitz-AG (Teil von TLG)
            "PBB.DE",  # Deutsche Pfandbriefbank AG (Immobilienfinanzierung)
            "HAU.DE"  # HAUCK AUFHAEUSER Investment (Immobilien verwaltet)

        ]
        big_two_tickers_real_estate_fonds_germany = [
            "VNA.DE",  # Vonovia SE
            "LEG.DE",  # LEG Immobilien SE

        ]

        # Frankreich
        real_estate_france = [
            "LI.PA",  # Klepierre
            "ICAD.PA",  # Icade
            "CARM.PA",  # Carmila
        ]

        # Spanien
        real_estate_spain = [
            "COL.MC",  # Colonial
        ]

        # Italien
        real_estate_italy = [
            "IGD.MI",  # Immobiliare Grande Distribuzione
            "BAMI.MI",  # Banca Mediolanum (enthält Immobilieninvestments)
        ]

        # Niederlande
        real_estate_netherlands = [
            "WDP.BR",  # Warehouses De Pauw
            "VASTN.AS",  # Vastned Retail
        ]

        # Schweden
        real_estate_sweden = [
            "WIHL.ST",  # Wihlborgs Fastigheter AB
            "FABG.ST",  # Fabege AB
        ]

        # Belgien
        real_estate_belgium = [
            "COFB.BR",  # Cofinimmo
            "AED.BR",  # Aedifica
            "XIOR.BR",  # Xior Student Housing
        ]

        # Schweiz
        real_estate_switzerland = [
            "SPSN.SW",  # Swiss Prime Site
            "HIAG.SW",  # HIAG Immobilien
            "PSPN.SW",  # PSP Swiss Property AG
        ]

        # Großbritannien
        real_estate_uk = [
            "LAND.L",  # Land Securities Group
            "BLND.L",  # British Land
            "SGRO.L",  # Segro PLC
            "UTG.L",  # Unite Group
            "DLN.L",  # Derwent London
            "PHP.L",  # Primary Health Properties
            "SAFE.L",  # Safestore Holdings
            "BYG.L",  # Big Yellow Group
            "GR1T.L",  # Grit Real Estate Income Group
            "WKP.L",  # Workspace Group PLC
            "RGL.L",  # Regional REIT Limited
            "AIRE.L",  # Alternative Income REIT
            "BBOX.L",  # Tritax EuroBox
            "HMSO.L",  # Hammerson PLC
        ]

        real_estate_turkey = [
            "ISGYO.IS",  # İş Gayrimenkul Yatırım Ortaklığı A.Ş. (Is REIT)
            "HLGYO.IS",  # Halk Gayrimenkul Yatırım Ortaklığı A.Ş. (Halk REIT)
            "AKSGY.IS",  # Akasya Gayrimenkul Yatırım Ortaklığı A.Ş.
            "SNGYO.IS",  # Sinpaş Gayrimenkul Yatırım Ortaklığı A.Ş.
            "TRGYO.IS",  # Torunlar Gayrimenkul Yatırım Ortaklığı A.Ş.
            "KLGYO.IS",  # Kiler Gayrimenkul Yatırım Ortaklığı A.Ş.
            "OZKGY.IS",  # Özak Gayrimenkul Yatırım Ortaklığı A.Ş.
            "ALKIM.IS",  # Alkim Gayrimenkul Yatırım Ortaklığı A.Ş.
            "VKGYO.IS",  # Vakıf Gayrimenkul Yatırım Ortaklığı A.Ş.
            "METRO.IS",  # Metro Gayrimenkul Yatırım Ortaklığı A.Ş.
            "DGGYO.IS",  # Doğuş Gayrimenkul Yatırım Ortaklığı A.Ş.
            "MRGYO.IS",  # Martı Gayrimenkul Yatırım Ortaklığı A.Ş.
            "EUKYO.IS",  # Euromenkul Yatırım Ortaklığı A.Ş.
        ]

        real_estate_fonds_europe = (
                real_estate_uk +
                real_estate_france +
                real_estate_spain +
                real_estate_italy +
                real_estate_netherlands +
                real_estate_sweden +
                real_estate_belgium +
                real_estate_switzerland +
                real_estate_turkey
        )

        big_two_tickers_real_estate_fonds_europe = [
            "LAND.L",  # Land Securities Group
            "BLND.L",  # British Land
        ]

        real_estate_china = [
            "1109.HK",  # China Resources Land
            "1997.HK",  # Wharf Holdings
            "3380.HK",  # Logan Group Company
            "3883.HK",  # China Aoyuan
            "3301.HK",  # Ronshine China Holdings
            "1813.HK",  # KWG Group Holdings
            "1777.HK",  # Fantasia Holdings Group
            "2777.HK",  # Guangzhou R&F Properties
            "3900.HK",  # Greentown China
            "1238.HK",  # Powerlong Real Estate
        ]

        big_two_tickers_real_estate_fonds_china = [
            "1109.HK",  # China Resources Land
            "1997.HK",  # Wharf Holdings

        ]

        real_estate_japan = [
            "3289.T",  # Mitsui Fudosan Logistics Park
            "8801.T",  # Mitsui Fudosan Co.
            "8802.T",  # Mitsubishi Estate
            "8804.T",  # Tokyo Tatemono Co.
            "3288.T",  # Advance Residence Investment Corporation
            "8952.T",  # Japan Real Estate Investment Corporation
            "8960.T",  # United Urban Investment Corporation
            "3279.T",  # Activia Properties Inc.
            "3281.T",  # GLP J-REIT
            "3292.T",  # AEON REIT Investment Corporation
            "8953.T",  # Japan Retail Fund Investment Corporation
            "3283.T",  # NIPPON REIT Investment Corporation
            "8951.T",  # Nippon Building Fund Inc.
            "8984.T",  # Daiwa House REIT Investment
            "8976.T",  # Daiwa Office Investment Corporation
            "3295.T",  # Hulic Reit
            "3278.T",  # Kenedix Residential Next Investment Corporation
            "3269.T",  # Sekisui House REIT
            "8963.T"  # Invincible Investment Corporation
        ]

        big_two_tickers_real_estate_fonds_japan = [
            "3289.T",  # Mitsui Fudosan Logistics Park
            "8801.T",  # Mitsui Fudosan Co.

        ]

        real_estate_australia = [
            "SGP.AX",  # Stockland
            "GPT.AX",  # GPT Group
            "CQR.AX",  # Charter Hall Retail REIT
            "GOZ.AX",  # Growthpoint Properties Australia
            "DXS.AX",  # Dexus
            "VCX.AX",  # Vicinity Centres
            "SCG.AX",  # Scentre Group
            "CHC.AX",  # Charter Hall Group
            "CLW.AX",  # Charter Hall Long WALE REIT
            "ARF.AX",  # Arena REIT
            "NSR.AX",  # National Storage REIT
            "INA.AX",  # Ingenia Communities Group
            "BWP.AX",  # BWP Trust
            "CIP.AX",  # Centuria Industrial REIT
            "CMW.AX",  # Cromwell Property Group
            "RFF.AX",  # Rural Funds Group
            "IOF.AX",  # Investa Office Fund
            "MGR.AX",  # Mirvac Group
        ]

        big_two_tickers_real_estate_fonds_australia = [
            "SGP.AX",  # Stockland
            "GPT.AX",  # GPT Group

        ]

        real_estate_canada = [
            "REI-UN.TO",  # RioCan Real Estate Investment Trust
            "CAR-UN.TO",  # Canadian Apartment Properties REIT
            "GRT-UN.TO",  # Granite Real Estate Investment Trust
            "SRU-UN.TO",  # SmartCentres Real Estate Investment Trust
            "DIR-UN.TO",  # Dream Industrial Real Estate Investment Trust
            "HR-UN.TO",  # H&R Real Estate Investment Trust
            "BEI-UN.TO",  # Boardwalk Real Estate Investment Trust
            "AP-UN.TO",  # Allied Properties Real Estate Investment Trust
            "CHP-UN.TO",  # Choice Properties REIT
            "CRR-UN.TO",  # Crombie Real Estate Investment Trust
            "IIP-UN.TO",  # InterRent Real Estate Investment Trust
            "MEQ.TO",  # Mainstreet Equity Corp
            "NWH-UN.TO",  # NorthWest Healthcare Properties REIT
            "MRC.TO",  # Morguard Real Estate Investment Trust
            "PRV-UN.TO",  # Pro Real Estate Investment Trust
            "AX-UN.TO"  # Artis REIT
        ]
        big_two_tickers_real_estate_fonds_canada = [
            "REI-UN.TO",  # RioCan Real Estate Investment Trust
            "CAR-UN.TO",  # Canadian Apartment Properties REIT

        ]

        real_estate_usa = [
            "AMT",  # American Tower Corp.
            "PLD",  # Prologis Inc.
            "CCI",  # Crown Castle International
            "SPG",  # Simon Property Group
            "EQIX",  # Equinix Inc.
            "PSA",  # Public Storage
            "O",  # Realty Income Corp.
            "WELL",  # Welltower Inc.
            "VTR",  # Ventas Inc.
            "AVB",  # AvalonBay Communities
            "EQR",  # Equity Residential
            "ESS",  # Essex Property Trust
            "MAA",  # Mid-America Apartment Communities
            "DLR",  # Digital Realty Trust
            "EXR",  # Extra Space Storage
            "ARE",  # Alexandria Real Estate Equities
            "UDR",  # UDR Inc.
            "HST",  # Host Hotels & Resorts
            "BXP",  # Boston Properties
            "SUI",  # Sun Communities
            "INVH",  # Invitation Homes
            "IRM",  # Iron Mountain Inc.
            "CPT",  # Camden Property Trust
            "GLPI",  # Gaming and Leisure Properties
            "EPR",  # EPR Properties
            "VICI",  # VICI Properties
            "WY",  # Weyerhaeuser Co.
            "REG",  # Regency Centers Corp.
            "KIM",  # Kimco Realty
            "FRT",  # Federal Realty Investment Trust
            "NNN",  # National Retail Properties
            "SLG",  # SL Green Realty Corp.
            "HPP",  # Hudson Pacific Properties
            "RHP",  # Ryman Hospitality Properties
            "SBRA",  # Sabra Health Care REIT
            "LXP",  # LXP Industrial Trust
            "MPW",  # Medical Properties Trust
            "BRX",  # Brixmor Property Group
            "COLD",  # Americold Realty Trust
            "CHCT",  # Community Healthcare Trust
            "PINE",  # Alpine Income Property Trust
            "GOOD",  # Gladstone Commercial Corp.
            "HIW",  # Highwoods Properties
            "ABR",  # Arbor Realty Trust
            "SAFE"  # Safehold Inc.
        ]

        big_two_tickers_real_estate_fonds_usa= [
            "AMT",  # American Tower Corp.
            "PLD",  # Prologis Inc.

        ]




    # Mehrfachauswahl für Ticker (Deutschland)
    tickers_portfolio_performance_optimization_germany = st.sidebar.multiselect('Deutsche Tickers (mind. 1 auswählen):',
                                                                               options=real_estate_germany,
                                                                               key='tickers_portfolio_performance_optimization_germany',
                                                                               default=big_two_tickers_real_estate_fonds_germany)

    # Mehrfachauswahl für Ticker (EU)
    tickers_portfolio_performance_optimization_europe = st.sidebar.multiselect('Europ. Tickers (mind. 1 auswählen):',
                                                                        options=real_estate_fonds_europe,
                                                                        key='tickers_portfolio_performance_optimization_europe',
                                                                        default=big_two_tickers_real_estate_fonds_europe)

    # Mehrfachauswahl für Ticker (China)
    tickers_portfolio_performance_optimization_china = st.sidebar.multiselect('Chines. Tickers (mind. 1 auswählen):',
                                                                               options=real_estate_china,
                                                                               key='tickers_portfolio_performance_optimization_china',
                                                                               default=big_two_tickers_real_estate_fonds_china)

    # Mehrfachauswahl für Ticker (Japan)
    tickers_portfolio_performance_optimization_japan = st.sidebar.multiselect('Japan. Tickers (mind. 1 auswählen):',
                                                                              options=real_estate_japan,
                                                                              key='tickers_portfolio_performance_optimization_japan',
                                                                              default=big_two_tickers_real_estate_fonds_japan)

    # Mehrfachauswahl für Ticker (Australien)
    tickers_portfolio_performance_optimization_australia = st.sidebar.multiselect('Austr. Tickers (mind. 1 auswählen):',
                                                                              options=real_estate_australia,
                                                                              key='tickers_portfolio_performance_optimization_australia',
                                                                              default=big_two_tickers_real_estate_fonds_australia)

    # Mehrfachauswahl für Ticker (Kanada)
    tickers_portfolio_performance_optimization_canada = st.sidebar.multiselect('Kanad. Tickers (mind. 1 auswählen):',
                                                                                  options=real_estate_canada,
                                                                                  key='tickers_portfolio_performance_optimization_canada',
                                                                                  default=big_two_tickers_real_estate_fonds_canada)

    # Mehrfachauswahl für Ticker (USA)
    tickers_portfolio_performance_optimization_usa = st.sidebar.multiselect('US-Amer. Tickers (mind. 1 auswählen):',
                                                                                options=real_estate_usa,
                                                                                key='tickers_portfolio_performance_optimization_usa',
                                                                                default=big_two_tickers_real_estate_fonds_usa)

    tickers_portfolio_performance_optimization = tickers_portfolio_performance_optimization_germany + tickers_portfolio_performance_optimization_europe + tickers_portfolio_performance_optimization_usa + tickers_portfolio_performance_optimization_china + tickers_portfolio_performance_optimization_japan + tickers_portfolio_performance_optimization_canada + tickers_portfolio_performance_optimization_australia












    #st.write(market_caps)
    performance_optimization_date_from_col, performance_optimization_date_to_col = st.sidebar.columns(2)
    from dateutil.relativedelta import relativedelta

    today = datetime.datetime.today().date()

    today_minus_one_year = today - relativedelta(years=1)
    with performance_optimization_date_from_col:
        performance_optimization_date_from = st.date_input(label='Von:',
                                         value=today_minus_one_year,
                                         key='performance_optimization_date_from')

    performance_optimization_date_from_plus_one_minute = performance_optimization_date_from + relativedelta(minutes=1)

    with performance_optimization_date_to_col:
        performance_optimization_date_to = st.date_input(label='Bis:',
                                       value=today,
                                       min_value=performance_optimization_date_from_plus_one_minute,
                                       max_value=today,
                                       key='performance_optimization_date_to')

    # Liste der Methodennamen
    optimization_method_names = [
                "Mean-Variance Optimization",
                "Minimum Variance Portfolio",
                "Maximum Sharpe Ratio Portfolio",
                "Equal Weight Portfolio",
                "Risk Parity Portfolio",
                "Inverse Variance Portfolio",
                "Maximum Diversification Portfolio",
                "Maximum Decorrelation Portfolio",
                "Black-Litterman Model Portfolio",
                "Hierarchical Risk Parity Portfolio"
                ]

    selected_optimization_method = st.sidebar.selectbox('Optimierungsmethode:',
                                                        options=optimization_method_names,
                                                        key='selected_optimization_method')



    # Marktkapital für Fonds

    market_caps = get_market_caps_funds(tickers_portfolio_performance_optimization)


    # Foto Sidebar Stocks API
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')

    # Page Title
    Centred_Title.run_centred_title('Portfolio Performance Optimization')


    st.markdown(
        f"""
            <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                {selected_optimization_method}
            </div>
            """,
        unsafe_allow_html=True
    )

    st.write('')
    st.write('')

    data = portfolio_performacne_fetch_data(tickers_portfolio_performance_optimization,
                                            performance_optimization_date_from,
                                            performance_optimization_date_to)

    data = data.reset_index()










    # Daten visualisieren
    create_line_chart(data)

    # Calculate Perofrmance Optimization

    result_text, result_df =calculate_performance_optimization(data=data,
                                                               selected_optimization_method=selected_optimization_method,
                                                               market_caps=market_caps)

    #st.write(result_df)
    # Index-Spalte umbennen (index -> Ticker)
    result_df = result_df.rename(columns={'index':'Ticker'})

    # Ergebnis nach Gewichten absteigend sortieren
    result_df = result_df.sort_values(by= 'Weight',
                                      ascending= False)



    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    create_pie_chart(result_df)
    tickers_count  = len(result_df['Ticker'].values)

    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)


    ticker_weight_col_one, ticker_weight_col_two, ticker_weight_col_three, ticker_weight_col_four = st.columns(4)

    with ticker_weight_col_one:
        iteration = 1

        for ticker in result_df['Ticker']:
            origin = get_country_abbr(ticker).lower()
            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)
            if iteration % 4 == 1:
                make_metric(ticker,weight,tickers_count,market_caps,origin)
            iteration += 1

    with ticker_weight_col_two:
        iteration = 1
        for ticker in result_df['Ticker']:
            origin = get_country_abbr(ticker).lower()
            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)
            if iteration % 4 == 2:
                make_metric(ticker,weight,tickers_count,market_caps,origin)
            iteration += 1

    with ticker_weight_col_three:
        iteration = 1
        for ticker in result_df['Ticker']:
            origin = get_country_abbr(ticker).lower()
            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)
            if iteration % 4 == 3:
                make_metric(ticker,weight,tickers_count,market_caps,origin)
            iteration += 1

    with ticker_weight_col_four:
        iteration = 1
        for ticker in result_df['Ticker']:
            origin = get_country_abbr(ticker).lower()
            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)
            if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                make_metric(ticker,weight,tickers_count,market_caps,origin)
            iteration += 1


    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    st.write('')
    st.write('')
    st.write('')
    st.write('')

    # "Created by K. B."
    st.write(f'**Erstellt von K. B.**')
