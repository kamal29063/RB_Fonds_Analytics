def run_candle_scope(language_index):
    import streamlit as st
    import datetime
    import pandas as pd
    import yfinance as yf
    import Process_Button_Styling
    import Select_Store_Location
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




    st.cache
    def candle_scope_load_data(start_date, end_date, selected_ticker, selected_interval, candle_scope_tech_indicator_periods_count):
        import pandas_ta as ta
        selected_ticker_dummy = selected_ticker





        selected_ticker = str(selected_ticker).upper()
        title = selected_ticker_dummy + ' / USD'


        # Lade die Daten des aktuellen Tickers
        data = yf.download(tickers=selected_ticker,
                           interval=selected_interval,
                           start=start_date,
                           end=end_date)


        # Lösche die Ticker-Level aus den Daten
        data.columns = data.columns.droplevel(1)

        # Index Spalte zurücksetzen
        data = data.reset_index()

        # Umbennen der Spalte 'Date' zu 'Datetime'
        data = data.rename(columns={"Date": "Datetime"})

        # Datetime format anpasse
        data["Datetime"] = data["Datetime"].dt.tz_localize(None)

        # Füge eine neue Spalte mit Tickernamen als erste Spalte im DataFrame
        data.insert(0, 'Ticker', selected_ticker)

        # Berechne Tech. Indikatoren
        data["Datetime"] = pd.to_datetime(data["Datetime"])
        data["BarColor"] = data[["Open", "Close"]].apply(lambda o: "red" if o.Open > o.Close else "green",
                                                                 axis=1)
        data["Date_Text"] = data["Datetime"].astype(str)
        talib_indicators = []


        try:
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 14
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            # Berechnung des Simple Moving Average (SMA)
            data["SMA"] = ta.sma(data["Close"], length=tech_indicator_periods_length)

            # Simple Moving Average (SMA)
            data["SMA"] = ta.sma(data["Close"], length=tech_indicator_periods_length)

            # Exponential Moving Average (EMA)
            data["EMA"] = ta.ema(data["Close"], length=tech_indicator_periods_length)

            # Weighted Moving Average (WMA)
            data["WMA"] = ta.wma(data["Close"], length=tech_indicator_periods_length)

            # Relative Strength Index (RSI)
            data["RSI"] = ta.rsi(data["Close"], length=tech_indicator_periods_length)

            # Füge die Werte zur Idikatoren-Liste
            talib_indicators = talib_indicators+["MA", "EMA", "SMA", "WMA", "RSI"]
        except:
            pass

        try:
            # Moving Average Convergence Divergence (MACD)
            macd = ta.macd(data["Close"], fast=12, slow=26, signal=9)
            data["MACD"] = macd["MACD_12_26_9"]
            data["Signal"] = macd["MACDs_12_26_9"]
            data["Histogram"] = macd["MACDh_12_26_9"]
            talib_indicators = talib_indicators + ["MACD", "Signal", "Histogram"]

        except:
            pass

        try:
            # Bollinger Bands
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 20
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            bbands = ta.bbands(data["Close"], length=tech_indicator_periods_length, std=2)
            data["BB_upper"] = bbands["BBU_20_2.0"]
            data["BB_middle"] = bbands["BBM_20_2.0"]
            data["BB_lower"] = bbands["BBL_20_2.0"]
            talib_indicators = talib_indicators + ["BB_upper", "BB_middle", "BB_lower"]
        except:
            pass

        try:
            # Stochastic Oscillator
            stoch = ta.stoch(data["High"], data["Low"], data["Close"], k=14, d=3)
            data["Stoch_K"] = stoch["STOCHk_14_3_3"]
            data["Stoch_D"] = stoch["STOCHd_14_3_3"]
            talib_indicators = talib_indicators + ["Stoch_K", "Stoch_K"]
        except:
            pass

        try:
            # Average Directional Index (ADX)
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 14
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            adx = ta.adx(data["High"],
                         data["Low"],
                         data["Close"],
                         length=tech_indicator_periods_length)
            data["ADX"] = adx["ADX_14"]
            talib_indicators = talib_indicators + ["ADX"]
        except:
            pass

        try:
            # Momentum (MOM)
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 10
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            data["MOM"] = ta.mom(data["Close"],
                                 length=tech_indicator_periods_length)
            talib_indicators = talib_indicators + ["MOM"]
        except:
            pass

        try:
            # TRIX
            data["TRIX"] = ta.trix(data["Close"], length=15)
            talib_indicators = talib_indicators + ["TRIX"]
        except:
            pass

        try:
            # Commodity Channel Index (CCI)
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 20
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            data["CCI"] = ta.cci(data["High"], data["Low"], data["Close"], length=tech_indicator_periods_length)
            talib_indicators = talib_indicators + ["CCI"]
        except:
            pass


        try:
            # Williams %R
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 14
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            data["WilliamsR"] = ta.willr(data["High"],
                                         data["Low"],
                                         data["Close"],
                                         length=tech_indicator_periods_length)
            talib_indicators = talib_indicators + ["WilliamsR"]
        except:
            pass

        try:
            # Supertrend
            if candle_scope_tech_indicator_periods_count == 'Default':
                tech_indicator_periods_length = 10
            else:
                tech_indicator_periods_length = int(candle_scope_tech_indicator_periods_count)

            supertrend = ta.supertrend(data["High"],
                                       data["Low"],
                                       data["Close"],
                                       length=tech_indicator_periods_length,
                                       multiplier=3)

            data["Supertrend"] = supertrend["SUPERT_10_3.0"]
            talib_indicators = talib_indicators + ["Supertrend"]
        except:
            pass

        return data,talib_indicators,title


    def create_chart(title,df, close_price_line=False, open_price_line=False, low_price_line=False, high_price_line=False, indicators=[], selected_ticker='',indicator_colors=False):
        from bokeh.plotting import figure, column
        ## Candlestick Pattern Logic
        candle = figure(x_axis_type="datetime",
                        outer_height=500,
                        inner_height=500,
                        x_range=(df.Datetime.values[0], df.Datetime.values[-1]),
                        tooltips=[("Datetime", "@Date_Text"),
                                  ("Open", "@Open"),
                                  ("High", "@High"),
                                  ("Low", "@Low"),
                                  ("Close", "@Close")], )

        candle.segment("Datetime", "Low", "Datetime", "High", color="black", line_width=0.5, source=df)
        candle.segment("Datetime", "Open", "Datetime", "Close", line_color="BarColor", line_width=2 if len(df) > 100 else 6,
                       source=df)



        # Setze die Hintergrundfarbe
        candle.background_fill_color = '#eeeeee'  # Hier kannst du die Farbe ändern
        candle.border_fill_color = '#d5d5d5'  # Die Farbe des Rahmens (optional)


        # Diagramm Titel
        candle.title.text = f'{title}'
        candle.title_location = "above"  # Titel über dem Diagramm
        candle.title.align = "center"  # Zentriere den Titel horizontal

        # Achsen Beschriftung
        candle.xaxis.axis_label = "Datetime"
        candle.yaxis.axis_label = f"Price ($)"

        ## Close Price Line
        if close_price_line:
            candle.line("Datetime",
                        "Close",
                        color='#009999',
                        source=df,
                        legend_label='Close')

        ## Open Price Line
        if open_price_line:
            candle.line("Datetime",
                        "Open",
                        color='#FF6F61',
                        source=df,
                        legend_label='Open')

        ## Low Price Line
        if low_price_line:
            candle.line("Datetime",
                        "Low",
                        color='#6B5B95',
                        source=df,
                        legend_label='Low')

        ## High Price Line
        if high_price_line:
            candle.line("Datetime",
                        "High",
                        color='#88B04B',
                        source=df,
                        legend_label='High')

        for indicator in indicators:
            candle.line("Datetime", indicator, color=indicator_colors[indicator], line_width=2, source=df,
                        legend_label=indicator)

        return column(children=[candle], sizing_mode="scale_width")

    # Logo sidebar
    st.sidebar.image("Images/RB Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)

    # Market auswählen
    markt_options = ['Deutschland','Andere EU-Länder','USA','China','Japan','Kanada','Australien']
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
                real_estate_switzerland+
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

        # Zuordnung der Märkte zu den Listen
        if selected_market == 'Deutschland':
            tickers = real_estate_germany

        elif selected_market == 'Andere EU-Länder':
            tickers = real_estate_fonds_europe

        elif selected_market == 'USA':
            tickers = real_estate_usa

        elif selected_market == 'China':
            tickers = real_estate_china

        elif selected_market == 'Japan':
            tickers = real_estate_japan

        elif selected_market == 'Kanada':
            tickers = real_estate_canada

        elif selected_market == 'Australien':
            tickers = real_estate_australia

        else:
            tickers = []

        # Einfachauswahl für Ticker
        candle_scope_selected_ticker = st.selectbox(
            label="Ticker:",
            options=tickers
        )



    with selected_interval_col:
        # Liste der Intervalle für yfinance
        intervals = [

            "2m",  # 2 minutes
            "5m",  # 5 minutes
            "15m",  # 15 minutes
            "30m",  # 30 minutes
            "60m",  # 1 hour
            "90m",  # 90 minutes
            "1h",  # 1 hour (alias for "60m")
            "1d",  # 1 day
            "5d",  # 5 days
            "1wk",  # 1 week
            "1mo",  # 1 month
            "3mo"  # 3 months
        ]

        # Liste umkehren
        intervals.reverse()

        # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
        selected_interval = st.selectbox("Intervall:",
                                     options= intervals,
                                     index=4
                                     )


    candle_scope_date_from_col, candle_scope_date_to_col = st.sidebar.columns(2)
    from dateutil.relativedelta import relativedelta

    today = datetime.datetime.today().date()




    candle_scope_today_minus_one_month = today - relativedelta(months=1)
    candle_scope_today_minus_twenty_years = today - relativedelta(years=20)
    with candle_scope_date_from_col:
        candle_scope_date_from = st.date_input(label='Von:',
                                         min_value=candle_scope_today_minus_twenty_years,
                                         value=candle_scope_today_minus_one_month,
                                        key='candle_scope_date_from')

    candle_scope_date_from_plus_one_minute= candle_scope_date_from + relativedelta(minutes=1)

    with candle_scope_date_to_col:
        candle_scope_date_to = st.date_input(label='Bis:',
                                         value=today,
                                         min_value=candle_scope_date_from_plus_one_minute,
                                         max_value=today,
                                         key='candle_scope_date_to')

    candle_scope_close_price_line = False
    candle_scope_open_price_line = False
    candle_scope_low_price_line = False
    candle_scope_high_price_line = False
    candle_scope_volume_line_chart = False

    candle_scope_included_kpis_options = ['Schlusskurs', 'Eröffnungskurs', 'Tiefstkurs', 'Höchstkurs', 'Handelsvolumen']

    candle_scope_included_kpis = st.sidebar.multiselect(label="Kennzahlen:",
                                   options=candle_scope_included_kpis_options,
                                   key='candle_scope_included_kpis')

    if 'Schlusskurs' in candle_scope_included_kpis:
        candle_scope_close_price_line = True
        # st.write(candle_scope_close_price_line)

    if 'Eröffnungskurs' in candle_scope_included_kpis:
        candle_scope_open_price_line = True
        # st.write(candle_scope_open_price_line)

    if 'Tiefstkurs' in candle_scope_included_kpis:
        candle_scope_low_price_line = True
        # st.write(candle_scope_low_price_line)

    if 'Höchstkurs' in candle_scope_included_kpis:
        candle_scope_high_price_line = True
        # st.write(candle_scope_high_price_line)

    if 'Handelsvolumen' in candle_scope_included_kpis:
        candle_scope_volume_line_chart = True
        # st.write(candle_scope_volume_line_chart)


    # Page Title
    Centred_Title.run_centred_title('CandleScope')
    if 'candle_scope_tech_indicator_periods_count' not in st.session_state:
        st.session_state.candle_scope_tech_indicator_periods_count = 'Default'

    candle_scope_tech_indicator_periods_count = st.session_state.candle_scope_tech_indicator_periods_count

    # Charts
    candle_scope_data,candle_scope_talib_indicators,title  = candle_scope_load_data(start_date=candle_scope_date_from,
                                                                             end_date=candle_scope_date_to,
                                                                             selected_ticker=candle_scope_selected_ticker,
                                                                             selected_interval=selected_interval,
                                                                             candle_scope_tech_indicator_periods_count= candle_scope_tech_indicator_periods_count
                                                                             )


    candle_scope_tech_indicators_col,candle_scope_tech_indicator_periods_count_col= st.columns([10,1])

    with candle_scope_tech_indicators_col:
        # Farbzuordnung für Indikatoren
        candle_scope_indicator_colors = {
            "SMA": "#FF5733",  # Bright Orange
            "EMA": "#6A0DAD",  # Deep Purple
            "WMA": "#3498DB",  # Sky Blue
            "RSI": "#F1C40F",  # Vibrant Yellow
            "MOM": "#2C3E50",  # Dark Blue-Gray
            "DEMA": "#E74C3C",  # Bright Red
            "MA": "#16A085",  # Teal Green
            "TEMA": "#1ABC9C",  # Aqua
            "MACD": "#8E44AD",  # Purple
            "Signal": "#2ECC71",  # Green
            "Histogram": "#D35400",  # Orange
            "BB_upper": "#E67E22",  # Pumpkin Orange
            "BB_middle": "#BDC3C7",  # Light Gray
            "BB_lower": "#3498DB",  # Sky Blue
            "Stoch_K": "#9B59B6",  # Amethyst
            "Stoch_D": "#34495E",  # Wet Asphalt
            "ADX": "#F39C12",  # Yellow Orange
            "TRIX": "#C0392B",  # Red
            "CCI": "#2980B9",  # Belize Hole Blue
            "WilliamsR": "#27AE60",  # Emerald Green
            "Supertrend": "#1F618D"  # Dark Blue
        }


        candle_scope_tech_indicators = st.multiselect(label="Technische Indikatoren:",
                                    options=candle_scope_talib_indicators,
                                    key='candle_scope_tech_indicators')


    with candle_scope_tech_indicator_periods_count_col:

        candle_scope_periods_count_list = ['Default']
        for i in range(2,51):
            candle_scope_periods_count_list.append(i)
        candle_scope_tech_indicator_periods_count = st.selectbox(label='Anzahl der Perioden:',
                                                               options=candle_scope_periods_count_list,
                                                               key='candle_scope_tech_indicator_periods_count')



    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    
    st.bokeh_chart(create_chart(title,candle_scope_data, candle_scope_close_price_line,candle_scope_open_price_line,candle_scope_low_price_line,candle_scope_high_price_line,  candle_scope_tech_indicators, candle_scope_selected_ticker,candle_scope_indicator_colors), use_container_width=True)

    ## Volume Bars Logic
    if candle_scope_volume_line_chart:

        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        import plotly.express as px

        # Interaktives Liniendiagramm mit Plotly und Streamlit
        fig = px.line(candle_scope_data,
                      x='Datetime',
                      y='Volume')

        # Hintergrund und Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'Handelsvolumen zwischen {candle_scope_date_from} und {candle_scope_date_to} für {candle_scope_selected_ticker}',
                # Titeltext
                x=0.5,  # Zentriert den Titel
                xanchor='center',  # Verankert den Titel in der Mitte
                font=dict(size=25)  # Schriftgröße des Titels
            )

        )

        # Achsenfarben anpassen
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Change the line color
        fig.update_traces(line=dict(color='#009999'))


        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)

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
                basics_columns = ['Datetime', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
                store_columns = basics_columns + candle_scope_tech_indicators
                candle_scope_data = candle_scope_data[store_columns]
                candle_scope_data.insert(0,'Ticker',title)
                candle_scope_data.to_excel(rf'{store_location_path}/Stocksdata.xlsx',
                              sheet_name='Stocks Data',
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