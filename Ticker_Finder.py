def run_Ticker_Finder(language_index):
    import streamlit as st
    import yfinance as yf
    import pycountry  # Für dynamische Ländercodes
    import Background_Style
    import Centred_Title


    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    # Funktion zum Abrufen des ISO-3166-Alpha-2-Codes aus einem Ländernamen
    def get_country_code(country_name,ticker):
        try:
            country = pycountry.countries.get(name=country_name)

            return country.alpha_2 if country else get_country_abbr(ticker)


        except KeyError:
            return "Empty"

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


    def make_metric(ticker, name,country_name, country_abbr):

        try:

            # Path to your local SVG file
            svg_path = rf'Images\Countries Flags\{country_abbr}.svg'

            import urllib.parse

            # Read the SVG content
            with open(svg_path, 'r') as file:
                svg_content = file.read()

            # Encode the content to escape special characters
            svg_encoded = urllib.parse.quote(svg_content)

            st.markdown(
                f"""
                <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; display: flex; flex-direction: column; justify-content: center;'>
                    <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; flex: 1;'>
                        {country_name}
                        <img src='data:image/svg+xml;utf8,{svg_encoded}' alt='SVG Image' style='width: 20px; height: 20px; vertical-align: middle;'/>
                    </h1>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; flex: 1;min-height:370px;'>
                        <span style='color:#FFD700;'>
                        <span style='color:#FFD700; '>‎ </span>
                        {name}
                        </span>
                    </h1>
                    <h1 style='text-align: center; background-color:#d5d5d5; color:#009999; margin: 0; padding: 5px; flex: 1;'>{ticker}</h1>
                </div>
                """, unsafe_allow_html=True
            )

            st.write('')
            st.write('')
        except:
            pass







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

    selected_ticker_col, selected_interval_col = st.sidebar.columns([1999,0.1])

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

        big_two_tickers_real_estate_fonds_usa = [
            "AMT",  # American Tower Corp.
            "PLD",  # Prologis Inc.

        ]

        # Zuordnung der Märkte zu den Listen
        if selected_market == 'Deutschland':
            tickers = real_estate_germany
            default_tickers = big_two_tickers_real_estate_fonds_germany

        elif selected_market == 'Andere EU-Länder':
            tickers = real_estate_fonds_europe
            default_tickers = big_two_tickers_real_estate_fonds_europe

        elif selected_market == 'USA':
            tickers = real_estate_usa
            default_tickers = big_two_tickers_real_estate_fonds_usa

        elif selected_market == 'China':
            tickers = real_estate_china
            default_tickers = big_two_tickers_real_estate_fonds_china

        elif selected_market == 'Japan':
            tickers = real_estate_japan
            default_tickers = big_two_tickers_real_estate_fonds_japan

        elif selected_market == 'Kanada':
            tickers = real_estate_canada
            default_tickers = big_two_tickers_real_estate_fonds_canada

        elif selected_market == 'Australien':
            tickers = real_estate_australia
            default_tickers = big_two_tickers_real_estate_fonds_australia

        else:
            tickers = []
            default_tickers = []


    # Mehrfachauswahl für Ticker (All)
    tickers_portfolio_ticker_finder_all= st.sidebar.multiselect('Tickers (mind. 1 auswählen):',
                                                                      options=tickers,
                                                                      key='tickers_portfolio_ticker_finder_all',
                                                                      default=default_tickers)




    # Page Title
    Centred_Title.run_centred_title('Ticker-Informationsnavigator')


    # Schritt 3: Dynamische Anzeige von Informationen
    if tickers_portfolio_ticker_finder_all:
        ticker_weight_col_one, ticker_weight_col_two, ticker_weight_col_three, ticker_weight_col_four = st.columns(4)

        with ticker_weight_col_one:
            iteration = 1
            for selected_ticker in tickers_portfolio_ticker_finder_all:
                # Verwenden Sie yfinance, um Details zum Ticker zu erhalten
                ticker_data = yf.Ticker(selected_ticker)
                company_name = ticker_data.info.get("longName", "Name nicht verfügbar")
                country = ticker_data.info.get("country", "Land nicht verfügbar")

                # Dynamische Bestimmung der Länderabkürzung
                country_code = get_country_code(country,selected_ticker)

                if iteration % 4 == 1:
                    make_metric(selected_ticker, company_name, country, country_code)
                iteration += 1

        with ticker_weight_col_two:
            iteration = 1
            for selected_ticker in tickers_portfolio_ticker_finder_all:
                # Verwenden Sie yfinance, um Details zum Ticker zu erhalten
                ticker_data = yf.Ticker(selected_ticker)
                company_name = ticker_data.info.get("longName", "Name nicht verfügbar")
                country = ticker_data.info.get("country", "Land nicht verfügbar")

                # Dynamische Bestimmung der Länderabkürzung
                country_code = get_country_code(country,selected_ticker)

                if iteration % 4 == 2:
                    make_metric(selected_ticker, company_name, country, country_code)
                iteration += 1

        with ticker_weight_col_three:
            iteration = 1
            for selected_ticker in tickers_portfolio_ticker_finder_all:
                # Verwenden Sie yfinance, um Details zum Ticker zu erhalten
                ticker_data = yf.Ticker(selected_ticker)
                company_name = ticker_data.info.get("longName", "Name nicht verfügbar")
                country = ticker_data.info.get("country", "Land nicht verfügbar")

                # Dynamische Bestimmung der Länderabkürzung
                country_code = get_country_code(country,selected_ticker)

                if iteration % 4 == 3:
                    make_metric(selected_ticker, company_name, country, country_code)
                iteration += 1

        with ticker_weight_col_four:
            iteration = 1
            for selected_ticker in tickers_portfolio_ticker_finder_all:
                # Verwenden Sie yfinance, um Details zum Ticker zu erhalten
                ticker_data = yf.Ticker(selected_ticker)
                company_name = ticker_data.info.get("longName", "Name nicht verfügbar")
                country = ticker_data.info.get("country", "Land nicht verfügbar")

                # Dynamische Bestimmung der Länderabkürzung
                country_code = get_country_code(country,selected_ticker)

                if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                    make_metric(selected_ticker, company_name, country, country_code)
                iteration += 1

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    st.write('')
    st.write('')
    st.write('')
    st.write('')

    # "Created by K. B."
    st.write(f'**Erstellt von K. B.**')



