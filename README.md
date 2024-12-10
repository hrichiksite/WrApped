# WhatsApp Stats

This is a simple Python script that reads a WhatsApp chat export and generates some statistics about the chat.

## Usage

1. Extract the chat database from WhatsApp. More info about that in this repo [KnugiHK/WhatsApp-Chat-Exporter](https://github.com/KnugiHK/WhatsApp-Chat-Exporter).
2. Generate the json file with the chat data using the exporter given in the previous step. (The following command is an example, you have to change the parameters as needed)
```bash
wtsexporter -a --enrich-from-vcard contacts.vcf --default-country-code COUNTRY_CODE -j --date '2023-01-01 00:00 - 2024-01-01 00:00'  --pretty-print-json --no-html
```
3. Run the python script with the path to the json file as edited in code.
```bash
python3 sort_thisyear.py
```


## To Do

- [ ] Add more statistics
- [ ] Add more visualizations
- [ ] More streamlined process for generating the json file and consuming it
