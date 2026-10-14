import pytest
import time
import threading
import random
from buggy_code import Resource, access_resources

# --- 2. Ваші модульні тести ---
def test_daemon_abrupt_termination():
    """Тест демонструє, що потік обривається через таймаут join"""
    R1 = Resource("R1")
    R2 = Resource("R2")
    
    # Штучно збільшуємо час виконання, щоб спровокувати проблему join
    original_sleep = time.sleep
    time.sleep = lambda x: original_sleep(2.0) 
    
    t1 = threading.Thread(target=access_resources, args=("TestThread", R1, R2), daemon=True)
    t1.start()
    
    t1.join(0.5) # Головний потік чекає лише 0.5с
    
    # Якщо потік ще живий, але головна програма пішла далі - daemon його вб'є
    assert t1.is_alive() is True 
    # Відновлюємо sleep
    time.sleep = original_sleep

def test_blocking_in_critical_section():
    """Тест демонструє відсутність паралелізму через sleep у lock"""
    R1 = Resource("R1")
    start = time.time()
    
    def use_res():
        with R1.lock:
            time.sleep(0.5)
            
    t1 = threading.Thread(target=use_res)
    t2 = threading.Thread(target=use_res)
    
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    duration = time.time() - start
    # Оскільки потоки блокують один одного, час виконання буде ~1 секунда (0.5 + 0.5), а не 0.5
    assert duration >= 1.0