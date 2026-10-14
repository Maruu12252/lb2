import threading, time, random

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.users = []

    def use(self, user_name):
        with self.lock:
            self.users.append(user_name)
            time.sleep(random.uniform(0.01, 0.05)) # Непередбачувана затримка
            print(f"[{user_name}] використовує {self.name}. Зайнято: {', '.join(self.users)}")
            self.users.remove(user_name)

def access_resources(user_name, res_one, res_two):
    try:
        if random.random() < 0.5:
            res_one.use(user_name)
            res_two.use(user_name)
        else:
            res_two.use(user_name)
            res_one.use(user_name)
    except Exception as e:
        print(f"Помилка в потоці {user_name}: {e}")

# Створюємо три ресурси
R1 = Resource("Ресурс-1")
R2 = Resource("Ресурс-2")
R3 = Resource("Ресурс-3")

t1 = threading.Thread(target=access_resources, args=("Потік-1", R1, R2), daemon=True)
t2 = threading.Thread(target=access_resources, args=("Потік-2", R2, R3), daemon=True)
t3 = threading.Thread(target=access_resources, args=("Потік-3", R3, R1), daemon=True)

threads = [t1, t2, t3]
for t in threads:
    t.start()

for t in threads:
    t.join(1)
    if t.is_alive():
        print(f"\nПотік {t.name} не завершився. Можливий Deadlock!")
