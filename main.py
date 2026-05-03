# كتابة كود التطبيق
%%writefile main.py
"""
KNX PRO MAX - Smart Home Professional
Version: 1.0.0
Password: Admin/97289073
"""

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
import sqlite3
import os
import webbrowser
from datetime import datetime

# إعدادات
Window.size = (400, 700)
ADMIN_PASSWORD = "Admin/97289073"
DATABASE = "knx_pro.db"

def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            model TEXT,
            price TEXT,
            brand TEXT,
            description TEXT,
            url TEXT,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        default_products = [
            ("ABB i-bus 6128", "Module éclairage", "450 SAR", "ABB", "Contrôle 8 canaux avec gradation", "https://new.abb.com", ""),
            ("Gira G1", "Écran tactile 7\"", "1850 SAR", "Gira", "Contrôle complet de la maison", "https://www.gira.com", ""),
            ("Siemens UP 258", "Détecteur mouvement", "320 SAR", "Siemens", "Détection 360°, 12 mètres", "https://www.siemens.com", ""),
            ("Schneider KNX", "Prise intelligente", "280 SAR", "Schneider", "Commande à distance", "https://www.se.com", ""),
            ("Jung 2134 REG", "Interface IP", "950 SAR", "Jung", "Contrôle via internet", "https://www.jung.de", ""),
        ]
        cursor.executemany("INSERT INTO products (name, model, price, brand, description, url, image) VALUES (?, ?, ?, ?, ?, ?, ?)", default_products)
    conn.commit()
    conn.close()

class KNXProApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_mode = False
        init_database()
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        return self.create_main_screen()
    
    def create_main_screen(self):
        screen = Screen()
        
        # شريط علوي
        toolbar = MDTopAppBar(
            title="KNX PRO MAX",
            elevation=4,
            left_action_items=[["menu", lambda x: self.show_menu()]],
            right_action_items=[["account-circle", lambda x: self.show_auth()]],
            md_bg_color=self.theme_cls.primary_color
        )
        screen.add_widget(toolbar)
        
        # منطقة التمرير
        scroll = ScrollView()
        self.products_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        self.products_layout.bind(minimum_height=self.products_layout.setter("height"))
        scroll.add_widget(self.products_layout)
        screen.add_widget(scroll)
        
        # زر إضافة (يظهر للمسؤول فقط)
        self.add_btn = MDRaisedButton(
            text="+ AJOUTER UN PRODUIT",
            md_bg_color=self.theme_cls.primary_color,
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            on_release=self.show_add_dialog
        )
        
        self.load_products()
        self.update_admin_ui()
        
        # شريط سفلي
        self.status_label = MDLabel(
            text="Mode: VISITEUR",
            halign="center",
            size_hint_y=None,
            height=dp(30),
            theme_text_color="Secondary"
        )
        screen.add_widget(self.status_label)
        
        return screen
    
    def load_products(self):
        self.products_layout.clear_widgets()
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, model, price, brand, description, url FROM products ORDER BY id")
        products = cursor.fetchall()
        conn.close()
        
        for p in products:
            card = MDCard(
                orientation="vertical",
                padding=dp(10),
                size_hint=(1, None),
                height=dp(180),
                elevation=2,
                ripple_behavior=True,
                md_bg_color=(0.15, 0.15, 0.2, 1)
            )
            
            # اسم المنتج
            name = MDLabel(
                text=p[1],
                font_style="H6",
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
            card.add_widget(name)
            
            # الموديل والمعلومات
            info = MDLabel(
                text=f"{p[2]}  |  {p[4]}",
                font_style="Caption",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(25)
            )
            card.add_widget(info)
            
            # السعر
            price = MDLabel(
                text=p[3],
                theme_text_color="Custom",
                text_color=(1, 0.4, 0.4, 1),
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
            card.add_widget(price)
            
            # الوصف
            desc = MDLabel(
                text=p[5][:50] + "..." if len(p[5]) > 50 else p[5],
                font_style="Caption",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(40)
            )
            card.add_widget(desc)
            
            # أزرار الإجراءات
            actions = MDBoxLayout(
                spacing=dp(10),
                size_hint_y=None,
                height=dp(40)
            )
            
            # زر الموقع
            if p[6]:
                url_btn = MDFlatButton(
                    text="SITE",
                    md_bg_color=(0.2, 0.5, 0.8, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, url=p[6]: webbrowser.open(url)
                )
                actions.add_widget(url_btn)
            
            # أزرار المسؤول (تظهر فقط في وضع المسؤول)
            if self.admin_mode:
                edit_btn = MDFlatButton(
                    text="✏️",
                    md_bg_color=(1, 0.6, 0, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, pid=p[0]: self.edit_product(pid)
                )
                actions.add_widget(edit_btn)
                
                delete_btn = MDFlatButton(
                    text="🗑️",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, pid=p[0]: self.delete_product(pid)
                )
                actions.add_widget(delete_btn)
            
            card.add_widget(actions)
            self.products_layout.add_widget(card)
    
    def update_admin_ui(self):
        if self.admin_mode:
            self.status_label.text = "Mode: ADMINISTRATEUR"
            self.status_label.text_color = (0.3, 0.8, 0.3, 1)
            self.root.add_widget(self.add_btn)
        else:
            self.status_label.text = "Mode: VISITEUR (lecture seule)"
            self.status_label.text_color = (0.7, 0.7, 0.7, 1)
            if self.add_btn in self.root.children:
                self.root.remove_widget(self.add_btn)
    
    def show_auth(self):
        dialog = MDDialog(
            title="Authentification",
            type="custom",
            content_cls=MDTextField(
                hint_text="Mot de passe",
                password=True,
                pos_hint={"center_x": 0.5}
            ),
            buttons=[
                MDFlatButton(text="Annuler", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="Admin", on_release=lambda x: self.login(dialog))
            ]
        )
        dialog.open()
    
    def login(self, dialog):
        pwd = dialog.content_cls.text
        if pwd == ADMIN_PASSWORD:
            self.admin_mode = True
            self.load_products()
            self.update_admin_ui()
            dialog.dismiss()
        else:
            dialog.content_cls.error = True
            dialog.content_cls.helper_text = "Mot de passe incorrect"
    
    def logout(self):
        self.admin_mode = False
        self.load_products()
        self.update_admin_ui()
    
    def show_menu(self):
        if self.admin_mode:
            MDDialog(
                title="Menu Admin",
                text="Voulez-vous quitter le mode Admin?",
                buttons=[
                    MDFlatButton(text="Non", on_release=lambda x: dialog.dismiss()),
                    MDRaisedButton(text="Oui, Logout", on_release=lambda x: self.logout())
                ]
            ).open()
    
    def show_add_dialog(self, instance):
        dialog = MDDialog(
            title="Ajouter un produit",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(350)
            )
        )
        
        name = MDTextField(hint_text="Nom du produit")
        model = MDTextField(hint_text="Modèle")
        price = MDTextField(hint_text="Prix")
        brand = MDTextField(hint_text="Marque")
        desc = MDTextField(hint_text="Description")
        url = MDTextField(hint_text="Lien web (optionnel)")
        
        dialog.content_cls.add_widget(name)
        dialog.content_cls.add_widget(model)
        dialog.content_cls.add_widget(price)
        dialog.content_cls.add_widget(brand)
        dialog.content_cls.add_widget(desc)
        dialog.content_cls.add_widget(url)
        
        def save(x):
            if name.text:
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO products (name, model, price, brand, description, url) VALUES (?, ?, ?, ?, ?, ?)",
                    (name.text, model.text, price.text, brand.text, desc.text, url.text)
                )
                conn.commit()
                conn.close()
                self.load_products()
                dialog.dismiss()
        
        dialog.buttons = [
            MDFlatButton(text="Annuler", on_release=lambda x: dialog.dismiss()),
            MDRaisedButton(text="Enregistrer", on_release=save)
        ]
        dialog.open()
    
    def edit_product(self, product_id):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name, model, price, brand, description, url FROM products WHERE id=?", (product_id,))
        p = cursor.fetchone()
        conn.close()
        
        dialog = MDDialog(
            title="Modifier le produit",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(350)
            )
        )
        
        name = MDTextField(text=p[0], hint_text="Nom")
        model = MDTextField(text=p[1], hint_text="Modèle")
        price = MDTextField(text=p[2], hint_text="Prix")
        brand = MDTextField(text=p[3], hint_text="Marque")
        desc = MDTextField(text=p[4], hint_text="Description")
        url = MDTextField(text=p[5], hint_text="Lien web")
        
        dialog.content_cls.add_widget(name)
        dialog.content_cls.add_widget(model)
        dialog.content_cls.add_widget(price)
        dialog.content_cls.add_widget(brand)
        dialog.content_cls.add_widget(desc)
        dialog.content_cls.add_widget(url)
        
        def update(x):
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name=?, model=?, price=?, brand=?, description=?, url=? WHERE id=?",
                (name.text, model.text, price.text, brand.text, desc.text, url.text, product_id)
            )
            conn.commit()
            conn.close()
            self.load_products()
            dialog.dismiss()
        
        dialog.buttons = [
            MDFlatButton(text="Annuler", on_release=lambda x: dialog.dismiss()),
            MDRaisedButton(text="Enregistrer", on_release=update)
        ]
        dialog.open()
    
    def delete_product(self, product_id):
        confirm = MDDialog(
            title="Confirmation",
            text="Supprimer ce produit?",
            buttons=[
                MDFlatButton(text="Non", on_release=lambda x: confirm.dismiss()),
                MDRaisedButton(
                    text="Oui, supprimer",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.confirm_delete(product_id, confirm)
                )
            ]
        )
        confirm.open()
    
    def confirm_delete(self, product_id, dialog):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        self.load_products()
        dialog.dismiss()

if __name__ == "__main__":
    KNXProApp().run()