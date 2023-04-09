#import module
import requests
from flask import Flask, request, Response
from bs4 import BeautifulSoup
from googlesearch import search  


#membuka url
TOKEN ='5941067459:AAFKIIc4FZF1mMGsvNaUYdAmuHdtv8H26uA'
webhook = 'https://be1e-178-128-22-127.ap.ngrok.io'
url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook}"
buka_url = requests.get(url)


def inbox(message):
    id_pesan = message['message']['chat']['id']
    global pesan_masuk
    pesan_masuk = message['message']['text']
    global nama_depan
    nama_depan = message["message"]["chat"]["first_name"]
    #nama_belakang = message["message"]["chat"]["last_name"]
    #global nama
    #nama = nama_depan + " " + nama_belakang
    return id_pesan, pesan_masuk

def kirim_pesan(id_pesan, pesan):
    url_send = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id' : id_pesan,
        'text' : pesan
    }
    req_1 = requests.post(url_send, json = payload)
    return req_1

def main():
    welcome = f'''
    Selamat Datang {nama_depan}, silahkan masukkan pertanyaan anda!!!
    Catatan:
    1. Jika hasil pencarian tidak ditampilkan maka ubahlah bentuk pencarian
    2. Waktu yang dibutuhkan untuk melakukan pencarian maksimal 5 detik
    '''
    return welcome

def brainly():
    print('process')
    cari = f"{pesan_masuk} brainly"

    links = []

    for j in search(cari, tld="co.id", num=20, stop=20, pause=2): 
        if 'https://brainly.co.id/tugas/' in j:
            links.append(j)

    
    data = []

    try:
        for a in range(0,3):
            html = requests.get(links[a])
            soup = BeautifulSoup(html.content,'html.parser')
            jawaban_terverifikasi = soup.find('div',attrs={'data-testid':"answer_box_text"}).get_text()
            clear_data = jawaban_terverifikasi.replace('\n','')
            data.append(clear_data)

        jawaban = f'{data[0]}'
        return jawaban

    except:
        print('gagal')
        jawaban = 'Mohon maaf kami tidak dapat menyelesaikan pertanyaan tersebut'
        return jawaban

#main program
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        id_pesan,pesan_masuk = inbox(msg)

        if pesan_masuk == "/start":
            kirim_pesan(id_pesan, main())
        else:
            kirim_pesan(id_pesan, brainly())
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"

if __name__ == '__main__':
   app.run(debug=True)