import streamlit as st
import pandas as pd
import numpy as np
import sklearn
import pickle

# Sayfa Bilgileri
st.set_page_config(page_title="Kredi Uygunluğu", page_icon=":bank:", layout="wide")

st.markdown("<h1 style='text-align: center; font-size: 40px;'>Arat Banka Hoşgeldiniz!</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 20px;'>Aşağıda verilen gerekli bilgileri girerek müşterinin kredi uygunluğuna karar verebilirsiniz.</h1>", unsafe_allow_html=True)
st.markdown("---")

# Eğitilmiş modeli yüklemek
pickle_in = open('classifier.pkl', 'rb') 
model = pickle.load(pickle_in)

# Kullanıcı girdisi
Gender_input = st.selectbox(label = 'Başvuru sahibinin cinsiyeti nedir?', options = ("Erkek", "Kadın"))
Married_input = st.selectbox(label = 'Başvuru sahibi medeni hali', options = ("Evli", "Bekar"))
Dependents_input = st.selectbox(label = 'Başvuru sahibinin bakmakla yükümlü olduğu kişi sayısı kaçtır?', options = ("0"," 1", "2", "3+"))
Education_input = st.selectbox(label = 'Başvuru sahibinin eğitim seviyesi nedir?', options = ("Lisansüstü", "Lisans"))
Self_Employed_input = st.selectbox(label = 'Başvuru sahibi kendi işinin sahibi midir?', options = ("Evet", "Hayır"))
ApplicantIncome_input = st.slider(label = 'Başvuru sahibinin geliri ne kadardır?', min_value = 0, max_value = 100000)
CoapplicantIncome_input = st.slider(label = 'Başvuru sahibiyle birlikte başvuran kişinin geliri nedir?', min_value = 0.0, max_value = 50000.0)
LoanAmount_input = st.slider(label = 'İstenilen kredinin tutarı bin cinsinden ne kadardır?', min_value = 0.0, max_value = 1000.0)
Loan_Amount_Term_input = st.slider(label = 'İstenilen kredinin vadesi ay cinsinden ne kadardır?', min_value = 0.0, max_value = 480.0, step=1.0)
Credit_History_input = st.selectbox(label = 'Başvuru sahibinin kredi geçmişi var mı?', options = (1.0, 0.0))
Property_Area_input = st.selectbox(label = 'Kredi istenilen mülk alanı nerededir?', options = ("Yarı Kentsel", "Kentsel", "Kırsal"))

st.markdown("<h1 style='text-align: center; font-size: 40px;'>Başvuru Sahibinin Özet Bilgileri:</h1>", unsafe_allow_html=True)
summary_dictionary = {'Cinsiyeti': Gender_input,  'Medeni Hali': Married_input, 'Bağımlı Sayısı': Dependents_input, 'Eğitim': Education_input,  'Kendi İşi': Self_Employed_input,
'Geliri': ApplicantIncome_input, 'Birlikte Başvuranın Geliri': CoapplicantIncome_input, 'Kredi Miktarı': LoanAmount_input, 'Kredi Vadesi': Loan_Amount_Term_input,
'Kredi Geçmişi': Credit_History_input, 'Mülk Alanı': Property_Area_input}

summary_df  = pd.DataFrame([summary_dictionary])
st.table(summary_df)

# kullanıcının girdiği verileri kullanarak tahmin yapacak fonksiyonu tanımlama

def predict_(model, Gender_input, Married_input, Dependents_input, Education_input, Self_Employed_input, ApplicantIncome_input, CoapplicantIncome_input, LoanAmount_input,
 Loan_Amount_Term_input, Credit_History_input, Property_Area_input):
    
    # kullanıcı girdisini ön işleme
    if Gender_input == "Erkek":
        Gender_var = "Male"
    else:
        Gender_var = "Female"
    
    if Married_input == "Evli":
        Married_var = "Yes"
    else:
        Married_var = "No"

    if Education_input == "Lisansüstü":
        Education_var = "Graduate"
    else:
        Education_var = "Not Graduate"

    if Self_Employed_input == "Evet":
        Self_Employed_var = "Yes"
    else:
        Self_Employed_var = "No"
    
    if Property_Area_input == "Yarı Kentsel":
        Property_Area_var = "Semiurban"
    elif Property_Area_input == "Kentsel":
        Property_Area_var = "Urban"
    else:
        Property_Area_var = "Rural"

    features = {'Gender': Gender_var,  'Married': Married_var, 'Dependents': Dependents_input, 'Education': Education_var,  'Self_Employed': Self_Employed_input, 
    'ApplicantIncome': ApplicantIncome_input, 'CoapplicantIncome': CoapplicantIncome_input, 'LoanAmount': LoanAmount_input, 'Loan_Amount_Term': Loan_Amount_Term_input,
    'Credit_History': Credit_History_input, 'Property_Area': Property_Area_var}

    features_df  = pd.DataFrame([features])
    
    prediction_ = model.predict(features_df)

    if prediction_ == 0:
        pred = 'red edildi.'
    else:
        pred = 'onaylandı.'
    
    return pred

# Tahmin butonuna tıklandığında, kaydedilmiş modelden tahmin elde et ve yazdır
st.markdown("---")

st.markdown("<h1 style='text-align: left; font-size: 20px;'>Girilen bilgilere göre başvuru sahibine kredi verilip verilmemesini öğrenmek için aşağıdaki butona tıklayınız:</h1>", unsafe_allow_html=True)

if st.button('Kredi verilsin mi?'):
    
    result_ = predict_(model, Gender_input, Married_input, Dependents_input, Education_input, Self_Employed_input, ApplicantIncome_input, CoapplicantIncome_input, LoanAmount_input, Loan_Amount_Term_input, Credit_History_input, Property_Area_input)

    if result_ == 'red edildi.':
        st.error('Krediniz {}'.format(result_))
    else:
        st.success('Krediniz {}'.format(result_))
        st.write(f'İstenilen kredi miktarı {LoanAmount_input * 1000: ,.2f} Türk lirasıdır.')

# ---- STREAMLIT STİLİNİ SAKLA ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)