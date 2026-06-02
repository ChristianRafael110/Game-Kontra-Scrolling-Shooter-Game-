# 🎮 KONTRA - 2D Side Scrolling Shooter Game

## 📖 Deskripsi Project

Kontra adalah game 2D side-scrolling shooter yang dibuat menggunakan Python dan library Pygame. Pemain mengendalikan seorang tentara yang harus menyelesaikan berbagai level dengan mengalahkan musuh, mengumpulkan item, menghindari rintangan, dan mencapai area keluar untuk melanjutkan ke level berikutnya.

Game ini mengimplementasikan konsep Object Oriented Programming (OOP), sprite management, collision detection, AI musuh sederhana, sistem senjata, item pickup, dan sistem level berbasis file CSV.

---

## 👥 Anggota Kelompok

| Nama | NRP/NIM |
|--------|--------|
| Christian Rafael H.S | 25051204110 |
| Anggota 2 | - |
| Anggota 3 | - |

> Sesuaikan dengan anggota kelompok yang sebenarnya.

---

## ✨ Fitur Utama

### 🎯 Gameplay
- Karakter dapat bergerak ke kiri dan kanan.
- Karakter dapat melompat.
- Karakter dapat menembak musuh.
- Karakter dapat melempar granat.
- Sistem nyawa (health).

### 🤖 AI Musuh
- Musuh dapat berpatroli.
- Musuh dapat mendeteksi pemain menggunakan vision area.
- Musuh dapat menembak pemain ketika berada dalam jangkauan.

### 🎁 Item Pickup
- Health Box (+25 HP)
- Ammo Box (+15 peluru)
- Grenade Box (+3 granat)

### 🌎 Sistem Dunia
- Multi-level (3 level).
- Map dibuat menggunakan file CSV.
- Sistem scrolling map.
- Background parallax scrolling.

### 💥 Efek dan Animasi
- Animasi Idle
- Animasi Run
- Animasi Jump
- Animasi Death
- Animasi Explosion
- Sound Effect
- Background Music

### 🎬 User Interface
- Start Menu
- Exit Button
- Restart Button
- Health Bar
- Tampilan Ammo
- Tampilan Grenade

---

## 🛠️ Teknologi yang Digunakan

- Python 3.x
- Pygame
- CSV Module
- OS Module
- Random Module

---

## 📂 Struktur Project

```text
Kontra/
│
├── Kontra.py
├── button.py
│
├── aset game/
│   ├── audio/
│   ├── img/
│   │   ├── player/
│   │   ├── enemy/
│   │   ├── tile/
│   │   ├── icons/
│   │   ├── explosion/
│   │   └── background/
│   │
│   ├── level1_data.csv
│   ├── level2_data.csv
│   └── level3_data.csv
│
└── README.md
```

---

## ▶️ Cara Menjalankan Project

### 1. Install Python

Pastikan Python 3 telah terinstall.

Cek dengan:

```bash
python --version
```

---

### 2. Install Pygame

```bash
pip install pygame
```

---

### 3. Pastikan Asset Lengkap

Pastikan folder:

```text
aset game/
```

berisi:

- gambar
- audio
- file CSV level

sesuai struktur project.

---

### 4. Jalankan Program

```bash
python Kontra.py
```

atau

```bash
py Kontra.py
```

---

## ⌨️ Kontrol Permainan

| Tombol | Fungsi |
|---------|----------|
| A | Bergerak ke kiri |
| D | Bergerak ke kanan |
| W | Lompat |
| SPACE | Menembak |
| Q | Melempar granat |
| ESC | Keluar game |

---

# 🏗️ Penjelasan Implementasi OOP

Program ini menerapkan konsep Object Oriented Programming (OOP) menggunakan class untuk merepresentasikan objek dalam game.

---

## 1. Class Tentara

```python
class Tentara(pygame.sprite.Sprite)
```

Merepresentasikan pemain dan musuh.

### Attribute

- health
- ammo
- grenades
- speed
- alive
- action
- animation_list

### Method

- update()
- gerak()
- shoot_bullet()
- ai()
- update_animation()
- update_action()
- check_alive()
- draw()

### Konsep OOP

✔ Encapsulation

Data seperti health, ammo, speed disimpan di dalam objek Tentara.

✔ Reusability

Class yang sama digunakan untuk:

- Player
- Enemy

---

## 2. Class World

```python
class World
```

Bertanggung jawab membangun dunia permainan dari file CSV.

### Method

- process_data()
- draw()

### Fungsi

- Membaca map
- Membuat obstacle
- Membuat musuh
- Membuat item
- Membuat exit

---

## 3. Class Bullet

```python
class Bullet(pygame.sprite.Sprite)
```

Merepresentasikan peluru.

### Fungsi

- Bergerak sesuai arah.
- Mendeteksi collision.
- Mengurangi health target.

---

## 4. Class Grenade

```python
class Grenade(pygame.sprite.Sprite)
```

Merepresentasikan granat.

### Fungsi

- Bergerak dengan gravitasi.
- Meledak setelah timer habis.
- Memberikan damage area.

---

## 5. Class Explosion

```python
class Explosion(pygame.sprite.Sprite)
```

Menampilkan animasi ledakan.

---

## 6. Class HealthBar

```python
class HealthBar
```

Menampilkan status HP pemain.

---

## 7. Class ItemBox

```python
class itemBox(pygame.sprite.Sprite)
```

Merepresentasikan item yang dapat diambil.

Jenis item:

- Health
- Ammo
- Grenade

---

## 8. Class Decoration

```python
class Decoration(pygame.sprite.Sprite)
```

Menampilkan objek dekorasi.

---

## 9. Class Water

```python
class Water(pygame.sprite.Sprite)
```

Area berbahaya yang menyebabkan karakter mati.

---

## 10. Class Exit

```python
class Exit(pygame.sprite.Sprite)
```

Area penyelesaian level.

---

## 11. Class ScreenFade

```python
class screenFade
```

Membuat animasi transisi layar.

---

# 🔍 Konsep OOP yang Digunakan

## Encapsulation

Data dan fungsi disimpan dalam class masing-masing.

Contoh:

```python
class Tentara:
    self.health
    self.ammo
    self.speed
```

---

## Inheritance

Menggunakan inheritance dari:

```python
pygame.sprite.Sprite
```

Contoh:

```python
class Bullet(pygame.sprite.Sprite)
```

```python
class Grenade(pygame.sprite.Sprite)
```

```python
class Water(pygame.sprite.Sprite)
```

---

## Polymorphism

Method:

```python
update()
```

digunakan oleh banyak class dengan implementasi berbeda.

Contoh:

```python
Bullet.update()
Grenade.update()
Explosion.update()
Water.update()
```

---

## Abstraction

Detail implementasi seperti:

- collision detection
- AI musuh
- animasi

disembunyikan dalam method class sehingga mudah digunakan dari game loop utama.

---

# 📸 Screenshot Tampilan Program


![contoh_game_kontra}(aset game/img/contoh_game_kontra.png)

---

# 📈 Kesimpulan

Project Kontra merupakan implementasi game 2D side-scrolling shooter menggunakan Python dan Pygame yang menerapkan konsep Object Oriented Programming (OOP), manajemen sprite, collision detection, AI sederhana, sistem senjata, sistem level, serta antarmuka pengguna yang interaktif. Project ini menunjukkan penerapan berbagai materi Struktur Data, Pemrograman Berorientasi Objek, dan Pengembangan Game dalam sebuah aplikasi nyata.
