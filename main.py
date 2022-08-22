from pprint import pprint
import csv
import re


#Чтение файла
def session(file_csv: str):
    with open(file_csv, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        return list(rows)


#ФИО расстановка
def arrangements_by_names(book_csv: list):
    for i, j in enumerate(book_csv[1:], start=1):
        name = ' '.join(j[:2]).split()
        k = 0
        while k < len(name):
            book_csv[i][k] = name[k]
            k += 1
    return book_csv


#Телефоны в едином формате
def phone_normalizer(book_csv: list):
    pattern = re.compile(
        r'[78]\s*\(?(\d{,3})\)?\s*-?(\d{,3})-?(\d{,2})-?(\d{,2})\s*\(?(?:\bдоб\b\.?)?\s*(\d*)'
    )
    for i, j in enumerate(book_csv[1:], start=1):
        phone = j[-2]
        res = pattern.search(phone)
        phone_gr = f' доб.{res.group(5)}' if res.group(5) else ""
        phone_format = f'+7({res.group(1)}){res.group(2)}-{res.group(3)}-{res.group(4)}{phone_gr}'
        book_csv[i][-2] = phone_format
    return book_csv


#Убираем дубликаты
def merge_duplicates(book_csv: list):
    phones_dict = {}
    for i, j in enumerate(book_csv[1:], start=1):
        phones_dict[book_csv[i][0]] = phones_dict.get(book_csv[i][0], []) + [i]
    book_dict = [book_csv[0]].copy()

    for k in phones_dict.values():
        if len(k) > 1:
            for n, i in enumerate(k):
                if n == 0:
                    s = book_csv[i].copy()
                else:
                    for j in range(len(book_csv[0])):
                        if not s[j]:
                            s[j] = book_csv[i][j]
        else:
            s = book_csv[k[0]].copy()
        book_dict.append(s)
    return book_dict

#Записываем результат в файл csv
def writing_to_book_csv(file_csv: str, book_csv: list):
    
    with open(file_csv, "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(book_csv)


if __name__ == '__main__':

    contacts_book = session("phonebook_raw.csv")
    contacts_book = arrangements_by_names(contacts_book)
    contacts_list = merge_duplicates(contacts_book)
    contacts_list = phone_normalizer(contacts_list)
    writing_to_book_csv("phonebook.csv", contacts_list)
    print(f'{contacts_list}')