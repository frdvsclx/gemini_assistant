'''
problem tanimi: gemini ile aisstant projesi
-kullanicinin dogal dilde verdigi komutlari anlar
-kural tabanli olarak notlar olcak
-bu chatbot notlara erisecek, özet verecek

model tanimi: Google gemini 
-gemini-2.0-flash

api tanimi: AIzaSyDuc28TxN32U3Kb0gVKoBqGf8bBkim9Ta4

plan program:
-assistant: chatbot 
-dataset:sqlite database 
-main: GUI uygulaması

pip install requests python-dotenv
pip freeze > requirements.txt

'''

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from assistant import get_gemini_response
from dataset import initialize_db, add_note, add_event, get_notes, get_events
import threading
from datetime import datetime

class GeminiAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Gemini Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Veritabanını başlat
        initialize_db()
        
        # Ana frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlıklarını ayarla
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="🤖 Gemini Assistant", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Sol panel - Butonlar
        self.create_buttons_panel(main_frame)
        
        # Sağ panel - Chat ve sonuçlar
        self.create_chat_panel(main_frame)
        
        # Alt panel - Not ve etkinlik ekleme
        self.create_input_panel(main_frame)
        
    def create_buttons_panel(self, parent):
        """Sol panel - Ana butonlar"""
        buttons_frame = ttk.LabelFrame(parent, text="🚀 Hızlı İşlemler", padding="15")
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Buton stilleri
        style = ttk.Style()
        style.configure('Action.TButton', padding=12, font=('Arial', 11, 'bold'))
        style.configure('Success.TButton', padding=12, font=('Arial', 11, 'bold'))
        style.configure('Warning.TButton', padding=12, font=('Arial', 11, 'bold'))
        
        # Başlık
        title_label = ttk.Label(buttons_frame, text="📋 Notlar & Etkinlikler", 
                               font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Butonlar
        ttk.Button(buttons_frame, text="📝 Notları Göster", 
                  command=self.show_notes, style='Action.TButton').pack(fill=tk.X, pady=8)
        
        ttk.Button(buttons_frame, text="📅 Etkinlikleri Göster", 
                  command=self.show_events, style='Action.TButton').pack(fill=tk.X, pady=8)
        
        ttk.Button(buttons_frame, text="📊 Not Özeti", 
                  command=self.show_notes_summary, style='Success.TButton').pack(fill=tk.X, pady=8)
        
        ttk.Button(buttons_frame, text="📈 Etkinlik Özeti", 
                  command=self.show_events_summary, style='Success.TButton').pack(fill=tk.X, pady=8)
        
        # Ayırıcı
        ttk.Separator(buttons_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Hızlı not ekleme
        ttk.Label(buttons_frame, text="⚡ Hızlı Not:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.quick_note_entry = ttk.Entry(buttons_frame, width=25, font=('Arial', 10))
        self.quick_note_entry.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Button(buttons_frame, text="➕ Not Ekle", 
                  command=self.add_quick_note, style='Success.TButton').pack(fill=tk.X, pady=5)
        
        # Ayırıcı
        ttk.Separator(buttons_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Temizle butonu
        ttk.Button(buttons_frame, text="🧹 Chat Temizle", 
                  command=self.clear_chat, style='Warning.TButton').pack(fill=tk.X, pady=8)
        
    def create_chat_panel(self, parent):
        """Sağ panel - Chat alanı"""
        chat_frame = ttk.LabelFrame(parent, text="💬 AI Chat", padding="15")
        chat_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Chat başlığı
        chat_title = ttk.Label(chat_frame, text="🤖 Gemini AI ile Sohbet", 
                              font=('Arial', 12, 'bold'))
        chat_title.grid(row=0, column=0, pady=(0, 10))
        
        # Chat alanı
        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                 height=18, font=('Arial', 10),
                                                 bg='#fafafa', fg='#333333')
        self.chat_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Mesaj girişi
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        # Mesaj giriş etiketi
        input_label = ttk.Label(input_frame, text="Mesajınız:", font=('Arial', 10, 'bold'))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Mesaj giriş alanı
        entry_frame = ttk.Frame(input_frame)
        entry_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        entry_frame.columnconfigure(0, weight=1)
        
        self.message_entry = ttk.Entry(entry_frame, font=('Arial', 11))
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.message_entry.bind('<Return>', self.send_message)
        
        # Gönder butonu
        send_button = ttk.Button(entry_frame, text="🚀 Gönder", 
                                command=self.send_message, style='Success.TButton')
        send_button.grid(row=0, column=1)
        
        # Hoş geldin mesajı
        self.add_message("Assistant", "Merhaba! Size nasıl yardımcı olabilirim? 🤖")
        
    def create_input_panel(self, parent):
        """Alt panel - Detaylı giriş"""
        input_frame = ttk.LabelFrame(parent, text="Detaylı Giriş", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        input_frame.columnconfigure(1, weight=1)
        
        # Not ekleme
        ttk.Label(input_frame, text="Not Ekle:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.note_entry = ttk.Entry(input_frame, width=50)
        self.note_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(input_frame, text="Not Ekle", 
                  command=self.add_note_from_input).grid(row=0, column=2)
        
        # Etkinlik ekleme
        ttk.Label(input_frame, text="Etkinlik:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.event_entry = ttk.Entry(input_frame, width=30)
        self.event_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        ttk.Label(input_frame, text="Tarih:").grid(row=1, column=2, sticky=tk.W, padx=(10, 10), pady=(10, 0))
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(input_frame, text="Etkinlik Ekle", 
                  command=self.add_event_from_input).grid(row=1, column=4, pady=(10, 0))
        
    def add_message(self, sender, message):
        """Chat alanına mesaj ekle"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        self.chat_area.see(tk.END)
        
    def send_message(self, event=None):
        """Mesaj gönder"""
        message = self.message_entry.get().strip()
        if not message:
            return
            
        self.add_message("Siz", message)
        self.message_entry.delete(0, tk.END)
        
        # Mesajı işle
        self.process_message(message)
        
    def process_message(self, message):
        """Mesajı işle ve yanıt ver"""
        message_lower = message.lower()
        
        # Komut kontrolü
        if message_lower.startswith("not ekle:"):
            content = message.split(":", 1)[1].strip()
            add_note(content)
            self.add_message("Assistant", f"✅ Not eklendi: {content}")
            
        elif message_lower.startswith("etkinlik ekle:"):
            parts = message.split(":", 1)[1].strip().split(" - ")
            if len(parts) >= 2:
                event = parts[0].strip()
                date = parts[1].strip()
                add_event(event, date)
                self.add_message("Assistant", f"✅ Etkinlik eklendi: {event} - {date}")
            else:
                self.add_message("Assistant", "❌ Format: etkinlik ekle: [etkinlik] - [tarih]")
                
        elif "notları göster" in message_lower or "notlar" in message_lower:
            self.show_notes()
            
        elif "etkinlikleri göster" in message_lower or "etkinlikler" in message_lower:
            self.show_events()
            
        else:
            # Gemini'ye yönlendir
            self.add_message("Assistant", "🤔 Düşünüyorum...")
            
            # Thread'de Gemini'yi çağır
            threading.Thread(target=self.get_gemini_response_async, args=(message,)).start()
            
    def get_gemini_response_async(self, message):
        """Gemini yanıtını async olarak al"""
        try:
            response = get_gemini_response(message)
            self.root.after(0, lambda: self.add_message("Gemini", response))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("Assistant", f"❌ Hata: {str(e)}"))
            
    def show_notes(self):
        """Notları göster"""
        notes = get_notes()
        if notes:
            result = "📝 Notlarınız:\n"
            for i, (content, created_at) in enumerate(notes, 1):
                result += f"{i}. {content} ({created_at})\n"
            self.add_message("Assistant", result)
        else:
            self.add_message("Assistant", "📝 Henüz not eklenmemiş.")
            
    def show_events(self):
        """Etkinlikleri göster"""
        events = get_events()
        if events:
            result = "📅 Etkinlikleriniz:\n"
            for i, (event, event_date) in enumerate(events, 1):
                result += f"{i}. {event} - {event_date}\n"
            self.add_message("Assistant", result)
        else:
            self.add_message("Assistant", "📅 Henüz etkinlik eklenmemiş.")
            
    def clear_chat(self):
        """Chat alanını temizle"""
        self.chat_area.delete(1.0, tk.END)
        self.add_message("Assistant", "Chat alanı temizlendi! 🧹")
        
    def show_notes_summary(self):
        """Notları özetle"""
        notes = get_notes()
        if not notes:
            self.add_message("Assistant", "📝 Henüz özetlenecek not bulunamadı")
            return
            
        self.add_message("Assistant", "🤔 Notlarınızı özetliyorum...")
        
        # Thread'de Gemini'yi çağır
        threading.Thread(target=self.get_notes_summary_async).start()
        
    def get_notes_summary_async(self):
        """Not özetini async olarak al"""
        try:
            notes = get_notes()
            all_notes_text = "\n".join([f"- {n[1]}: {n[0]}" for n in notes])
            prompt = f"Aşağıdaki notları özetler misin\n\n{all_notes_text}"
            summary = get_gemini_response(prompt)
            self.root.after(0, lambda: self.add_message("📊 Not Özeti", summary))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("Assistant", f"❌ Hata: {str(e)}"))
            
    def show_events_summary(self):
        """Etkinlikleri özetle"""
        events = get_events()
        if not events:
            self.add_message("Assistant", "📅 Henüz özetlenecek etkinlik bulunamadı")
            return
            
        self.add_message("Assistant", "🤔 Etkinliklerinizi özetliyorum...")
        
        # Thread'de Gemini'yi çağır
        threading.Thread(target=self.get_events_summary_async).start()
        
    def get_events_summary_async(self):
        """Etkinlik özetini async olarak al"""
        try:
            events = get_events()
            all_events_text = "\n".join([f"- {e[1]}: {e[0]}" for e in events])
            prompt = f"Aşağıdaki takvim etkinliklerini özetler misin\n\n{all_events_text}"
            summary = get_gemini_response(prompt)
            self.root.after(0, lambda: self.add_message("📈 Etkinlik Özeti", summary))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("Assistant", f"❌ Hata: {str(e)}"))
        
    def add_quick_note(self):
        """Hızlı not ekle"""
        note = self.quick_note_entry.get().strip()
        if note:
            add_note(note)
            self.add_message("Assistant", f"✅ Hızlı not eklendi: {note}")
            self.quick_note_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Lütfen not içeriği girin!")
            
    def add_note_from_input(self):
        """Alt panelden not ekle"""
        note = self.note_entry.get().strip()
        if note:
            add_note(note)
            self.add_message("Assistant", f"✅ Not eklendi: {note}")
            self.note_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Lütfen not içeriği girin!")
            
    def add_event_from_input(self):
        """Alt panelden etkinlik ekle"""
        event = self.event_entry.get().strip()
        date = self.date_entry.get().strip()
        
        if event and date:
            add_event(event, date)
            self.add_message("Assistant", f"✅ Etkinlik eklendi: {event} - {date}")
            self.event_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Lütfen etkinlik ve tarih girin!")

def main():
    """Ana uygulama"""
    root = tk.Tk()
    app = GeminiAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 