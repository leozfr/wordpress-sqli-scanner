<p align="center">
  <img src="assets/banner.png" alt="WordPress SQLi Scanner Banner" />
</p>

# WordPress Plugin SQL Injection Scanner 🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)

Bu proje, Google Dorklar kullanarak WordPress eklentileri üzerinden siteleri bulur,  
SQL Injection (SQLi) zaafiyetlerini test eder, başarılı olursa **otomatik olarak sqlmap başlatıp veritabanı bilgisini çeker**  
ve tüm verileri **düzenli bir şekilde kayıt eder.**

---

## 📚 İçindekiler

- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Notlar](#-notlar)
- [Lisans](#-lisans)
- [Lisans](#-screenshot)
- [Yasal Uyarı](#-yasal-uyarı)

---

## 🎯 Özellikler

- 🔎 **Google Dorklar ile Site Bulma** (plugin bazlı odaklı arama)
- 🔥 **SQL Injection Payloadlarıyla Test Etme**
- 🛡️ **Proxy Desteği** (isteğe bağlı açık/kapalı)
- 🚀 **Multi-threaded** Çoklu site tarama (hızlı)
- 📂 **Denenmiş Siteleri Kaydetme ve Atlamak**
- 🧠 **Başarılı SQL Injection Sonrası Otomatik `sqlmap` ile DB Dump**
- 📄 **Dump edilen verileri otomatik dosyaya kaydetme**

---

## 🛠️ Kurulum

1. Python bağımlılıklarını yükleyin:

```bash
pip install requests googlesearch-python
```
---
## 🚀 Kullanım

Ana scripti çalıştırın:
python scanner.py

---

## ⚡ Notlar

* Script multi-thread çalışır ve aynı anda birçok siteyi hızlıca tarar.
* Proxy kullanımı isteğe bağlıdır. (Başlangıçta seçenek sunulur.)
* sqlmap otomatik çalıştırılırken:
* --batch ➔ Tüm sorulara otomatik evet denir.
* --dump ➔ Veritabanı tabloları ve içerikleri çekilir.
* Çıktılar organize şekilde results/ klasöründe tutulur.
* Proje Python 3.8+ sürümleriyle uyumludur.

---
## 📜 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

MIT Lisansı, size özgürce kullanma, değiştirme ve dağıtma hakkı verir; ancak herhangi bir garanti vermez.

---
## 📷 Screenshot
Aşağıda WordPress SQL Injection tarayıcısının başarılı bir örnek çıktısını görebilirsiniz:
![Result](assets/results-screenshot.png)

## ⚖️ Yasal Uyarı
✍️ Bu proje yalnızca eğitim ve araştırma amaçlıdır.
Bu script yalnızca izinli sistemler üzerinde kullanılmalıdır.
İzinsiz kullanım, yürürlükteki yasaları ihlal edebilir ve cezai sorumluluk doğurabilir.
Kullanıcı, bu scripti kullanırken doğabilecek tüm yasal sonuçlardan kendi sorumludur.
---