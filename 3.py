from pprint import pprint
import re
import csv
from task1 import logger


@logger
def pars_contact(contact_list):
    pattern_number = r"(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})"
    pattern_ext_number = r"\s*\(*(доб.)\s*(\d*)\)*\s*"
    pattern_name = r"(^([А-я]+)\s([А-я]+)\s([А-я]+)\,\,)|(^([А-я]+)\,([А-я]+)\,([А-я]+))|(^([А-я]+)\s([А-я]+)(\,)\,)|(^([А-я]+)\,([А-я]+)\s([А-я]+)\,)"

    str_line = ','.join(contact_list)
    str_line = re.sub(pattern_name, r"\2\6\14\10,\3\7\11\15,\4\8\16", str_line)
    str_line = re.sub(pattern_number, r"+7(\2)\3-\4-\5", str_line)
    str_line = re.sub(pattern_ext_number, r" \1\2", str_line)
    return str_line.split(',')


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


update_contacts_list = []
for contact in contacts_list:
    update_contacts_list.append(pars_contact(contact))
out_contacts_list = []
contacts_list_length = len(update_contacts_list)
pass_records = []


for i in range(contacts_list_length - 1):
    if i in pass_records:
        continue
    contact = update_contacts_list[i]
    for j in range(i + 1, len(update_contacts_list)):
        if contact[0] == update_contacts_list[j][0] and contact[1] == update_contacts_list[j][1]:
            pass_records.append(j)
            contact = [contact[_] if contact[_] != "" else update_contacts_list[j][_]
                       for _ in range(len(contact))]
    out_contacts_list.append(contact)


with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(out_contacts_list)