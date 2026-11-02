# Installing the NBS mapping control tool on another computer

The package contains the application, its versioned configuration (all mapping versions and change history), the QCB validation rules, the review evidence, the latest stakeholder specification and the Python add-ons it needs (in `wheels`, so no internet is required). It does **not** contain the bank's account-level data: you choose those files on your computer in the tool.

## 1. Requirements

- Windows with Python 3.10–3.14 (python.org; tick "Add python.exe to PATH" when installing).
- About 4 GB free disk space for runs.

## 2. Start

1. Unzip anywhere, for example `C:\NBS_Mapping_Control`. If Windows marks downloaded files as blocked, right-click the zip before unzipping, choose Properties, tick **Unblock**, OK.
2. Double-click `Start_NBS_Rebuild.cmd`. It installs Flask, openpyxl and lxml from the `wheels` folder (offline), starts the tool and opens your browser. Keep its window open while you work.

## 3. Use it: four steps in the top menu

1. **Load files**: one row per source (ECB, All Loan, All Deposit, trial balance, GL mapping workbook, category entries, BO, earlier live NBS, QCB rules). Pick the files from your computer (or type a path) and press **Load** once. The account database takes about 6 minutes, the rest about 2. Files are copied into the tool's `inputs` folder with their SHA-256, so nothing depends on another computer.
2. **NBS report**: all 50 tables with the calculated values (optionally next to BO) and, for every line, how it is calculated: the source, the accounts selected (T24 category, sector, residency…) and the exact balance types added up. **Change** opens the logic builder for that line. Press **Generate NBS** on Home first.
3. **Balance types**: every T24 balance type in the ECB file with its total, the owner groups and product policies that use it, the NBS lines that take it and the GL Report lines that use it. The owner balance groups can be edited here (with name and reason; previous versions kept).
4. **Downloads**: the full NBS Excel in the BO table layout, the mapping file for stakeholders and the comparisons.

The 30 September reporting-basis policy is tied to the exact category file (SHA-256 `a9dc0021...`). A different file needs its own owner decision.

Command-line equivalents (from the unzipped folder):

```bash
python -m nbs_control build-bank-db --ecb "inputs\ECB_BALANCE Asset type wise (30.09.2026).xlsx" --loan "inputs\All Loan 30.09.2026.xlsx" --deposit "inputs\All Deposit 30.09.2026..xlsx" --tb "inputs\Historical_Trial_Balance  30.09.2026..xlsx"
```
```bash
python -m nbs_control rebuild-setup
```
```bash
python -m nbs_control rebuild-run
```

## No internet / proxy (office networks)

Office networks often block pypi.org, which shows as `ConnectTimeoutError ... pypi.org`. The starter therefore installs from the bundled `wheels` folder:

```bash
python -m pip install --user --no-index --find-links wheels -r requirements.txt
```

With a company proxy or internal mirror, the online install also works with `--proxy http://<proxy>:<port>` or `--index-url <mirror>`.

## Check the installation

```bash
python -m unittest discover -s tests -t .
```
Tests that need the original files are skipped automatically.
