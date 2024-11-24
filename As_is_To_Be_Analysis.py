def run_As_is_To_Be_Analysis(language_index):
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

    def create_is_plan_line_chart(line_chart_data, is_forecast_line_chart_date_from, is_forecast_line_chart_date_to, is_forecast_line_chart_ticker):
        import plotly.graph_objects as go
        import streamlit as st

        # Basisdiagramm erstellen
        fig = go.Figure()

        # Linie für "Close (Forecast)"
        fig.add_trace(go.Scatter(
            x=line_chart_data['Datetime'],
            y=line_chart_data['Close (Forecast)'],
            mode='lines',
            name='Close (Forecast)',  # Name in der Legende
            line=dict(color='#009999')  # Farbe der Linie
        ))

        # Linie für "Close (Actual)"
        if 'Close (Actual)' in line_chart_data.columns:  # Prüfen, ob die Spalte existiert
            fig.add_trace(go.Scatter(
                x=line_chart_data['Datetime'],
                y=line_chart_data['Close (Actual)'],
                mode='lines',
                name='Close (Actual)',  # Name in der Legende
                line=dict(color='#ff6600')  # Farbe der Linie
            ))

        # Hintergrund und Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'Close Preis (Forecast) vs. Close Preis (ist) zwischen {is_forecast_line_chart_date_from} und {is_forecast_line_chart_date_to} für {is_forecast_line_chart_ticker}',
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

    def create_actual_line_chart(line_chart_data, is_actual_line_chart_date_from, is_actual_line_chart_date_to,
                                  is_actual_line_chart_ticker):
        import plotly.graph_objects as go
        import streamlit as st

        # Basisdiagramm erstellen
        fig = go.Figure()

        # Linie für "Close (Forecast)"
        fig.add_trace(go.Scatter(
            x=line_chart_data['Datetime'],
            y=line_chart_data['Close (Actual)'],
            mode='lines',
            name='Close (Forecast)',  # Name in der Legende
            line=dict(color='#009999')  # Farbe der Linie
        ))



        # Hintergrund und Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'Explorative Daten zwischen {is_actual_line_chart_date_from} und {is_actual_line_chart_date_to} für {is_actual_line_chart_ticker}',
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

    def as_is_to_be_analysis_get_data(selected_ticker,
                                      explorative_date_from,
                                      explorative_date_to,
                                      training_date_from,
                                      training_date_to,
                                      forecast_start_date,
                                      count_of_forecast_periods):
        try:
            import logging
            logging.getLogger("prophet.plot").disabled = True
            from prophet import Prophet
            import numpy as np




            selected_ticker = str(selected_ticker).upper()
            title = selected_ticker + ' / USD'



            # Lade die Daten des aktuellen Tickers
            expolrative_actual_data = yf.download(tickers=selected_ticker,
                                      interval='1d',
                                      start=explorative_date_from,
                                      end=explorative_date_to)
            # Lösche die Ticker-Level aus den Daten
            expolrative_actual_data.columns = expolrative_actual_data.columns.droplevel(1)

            #  Index Spalte zurücksetzen
            expolrative_actual_data = expolrative_actual_data.reset_index()

            expolrative_actual_data = expolrative_actual_data.loc[:, ['Date', 'Close']]

            expolrative_actual_data = expolrative_actual_data.rename(columns={"Date": "Datetime"})

            # Datetime format anpasse
            expolrative_actual_data["Datetime"] = expolrative_actual_data["Datetime"].dt.tz_localize(None)

            expolrative_actual_data = expolrative_actual_data.rename(
                columns={ 'Close': 'Close (Actual)'})

            ######
            ######
            #####
            # Lade die Daten des aktuellen Tickers
            from datetime import date
            match_actual_data = yf.download(tickers=selected_ticker,
                                                  interval='1d',
                                                  start=pd.to_datetime('2002-01-01').date(),
                                                  end=date.today())
            # Lösche die Ticker-Level aus den Daten
            match_actual_data.columns = match_actual_data.columns.droplevel(1)

            #  Index Spalte zurücksetzen
            match_actual_data = match_actual_data.reset_index()

            match_actual_data = match_actual_data.loc[:, ['Date', 'Close']]

            match_actual_data = match_actual_data.rename(columns={"Date": "Datetime"})

            # Datetime format anpasse
            match_actual_data["Datetime"] = match_actual_data["Datetime"].dt.tz_localize(None)

            match_actual_data = match_actual_data.rename(
                columns={'Close': 'Close (Actual)'})



            #####
            ####
            ####

            # Lade die Daten des aktuellen Tickers
            training_data = yf.download(tickers=selected_ticker,
                               interval='1d',
                               start=training_date_from,
                               end=training_date_to)





            # Lösche die Ticker-Level aus den Daten
            training_data.columns = training_data.columns.droplevel(1)

            #  Index Spalte zurücksetzen
            training_data = training_data.reset_index()

            training_data = training_data.loc[:,['Date','Close']]


            training_data = training_data.rename(columns={"Date": "Datetime"})


            # Datetime format anpasse
            training_data["Datetime"] = training_data["Datetime"].dt.tz_localize(None)







            # FORECAST ERSTELLEN
            training_data = training_data.rename(
                columns={'Datetime':'ds', 'Close':'y'})

            #st.write('training_data',training_data)

            # Annahme: 'training_data' ist ein DataFrame mit Spalten ['ds', 'y'] (für Prophet)
            # Feiertage oder Markt-geschlossene Tage herausfiltern
            training_data = training_data[training_data['y'] > 0]

            # Logarithmische Transformation anwenden, um Werte zu stabilisieren
            training_data['y'] = np.log(training_data['y'])

            # Feiertage definieren (wenn verfügbar)
            # holidays_df = pd.DataFrame({
            #     'holiday': 'market_closed',
            #     'ds': pd.to_datetime(['2023-12-25', '2024-01-01']),  # Beispiel-Feiertage
            #     'lower_window': 0,
            #     'upper_window': 0,
            # })

            # Prophet-Modell initialisieren
            model = Prophet(weekly_seasonality=True, yearly_seasonality=True)

            # Falls Feiertage definiert sind, dem Modell hinzufügen
            model.add_country_holidays(country_name='US')  # Für US-Feiertage
            #model.add_regressor('holiday') # Optional für spezifische Feiertage

            # Modell trainieren
            model.fit(training_data)

            # Zukünftigen Zeitraum definieren
            future = model.make_future_dataframe(periods=count_of_forecast_periods+1, freq='D')

            # Vorhersage erstellen
            forecast_result_dataframe = model.predict(future)

            # Exponentielle Rücktransformation der Vorhersagen
            forecast_result_dataframe['yhat'] = np.exp(forecast_result_dataframe['yhat'])

            # Negative Werte durch Mindestwert (z. B. 0) ersetzen
            forecast_result_dataframe['yhat'] = forecast_result_dataframe['yhat'].clip(lower=0)

            # Ausgabe: DataFrame mit den vorhergesagten Werten
            forecast_result_dataframe = forecast_result_dataframe.loc[:,['ds','yhat']]


            forecast_result_dataframe = forecast_result_dataframe.rename(
                columns={'ds': 'Datetime', 'yhat': 'Close (Forecast)'})


            forecast_result_dataframe['Is Forecast'] = forecast_result_dataframe['Datetime'].apply(
                lambda x: 'Yes' if x > pd.to_datetime(forecast_start_date) else 'No'
            )



            forecast_result_dataframe = forecast_result_dataframe[forecast_result_dataframe['Is Forecast'] == 'Yes']


            forecast_result_dataframe = forecast_result_dataframe.loc[:, ['Datetime', 'Close (Forecast)']]
            #st.write('forecast_result_dataframe', forecast_result_dataframe)

            # Merge on the 'Datetime' column
            forecast_data = pd.merge(
                    forecast_result_dataframe,
                    match_actual_data,
                    on='Datetime',  # Specify the common column
                    how='inner'     # Choose 'inner', 'outer', 'left', or 'right' join as needed
                    )

            #st.write('forecast_data',forecast_data)

            # Füge eine neue Spalte mit Tickernamen als erste Spalte im DataFrame
            forecast_data.insert(0, 'Ticker', selected_ticker)

            expolrative_actual_data.insert(0,'Ticker',selected_ticker)
            return forecast_data,expolrative_actual_data, title
        except:
            st.warning('Bitte andere Daten Wählen')
            return pd.DataFrame({'Datetime':[],'Close (Forecast)':[],'Close (Actual)':[]}),pd.DataFrame({'Datetime':[],'Close (Actual)':[]}),''

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
    selected_ticker = st.sidebar.selectbox(
        label="Ticker:",
        options=tickers
    )

    from dateutil.relativedelta import relativedelta
    today = datetime.datetime.today().date()
    today_minus_ten_years = today - relativedelta(years=10)


    explorative_date_from_col, explorative_date_to_col, = st.sidebar.columns(2)

    with explorative_date_from_col:
        explorative_date_from = st.date_input(label='Von (Explorativ):',
                                             value=today_minus_ten_years,
                                             min_value=today_minus_ten_years,
                                             max_value=today,
                                             key='explorative_date_from')


    with explorative_date_to_col:
        explorative_date_to = st.date_input(label='Bis (Explorativ):',
                                             value=today,
                                             min_value=today_minus_ten_years,
                                             max_value=today,
                                             key='explorative_date_to')

    training_date_from_col, training_date_to_col, = st.sidebar.columns(2)

    with training_date_from_col:
        training_date_from = st.date_input(label='Von (Training):',
                                              value=today_minus_ten_years,
                                              min_value=today_minus_ten_years,
                                              max_value=today,
                                              key='training_date_from')

    with training_date_to_col:
        training_date_to = st.date_input(label='Bis (Training):',
                                            value=pd.to_datetime('2022-12-31').date(),
                                            min_value=today_minus_ten_years,
                                            max_value=today,
                                            key='training_date_to')



    count_of_forecast_periods = st.sidebar.number_input(label='Anzahl der Forecast-Tage:',
                                       min_value=12,
                                       max_value=1000,
                                       value=365,
                                       key='count_of_forecast_periods')



    # Page Title
    Centred_Title.run_centred_title('As-Is/To-Be Analysis')

    forecast_start_date = training_date_to + relativedelta(days=1)
    forecast_data,actual_data,  title = as_is_to_be_analysis_get_data(selected_ticker,
                                                                      explorative_date_from,
                                                                      explorative_date_to,
                                                                      training_date_from,
                                                                      training_date_to,
                                                                      forecast_start_date,
                                                                      count_of_forecast_periods)

    forecast_end_date = forecast_start_date + relativedelta(days=count_of_forecast_periods)

    # Übersetzung
    st.markdown(
        f"""
                  <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                      Explorative Anaylse (Actual)
                  </div>
                """,
        unsafe_allow_html=True
    )

    create_actual_line_chart(actual_data, explorative_date_from, explorative_date_to, selected_ticker)

    # Eine horizontale ein Pixel Linie hinzufügen
    draw_line(1)


    st.markdown(
        f"""
              <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                  Forecast vs. Ist-Daten
              </div>
            """,
        unsafe_allow_html=True
    )
    st.write('')


    create_is_plan_line_chart(forecast_data,forecast_start_date,forecast_end_date,selected_ticker)





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

                forecast_data.to_excel(rf'{store_location_path}/Forecast vs. Actual.xlsx',
                                          sheet_name='Forecast vs. Actual',
                                          index=False)

                actual_data.to_excel(rf'{store_location_path}/Explorative Data.xlsx',
                                       sheet_name='Explorative Data',
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