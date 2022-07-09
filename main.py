from pprint import pprint
import csv
import re


def reader():
    # reading up the csv file to get the data to work with
    file_name = "phonebook_raw.csv"
    # my_list = []
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def splitter(contacts_list):
    # splitting the stings inside the list so that lastname, firstname and surname go separately using
    # elements under indexes [0] and [1] as they contain the required data
    my_list = []
    for row in contacts_list:
        res = []
        if len(row[0].split()) == 3:
            row[0] = row[0].split()
            row[1], row[2], row[0] = row[0][1], row[0][2], row[0][0]
        elif len(row[0].split()) == 2:
            row[0] = row[0].split()
            row[1], row[0] = row[0][1], row[0][0]
        elif len(row[1].split()) == 2:
            row[1] = row[1].split()
            row[2], row[1] = row[1][1], row[1][0]
        for el in row:
            if type(el) != list:
                res.append(el)
            else:
                for i in el:
                    res.append(i)
        my_list.append(res)
# checkin for repeated elements and if found eleminating them.
# Adding the data from repeated peron's info into a single row
    for i in my_list:
        if len(i) > 7:
            i.pop()
        for j in my_list:
            if i[0] == j[0] and i[1] == j[1] and i is not j:
                if i[2] == '':
                    i[2] = j[2]
                if i[3] == '':
                    i[3] = j[3]
                if i[4] == '':
                    i[4] = j[4]
                if i[5] == '':
                    i[5] = j[5]
                if i[6] == '':
                    i[6] = j[6]
        for el in i:
            if i.index(el) > 6:
                i.remove(el)
        if my_list.count(i) > 1:
            my_list.remove(i)
    return my_list


def phone_formatter(my_list):
    # formatting the phone numbers using regex (managed to match all but one phone number)
    formatted_list = []
    for row in my_list:
        text = ",".join(row)
        pattern = re.compile(
            r"(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)(\s*)(\d{3})(\s*)(\-*)(\d{2})(\s*)(\-*)(\d{2})(\s*)(\(*)(доб)*(\.*)(\s*)(\d+)*(\)*)")
        result = pattern.sub(r"+7(\4)\8-\11-\14\15\17\18\20", text)
        new_text = result.split(',')
        formatted_list.append(new_text)
    return formatted_list


def final_formatter(formatted_list):
    # formatting the remaining phone number with a specifically written pattern
    final_formatted_list = []
    for row in formatted_list:
        text = ",".join(row)
        patten2 = re.compile(r"(8)\s(\d{3})-(\d{3})-(\d{2})(\d{2})")
        result = patten2.sub(r"+7(\2)\3-\4-\5", text)
        new_text = result.split(',')
        final_formatted_list.append(new_text)
    # pprint(final_formatted_list)
    return final_formatted_list


def writer(final_formatted_list):
    # writing down editted phonebook into a newly created csv file
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_formatted_list)


def main():
    contacts_list = reader()
    my_list = splitter(contacts_list)
    formatted_list = phone_formatter(my_list)
    final_formatted_list = final_formatter(formatted_list)
    writer(final_formatted_list)


if __name__ == '__main__':
    main()
