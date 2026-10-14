import threading, time, random

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.users = []

    def add_user(self, user_name):
        with self.lock:
            self.users.append(user_name)
            
    def remove_user(self, user_name):
        with self.lock:
            self.users.remove(user_name)

def access_resources_safe(user_name, res_one, res_two):
    try:
        # Впорядковуємо ресурси для уникнення взаємного блокування
        resources = sorted([res_one, res_two], key=lambda r: r.name)
        
        # Одночасне безпечне захоплення в строгому порядку
        with resources[0].lock:
            with resources[1].lock:
                resources[0].users.append(user_name)
                resources[1].users.append(user_name)
                print(f"[{user_name}] ексклюзивно працює з {res_one.name} та {res_two.name}.")
                
        # Тривала операція винесена за межі блокування
        time.sleep(random.uniform(0.01, 0.05))
        
        # Очищення
        with resources[0].lock:
            resources[0].users.remove(user_name)
        with resources[1].lock:
            resources[1].users.remove(user_name)
            
    except Exception as e:
        print(f"Помилка в потоці {user_name}: {e}")

# Ініціалізація
R1 = Resource("Ресурс-1")
R2 = Resource("Ресурс-2")
R3 = Resource("Ресурс-3")

# Потоки не є daemon, щоб гарантувати завершення роботи
t1 = threading.Thread(target=access_resources_safe, args=("Потік-1", R1, R2))
t2 = threading.Thread(target=access_resources_safe, args=("Потік-2", R2, R3))
t3 = threading.Thread(target=access_resources_safe, args=("Потік-3", R3, R1))

threads = [t1, t2, t3]
for t in threads:
    t.start()

# Дозволяємо потокам нормально завершити роботу без таймауту
for t in threads:
    t.join()
print("Всі потоки безпечно завершили роботу. Deadlock неможливий.")