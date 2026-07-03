import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import logic

class ImageDuplicateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("類似画像検索・削除ツール")
        self.root.geometry("1000x800")
        self.current_folder = None  # フォルダパス保持用
        self.create_widgets()

    def create_widgets(self):
        # --- 設定エリア ---
        config_frame = tk.LabelFrame(self.root, text="スキャン設定", padx=10, pady=10)
        config_frame.pack(fill=tk.X, padx=10, pady=10)

        self.btn_select = tk.Button(config_frame, text="フォルダを選択", command=self.select_folder)
        self.btn_select.pack(side=tk.LEFT, padx=5)

        tk.Label(config_frame, text="閾値:").pack(side=tk.LEFT, padx=5)
        self.threshold_scale = tk.Scale(config_frame, from_=0, to_=30, orient=tk.HORIZONTAL)
        self.threshold_scale.set(8)
        self.threshold_scale.pack(side=tk.LEFT, padx=5)

        self.btn_rescan = tk.Button(config_frame, text="🔄 このフォルダで再検索",
                                   command=self.run_scan, state=tk.DISABLED, bg="#d1e7ff")
        self.btn_rescan.pack(side=tk.LEFT, padx=20)

        # --- 進捗表示エリア ---
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(fill=tk.X, padx=15)
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=2)
        self.status_label = tk.Label(self.progress_frame, text="フォルダを選択してください")
        self.status_label.pack(side=tk.LEFT)

        # --- 結果表示エリア ---
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

    def select_folder(self):
        """フォルダを選択し、初回スキャンを実行する"""
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.btn_rescan.config(state=tk.NORMAL) # 再検索ボタンを使えるようにする
            self.run_scan()

    def run_scan(self):
        """現在のフォルダと閾値でスキャンを実行する"""
        if not self.current_folder:
            return

        # 画面をクリア
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        def update_ui(current, total, filename):
            percent = (current / total) * 100
            self.progress_bar["value"] = percent
            self.status_label.config(text=f"スキャン中: {current}/{total} - {filename[:20]}")
            self.root.update()

        # ロジック実行
        thresh = self.threshold_scale.get()
        duplicates = logic.find_duplicates(self.current_folder, threshold=thresh, progress_callback=update_ui)

        self.status_label.config(text=f"完了: {len(duplicates)}組の類似画像を発見", fg="green")
        self.display_results(duplicates)

    def display_results(self, duplicates):
        if not duplicates:
            messagebox.showinfo("結果", "類似画像は見つかりませんでした。")
            return

        for img_a, img_b in duplicates:
            row = tk.Frame(self.scrollable_frame, bd=1, relief=tk.GROOVE, pady=10)
            row.pack(fill=tk.X, padx=5, pady=5)
            self.add_preview(row, img_a, tk.LEFT)
            self.add_preview(row, img_b, tk.RIGHT)

    def add_preview(self, parent, path, side):
        frame = tk.Frame(parent, padx=10)
        frame.pack(side=side, expand=True)

        try:
            img = Image.open(path)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(frame, image=photo)
            lbl.image = photo
            lbl.pack()
        except:
            tk.Label(frame, text="読み込みエラー").pack()

        tk.Label(frame, text=os.path.basename(path), font=("", 8), wraplength=180).pack()

        btn_f = tk.Frame(frame)
        btn_f.pack(pady=5)
        tk.Button(btn_f, text="🗑 削除", bg="#ff4d4d", fg="white",
                  command=lambda: self.confirm_delete(path, frame)).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_f, text="📁 フォルダ",
                  command=lambda: logic.open_folder_at_path(path)).pack(side=tk.LEFT, padx=2)

    def confirm_delete(self, path, frame):
        if messagebox.askyesno("削除確認", "この画像を削除しますか？"):
            if logic.delete_file(path):
                frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDuplicateApp(root)
    root.mainloop()
