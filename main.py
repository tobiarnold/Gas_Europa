import streamlit as st
import requests
from datetime import date #timedelta
import pandas as pd
import altair as alt

def main():
    st.set_page_config(page_title="Gasfüllstände Europa", page_icon="🇪🇺", layout="centered")
    st.title("🇪🇺 Gasfüllstände Europa")
    #st.write("Die folgende Anwendung greift auf die API des AGSI (Aggregated Gas Storage Inventory) zu und gibt die Gasfüllstände zurück.")
    st.write("Die folgende Anwendung gibt die Gasfüllstände verschiedener europäischer Länder zurück.")
    st.markdown("""----""")
    st.subheader("💡 Parameter auswählen")
    #st.write("Parameter auswählen")
    #with st.form('Form1'):
    option = st.selectbox(
        "Welches Land soll eingeblendet werden?",
        ("EU", "Belgien", "Bulgarien", "Dänemark",	"Deutschland", "Frankreich", "Italien",	"Kroatien",	"Niederlande", "Österreich", "Polen", "Portugal", "Rumänien", "Schweden", "Slowakei", "Spanien", "Tschechien", "Ungarn"),index=4)
    if option == "EU":
        land = "eu"
    elif option == "Belgien":
        land = "be"
    elif option == "Bulgarien":
        land = "bg"
    elif option == "Dänemark":
        land = "dk"
    elif option == "Deutschland":
        land = "de"
    elif option == "Frankreich":
        land = "fr"
    elif option == "Italien":
        land = "it"
    elif option == "Kroatien":
        land = "hr"
    elif option == "Niederlande":
        land = "nl"
    elif option == "Österreich":
        land = "at"
    elif option == "Polen":
        land = "pl"
    elif option == "Portugal":
        land = "pt"
    elif option == "Rumänien":
        land = "ro"
    elif option == "Schweden":
        land = "se"
    elif option == "Slowakei":
        land = "sk"
    elif option == "Spanien":
        land = "es"
    elif option == "Tschechien":
        land = "cz"
    elif option == "Ungarn":
        land = "hu"
    try:
        start_end = st.slider(
            "Start und Enddatum?",
            date(2021, 1, 1), date.today(), (date(2021, 1, 1), date.today()),format="DD/MM/YY")
        #(date.today()-timedelta(days=365), date.today())
        size = (int((start_end[-1] - start_end[0]).days))
        differenz=size
        if size >= 300:
            size = 300
        elif size<300:
            size=size
        if size < 300 and land !="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?country=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            r1 = requests.get(url1, headers=headers)
            data1 = r1.json()
            json_data1 = data1["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df = df1
        elif size >= 300 and land !="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?country=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            size_page2 = (int((start_end[-1] - start_end[0]).days) - 300)
            url2 = (r"https://agsi.gie.eu/api?country=" + land + "&from" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=2&size=" + str(size_page2))
            r1 = requests.get(url1, headers=headers)
            r2 = requests.get(url2, headers=headers)
            data1 = r1.json()
            data2 = r2.json()
            json_data1 = data1["data"]
            json_data2 = data2["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df2 = pd.DataFrame.from_dict(json_data2)
            frames = [df1, df2]
            df = pd.concat(frames)
        elif size < 300 and land =="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?type=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            r1 = requests.get(url1, headers=headers)
            data1 = r1.json()
            json_data1 = data1["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df = df1
        elif size >= 300 and land =="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?type=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            size_page2 = (int((start_end[-1] - start_end[0]).days) - 300)
            url2 = (r"https://agsi.gie.eu/api?type=" + land + "&from" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=2&size=" + str(size_page2))
            r1 = requests.get(url1, headers=headers)
            r2 = requests.get(url2, headers=headers)
            data1 = r1.json()
            data2 = r2.json()
            json_data1 = data1["data"]
            json_data2 = data2["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df2 = pd.DataFrame.from_dict(json_data2)
            frames = [df1, df2]
            df = pd.concat(frames)
        df = df.reset_index()
        df.drop(["index","name", "url", "info", "code", "consumption", "consumptionFull", "workingGasVolume","injectionCapacity", "withdrawalCapacity", "status"], axis=1, inplace=True)
        df = df.rename({"gasDayStart": "Datum (J-M-T)", "gasInStorage": "Gasvorrat in TWh", "injection": "Zufluss in GWh/d","withdrawal": "Abfluss in GWh/d", "trend": "Trend in %", "full": "Füllstand in %"},axis=1)
        df = df[["Datum (J-M-T)", "Füllstand in %", "Trend in %", "Gasvorrat in TWh", "Zufluss in GWh/d","Abfluss in GWh/d"]]
        df["Datum (J-M-T)"] = pd.to_datetime(df["Datum (J-M-T)"], format="%Y-%m-%d").dt.date
        cols = ["Gasvorrat in TWh", "Zufluss in GWh/d", "Abfluss in GWh/d", "Füllstand in %", "Trend in %"]
        df[cols] = df[cols].apply(pd.to_numeric, errors="coerce", axis=1)
        df["Differnz Zu- und Abfluss in GWh/d"]=df["Zufluss in GWh/d"]-df["Abfluss in GWh/d"]
        tabelle = st.radio("Datentabelle ein- oder ausblenden",("Einblenden", "Ausblenden"))
           # submitted = st.form_submit_button("Eingaben übernehmen")
        st.markdown("""---""")
        st.subheader("👩‍💻 Tabelle")
        if tabelle == "Einblenden":
            st.write("Du hast " + str(option) + " gewählt")
            st.text("Startdatum: " + str(start_end[0].strftime("%d-%m-%Y")) + "     Enddatum: " + str(
                start_end[-1].strftime("%d-%m-%Y")) + "     Differenz in Tagen: " + str(differenz))
            # df_show = df.style.set_precision(2)
            style1 = (lambda x: "background-color : #90EE90" if x > 0 else (
                "background-color : #FF7F7F" if x < 0 else "background-color : #ffffa1"))
            # df_show = df.style.applymap(style1, subset=["Trend in %"])
            df_show = df.style.format({"Gasvorrat in TWh": "{:,.4f}",
                                       "Zufluss in GWh/d": "{:,.2f}",
                                       "Abfluss in GWh/d": "{:,.2f}",
                                       "Trend in %": "{:,.2f}",
                                       "Füllstand in %": "{:,.2f}",
                                       "Differnz Zu- und Abfluss in GWh/d": "{:,.2f}"}) \
                .applymap(style1, subset=["Trend in %"])
            st.dataframe(df_show)
        else:
            st.write("Datentabelle ist ausgeblendet.")
        st.markdown("""---""")
        st.subheader("📊 Diagramme")
        line = alt.Chart(df, title="Gasvorräte Füllstand in %").mark_line().encode(x="Datum (J-M-T):T",
                                                                                   y="Füllstand in %",
                                                                                   color=alt.value("#1F77B4"),
                                                                                   tooltip=["Datum (J-M-T):T",
                                                                                            "Füllstand in %:Q"]).interactive()
        st.altair_chart(line, use_container_width=True)
        base = alt.Chart(df.reset_index()).encode(x="Datum (J-M-T):T")
        line = alt.layer(
            base.mark_line().encode(y="Zufluss in GWh/d", color=alt.value("#4ee44e"),
                                    tooltip=["Datum (J-M-T)", "Zufluss in GWh/d"]).interactive(),
            base.mark_line().encode(y="Abfluss in GWh/d", color=alt.value("#FF7F7F"),
                                    tooltip=["Datum (J-M-T)", "Abfluss in GWh/d"]).interactive()
            .properties(title="Zufluss und Abfluss des Gas"))
        st.altair_chart(line, use_container_width=True)
        line = alt.Chart(df, title="Differenz Zu- und Abflüsse").mark_bar().encode(x="Datum (J-M-T):T",
                                                                                   y="Differnz Zu- und Abfluss in GWh/d",
                                                                                   color=alt.value("#1F77B4"),
                                                                                   tooltip=["Datum (J-M-T):T",
                                                                                            "Differnz Zu- und Abfluss in GWh/d:Q"]).interactive()
        st.altair_chart(line, use_container_width=True)
    except:
        st.write("⚠️Bitte andere Parameter wählen")
    st.markdown("""----""")
    st.write("Datenquelle: https://agsi.gie.eu/")

if __name__ == "__main__":
  main()
