# csv2vcf
csv2vcf is a small command line tool to convert CSV files to VCard
(.vcf) files. Based on https://github.com/mridah/csv2vcf but
largely rewritten.


## Usage :

Go to terminal or command prompt and type :

```
python csv2vcf.py CSV_FILE_NAME OUTDIR INPUT_FILE_FORMAT
```

Where :

- `CSV_FILE_NAME` is the full name of the CSV file you want to convert
- `OUTDIR` is the output directory where vcf files will be written
- `INPUT_FILE_FORMAT` is a JSON formatted string which tells **csv2vcf** how to parse your input file


###### JSON Format :

The JSON string can have the following keys :

`n`, `fn`, `email`, `tel`, `bday`, `categories` where each property is
in accordance
with [vCard property types](https://en.wikipedia.org/wiki/VCard)

Format is `{KEY_1:KEY_1_COLUMN_NO, KEY_2:KEY_2_COLUMN_NO, ...}`


###### Example :

Suppose you have a CSV file `contacts.csv` with the following content :

```
+-----------+-------------+
|    NAME   |    MOBILE   |
+-----------+-------------+
|   Mrid    |  1111111111 |
|   Arnav   |  2222222222 |
|   Sunil   |  3333333333 |
|     .     |      .      |
|     .     |      .      |
|     .     |      .      |
+-----------+-------------+
```

To convert this file to vCard, you will have to write :

`python csv2vcf.py contacts.csv some/output/dir '{"name":1, "tel":2}'`

## Copyright and license :

The license is available within the repository in
the
[LICENSE](https://github.com/mridah/csv2vcf/blob/master/LICENSE.md)
file.
