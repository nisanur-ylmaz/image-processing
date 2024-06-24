import fitz  # PyMuPDF
import numpy as np
import tkinter as tk
from tkinter import filedialog

def extract_rectangles_from_pdf(pdf_path):
    """
    PDF dosyasından dikdörtgenleri çıkarır.
    """
    doc = fitz.open(pdf_path)  # PDF dosyasını aç
    rectangles = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Her sayfayı sırayla yükle
        shapes = page.get_drawings()  # Sayfadaki çizimleri al
        for shape in shapes:
            for item in shape["items"]:
                if item[0] == "re":  # "re" dikdörtgen anlamına gelir
                    rect = item[1]
                    width = int(rect.width)
                    height = int(rect.height)
                    rectangles.append((rect, width, height))
    return rectangles

def filter_large_rectangles(rectangles, min_size=1):
    """
    Belirtilen boyuttan büyük olan dikdörtgenleri filtreler.
    """
    return [rect for rect in rectangles if rect[1] > min_size and rect[2] > min_size]

def calculate_area(width, height):
    """
    Dikdörtgenin alanını hesaplar.
    """
    return width * height

def main():
    """
    Kullanıcıdan dosya seçmesini isteyen ve seçilen dosyayı işleyerek sonuçları yazdıran ana fonksiyon.
    """
    root = tk.Tk()
    root.withdraw()  # Tkinter GUI penceresini gizle
    
    # Kullanıcıdan PDF dosyasını seçmesini iste
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    if not file_path:
        print("Dosya seçilmedi.")  # Dosya seçilmezse mesaj yazdır ve çık
        return
    
    # PDF dosyasından dikdörtgenleri çıkar ve büyük dikdörtgenleri filtrele
    rectangles = extract_rectangles_from_pdf(file_path)
    large_rectangles = filter_large_rectangles(rectangles)
    
    # Dikdörtgenleri ve alanlarını göster
    for i, (rect, width, height) in enumerate(large_rectangles):
        area = calculate_area(width, height)
        print(f"Rectangle {i + 1}: Width: {width}, Height: {height}, Area: {area}")

if __name__ == "__main__":
    main()
