print("Введите логин и пароль")
Acc_name = input("Логин: ")
Acc_password = input("Пароль: ")
print("немного подождите идет проверка")
if Acc_name == "Jalopy" and Acc_password == "123456":
    print("Доступ разрешен")
else:
    print("Доступ запрещен")
print("1.Расчитать зарплату")
print("2.Выход")
Pass1 = int(input(""))
if Pass1 == 1:
    print(Acc_name, "впишите параметры:")
    Ac = int(input("Зп за полный рабочий день: "))
    Bc = int(input("Отработаных дней: "))
    Cc = 13
    Gryzniy_dohod = (Ac * Bc)
    ndfl = ((Gryzniy_dohod * Cc ) / 100)
    Chistiy_dohod = Gryzniy_dohod - ndfl
    print("грязный доход: ", Gryzniy_dohod)
    print("НДФЛ: ", ndfl)
    print("Чистый доход: ",Chistiy_dohod)
elif Pass1 == 2:
     print("Пока!")