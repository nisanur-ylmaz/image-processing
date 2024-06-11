import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Tesseract OCR'ın yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    """
    Görüntüyü gri tonlamaya dönüştürür ve ardından ikili eşikleme uygular.
    OCR (Optical Character Recognition) kullanarak metni çıkarır.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Görüntüyü gri tonlamaya dönüştür
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # İkili eşikleme uygula
    return pytesseract.image_to_string(thresh, config='--psm 6')  # OCR kullanarak metni çıkar

def read_optik_form(file_path, poppler_path):
    """
    PDF dosyasını görüntüye dönüştürür, belirli bölgelerden metni çıkarır.
    """
    images = convert_from_path(file_path, poppler_path=poppler_path)  # PDF dosyasını görüntüye dönüştür
    image = np.array(images[0])  # İlk sayfayı numpy dizisine dönüştür
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Görüntüyü BGR renk formatına dönüştür
    
    # Okul numarası bölgesi (koordine göre ayarlanmıştır, gerekirse değiştirin)
    okul_numarası_bölgesi = image[80:180, 100:500]
    okul_numarası = extract_text_from_image(okul_numarası_bölgesi).strip()  # Okul numarasını çıkar
    
    # Cevap anahtarı bölgeleri (koordine göre ayarlanmıştır, gerekirse değiştirin)
    cevap_anahtarı_bölge1 = image[300:800, 50:450]
    cevap_anahtarı_bölge2 = image[300:800, 450:850]
    cevap_anahtarı_bölge3 = image[850:1350, 50:450]
    cevap_anahtarı_bölge4 = image[850:1350, 450:850]
    
    # Her bir bölgeden metni çıkar
    cevap_anahtarı1 = extract_text_from_image(cevap_anahtarı_bölge1)
    cevap_anahtarı2 = extract_text_from_image(cevap_anahtarı_bölge2)
    cevap_anahtarı3 = extract_text_from_image(cevap_anahtarı_bölge3)
    cevap_anahtarı4 = extract_text_from_image(cevap_anahtarı_bölge4)
    
    # Çıkarılan metinleri döndür
    return okul_numarası, cevap_anahtarı1, cevap_anahtarı2, cevap_anahtarı3, cevap_anahtarı4

def main():
    """
    Kullanıcıdan dosya seçmesini isteyen ve seçilen dosyayı işleyerek sonuçları yazdıran ana fonksiyon.
    """
    root = tk.Tk()
    root.withdraw()  # Tkinter GUI penceresini gizle
    
    # Kullanıcıdan PDF veya görüntü dosyasını seçmesini iste
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Image files", "*.png;*.jpg;*.jpeg")])
    
    if not file_path:
        print("Dosya seçilmedi.")  # Dosya seçilmezse mesaj yazdır ve çık
        return
    
    # Poppler'ın kurulu olduğu yolu belirtin
    poppler_path = r'C:\Program Files\Release-24.02.0-0\poppler-24.02.0\Library\bin'
    
    # Optik formu oku ve sonuçları al
    okul_numarasi, cevap_anahtari1, cevap_anahtari2, cevap_anahtari3, cevap_anahtari4 = read_optik_form(file_path, poppler_path)
    
    # Sonuçları yazdır
    print(f"Okul Numarası: {okul_numarasi}")
    print("Cevap Anahtarı Bölge 1:")
    print(cevap_anahtari1)
    print("Cevap Anahtarı Bölge 2:")
    print(cevap_anahtari2)
    print("Cevap Anahtarı Bölge 3:")
    print(cevap_anahtari3)
    print("Cevap Anahtarı Bölge 4:")
    print(cevap_anahtari4)

if __name__ == "__main__":
    main()  # Ana fonksiyonu çalıştır
