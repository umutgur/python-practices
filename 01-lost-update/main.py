class InsufficientFundsError(Exception):
    pass
class NegativeOrZeroAmountError(Exception):
    pass

class Account:
    def __init__(self, balance: int = 0):
        self.balance = balance

class Transaction:
    def __init__(self, account: Account):
        self.account = account

    def __enter__(self):
        self.snapshot = self.account.balance
        return self.account
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.account.balance = self.snapshot

account = Account(0)
continue_program = True

def audit(func):
    import functools

    @functools.wraps(func)

    def wrapper(*args, **kwargs):
        try:
            print(f"'{func.__name__}' çalıştırılıyor...")
            result = func(*args, **kwargs)
            print(f"'{func.__name__}' {result} değerini döndürdü.")
            return result
        except Exception as e:
            print(f"'{func.__name__}' işlevinde bir hata oluştu: {e}")
            raise
    return wrapper

def timed(func):
    import time
    import functools

    @functools.wraps(func) 

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            print(f"'{func.__name__}' {end_time - start_time:.4f} saniye içinde çalıştırıldı.")
    return wrapper

@audit
@timed
def top_up(balance,amount):
    if amount <= 0:
        raise NegativeOrZeroAmountError("Negatif veya sıfır miktar girilemez.")
    balance += amount
    return balance

@audit
@timed
def withdraw(balance,amount):
    if amount <= 0:
        raise NegativeOrZeroAmountError("Negatif veya sıfır miktar girilemez.")
    if amount <= balance:
        balance -= amount
    else:
        raise InsufficientFundsError("Yetersiz bakiye. Çekmek istediğiniz miktar mevcut bakiyenizden fazla.")
    return balance

HANDLERS = {
    "2": top_up,
    "3": withdraw
}

while continue_program:
    print("İşleminizi seçiniz:")
    print("1. Bakiye Sorgulama")
    print("2. Para Yatırma")
    print("3. Para Çekme")
    print("4. Çıkış")

    input_choice = input("Seçiminizi yapınız: ")

    try:
        if input_choice == "1":
            print(f"Mevcut bakiyeniz: {account.balance}")
        elif input_choice in HANDLERS:
            amount = int(input("Miktarı giriniz: "))
            
            with Transaction(account) as acc:
                acc.balance = HANDLERS[input_choice](acc.balance, amount)
                
            print(f"Yeni bakiyeniz: {account.balance}")
        elif input_choice == "4":
            print("Programdan çıkılıyor...")
            continue_program = False

    except InsufficientFundsError as e:
        print(e)
    except NegativeOrZeroAmountError as e:
        print(e)
    except ValueError:
        print("Geçersiz giriş. Lütfen geçerli bir sayı giriniz.")