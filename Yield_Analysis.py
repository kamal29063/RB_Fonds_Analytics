def run_Yield_Analysis(language_index):
    import streamlit as st
    import yfinance as yf
    import pandas as pd
    import numpy as np
    import scipy.optimize as sco
    import datetime
    from scipy.optimize import minimize
    import Centred_Title
    import Background_Style
    import Process_Button_Styling
    import Select_Store_Location
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    def get_country_name(ticker):
        if ticker in real_estate_germany:
            origin = 'Germany'
        elif ticker in real_estate_france:
            origin = 'France'
        elif ticker in real_estate_spain:
            origin = 'Spain'
        elif ticker in real_estate_italy:
            origin = 'Italy'
        elif ticker in real_estate_netherlands:
            origin = 'Netherlands'
        elif ticker in real_estate_sweden:
            origin = 'Sweden'
        elif ticker in real_estate_belgium:
            origin = 'Belgium'
        elif ticker in real_estate_switzerland:
            origin = 'Switzerland'
        elif ticker in real_estate_uk:
            origin = 'United Kingdom'
        elif ticker in real_estate_turkey:
            origin = 'Turkey'
        elif ticker in real_estate_usa:
            origin = 'United States'
        elif ticker in real_estate_canada:
            origin = 'Canada'
        elif ticker in real_estate_australia:
            origin = 'Australia'
        elif ticker in real_estate_japan:
            origin = 'Japan'
        elif ticker in real_estate_china:
            origin = 'China'
        else:
            origin = 'Unknown'

        return origin

    def make_metric(ticker, weight, tickers_count, market_caps, origin):
        distributed_weight = 1 / tickers_count

        try:

            market_cap = float(market_caps[market_caps['Ticker'] == ticker]['Market Cap'])

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

        # st.write(market_cap)

        weight = weight * 100
        distributed_weight = distributed_weight * 100

        # Path to your local SVG file
        svg_path = rf'Images\Countries Flags\{origin}.svg'

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

    # Daten abrufen
    st.cache
    def yield_analysis_fetch_data(tickers, start_date, end_date, date_point, selected_ticker_bench_mark):

        try:
            # Benchmark-Daten laden
            benchmark_data = yf.download(selected_ticker_bench_mark, start=start_date, end=end_date, interval='1d')
            benchmark_data.columns = benchmark_data.columns.droplevel(1)
            benchmark_data['Returns'] = benchmark_data['Adj Close'].pct_change()
            benchmark_data = benchmark_data.reset_index()
            # Neue Spalte für das Jahr hinzufügen
            benchmark_data.insert(1, 'Year', benchmark_data['Date'].dt.year)
            benchmark_data.insert(2, 'Month', benchmark_data['Date'].dt.month)

            # Risikofreier Zinssatz und Konfidenzniveau
            risk_free_rate = 0.02  # Beispiel: 2% jährlicher risikofreier Zinssatz
            confidence_level = 0.05  # 5% Value-at-Risk

            result_data = pd.DataFrame()
            for ticker in [ticker.upper() for ticker in tickers]:


                # Kursdaten abrufen
                data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

                # Wenn MultiIndex vorhanden, Ticker-Level entfernen
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)

                data = data.reset_index()
                data = data.loc[:, ['Date',  'Adj Close']]


                data.insert(0, 'Ticker', ticker)  # Tickerspalte hinzufügen


                # Neue Spalte für das Jahr hinzufügen
                data.insert(2, 'Year', data['Date'].dt.year)
                data.insert(3, 'Month', data['Date'].dt.month)
                data.insert(4, 'Country', get_country_name(ticker))
                # Liste zur Speicherung jährlicher Ergebnisse
                year_monthly_data = []

                for year_month, group in data.groupby(['Year', 'Month']):
                    year, month = year_month
                    group = group.copy()

                    # Tagesrenditen berechnen
                    group['Returns'] = group['Adj Close'].pct_change()

                    # Kumulative Renditen berechnen
                    group['Cumulative Returns'] = (1 + group['Returns']).cumprod() - 1

                    # Jährliche Rendite berechnen
                    # Warum? Zeigt das durchschnittliche jährliche Wachstum des Investments.
                    monthly_return = ((1 + group['Cumulative Returns'].iloc[-1]) ** (365.25 / len(group)) - 1)
                    group['Monthly Returns'] = monthly_return

                    # Volatilität (Standardabweichung der Renditen) berechnen
                    # Warum? Quantifiziert die Schwankungsbreite der Renditen und damit das Risiko.
                    group['Volatility'] = group['Returns'].std() * (365 ** 0.5)

                    # Sharpe Ratio berechnen
                    # Warum? Misst die risikobereinigte Rendite, indem sie den risikofreien Zinssatz berücksichtigt.
                    if group['Volatility'].iloc[0] != 0:
                        group['Sharpe Ratio'] = (monthly_return - risk_free_rate) / group['Volatility']
                    else:
                        group['Sharpe Ratio'] = None

                    # Maximaler Drawdown berechnen
                    # Warum? Zeigt den maximalen Verlust vom Höchststand während eines Zeitraums.
                    group['Running Max'] = group['Cumulative Returns'].cummax()
                    group['Drawdown'] = group['Cumulative Returns'] / group['Running Max'] - 1
                    max_drawdown = group['Drawdown'].min()

                    # Sortino Ratio berechnen
                    # Warum? Misst die risikobereinigte Rendite unter Berücksichtigung nur negativer Renditeschwankungen.
                    downside_deviation = group.loc[group['Returns'] < 0, 'Returns'].std() * (365 ** 0.5)
                    if downside_deviation and downside_deviation != 0:
                        group['Sortino Ratio'] = (monthly_return - risk_free_rate) / downside_deviation
                    else:
                        group['Sortino Ratio'] = None

                    # Value at Risk (VaR) berechnen
                    # Warum? Zeigt den maximalen Verlust, der mit einer bestimmten Wahrscheinlichkeit (hier: 5%) eintreten könnte.
                    group['VaR'] = group['Returns'].quantile(confidence_level)

                    # --- Benchmark Analysis ---
                    benchmark_group = benchmark_data[
                        (benchmark_data['Year'] == year) & (benchmark_data['Month'] == month)].copy()
                    benchmark_group['Returns'] = benchmark_group['Adj Close'].pct_change()
                    benchmark_group['Cumulative Returns'] = (1 + benchmark_group['Returns']).cumprod() - 1

                    # Beta und Alpha berechnen
                    # Warum? Beta misst die Sensitivität gegenüber dem Benchmark, Alpha die risikoadjustierte Überrendite.
                    if len(benchmark_group) > 1:
                        covariance = group['Returns'].cov(benchmark_group['Returns'])
                        benchmark_variance = benchmark_group['Returns'].var()

                        beta = covariance / benchmark_variance if benchmark_variance != 0 else None
                        if beta is not None:
                            alpha = monthly_return - (
                                    risk_free_rate + beta * (benchmark_group['Returns'].mean() - risk_free_rate))
                        else:
                            alpha = None
                    else:
                        beta = None
                        alpha = None

                    group['Beta'] = beta
                    group['Alpha'] = alpha

                    # Tracking Error berechnen
                    # Warum? Misst die Abweichung der Renditen des Assets vom Benchmark.
                    if len(benchmark_group) > 1:
                        group['Tracking Error'] = (group['Returns'] - benchmark_group['Returns']).std() * (365 ** 0.5)
                    else:
                        group['Tracking Error'] = None

                    # Information Ratio berechnen
                    # Warum? Misst die risikobereinigte Überrendite gegenüber dem Benchmark.
                    if group['Tracking Error'].iloc[0] != 0 and group['Tracking Error'].iloc[0] is not None:
                        group['Information Ratio'] = (monthly_return - benchmark_group['Returns'].mean()) / group[
                            'Tracking Error']
                    else:
                        group['Information Ratio'] = None

                    # Ergebnisse speichern
                    year_monthly_data.append(group)


                final_data = pd.concat(year_monthly_data)
                final_data['Impact'] = final_data['Date'].apply(
                    lambda x: 'Yes' if x >= pd.to_datetime(date_point) else 'No')


                result_data = pd.concat([result_data, final_data])


            year_monthly_summary = result_data.groupby(['Ticker', 'Year', 'Month']).agg(
                monthly_returns=('Monthly Returns', 'first'),
                Volatility=('Volatility', 'first'),
                sharpe_ratio=('Sharpe Ratio', 'first'),
                sortino_ratio=('Sortino Ratio', 'first'),
                Beta=('Beta', 'first'),
                Alpha=('Alpha', 'first'),
                tracking_error=('Tracking Error', 'first'),
                information_ratio=('Information Ratio', 'first'),
            ).reset_index()


            year_monthly_summary.insert(1, 'Country', year_monthly_summary['Ticker'].apply(get_country_name))

            year_monthly_summary = year_monthly_summary.rename(columns={'monthly_returns': 'Monthly Returns',
                                                                        'sharpe_ratio': 'Sharpe Ratio',
                                                                        'sortino_ratio': 'Sortino Ratio',
                                                                        'tracking_error': 'Tracking Error',
                                                                        'information_ratio': 'Information Ratio',
                                                                        })

            result_data.drop(columns=['Monthly Returns', 'Volatility', 'Sharpe Ratio', 'Sortino Ratio',
                                      'VaR', 'Tracking Error', 'Information Ratio',
                                      'Alpha', 'Beta'], inplace=True)


            return result_data, year_monthly_summary
        except:
            return pd.DataFrame(),pd.DataFrame()
        

    # Logo sidebar
    st.sidebar.image("Images/RB Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)

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

    big_two_tickers_real_estate_fonds_usa = [
        "AMT",  # American Tower Corp.
        "PLD",  # Prologis Inc.

    ]


    # Market auswählen
    markt_options_base_one = ['Deutschland', 'Andere EU-Länder', 'USA', 'China', 'Japan', 'Kanada', 'Australien']
    # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
    selected_markt_base_one = st.sidebar.selectbox("Ersten Markt auswählen (Base):",
                                               options=markt_options_base_one,
                                               index=0,
                                               key='selected_markt_base_one'
                                               )

    # Zuordnung der Märkte zu den Listen
    if selected_markt_base_one == 'Deutschland':
        tickers_base_one = real_estate_germany.copy()

    elif selected_markt_base_one == 'Andere EU-Länder':
        tickers_base_one = real_estate_fonds_europe.copy()

    elif selected_markt_base_one == 'USA':
        tickers_base_one = real_estate_usa.copy()

    elif selected_markt_base_one == 'China':
        tickers_base_one = real_estate_china.copy()

    elif selected_markt_base_one == 'Japan':
        tickers_base_one = real_estate_japan.copy()

    elif selected_markt_base_one == 'Kanada':
        tickers_base_one = real_estate_canada.copy()

    elif selected_markt_base_one == 'Australien':
        tickers_base_one = real_estate_australia.copy()

    else:
        tickers_base_one = []

    selected_ticker_base_one= st.sidebar.selectbox(label='Ersten Ticker (Base):',
                                                      options=tickers_base_one,
                                                      key='selected_ticker_base_one')

    # Market auswählen
    markt_options_base_two = ['Deutschland', 'Andere EU-Länder', 'USA', 'China', 'Japan', 'Kanada', 'Australien']
    # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
    selected_markt_base_two = st.sidebar.selectbox("Zweiten Markt auswählen (Base):",
                                                   options=markt_options_base_two,
                                                   index=0,
                                                   key='selected_markt_base_two'
                                                   )

    # Zuordnung der Märkte zu den Listen
    if selected_markt_base_two == 'Deutschland':
        tickers_base_two = real_estate_germany.copy()

    elif selected_markt_base_two == 'Andere EU-Länder':
        tickers_base_two = real_estate_fonds_europe.copy()

    elif selected_markt_base_two == 'USA':
        tickers_base_two = real_estate_usa.copy()

    elif selected_markt_base_two == 'China':
        tickers_base_two = real_estate_china.copy()

    elif selected_markt_base_two == 'Japan':
        tickers_base_two = real_estate_japan.copy()

    elif selected_markt_base_two == 'Kanada':
        tickers_base_two = real_estate_canada.copy()

    elif selected_markt_base_two == 'Australien':
        tickers_base_two = real_estate_australia.copy()

    else:
        tickers_base_two = []

    if selected_markt_base_one == selected_markt_base_two:
        tickers_base_two.remove(selected_ticker_base_one)

    selected_ticker_base_two = st.sidebar.selectbox(label='Zweiten Ticker (Base):',
                                                    options=tickers_base_two,
                                                    key='selected_ticker_base_two')


    # Market auswählen
    markt_options_bench_mark  = ['Deutschland', 'Andere EU-Länder', 'USA', 'China', 'Japan', 'Kanada', 'Australien']
    # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
    selected_markt_bench_mark = st.sidebar.selectbox("Markt auswählen (Benchmark):",
                                           options=markt_options_bench_mark,
                                           index=0,
                                           key='selected_bench_mark'
                                           )

    # Zuordnung der Märkte zu den Listen
    if selected_markt_bench_mark == 'Deutschland':
        tickers_bench_mark = real_estate_germany.copy()

    elif selected_markt_bench_mark == 'Andere EU-Länder':
        tickers_bench_mark = real_estate_fonds_europe

    elif selected_markt_bench_mark == 'USA':
        tickers_bench_mark = real_estate_usa.copy()

    elif selected_markt_bench_mark == 'China':
        tickers_bench_mark = real_estate_china.copy()

    elif selected_markt_bench_mark == 'Japan':
        tickers_bench_mark = real_estate_japan.copy()

    elif selected_markt_bench_mark == 'Kanada':
        tickers_bench_mark = real_estate_canada.copy()

    elif selected_markt_bench_mark == 'Australien':
        tickers_bench_mark= real_estate_australia.copy()

    else:
        tickers_bench_mark = []

    if selected_markt_base_one == selected_markt_bench_mark:
        try:
            tickers_bench_mark.remove(selected_ticker_base_one)
        except:
            pass

    if selected_markt_base_two == selected_markt_bench_mark:
        try:
            tickers_bench_mark.remove(selected_ticker_base_two)

        except:
            pass

    selected_ticker_bench_mark= st.sidebar.selectbox(label='Ticker (Benchmark):',
                                             options=tickers_bench_mark,
                                             key='selected_ticker_bench_mark')


    # st.write(market_caps)
    yield_analysis_date_from_col, yield_analysis_date_to_col = st.sidebar.columns(2)
    from dateutil.relativedelta import relativedelta

    today = datetime.datetime.today().date()

    today_minus_one_year = today - relativedelta(years=1)
    with yield_analysis_date_from_col:
        yield_analysis_date_from = st.date_input(label='Von:',
                                                           value=today_minus_one_year,
                                                           key='yield_analysis_date_from')

    yield_analysis_date_from_plus_one_minute = yield_analysis_date_from + relativedelta(minutes=1)

    with yield_analysis_date_to_col:
        yield_analysis_date_to = st.date_input(label='Bis:',
                                                         value=today,
                                                         min_value=yield_analysis_date_from_plus_one_minute,
                                                         max_value=today,
                                                         key='yield_analysis_date_to')


    # Marktkapital für Fonds

    from dateutil.relativedelta import relativedelta
    today = datetime.datetime.today().date()
    date_value = pd.to_datetime('2022-01-01').date()
    today_minus_ten_years = today - relativedelta(years=10)

    date_point = st.sidebar.date_input(label='Datum-Punkt:',
                                          value=date_value,
                                          min_value=today_minus_ten_years,
                                          max_value=today,
                                          key='date_point')


    # Foto Sidebar Stocks API
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')

    # Page Title
    Centred_Title.run_centred_title('Yield Analysis')

    st.markdown(
        f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                    {'HIER KANN EIN TEXT STEHEN'}
                </div>
                """,
        unsafe_allow_html=True
    )

    st.write('')
    st.write('')

    selected_tickers_base = [selected_ticker_base_one ,selected_ticker_base_two]
    data_result,summary_result = yield_analysis_fetch_data(selected_tickers_base,
                                                            yield_analysis_date_from,
                                                            yield_analysis_date_to,
                                                            date_point,
                                                           selected_ticker_bench_mark)

    st.write(data_result,summary_result)

    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    store_location_path = Select_Store_Location.run_select_store_location(language_index=language_index)

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)
    # Daten speichern
    process_button_dummy_one, process_button, process_button_dummy_two = st.columns([1.5, 1, 1.5])
    with process_button_dummy_one:
        pass
    with process_button:
        Process_Button_Styling.run_process_button_style()
        if st.button("Daten lokal speichern"):
            if len(store_location_path) > 0:

                data_result.to_excel(rf'{store_location_path}/Data Result.xlsx',
                                        sheet_name='Data Result',
                                        index=False)

                summary_result.to_excel(rf'{store_location_path}/Summary Result.xlsx',
                                          sheet_name='Summary Result',
                                          index=False)

                st.success('Alles geklappt')
            else:
                st.warning(
                    # "Please complete your details and check them for accuracy"
                    f'Bitte vervollständigen')
    with process_button_dummy_two:
        pass


    st.write('')
    st.write('')
    st.write('')
    st.write('')

    # "Created by K. B."
    st.write(f'**Erstellt von K. B.**')
