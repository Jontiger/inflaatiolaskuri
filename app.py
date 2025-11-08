import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# =====================================================
# 📄 1. PERUSASETUKSET JA TYYLI
# =====================================================

st.set_page_config(layout="wide")


st.markdown("""
    <style>
        /* --- Päivitetyt korttivärit teemaan sopiviksi --- */
        .inflaatio-card {
            background-color: #E0F2F1;
            padding: 10px 16px;
            border-radius: 10px;
            border: 1px solid #009688;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
            text-align: center;
            margin: 6px;
        }
        .inflaatio-card p {
            color: #003333;
            margin: 0;
        }
        .inflaatio-card .label {
            font-size: 13px;
            color: #00695C;
        }
        .inflaatio-card .value {
            font-size: 19px;
            font-weight: bold;
            color: #004D40;
        }
    </style>
""", unsafe_allow_html=True)



# =====================================================
# 🏷️ 2. OTSIKKO
# =====================================================

st.markdown("<h1 class='center'>Inflaatiolaskuri</h1>", unsafe_allow_html=True)


# =====================================================
# 📘 3. TEORIA JA OHJEET
# =====================================================

with st.expander("Mikä on inflaatio?"):
    st.markdown("""
        **Inflaatio** tarkoittaa yleistä hintatason nousua taloudessa.  
        Kun hinnat nousevat, samalla rahalla saa vähemmän tuotteita ja palveluita kuin ennen.

        Kaikki hinnat eivät kuitenkaan muutu samassa suhteessa.  
        Esimerkiksi jos vuosi sitten sait 10 eurolla ostettua paketin kahvia ja sama summa ei enää riitä tänään, se johtuu kahvin hinnan noususta.  
        Samalla on mahdollista, että 10 eurolla saa edelleen saman määrän jauhelihaa kuin aiemmin. Tämä osoittaa, että inflaatio vaikuttaa eri tuotteisiin eri tavoin.

        **Miksi inflaatiota silti mitataan yhdellä prosenttiluvulla?**  
        Yleinen inflaatio kuvaa kotitalouksien kulutuksen keskimääräistä hinnanmuutosta.  
        Se lasketaan kuluttajahintaindeksin avulla, jossa eri hyödykkeille annetaan painoarvot sen mukaan, kuinka suuren osan ne vievät kotitalouksien kokonaiskuluista.  
        Kun näiden hyödykkeiden hinnanmuutokset yhdistetään painojen mukaisesti, saadaan yksi prosenttiluku, joka kertoo, kuinka paljon hintataso on keskimäärin noussut koko taloudessa. Koko suomen talouden hintojen nouseminen ei tarkoita sitä, että juuri sinun menosi olisivat nousseet samalla tavalla.
    """)



with st.expander("Ohjeet"):
    st.markdown("""
    Syötä kuukausittaiset menosi eri kulutuskategorioihin, jotta laskuri voi arvioida henkilökohtaisen inflaatiosi.  
    Sovellus hyödyntää Tilastokeskuksen kuluttajahintaindeksiä ja vertaa kulutustietojasi yleiseen hintatason kehitykseen arvioidakseen, miten hinnanmuutokset ovat vaikuttaneet ostovoimaasi.  
    Lukujen ei tarvitse olla tarkkoja. Jos et tiedä tarkasti kulutustasi, voit antaa arvion.  
    Jos et ole käyttänyt rahaa johonkin kategoriaan, sen voi jättää nollaksi. Se ei vaikutta laskennan luotettavuuteen.  


    ---

    **Huomio:**  
    Näytetyt luvut ovat arvioita henkilökohtaisesta inflaatiostasi.  
    Todellinen inflaatio edellyttäisi kaikkien kuluttamiesi tuotteiden ja palveluiden tarkkaa seurantaa.  
    Tämä laskentatapa kuitenkin antaa luotettavan yleiskuvan siitä, miten oma hintatasosi on kehittynyt.  
    Kategoriat edustavat tavallisimpia kuukausittaisia kulutusalueita.  

    <p style='color:#ffb84d; font-weight:bold;'>Tämän sovelluksen data ulottuu syyskuuhun 2025 asti, ja laskuri antaa tulokset kyseiselle kuukaudelle. Tulokset kuvaavat hintojen muutosta verrattuna vuoden 2024 hintoihin..</p>
    """, unsafe_allow_html=True)


# =====================================================
# 🧮 4. DATAN LUKEMINEN JA KATEGORIAT
# =====================================================

df = pd.read_excel("cpi_master.xlsx", engine="openpyxl")

df["Päivämäärä"] = pd.to_datetime(df["Päivämäärä"], format="%d.%m.%Y", errors="coerce")

jarjestys = [
    "ASUMINEN, VESI, SÄHKÖ, KAASU JA MUUT POLTTOAINEET",
    "ELINTARVIKKEET JA ALKOHOLITTOMAT JUOMAT",
    "LIIKENNE",
    "VIESTINTÄ",
    "KULTTUURI JA VAPAA-AIKA",
    "RAVINTOLAT JA HOTELLIT",
    "VAATETUS JA JALKINEET",
    "ALKOHOLIJUOMAT, TUPAKKA"
]

kategoriat = [orig for orig in df["Kategoria"].unique() if orig.strip().upper() in jarjestys]
kategoriat = sorted(kategoriat, key=lambda x: jarjestys.index(x.strip().upper()))


# =====================================================
# 🧾 5. KÄYTTÖLIITTYMÄ: KULUT JA PALKKA
# =====================================================

col1, col2 = st.columns([2, 1])

# --- Kulut ---
col1.subheader("Kuukausittaiset kulut (€)")
kulut = {}

selitteet = {
    "ASUMINEN, VESI, SÄHKÖ, KAASU JA MUUT POLTTOAINEET": (
        "Asumisen ja energiankulutuksen kustannukset. "
        "Sisältää vuokran, lainanlyhennykset, vastikkeet, sähkön, veden, lämmityksen, maakaasun ja muut asumiseen liittyvät polttoaineet."
    ),

    "ELINTARVIKKEET JA ALKOHOLITTOMAT JUOMAT": (
        "Sisältää kaikki ruokaan ja alkoholittomiin juomiin liittyvät ostokset. "
        
    ),

    "LIIKENNE": (
        "Liikkumiseen liittyvät menot. "
        "Sisältää auton hankinnan, polttoaineet, huollot, vakuutukset ja julkisen liikenteen."
    ),

    "VIESTINTÄ": (
        "Yhteydenpitoon liittyvät palvelut. "
        "Sisältää matkapuhelin- ja internetliittymät, puhelinlaitteet ja postipalvelut."
    ),

    "KULTTUURI JA VAPAA-AIKA": (
        "Harrastukset, viihde ja vapaa-aika. "
        "Sisältää elokuvat, kirjat, pelit, urheilun, musiikin, harrastusvälineet, kulttuuripalvelut, lemmikit ja kotimaan matkailun."
    ),

    "RAVINTOLAT JA HOTELLIT": (
        "Ravintola- ja kahvilakulut sekä majoitus. "
        "Sisältää kodin ulkopuolisen ruokailun, baarit ja hotellit."
    ),

    "VAATETUS JA JALKINEET": (
        "Vaatteet, kengät ja asusteet. "
        "Sisältää myös pesula- ja korjauspalvelut."
    ),

    "ALKOHOLIJUOMAT, TUPAKKA": (
        "Alkoholi ja tupakkatuotteet. "
        "Sisältää oluen, viinin, väkevät alkoholijuomat, savukkeet ja muut tupakkatuotteet."
    )
}


for kategoria in kategoriat:
    kulut[kategoria] = col1.number_input(
        f"{kategoria}", min_value=0.0, value=0.0, step=50.0, key=f"kulut_{kategoria}"
    )
    col1.caption(selitteet.get(kategoria, ""))


# --- Palkka ---
col2.subheader("Palkka (€)")
palkka = col2.number_input("Mikä oli palkkasi vuosi sitten?", min_value=0.0, value=3000.0, step=100.0)

with col2.expander("💬 Miksi palkkasi kysytään?"):
    st.markdown("Palkkatieto tarvitaan, jotta laskuri voi arvioida reaalipalkkasi.")


# =====================================================
# 🔢 6. LASKENTA
# =====================================================

if sum(kulut.values()) > 0:
    painot = {k: v / sum(kulut.values()) for k, v in kulut.items()}
else:
    painot = {k: 0 for k in kategoriat}

yleinen_df = df[df["Kategoria"].str.upper() == "KULUTTAJAHINTAINDEKSI"].sort_values("Päivämäärä")
yleinen_df["Yleinen inflaatio"] = yleinen_df["Pisteluku"].pct_change(12) * 100

dates = sorted(df["Päivämäärä"].unique())
hist_values = []

for date in dates:
    muutos = {}
    for kategoria in kategoriat:
        data_kat = df[df["Kategoria"] == kategoria].sort_values("Päivämäärä")
        current_idx = data_kat.index[data_kat["Päivämäärä"] == date]
        if len(current_idx) == 0:
            muutos[kategoria] = None
            continue
        idx_pos = data_kat.index.get_loc(current_idx[0])
        if idx_pos < 12:
            muutos[kategoria] = None
            continue
        prev_idx = idx_pos - 12
        muutos[kategoria] = (data_kat.iloc[idx_pos]["Pisteluku"] /
                             data_kat.iloc[prev_idx]["Pisteluku"] - 1) * 100
    val = sum((muutos[k] or 0) * painot.get(k, 0) for k in kategoriat)
    hist_values.append(val)

hist_df = pd.DataFrame({
    "Päivämäärä": dates,
    "Henkilökohtainen inflaatio": hist_values,
})
hist_df = hist_df.merge(yleinen_df[["Päivämäärä", "Yleinen inflaatio"]], on="Päivämäärä", how="left")
hist_df = hist_df[hist_df["Päivämäärä"] >= "2021-01-01"]

henk_inflaatio = hist_df["Henkilökohtainen inflaatio"].iloc[-1] if not hist_df.empty else 0
yleinen_inflaatio = hist_df["Yleinen inflaatio"].iloc[-1] if not hist_df.empty else 0
reaalipalkka = palkka / (1 + (henk_inflaatio or 0) / 100)

if reaalipalkka > palkka:
    reaalipalkka = palkka


# =====================================================
# 💳 7. LASKELMAN TULOKSET (KORTIT)
# =====================================================

st.markdown("<h3 style='text-align:center; margin-top:15px;'>Laskelman tulokset</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

card_style = """
<div class="inflaatio-card">
    <p class="label">{title}</p>
    <p class="value">{value}</p>
</div>
"""



with col1:
    st.markdown(card_style.format(title="Henkilökohtainen inflaatio", value=f"{henk_inflaatio:.2f} %"), unsafe_allow_html=True)
with col2:
    st.markdown(card_style.format(title="Yleinen inflaatio", value=f"{yleinen_inflaatio:.2f} %"), unsafe_allow_html=True)
with col3:
    st.markdown(card_style.format(title="Reaalipalkkasi nykyhinnoin", value=f"{reaalipalkka:.2f} €"), unsafe_allow_html=True)




# =====================================================
# 8 HINNAT NOUSUSSA VAI LASKUSSA
# =====================================================


latest_date = df["Päivämäärä"].max()
year_ago_date = latest_date - pd.DateOffset(years=1)
inflaatiot = {}

for kategoria in kategoriat:
    data_kat = df[df["Kategoria"] == kategoria].sort_values("Päivämäärä")
    if len(data_kat) == 0:
        inflaatiot[kategoria] = None
        continue
    current = data_kat[data_kat["Päivämäärä"] == latest_date]["Pisteluku"]
    prev = data_kat[data_kat["Päivämäärä"] == year_ago_date]["Pisteluku"]
    if not current.empty and not prev.empty:
        inflaatiot[kategoria] = (current.values[0] / prev.values[0] - 1) * 100
    else:
        inflaatiot[kategoria] = None

def inflaatio_vari(arvo):
    if arvo is None:
        return "#888888"
    elif arvo < 0:
        return "#4da6ff"  # sininen
    elif 0 <= arvo < 2:
        return "#ffbf00"  # keltainen
    elif 2 <= arvo < 4:
        return "#ff9933"  # oranssi
    else:
        return "#ef553b"  # punainen

# --- Uudet kortit: pääkortti (rahallinen muutos) + alikortti (prosentti) ---
cols = st.columns(2)

def euro_muutos_text(arvo):
    if arvo is None:
        return "–"
    return f"{arvo:+.1f} € / kk"

for i, kategoria in enumerate(kategoriat):
    osuus = (kulut[kategoria] / sum(kulut.values()) * 100) if sum(kulut.values()) > 0 else 0
    inflaatio = inflaatiot.get(kategoria)
    vari = inflaatio_vari(inflaatio)

    euro_muutos = None if inflaatio is None else kulut[kategoria] * (inflaatio / 100.0)

    # --- Pääkortti: iso rahallinen muutos ---
    paakortti = f"""
        <div style="
            background-color:#E0F2F1;
            padding:12px 18px;
            border-radius:12px;
            border:1px solid #009688;
            box-shadow:0 1px 4px rgba(0,0,0,0.15);
            margin-bottom:6px;">
            <p style="font-size:14px; color:#004D40; margin:0 0 4px 0;">{kategoria}</p>
            <p style="font-size:13px; color:#00695C; margin:0 0 6px 0;">
                Osuus kulutuksestasi: {osuus:.1f} %
            </p>
            <p style="font-size:22px; font-weight:700; color:#003333; margin:0;">
                {euro_muutos_text(euro_muutos)}
            </p>
        </div>
    """

    # --- Alikortti: prosenttimuutos ---
    inflaatio_txt = "–" if inflaatio is None else f"{inflaatio:+.1f} %"
    alikortti = f"""
        <div style="
            background-color:#D0ECEA;
            padding:8px 14px;
            border-radius:10px;
            border:1px solid #009688;
            box-shadow:0 1px 3px rgba(0,0,0,0.1);
            margin-bottom:12px;">
            <span style="font-size:12px; color:#004D40;">Korin yleinen muutos:</span>
            <span style="font-size:14px; font-weight:600; color:{vari}; margin-left:6px;">
                {inflaatio_txt}
            </span>
        </div>
    """

    with cols[i % 2]:
        st.markdown(paakortti, unsafe_allow_html=True)
        st.markdown(alikortti, unsafe_allow_html=True)




with st.expander("Miten tuloksia luetaan?"):
    st.markdown("""
Tuloksissa esitetään, miten kulutuksesi ja ostovoimasi ovat muuttuneet vuoden aikana.

**Yleinen inflaatio** kuvaa Suomen keskimääräistä hintojen nousua kuluttajahintaindeksin perusteella.  
Sitä käytetään vertailuarvona oman inflaation arvioinnissa.  

**Henkilökohtainen inflaatio** kertoo, kuinka paljon hintataso on noussut omien kulutustottumustesi perusteella.  
Jos henkilökohtainen inflaatio on korkeampi kuin yleinen inflaatio, sinun kulutuksesi on kallistunut keskimääräistä enemmän.  

**Reaalipalkka** näyttää palkkasi ostovoiman inflaation vaikutuksen jälkeen.  
Jos reaalipalkka on pienempi kuin viimevuotinen palkka, ostovoimasi on laskenut.  
Jos reaalipalkka on sama kuin viimevuotinen palkka, ostovoimasi on säilynyt suurin piirtein samana.  
Reaalipalkka ei voi olla nimellispalkkaa suurempi, sillä laskuri kuvaa ostovoimaa eikä palkankorotusta.



**Rahallinen muutos (€ / kk)** näyttää, kuinka paljon kyseisen menokategorian kustannukset ovat muuttuneet euroissa kuukaudessa verrattuna viimevuoden hintoihin.  
Se on laskettu omien kulutustietojesi perusteella.  

**Korin yleinen muutos (%)** kuvaa, kuinka paljon kyseisen kulutuskategorian hinnat ovat keskimäärin muuttuneet vuoden sisällä.  
Tämä perustuu Tilastokeskuksen kuluttajahintaindeksiin, ei yksittäisiin kulutustietoihisi.  

---

**Värien merkitykset:**

- 🔵 **Sininen:** hinnat ovat **laskeneet** (negatiivinen inflaatio)  
- 🟡 **Keltainen:** hinnat ovat **pysyneet lähes ennallaan** (0–2 %)  
- 🟠 **Oranssi:** hinnat ovat **nousseet maltillisesti** (2–4 %)  
- 🔴 **Punainen:** hinnat ovat **nousseet selvästi** (yli 4 %)
""")

# --- KULUTUSKORIN PAINOTUKSET ---
with st.expander(" Kulutuskorisi painotukset"):
    st.markdown("<h3 style='text-align:center;'>Kulutuskorisi painotukset</h3>", unsafe_allow_html=True)

    if sum(kulut.values()) > 0:
        kulut_df = pd.DataFrame({
            "Kategoria": list(kulut.keys()),
            "Summa": list(kulut.values())
        })
        kulut_df["Osuus (%)"] = kulut_df["Summa"] / kulut_df["Summa"].sum() * 100

        fig_paino = go.Figure(
            data=[go.Pie(
                labels=kulut_df["Kategoria"],
                values=kulut_df["Summa"],
                hole=0.55,
                textinfo="percent+label",
                hovertemplate="%{label}<br>%{value:.0f} € (%{percent})<extra></extra>",
                marker=dict(line=dict(color="#1a1a1a", width=2)),
                pull=[0.02]*len(kulut_df)
            )]
        )

        fig_paino.update_layout(
            template="plotly_white",
            showlegend=False,
            margin=dict(l=50, r=50, t=20, b=20),
            height=400,
        )

        st.plotly_chart(fig_paino, use_container_width=True)

    else:
        st.info("Syötä kuukausittaiset kulusi nähdäksesi kulutuskorisi painotukset.")


# =====================================================
# 9 INFLAATIOKEHITYS (kaikki viivat valittavissa)
# =====================================================

# --- Valintalistan tyylitys ---
st.markdown("""
    <style>
        div[data-baseweb="select"] {
            font-size: 13px !important;
        }
        div[data-baseweb="tag"] {
            background-color: #c27ba0 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 2px 6px !important;
            font-size: 12px !important;
            font-weight: 500 !important;
        }
        div[data-baseweb="popover"] div[role="listbox"] {
            font-size: 13px !important;
        }
        div[data-baseweb="select"] input {
            color: #eee !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Valintalista (kaavion alapuolella) ---
kaikki_vaihtoehdot = ["Sinun inflaatio", "Yleinen inflaatio"] + kategoriat
valitut_kategoriat = st.multiselect(
    "Valitse viivat",
    options=kaikki_vaihtoehdot,
    default=["Sinun inflaatio", "Yleinen inflaatio"],
    label_visibility="collapsed"
)

# --- Rakennetaan kaavio dynaamisesti ---
fig = go.Figure()

for kategoria in valitut_kategoriat:
    if kategoria == "Sinun inflaatio":
        fig.add_trace(go.Scatter(
            x=hist_df[hist_df["Päivämäärä"] >= "2021-01-01"]["Päivämäärä"],
            y=hist_df[hist_df["Päivämäärä"] >= "2021-01-01"]["Henkilökohtainen inflaatio"],
            mode="lines",
            name="Sinun inflaatio",
            line=dict(width=2.5, color="#c27ba0"),
            hovertemplate="Sinun inflaatio: %{y:.2f} %<extra></extra>"
        ))

    elif kategoria == "Yleinen inflaatio":
        fig.add_trace(go.Scatter(
            x=hist_df[hist_df["Päivämäärä"] >= "2021-01-01"]["Päivämäärä"],
            y=hist_df[hist_df["Päivämäärä"] >= "2021-01-01"]["Yleinen inflaatio"],
            mode="lines",
            name="Yleinen inflaatio",
            line=dict(width=2.5, color="#1f77b4"),
            hovertemplate="Yleinen inflaatio: %{y:.2f} %<extra></extra>"
        ))

    else:
        data_kat = df[df["Kategoria"] == kategoria].sort_values("Päivämäärä")
        data_kat["Muutos (%)"] = data_kat["Pisteluku"].pct_change(12) * 100
        data_kat = data_kat[data_kat["Päivämäärä"] >= "2021-01-01"]

        fig.add_trace(go.Scatter(
            x=data_kat["Päivämäärä"],
            y=data_kat["Muutos (%)"],
            mode="lines",
            name=kategoria,
            line=dict(width=2.5),
            hovertemplate=f"{kategoria}: "+"%{y:.2f} %<extra></extra>"
        ))

# --- Ulkoasu ---
fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    hoverlabel=dict(namelength=-1, font=dict(size=13)),
    legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center"),
    xaxis_title="Vuosi",
    yaxis_title="Inflaatio (%)",
    margin=dict(l=30, r=30, t=50, b=50),
    xaxis=dict(
        tickformat="%Y",
        range=["2021-01-01", hist_df["Päivämäärä"].max()]  # alkaa vuodesta 2021
    )
)
fig.update_xaxes(dtick="M12", tickformat="%Y", hoverformat="%b %Y")

st.plotly_chart(fig, use_container_width=True)

with st.expander("Mikä tämä kaavio on?", expanded=False):
    st.markdown("""
Tämä kaavio esittää **inflaation kehityksen vuodesta 2021 eteenpäin**.  
Voit tarkastella, miten **yleinen inflaatio**, **henkilökohtainen inflaatio**  
sekä valitsemasi **kulutuskategoriat** ovat muuttuneet ajan myötä.  

Kaavion avulla näet, onko oma hintatason kehityksesi ollut nopeampaa vai hitaampaa kuin Suomen keskiarvo.  
Voit piilottaa tai lisätä viivoja alla olevasta valikosta valitsemalla haluamasi kategoriat.
""")

with st.expander("Lähteet"):
    st.markdown("""
Sovelluksen inflaatiolaskenta perustuu Tilastokeskuksen viralliseen kuluttajahintaindeksiin (CPI) sekä taloustieteen kirjallisuuteen.

**Tilastokeskus** – [Kuluttajahintaindeksi (CPI)](https://stat.fi/tilasto/khi)  

**Pohjola, Matti (2019).** *Taloustieteen oppikirja.* (s. 198)
""")





























