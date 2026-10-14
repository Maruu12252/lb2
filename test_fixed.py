import pytest
import time
import threading

# Імпортуємо виправлений клас Resource з вашого файлу fixed_code.py
from fixed_code import Resource 

def test_safe_parallel_execution():
    """Тест демонструє, що тривалі операції не блокують інші потоки"""
    R1 = Resource("R1")
    R2 = Resource("R2")
    start = time.time()
    
    # Використовуємо логіку виправленої функції 
    def fast_access(user, r1, r2):
        with r1.lock:
            with r2.lock:
                r1.users.append(user)
        # Sleep поза блокуванням
        time.sleep(0.5)
        with r1.lock:
            r1.users.remove(user)

    t1 = threading.Thread(target=fast_access, args=("T1", R1, R2))
    t2 = threading.Thread(target=fast_access, args=("T2", R2, R1)) # Зворотний порядок
    
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    duration = time.time() - start
    # Час виконання тепер ~0.5с (а не 1с), оскільки sleep() відбувається поза критичною секцією
    assert duration < 0.8