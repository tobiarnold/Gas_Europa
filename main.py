import streamlit as st
import yfinance as yf
import requests
from datetime import date, timedelta
import pandas as pd
import altair as alt
#import time


def main():
    st.set_page_config(page_title="Gasfüllstände Europa", page_icon="🇪🇺", layout="centered")
    st.title("🇪🇺 Gasfüllstände Europa")
    #st.write("Die folgende Anwendung greift auf die API des AGSI (Aggregated Gas Storage Inventory) zu und gibt die Gasfüllstände zurück.")
    st.write("""
    - Die folgende Anwendung gibt die Gasfüllstände verschiedener europäischer Länder und den Erdgaspreis am Weltmarkt zurück.
    - Es können maximal die letzten 900 Tage ausgehend vom heutigen Datum betrachtet werden
    - Standardmäßig sind als Betrachtungszeitraum die letzten 365 Tage eingestellt
    """)
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
            (date.today()-timedelta(days=900)), date.today(), (date.today()-timedelta(days=365), date.today()),format="DD/MM/YY")
        size = (int((start_end[-1] - start_end[0]).days))
        differenz=size
        if size >= 300:
            size = 300
        elif size<300:
            size=size
        if differenz < 300 and land !="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?country=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            r1 = requests.get(url1, headers=headers)
            data1 = r1.json()
            json_data1 = data1["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df = df1
        elif differenz >= 300 and differenz <=600 and land !="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?country=" + land + "&from=" + str(start_end[0]) + "&to=" + str(
                start_end[-1]) + "&page=1&size=" + str(size))
            last_page = (int((start_end[-1] - start_end[0]).days) - 300)
            url2 = (r"https://agsi.gie.eu/api?country=" + land + "&from" + str(start_end[0]-timedelta(days=302)) + "&to=" + str(start_end[-1]-timedelta(days=302)) + "&page=1&size=" + str(last_page))
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
        elif differenz >600 and land != "eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?country=" + land + "&from=" + str(start_end[0]) + "&to=" + str(
                start_end[-1]) + "&page=1&size=" + str(size))
            url2 = (r"https://agsi.gie.eu/api?country=" + land + "&from=" + str(start_end[0]) + "&to=" + str(
                start_end[-1]) + "&page=2&size=" + str(size))
            last_page = (int((start_end[-1] - start_end[0]).days) - 600)
            url3 = (r"https://agsi.gie.eu/api?country=" + land + "&from" + str(start_end[0]) + "&to=" +  str(start_end[0]-timedelta(days=602)) + "&to=" + str(start_end[-1]-timedelta(days=602)) + "&page=1&size=" + str(last_page))
            r1 = requests.get(url1, headers=headers)
            r2 = requests.get(url2, headers=headers)
            r3 = requests.get(url3, headers=headers)
            data1 = r1.json()
            data2 = r2.json()
            data3 = r3.json()
            json_data1 = data1["data"]
            json_data2 = data2["data"]
            json_data3 = data3["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df2 = pd.DataFrame.from_dict(json_data2)
            df3 = pd.DataFrame.from_dict(json_data3)
            frames = [df1, df2, df3]
            df = pd.concat(frames)
        elif differenz < 300 and land =="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?type=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            r1 = requests.get(url1, headers=headers)
            data1 = r1.json()
            json_data1 = data1["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df = df1
        elif differenz >= 300 and differenz <=600 and land =="eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?type=" + land + "&from=" + str(start_end[0]) + "&to=" + str(start_end[-1]) + "&page=1&size=" + str(size))
            last_page = (int((start_end[-1] - start_end[0]).days) - 300)
            url2 = (r"https://agsi.gie.eu/api?type=" + land + "&from" + str(start_end[0]-timedelta(days=302)) + "&to=" + str(start_end[-1]-timedelta(days=302)) + "&page=1&size=" + str(last_page))
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
        elif differenz > 600 and land == "eu":
            headers = {"x-key": "38babf682b901932a802d667aa2085c4"}
            url1 = (r"https://agsi.gie.eu/api?type=" + land + "&from=" + str(start_end[0]) + "&to=" + str(
                start_end[-1]) + "&page=1&size=" + str(size))
            url2 = (r"https://agsi.gie.eu/api?type=" + land + "&from=" + str(start_end[0]) + "&to=" + str(
                start_end[-1]) + "&page=2&size=" + str(size))
            last_page = (int((start_end[-1] - start_end[0]).days) - 600)
            url3 = (r"https://agsi.gie.eu/api?type=" + land + "&from" + str(start_end[0]) + "&to="+ str(start_end[0]-timedelta(days=602)) + "&to=" + str(start_end[-1]-timedelta(days=602)) + "&page=1&size=" + str(last_page))
            r1 = requests.get(url1, headers=headers)
            r2 = requests.get(url2, headers=headers)
            r3 = requests.get(url3, headers=headers)
            data1 = r1.json()
            data2 = r2.json()
            data3 = r3.json()
            json_data1 = data1["data"]
            json_data2 = data2["data"]
            json_data3 = data3["data"]
            df1 = pd.DataFrame.from_dict(json_data1)
            df2 = pd.DataFrame.from_dict(json_data2)
            df3 = pd.DataFrame.from_dict(json_data3)
            frames = [df1, df2, df3]
            df = pd.concat(frames)
        df = df.reset_index()
        df.drop(["index","name", "url", "info", "code", "consumption", "consumptionFull", "workingGasVolume","injectionCapacity", "withdrawalCapacity", "status"], axis=1, inplace=True)
        df = df.rename({"gasDayStart": "Datum (J-M-T)", "gasInStorage": "Gasvorrat in TWh", "injection": "Zufluss in GWh/d","withdrawal": "Abfluss in GWh/d", "trend": "Trend in %", "full": "Füllstand in %"},axis=1)
        df = df[["Datum (J-M-T)", "Füllstand in %", "Trend in %", "Gasvorrat in TWh", "Zufluss in GWh/d","Abfluss in GWh/d"]]
        df["Datum (J-M-T)"] = pd.to_datetime(df["Datum (J-M-T)"], format="%Y-%m-%d").dt.date
        cols = ["Gasvorrat in TWh", "Zufluss in GWh/d", "Abfluss in GWh/d", "Füllstand in %", "Trend in %"]
        df[cols] = df[cols].apply(pd.to_numeric, errors="coerce", axis=1)
        df["Differnz Zu- und Abfluss in GWh/d"]=df["Zufluss in GWh/d"]-df["Abfluss in GWh/d"]
        df_diagram=df
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
                .map(style1, subset=["Trend in %"])
            st.dataframe(df_show)
        else:
            st.write("Datentabelle ist ausgeblendet.")
        st.markdown("""---""")
        st.subheader("📊 Diagramme")
        line = alt.Chart(df_diagram, title="Gasvorräte Füllstand in %").mark_line().encode(x="Datum (J-M-T):T",
                                                                                   y="Füllstand in %",
                                                                                   color=alt.value("#1F77B4"),
                                                                                   tooltip=["Datum (J-M-T):T",
                                                                                            "Füllstand in %:Q"]).interactive()
        st.altair_chart(line, use_container_width=True)
        base = alt.Chart(df_diagram.reset_index()).encode(x="Datum (J-M-T):T")
        line = alt.layer(
            base.mark_line().encode(y="Zufluss in GWh/d", color=alt.value("#4ee44e"),
                                    tooltip=["Datum (J-M-T)", "Zufluss in GWh/d"]).interactive(),
            base.mark_line().encode(y="Abfluss in GWh/d", color=alt.value("#FF7F7F"),
                                    tooltip=["Datum (J-M-T)", "Abfluss in GWh/d"]).interactive()
            .properties(title="Zufluss und Abfluss des Gas"))
        st.altair_chart(line, use_container_width=True)
        line = alt.Chart(df_diagram, title="Differenz Zu- und Abflüsse").mark_bar().encode(x="Datum (J-M-T):T",
                                                                                   y="Differnz Zu- und Abfluss in GWh/d",
                                                                                   color=alt.value("#1F77B4"),
                                                                                   tooltip=["Datum (J-M-T):T",
                                                                                            "Differnz Zu- und Abfluss in GWh/d:Q"]).interactive()
        st.altair_chart(line, use_container_width=True)
    except:
        st.write("⚠️Bitte andere Parameter wählen")
    try:
       # time.sleep(2)
        natural_gas = yf.download("NG=F", start=start_end[0], end=start_end[-1],auto_adjust=False)[["Close"]]
        natural_gas["Datum (J-M-T)"] = pd.to_datetime(natural_gas.index)
        natural_gas.columns = [col[0] for col in natural_gas.columns]  # Nur den ersten Level behalten
        natural_gas = natural_gas.rename(columns={"Close": "Schlusskurs in US$"})
        natural_gas["Datum (J-M-T)"] = pd.to_datetime(natural_gas.index)
        #natural_gas=natural_gas.to_frame()
        #natural_gas["Date"] = natural_gas.index
        #natural_gas["Date"] = pd.to_datetime( natural_gas["Date"], format="%Y-%m-%d").dt.date
        #natural_gas=natural_gas.rename(columns={"Date": "Datum (J-M-T)", "Close": "Schlusskurs in US$"})
        line = (
        alt.Chart(natural_gas, title="Erdgaspreis in US$")
        .mark_line()
        .encode(
            x="Datum (J-M-T):T",
            y="Schlusskurs in US$:Q",
            color=alt.value("#cc0000"),
            tooltip=["Datum (J-M-T):T", "Schlusskurs in US$:Q"],).interactive())
        st.altair_chart(line, use_container_width=True)
    except:
        st.write("⚠️Bitte andere Parameter wählen")
    st.write("Datenquelle: https://agsi.gie.eu/ und https://finance.yahoo.com/quote/NG%3DF/")

if __name__ == "__main__":
  main()
