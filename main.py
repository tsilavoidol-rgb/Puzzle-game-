from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from PIL import Image as PILImage
import os
import random

# Découpe l'image en 3x3 morceaux
def split_image(image_path):
    temp_dir = "pieces"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    img = PILImage.open(image_path)
    width, height = img.size
    piece_width = width // 3
    piece_height = height // 3

    pieces = []
    count = 0
    for i in range(3):
        for j in range(3):
            count += 1
            if count < 9:  # dernière pièce = case vide
                box = (j*piece_width, i*piece_height, (j+1)*piece_width, (i+1)*piece_height)
                piece = img.crop(box)
                piece_path = f"{temp_dir}/piece{count}.png"
                piece.save(piece_path)
                pieces.append(piece_path)
    return pieces

class PuzzleApp(App):
    def build(self):
        self.pieces = split_image("puzzle.png")
        self.grid = list(range(8)) + [None]
        random.shuffle(self.grid)

        self.layout = GridLayout(cols=3, spacing=5, padding=5)
        self.buttons = []

        # Créer les boutons pour chaque pièce
        for idx in self.grid:
            btn = Button()
            if idx is not None:
                btn.background_normal = self.pieces[idx]
            btn.bind(on_press=self.move)
            self.buttons.append(btn)
            self.layout.add_widget(btn)

        # Label pour “You Win!”
        self.win_label = Label(text="", size_hint_y=None, height=40)
        self.layout.add_widget(self.win_label)

        # Boutons en bas : Indice, Reset, Shuffle
        self.hint_btn = Button(text="Indice", size_hint_y=None, height=50)
        self.hint_btn.bind(on_press=self.show_hint)
        self.reset_btn = Button(text="Reset", size_hint_y=None, height=50)
        self.reset_btn.bind(on_press=self.reset)
        self.shuffle_btn = Button(text="Shuffle", size_hint_y=None, height=50)
        self.shuffle_btn.bind(on_press=self.shuffle)

        self.layout.add_widget(self.hint_btn)
        self.layout.add_widget(self.reset_btn)
        self.layout.add_widget(self.shuffle_btn)

        return self.layout

    def move(self, instance):
        idx = self.buttons.index(instance)
        zero_idx = self.grid.index(None)
        if (idx % 3 != 0 and idx - 1 == zero_idx) or \
           (idx % 3 != 2 and idx + 1 == zero_idx) or \
           (idx - 3 == zero_idx) or \
           (idx + 3 == zero_idx):
            self.grid[zero_idx], self.grid[idx] = self.grid[idx], self.grid[zero_idx]
            self.update_buttons()

        # Vérifier si gagné
        if self.grid == list(range(8)) + [None]:
            self.win_label.text = "🎉 Bravo, tu as gagné !"

    def update_buttons(self):
        for i, btn in enumerate(self.buttons):
            if self.grid[i] is not None:
                btn.background_normal = self.pieces[self.grid[i]]
            else:
                btn.background_normal = ""

    def reset(self, instance):
        self.grid = list(range(8)) + [None]
        self.update_buttons()
        self.win_label.text = ""

    def shuffle(self, instance):
        random.shuffle(self.grid)
        self.update_buttons()
        self.win_label.text = ""

    def show_hint(self, instance):
        for i in range(8):
            if self.grid[i] != i:
                zero_idx = self.grid.index(None)
                self.grid[i], self.grid[zero_idx] = self.grid[zero_idx], self.grid[i]
                break
        self.update_buttons()

if __name__ == "__main__":
    PuzzleApp().run()
