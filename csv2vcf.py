import os
import sys
import csv
import json
import unidecode
from optparse import OptionParser

prop_names = ['n', 'fn', 'email', 'tel', 'bday', 'categories']


class Csv:
    def __init__(self, value_list, name_to_index_dict):
        tmp = {
            propname: value_list[name_to_index_dict[propname]]
            for propname in prop_names
            if propname in name_to_index_dict
        }
        self.name_to_value_dict = {
            k: v for k, v in tmp.items() if v is not None
        }
        if self.name_to_value_dict.get("fn", "").count(" ") == 1:
            sname, fname = self.name_to_value_dict["fn"].split(" ")
            sname = sname.capitalize()
            fname = fname.capitalize()
            self.name_to_value_dict["n"] = "{sname};{fname};;;".format(
                sname=sname,
                fname=fname,
                **self.name_to_value_dict
            )

    def __str__(self):
        prop_fmt_dict = {
            propname: "{propname}:{propvalue}"
            for propname in prop_names
        }
        res = ['BEGIN:VCARD', 'VERSION:3.0', 'CALSCALE=gregorian']
        res.extend(['KIND:individual', 'ORG:LMA'])          # TODO
        for propname, propvalue in self.name_to_value_dict.items():
            res.append(prop_fmt_dict[propname].format(
                propname=propname.upper(),
                propvalue=propvalue,
                **self.name_to_value_dict
            ))
        res.append("UID:{:d}".format(
            abs(hash(
                "would you like some salt?"+"".join(res))
            ))
        )
        res.append('END:VCARD')
        return "\n".join(res)

    def file_name(self):
        filename = self.name_to_value_dict["fn"].replace(" ", "_")
        filename += ".vcf"
        filename = filename.lower()
        return unidecode.unidecode(filename)


def csv_to_students_array(input_file, input_file_format):
    index_to_name_dict = {prop_name: None for prop_name in prop_names}
    for propname in prop_names:
        index_to_name_dict[propname] = input_file_format.get(propname, None)
    with open(input_file, 'r') as source_file:
        reader = csv.reader(source_file)
        students_array = []
        for row in reader:
            student = Csv(row, input_file_format)
            students_array.append(student)
    return students_array


if __name__ == '__main__':
    conf_fmt = "  - Data for {value[fn]} written to {filename}"
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) !=3:
        raise Exception(
            "Wrong number of arguments: {:d} given instead of 3".format(len(args))
        )
    input_file = args[0]
    output_dir = args[1]
    input_file_format = json.loads(args[2])
    if not os.path.isdir(output_dir):
        error_msg = "{} is not a directory".format(output_dir)
        raise Exception(error_msg)
    print("Creating files under {output_dir}".format(output_dir=output_dir))
    students_array = csv_to_students_array(input_file, input_file_format)
    for student in students_array:
        filename = student.file_name()
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            f.write(str(student))
            print(conf_fmt.format(
                value=student.name_to_value_dict,
                filename = filename
            ))
