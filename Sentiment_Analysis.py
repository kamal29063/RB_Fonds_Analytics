def run_Sentiment_Analysis(language_index):
    from transformers import pipeline, MarianMTModel, MarianTokenizer
    import streamlit as st
    import Centred_Title
    import Background_Style
    import Process_Button_Styling


    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)


    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    # Wahrscheinlichkeiten Erklärungen visualisieren
    def make_sidebar_metric(probability_text, probability_value):

        if probability_text =='Sehr sicher':
            text_color = 'green'
        elif probability_text =='Moderat sicher':
            text_color = '#FFD700'
        elif probability_text =='Unsicher':
            text_color = '#871614'

        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;color:{text_color};'> {probability_text}</h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:black; '>
                    {probability_value} 
                    </span>
                </h1>
               
            </div>
            """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')


    # Sentiment Score visualisieren
    def make_result_score_metric(score_text, score_value):


        if score_text == 'Positive':
            text_color = 'green'
        elif score_text == 'Neutral':
            text_color = '#FFD700'
        elif score_text == 'Negative':
            text_color = '#871614'


        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;color:{text_color};'> {score_text}</h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:black;'>
                    {score_value*100:.2f}%
                    </span>
                </h1>

            </div>
            """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')


    # Keywords metrics visualisieren
    def make_result_keywords_metric(keyword_type, keyword_value):



        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'> {keyword_type}</h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:black;'>
                    {keyword_value } 
                    </span>
                </h1>

            </div>
            """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')



    # Lade Modelle
    @st.cache_resource
    def load_translation_model():
        model_name = "Helsinki-NLP/opus-mt-de-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return pipeline("translation", model=model, tokenizer=tokenizer)

    @st.cache_resource
    def load_finbert():
        return pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

    @st.cache_resource
    def load_ner_model():
        return pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

    translator = load_translation_model()
    finbert = load_finbert()
    ner_model = load_ner_model()

    # Logo sidebar
    st.sidebar.image("Images/RB Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)
    st.sidebar.markdown(
        f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                    Wahrscheinlichkeiten
                </div>
                """,
        unsafe_allow_html=True
    )
    st.sidebar.write('')

    _,probability_col,_ = st.sidebar.columns([1,10000,1])
    with probability_col:

        make_sidebar_metric('Sehr sicher','86% – 100%')
        make_sidebar_metric('Moderat sicher', '66% – 85%')
        make_sidebar_metric('Unsicher', '50% – 65%')



    # Page Title
    Centred_Title.run_centred_title('Sentimentanalyse und Entitäts-Extraktion in Finanztexten mit FinBERT und NER')


    default_text = \
                """
                Ab dem 1. Januar 2023 tritt eine Änderung des Einkommensteuergesetzes in Kraft, die eine Erhöhung der Abgeltungssteuer auf Erträge aus Immobilienfonds vorsieht. Konkret steigt der Steuersatz von bisher 25 % auf 28 %. Diese Maßnahme betrifft sowohl private als auch institutionelle Anleger, die in Immobilienfonds investieren.
                Die Bundesregierung begründet diese Änderung mit der Notwendigkeit, die Steuerbasis zu verbreitern und zusätzliche Einnahmen für den Bundeshaushalt zu generieren. Ziel sei es, den gestiegenen Finanzierungsbedarf in Bereichen wie Klimaschutz, Infrastruktur und Bildung zu decken. Die Erhöhung der Abgeltungssteuer sei dabei ein Schritt in Richtung einer 'gerechteren Besteuerung', da sie insbesondere wohlhabendere Anleger stärker belaste.
                Kritiker aus der Immobilien- und Finanzbranche warnen jedoch vor negativen Folgen dieser Regelung. Sie argumentieren, dass die Attraktivität von Immobilienfonds als Anlagestrategie durch die höhere Steuer geschwächt werde. Vor allem Kleinanleger könnten sich durch die geringeren Renditen von Immobilieninvestitionen abwenden. Auch international könnte der deutsche Immobilienmarkt an Wettbewerbsfähigkeit verlieren, da vergleichbare Märkte in Europa wie Frankreich oder die Niederlande weiterhin mit niedrigeren Steuersätzen operieren.
                Einige Experten betonen zudem, dass die Steuererhöhung in einem wirtschaftlich schwierigen Umfeld erfolgt. Steigende Zinsen und hohe Baukosten haben bereits zu einer spürbaren Abkühlung im Immobiliensektor geführt. Die zusätzliche Steuerlast könnte diesen Trend verstärken und das Wachstum weiter dämpfen.
                Auf der anderen Seite sehen Befürworter der Regelung auch Chancen. Sie argumentieren, dass eine höhere Besteuerung spekulativer Immobilieninvestitionen langfristig dazu beitragen könnte, den überhitzten Immobilienmarkt zu beruhigen. Dies könnte dazu führen, dass Wohnraum für Durchschnittsverdiener wieder erschwinglicher wird.
                Die öffentliche Meinung zu der Gesetzesänderung ist gespalten. Während einige Bürger die Maßnahme als notwendig für eine gerechtere Steuerpolitik ansehen, befürchten andere, dass die Belastung für Kleinanleger und die Wirtschaft insgesamt zu hoch sein könnte. Eine abschließende Bewertung der Auswirkungen wird wohl erst nach Inkrafttreten der Regelung möglich sein."""


    positive_text = \
    """Ab dem 1. Januar 2023 wird die Abgeltungssteuer auf Erträge aus Immobilienfonds von 25 % auf 28 % erhöht. Diese Maßnahme ist Teil eines umfassenden Reformpakets der Bundesregierung, das darauf abzielt, die Steuereinnahmen zu erhöhen und gleichzeitig gezielte Entlastungen für private Anleger zu schaffen.
        Neben der Steuererhöhung führt die Regierung eine Reihe von Maßnahmen ein, die Anlegern und der Immobilienbranche zugutekommen sollen. So wird der Freibetrag für Kapitalerträge für Privatpersonen ab 2023 von 801 € auf 1.200 € erhöht. Dies bedeutet, dass vor allem Kleinanleger ihre ersten Gewinne aus Immobilienfonds weiterhin steuerfrei vereinnahmen können. Dadurch werden kleinere Investoren geschützt und ermutigt, langfristig in den stabilen deutschen Immobilienmarkt zu investieren.
        Ein weiteres positives Signal für Anleger ist die Einführung eines neuen Förderprogramms für nachhaltige Immobilienfonds. Fonds, die in umweltfreundliche Bauprojekte oder energieeffiziente Modernisierungen investieren, können von Steuervergünstigungen profitieren. Dies könnte nicht nur die Attraktivität dieser Fonds steigern, sondern auch einen wichtigen Beitrag zum Klimaschutz leisten. Gleichzeitig profitieren Anleger von stabileren Renditen, da der Markt für nachhaltige Immobilien stark wächst.
        Die Bundesregierung hat zudem angekündigt, die Transparenz und Planbarkeit für Anleger zu verbessern. So wird ein langfristiger Plan zur Steuerpolitik im Immobiliensektor veröffentlicht, der Investoren mehr Sicherheit für ihre Entscheidungen gibt. Die neuen Regelungen sollen sicherstellen, dass Immobilienfonds weiterhin eine attraktive und planbare Anlagestrategie für private und institutionelle Anleger bleiben.
        Befürworter der Reform betonen, dass die Steuererhöhung in Kombination mit den Erleichterungen und neuen Förderungen zu einer gerechteren und nachhaltigeren Steuerpolitik führt. Zudem wird erwartet, dass die höheren Steuereinnahmen genutzt werden, um den Wohnungsbau zu fördern und den Druck auf die angespannte Situation am Immobilienmarkt zu reduzieren. Langfristig könnten diese Maßnahmen dazu beitragen, bezahlbaren Wohnraum zu schaffen, was sowohl Investoren als auch der Gesellschaft insgesamt zugutekommt.
        Insgesamt zeigt die Reform, dass die Bundesregierung nicht nur kurzfristige Einnahmen generieren möchte, sondern auch Maßnahmen ergreift, um den Immobiliensektor nachhaltiger, transparenter und zukunftsfähiger zu gestalten.
    """
    user_input = st.text_area("Gesetzestext (Deutsch):",
                              height=500,
                              value=default_text)

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)


    if st.button("Text Analysieren"):

        if user_input.strip():#

            translated_text = translator(user_input)[0]['translation_text']

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)
            # Übersetzung
            st.markdown(
                f"""
                           <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                               Übersetzung ins Englische
                           </div>
                           """,
                unsafe_allow_html=True
            )
            st.write('')


            st.write(translated_text)

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            # Sentiment-Analyse
            st.markdown(
                f"""
               <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                  Sentiment-Score und Keywords
               </div>
               """,
                unsafe_allow_html=True
            )
            st.write('')

            # Übersetzung
            sentiment = finbert(translated_text)



            for result in sentiment:
                result_text = result['label']
                result_value = result['score']
                make_result_score_metric(result_text,result_value)


            st.write('')
            st.write('')

            # NER KEWWORDS
            entities = ner_model(translated_text)

            keywords_col_one, keywords_col_two, keywords_col_three, keywords_col_four = st.columns(4)
            with keywords_col_one:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 1:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1

            with keywords_col_two:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 2:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1


            with keywords_col_three:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 3:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1



            with keywords_col_four:

                iteration = 1
                for entity in entities:
                    if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1




        else:
            st.warning("Bitte gib einen Text ein.")




    st.write('')
    st.write('')
    st.write('')
    st.write('')

    # "Created by K. B."
    st.write(f'**Erstellt von K. B.**')