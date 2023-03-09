
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_ = pd.read_csv("flo_data_20k.csv")
df = df_.copy()
df.head(10)
df.info()
df.describe().T
df.isnull().sum()



df["total_shopping"] = df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]
df["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

df['first_order_date'] = pd.to_datetime(df['first_order_date'])
df['last_order_date'] = pd.to_datetime(df['last_order_date'])
df['last_order_date_online'] = pd.to_datetime(df['last_order_date_online'])
df['last_order_date_offline'] = pd.to_datetime(df['last_order_date_offline'])

df["order_channel"].value_counts()
df["total_shopping"].describe()
df["total_spending"].describe()
df["total_shopping"].value_counts()
df.groupby("master_id")["total_spending"].sum().nlargest(10)
df.groupby("master_id")["total_shopping"].sum().nlargest(10)

def prep(dataframe):

    dataframe["total_shopping"] = dataframe["order_num_total_ever_offline"] + dataframe["order_num_total_ever_online"]
    dataframe["total_spending"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    dataframe['first_order_date'] = pd.to_datetime(dataframe['first_order_date'])
    dataframe['last_order_date'] = pd.to_datetime(dataframe['last_order_date'])
    dataframe['last_order_date_online'] = pd.to_datetime(dataframe['last_order_date_online'])
    dataframe['last_order_date_offline'] = pd.to_datetime(dataframe['last_order_date_offline'])

    print(dataframe["order_channel"].value_counts())
    print(dataframe["total_shopping"].describe())
    print(dataframe["total_spending"].describe())

    print(dataframe.groupby("master_id")["total_spending"].sum().nlargest(10))
    print(dataframe.groupby("master_id")["total_shopping"].sum().nlargest(10))

    return dataframe

prep(df)


# GÖREV 2: RFM Metriklerinin Hesaplanması



df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)



rfm = df.groupby('master_id').agg({'last_order_date': lambda date: (today_date - date.max()).days,
                                            'total_shopping': lambda num: num.sum(),
                                            "total_spending": lambda price: price.sum()})



rfm.reset_index(inplace=True)
rfm.columns = ["customer", 'recency', 'frequency', "monetary"]
rfm.head()



# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm = rfm[["customer", "recency", "frequency", "monetary", "segment"]]
rfm.index = rfm.index.astype(int)


# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                   # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                   # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                   # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
                   # alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
                   # olarak kaydediniz.

rfm.describe()
rfm.head()
rfm.info()



target_customers = rfm[((rfm['segment'] == 'champions') | (rfm['segment'] == 'loyal_customers'))]
avg_spent = target_customers.groupby('customer')['monetary'].mean().reset_index()
avg_spent.columns = ['master_id', 'Avg_Monetary']
qualified_customers = avg_spent[avg_spent['Avg_Monetary'] >= 250]

female_cat = df[df['interested_in_categories_12'].str.contains('KADIN')]

target_customers = qualified_customers.merge(female_cat, on='master_id')

target_customers[["master_id"]].to_csv("yeni_marka_hedef_müşteri_id", index=False)

# GÖREV 6: Tüm süreci fonksiyonlaştırınız.

def select_customer(dataframe, csv=False):
    dataframe["total_shopping"] = dataframe["order_num_total_ever_offline"] + dataframe["order_num_total_ever_online"]
    dataframe["total_spending"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    dataframe['first_order_date'] = pd.to_datetime(dataframe['first_order_date'])
    dataframe['last_order_date'] = pd.to_datetime(dataframe['last_order_date'])
    dataframe['last_order_date_online'] = pd.to_datetime(dataframe['last_order_date_online'])
    dataframe['last_order_date_offline'] = pd.to_datetime(dataframe['last_order_date_offline'])

    print(dataframe["order_channel"].value_counts())
    print(dataframe["total_shopping"].describe())
    print(dataframe["total_spending"].describe())

    print(dataframe.groupby("master_id")["total_spending"].sum().nlargest(10))
    print(dataframe.groupby("master_id")["total_shopping"].sum().nlargest(10))

    today_date = dt.datetime(2021, 6, 1)
    rfm = df.groupby('master_id').agg({'last_order_date': lambda date: (today_date - date.max()).days,
                                       'total_shopping': lambda num: num.sum(),
                                       "total_spending": lambda price: price.sum()})

    rfm.reset_index(inplace=True)
    rfm.columns = ["customer", 'recency', 'frequency', "monetary"]

    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["customer", "recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)


    target_customers = rfm[((rfm['segment'] == 'champions') | (rfm['segment'] == 'loyal_customers'))]
    avg_spent = target_customers.groupby('customer')['monetary'].mean().reset_index()
    avg_spent.columns = ['master_id', 'Avg_Monetary']
    qualified_customers = avg_spent[avg_spent['Avg_Monetary'] >= 250]

    female_cat = df[df['interested_in_categories_12'].str.contains('KADIN')]

    target_customers = qualified_customers.merge(female_cat, on='master_id')


    if csv:
    target_customers[["master_id"]].to_csv("yeni_marka_hedef_müşteri_id", index=False)

    return rfm


select_customer(df,csv=True)

###############################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################


# 2. Veri setinde
        # a. İlk 10 gözlem,
        # b. Değişken isimleri,
        # c. Boyut,
        # d. Betimsel istatistik,
        # e. Boş değer,
        # f. Değişken tipleri, incelemesi yapınız.



# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.



# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.


# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)



# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız. 



# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.




# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.




# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.


###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi



# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe


###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi




# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi


###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme


###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.



# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.



# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.
