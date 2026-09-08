import csv
import os
import shutil

# Configuration paths
INPUT_CSV_PATH = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Data\New Data.csv"
OUTPUT_CSV_PATH = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Data\New Data_Filtered.csv"
DEALS_CSV_PATH = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Deals.csv"

# Number of top header/metadata rows to preserve as-is
HEADER_ROW_COUNT = 5

# Explicit list of 232 items to delete from the Deal column
DELETE_DEAL_IDS = {
    "-",
    "AEI-PM-000137",
    "AESI-PM-000001",
    "AESI-PM-000002",
    "AESI-PM-000004",
    "AESI-PM-000005",
    "AESI-PM-000006",
    "AESI-PM-000007",
    "AESI-PM-000008",
    "AESI-PM-000009",
    "AESI-PM-000010",
    "AESI-PM-000011",
    "AESI-PM-000012",
    "AESI-PM-000013",
    "AESI-PM-000014",
    "AESI-PM-000015",
    "AESI-PM-000016",
    "AESI-PM-000017",
    "AESI-PM-000018",
    "AESI-PM-000019",
    "AESI-PM-000020",
    "AESI-PM-000021",
    "AESI-PM-000022",
    "AESI-PM-000023",
    "AESI-PM-000024",
    "AESI-PM-000025",
    "AESI-PM-000026",
    "AESI-PM-000027",
    "AESI-PM-000028",
    "AESI-PM-000029",
    "AESI-PM-000030",
    "AESI-PM-000031",
    "AESI-PM-000032",
    "AESI-PM-000033",
    "AESI-PM-000034",
    "AESI-PM-000035",
    "AESI-PM-000036",
    "AESI-PM-000037",
    "AESI-PM-000038",
    "AESI-PM-000039",
    "AESI-PM-000040",
    "AESI-PM-000041",
    "AESI-PM-000042",
    "AESI-PM-000043",
    "AESI-PM-000044",
    "AESI-PM-000045",
    "AESI-PM-000046",
    "AESI-PM-000047",
    "AESI-PM-000048",
    "AESI-PM-000049",
    "AESI-PM-000050",
    "AESI-PM-000051",
    "AESI-PM-000052",
    "AESI-PM-000053",
    "AESI-PM-000054",
    "AESI-PM-000055",
    "AESI-PM-000056",
    "AESI-PM-000057",
    "AESI-PM-000058",
    "AESI-PM-000059",
    "AESI-PM-000060",
    "AESI-PM-000061",
    "AESI-PM-000062",
    "AESI-PM-000063",
    "AESI-PM-000064",
    "AESI-PM-000065",
    "AESI-PM-000066",
    "AESI-PM-000067",
    "AESI-PM-000068",
    "AESI-PM-000069",
    "AESI-PM-000070",
    "AESI-PM-000072",
    "AESI-PM-000073",
    "AESI-PM-000074",
    "AESI-PM-000075",
    "AESI-PM-000078",
    "AESI-PM-000080",
    "AESI-PM-000081",
    "AESI-PM-000082",
    "AESI-PM-000083",
    "AESI-PM-000084",
    "AESI-PM-000085",
    "AESI-PM-000086",
    "AESI-PM-000087",
    "AESI-PM-000088",
    "AESI-PM-000089",
    "AESI-PM-000090",
    "AESI-PM-000091",
    "AESI-PM-000092",
    "AESI-PM-000094",
    "AESI-PM-000095",
    "AESI-PM-000096",
    "AESI-PM-000097",
    "AESI-PM-000098",
    "AESI-PM-000099",
    "AESI-PM-000100",
    "AESI-PM-000101",
    "AESI-PM-000102",
    "AESI-PM-000103",
    "AESI-PM-000104",
    "AESI-PM-000105",
    "AESI-PM-000106",
    "AESI-PM-000108",
    "AESI-PM-000109",
    "AESI-PM-000110",
    "AESI-PM-000111",
    "AESI-PM-000112",
    "AESI-PM-000113",
    "AESI-PM-000114",
    "AESI-PM-000115",
    "AESI-PM-000116",
    "AESI-PM-000117",
    "AESI-PM-000118",
    "AESI-PM-000119",
    "AESI-PM-000120",
    "AESI-PM-000121",
    "AESI-PM-000122",
    "AESI-PM-000123",
    "AESI-PM-000124",
    "AESI-PM-000125",
    "AESI-PM-000126",
    "AESI-PM-000127",
    "AESI-PM-000128",
    "AESI-PM-000129",
    "AESI-PM-000130",
    "AESI-PM-000131",
    "AESI-PM-000132",
    "AESI-PM-000133",
    "AESI-PM-000134",
    "AESI-PM-000135",
    "AESI-PM-000136",
    "AESI-PM-000137",
    "AESI-PM-000138",
    "AESI-PM-000140",
    "AESI-PM-000141",
    "AESI-PM-000142",
    "AESI-PM-000151",
    "AESI-PM-000152",
    "AESI-PM-000153",
    "AESI-PM-000154",
    "AESI-PM-000155",
    "AESI-PM-000156",
    "AESI-PM-000157",
    "AESI-PM-000158",
    "AESI-PM-000159",
    "AESI-PM-000160",
    "AESI-PM-000161",
    "AESI-PM-000162",
    "AESI-PM-000163",
    "AESI-PM-000164",
    "AESI-PM-000165",
    "AESI-PM-000166",
    "AESI-PM-000167",
    "AESI-PM-000233",
    "AESI-PM-000234",
    "AESI-PM-000235",
    "AESI-PM-000236",
    "AESI-PM-000237",
    "AESI-PM-000238",
    "AESI-PM-000239",
    "AESI-PM-000240",
    "AESI-PM-000241",
    "AESI-PM-000242",
    "AESI-PM-000243",
    "AESI-PM-000244",
    "AESI-PM-000245",
    "AESI-PM-000246",
    "AESI-PM-000247",
    "AESI-PM-000248",
    "AESI-PM-000249",
    "AESI-PM-000250",
    "AESI-PM-000251",
    "AESI-PM-000277",
    "AESI-PM-000291",
    "AESI-PM-000292",
    "AESI-PM-000293",
    "AESI-PM-000294",
    "AESI-PM-000295",
    "AESI-PM-000296",
    "AESI-PM-000297",
    "AESI-PM-000298",
    "AESI-PM-000299",
    "AESI-PM-000300",
    "AESI-PM-000301",
    "AESI-PM-000302",
    "AESI-PM-000303",
    "AESI-PM-000304",
    "AESI-PM-000305",
    "AESI-PM-000306",
    "AESI-PM-000307",
    "AESI-PM-000308",
    "AESI-PM-000309",
    "AESI-PM-000310",
    "AESI-PM-000311",
    "AESI-PM-000312",
    "AESI-PM-000313",
    "AESI-PM-000314",
    "AESI-PM-000315",
    "AESI-PM-000317",
    "AESI-PM-000320",
    "AESI-PM-000322",
    "AESI-PM-000323",
    "AESI-PM-000324",
    "AESI-PM-000325",
    "AESI-PM-000327",
    "AESI-PM-000328",
    "AESI-PM-000330",
    "AESI-PM-000331",
    "AESI-PM-000333",
    "AESI-PM-000334",
    "AESI-PM-000335",
    "AESI-PM-000342",
    "AESI-PM-000347",
    "AESI-PM-000351",
    "AESI-PM-000352",
    "AESI-PM-000365",
    "AESI-PM-000373",
    "AESI-PM-000376",
    "AESI-PM-000382",
    "AESI-PM-000383",
    "AESI-PM-000384",
    "AESI-PM-000385",
    "AESI-PM-000386",
    "AESI-PM-000387",
    "AESI-PM-000388",
    "AESI-PM-000915",
    "AESI-PM-001239",
    "AESI-PM-001244",
    "AESI-PM-001245",
    "AESI-PM-001246",
    "AESI-PM-001247",
    "MAIN",
}


def get_delete_set_from_deals_csv(deals_file: str) -> set:
    """Optionally load delete set dynamically from Deals.csv (Deal B - Deal A)."""
    if not os.path.exists(deals_file):
        return DELETE_DEAL_IDS

    deal_a = set()
    deal_b = set()
    with open(deals_file, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        for row in reader:
            if len(row) > 0 and row[0].strip():
                deal_a.add(row[0].strip())
            if len(row) > 1 and row[1].strip():
                deal_b.add(row[1].strip())

    dynamic_set = deal_b - deal_a
    return dynamic_set if dynamic_set else DELETE_DEAL_IDS


def filter_csv(
    input_file: str,
    output_file: str,
    delete_set: set,
    header_row_count: int = 5,
    deal_column_index: int = 1,
    overwrite_input: bool = False
):
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    # Read all rows
    with open(input_file, mode="r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.reader(f)
        all_rows = list(reader)

    if len(all_rows) <= header_row_count:
        print(f"Error: File has only {len(all_rows)} rows (<= header count of {header_row_count})")
        return

    headers = all_rows[:header_row_count]
    data_rows = all_rows[header_row_count:]

    kept_rows = []
    deleted_count = 0
    deleted_samples = []

    for row in data_rows:
        deal_val = row[deal_column_index].strip() if len(row) > deal_column_index else ""
        if deal_val in delete_set:
            deleted_count += 1
            if len(deleted_samples) < 10:
                deleted_samples.append(deal_val)
        else:
            kept_rows.append(row)

    # Write output
    output_target = input_file if overwrite_input else output_file

    # If overwriting, create a backup first
    if overwrite_input:
        backup_file = input_file + ".bak"
        shutil.copyfile(input_file, backup_file)
        print(f"[Backup created]: {backup_file}")

    with open(output_target, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(headers)
        writer.writerows(kept_rows)

    print("=" * 60)
    print("               CSV FILTERING SUMMARY")
    print("=" * 60)
    print(f"Input file           : {input_file}")
    print(f"Output file          : {output_target}")
    print(f"Total rows before    : {len(all_rows)} (Headers: {header_row_count}, Data: {len(data_rows)})")
    print(f"Rows deleted         : {deleted_count}")
    print(f"Data rows kept       : {len(kept_rows)}")
    print(f"Total rows after     : {len(headers) + len(kept_rows)}")
    print("=" * 60)
    print(f"[OK] Successfully saved filtered CSV to:\n     {output_target}")


if __name__ == "__main__":
    # Get deletion set (dynamically from Deals.csv or using explicit set)
    targets_to_delete = get_delete_set_from_deals_csv(DEALS_CSV_PATH)

    filter_csv(
        input_file=INPUT_CSV_PATH,
        output_file=OUTPUT_CSV_PATH,
        delete_set=targets_to_delete,
        header_row_count=HEADER_ROW_COUNT,
        deal_column_index=1,  # Column B is "Deal"
        overwrite_input=False  # Set to True if you want to overwrite New Data.csv directly
    )
