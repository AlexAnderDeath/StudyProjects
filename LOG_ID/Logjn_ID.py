import cv2
import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import face_recognition
import hashlib



# Создание главного окна приложения
root = tk.Tk()
root.title("LOGIN ID")
style = ttk.Style()
style.configure('TButton', font=('Arial', 15))



def detect_face(frame):
    # Загрузка классификатора для обнаружения лиц
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Преобразование кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц на кадре
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    if len(faces) > 0:
        return True
    else:
        return False

def new_user():
    # Создание нового окна
    new_user_window = tk.Toplevel(root)
    new_user_window.title("NEW USER")
    # Создание формы регистрации
    login_label = tk.Label(new_user_window, text="Логин:")
    login_entry = tk.Entry(new_user_window)
    password_label = tk.Label(new_user_window, text="Пароль:")
    password_entry = tk.Entry(new_user_window, show='*')
    register_button = ttk.Button(new_user_window, text="Зарегистрироваться",
                                 command=lambda: register(login_entry.get(), password_entry.get()))

    # Расположение элементов формы регистрации на окне
    login_label.pack(anchor="center")
    login_entry.pack(anchor="center")
    password_label.pack(anchor="center")
    password_entry.pack(anchor="center")
    register_button.pack(padx = 20)


def recognize_face(frame):
    # Загрузить БД зареганных юзеров
    registered_users = os.listdir("dataset")

    # Конверт кадра в подходящее цветовое пространство
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Детекст фейс в кадре
    face_locations = face_recognition.face_locations(frame_rgb)

    # Извлект эмбединнгов из детекченного фейса
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for face_encoding in face_encodings:
        # цикл сравнение энкодингов с зареганными лицами
        for user in registered_users:
            user_image = face_recognition.load_image_file(f"dataset/{user}/face.jpeg")
            user_encoding = face_recognition.face_encodings(user_image)[0]

            # Мэтч
            match = face_recognition.compare_faces([user_encoding], face_encoding)

            if match[0]:
                print("User already exists!")
                messagebox.showinfo("Recognition", "Такой пользователь уже есть!")
                return True

    return False

def register(login, password):
    # Регистрация ()
    ret, frame = video_capture.read()


    # Проверка на пустые значения
    if not login or not password:
        messagebox.showerror("Error", "Все поля нужно заполнить!")
        return
    else:
        if os.path.exists(f"dataset/{login}"):
            print("User already exists!")
            messagebox.showerror("Error", "Такой логин уже существует!")
            return

        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in invalid_chars for char in login):
            messagebox.showerror("Error", "Неправильный символ в логине!")
            return

        # Проверка, длины пароля
        if len(password) < 3:
            print("Password too short!")
            messagebox.showerror("Error", "Пароль должен содержать не менее 3 символов!")
            return

    #Если фейса в кадре нет
    if not detect_face(frame):
        print("Face not detected!")
        messagebox.showerror("Error", "Лицо не обнаружено!")
        return
    # Если юзер с таким фейсом уже есть в БД
    if recognize_face(frame):

        return

    else:
        print('User Createdf')
        messagebox.showinfo("Registration", "User created successfully!")
        os.mkdir(f"dataset/{login}")

        # Сохранение скрина с фейсом пользователя
        cv2.imwrite(f"dataset/{login}/face.jpeg", frame)

        # Сохранение логина и пароля в файле
        with open(f"dataset/{login}/info.txt", "w") as file:
            file.write(f"Логин: {login}\n")
            file.write(f"Хеш пароля: {hash_password(password)}")

def hash_password(password):
    # Создание объекта хеширования
    hash_object = hashlib.sha256(password.encode())
    # Получение хеша в виде строки
    password_hash = hash_object.hexdigest()
    return password_hash


def check_pass(password, stored_hash):
    # Создание объекта хеширования
    hash_object = hashlib.sha256(password.encode())
    # Получение хеша в виде строки
    password_hash = hash_object.hexdigest()
    # Сравнение полученного хеша с сохраненным хешем
    if password_hash == stored_hash:
        return True
    else:
        return False

def check_password(password, login, window):
    # проверка правильности ввводе пассворда
    with open(f"dataset/{login}/info.txt", "r") as file:
        file_data = file.readlines()
        stored_password= file_data[1].split(":")[1].strip()
        if check_pass(password, stored_password):
            print("Password correct!")
            messagebox.showinfo("Login", "Добро пожаловать!")
            window.destroy()
            root.destroy()
            return True
        else:
            print("Incorrect password!")
            messagebox.showerror("Login", "Неправильный пароль!")
            return False

def login():
    ret, frame = video_capture.read()

    registered_users = os.listdir("dataset")
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(frame_rgb)

    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
    for face_encoding in face_encodings:

        for user in registered_users:

            user_image = face_recognition.load_image_file(f"dataset/{user}/face.jpeg")
            user_encoding = face_recognition.face_encodings(user_image)[0]

            match = face_recognition.compare_faces([user_encoding], face_encoding)
            if match[0]:
                login = user.split(".")[0]
                print(f"User {login} exists!")

                password_window = tk.Toplevel()  # Open a new window for password entry
                password_label = tk.Label(password_window, text=f"Введите пароль, {login}: ")
                password_label.pack()
                password_entry = tk.Entry(password_window, show="*")
                password_entry.pack()
                password_submit = tk.Button(password_window, text="ВВОД",
                                            command=lambda: check_password(password_entry.get(), login,
                                                                           password_window))
                password_submit.pack()

                return True
                        # Face not recognized
    print("User not found!")
    messagebox.showerror("Error", "Пользователь не найден!")

    return False


# Создание кнопок “Новый пользователь” и “Войти”
new_user_button = ttk.Button(root, text="Новый пользователь", command=new_user)
login_button = ttk.Button(root, text="Войти",command = login)

# Расположение кнопок на холсте
new_user_button.pack()
login_button.pack()


video_label = tk.Label(root)
video_label.pack()

video_capture = cv2.VideoCapture(0)

def update_video():
    # Получение текущего кадра видео
    ret, frame = video_capture.read()
    if ret:
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Преобразование кадра в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Обнаружение лиц на кадре
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)
        # Нарисовать прямоугольник вокруг каждого найденного лица
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Конвертация цветового пространства BGR в RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Создание изображения Tkinter из массива numpy
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        # Обновление изображения в виджете Label
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    video_label.after(10, update_video)



# Вызов функции update_video() для начала обновления видео
update_video()

# Отображение главного окна
root.mainloop()

