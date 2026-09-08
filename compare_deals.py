import csv
import os

# File paths
CSV_PATH = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Deals.csv"
OUTPUT_REPORT_PATH = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Deals_Comparison_Result.csv"


def compare_deals(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    deal_a = []
    deal_b = []

    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        
        # Check column names
        headers = [h.strip() for h in (reader.fieldnames or [])]
        col_a = next((h for h in headers if "deal a" in h.lower()), None)
        col_b = next((h for h in headers if "deal b" in h.lower()), None)

        if not col_a or not col_b:
            # Fallback to standard column indexing if headers differ
            f.seek(0)
            raw_reader = csv.reader(f)
            header_row = next(raw_reader, [])
            for row in raw_reader:
                if len(row) > 0 and row[0].strip():
                    deal_a.append(row[0].strip())
                if len(row) > 1 and row[1].strip():
                    deal_b.append(row[1].strip())
        else:
            for row in reader:
                val_a = (row.get(col_a) or "").strip()
                val_b = (row.get(col_b) or "").strip()
                if val_a:
                    deal_a.append(val_a)
                if val_b:
                    deal_b.append(val_b)

    set_a = set(deal_a)
    set_b = set(deal_b)

    only_in_a = sorted(list(set_a - set_b))
    only_in_b = sorted(list(set_b - set_a))
    in_both = sorted(list(set_a & set_b))

    # Print Summary to Terminal
    print("=" * 60)
    print("               DEALS COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Total entries in Deal A: {len(deal_a)} (Unique: {len(set_a)})")
    print(f"Total entries in Deal B: {len(deal_b)} (Unique: {len(set_b)})")
    print("-" * 60)
    print(f"Items in Deal A but NOT Deal B : {len(only_in_a)}")
    print(f"Items in Deal B but NOT Deal A : {len(only_in_b)}")
    print(f"Items present in BOTH Deals     : {len(in_both)}")
    print("=" * 60)

    # Display items only in A
    print(f"\n--- [1] Present in Deal A but Missing in Deal B ({len(only_in_a)} items) ---")
    if only_in_a:
        for idx, item in enumerate(only_in_a, 1):
            print(f"{idx:>4}. {item}")
    else:
        print("None (All items in Deal A are present in Deal B)")

    # Display items only in B
    print(f"\n--- [2] Present in Deal B but Missing in Deal A ({len(only_in_b)} items) ---")
    if only_in_b:
        for idx, item in enumerate(only_in_b, 1):
            print(f"{idx:>4}. {item}")
    else:
        print("None (All items in Deal B are present in Deal A)")

    # Save to CSV Report
    max_len = max(len(only_in_a), len(only_in_b))
    with open(OUTPUT_REPORT_PATH, mode="w", newline="", encoding="utf-8-sig") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["Only in Deal A (Missing in B)", "Only in Deal B (Missing in A)"])
        for i in range(max_len):
            a_val = only_in_a[i] if i < len(only_in_a) else ""
            b_val = only_in_b[i] if i < len(only_in_b) else ""
            writer.writerow([a_val, b_val])

    print(f"\n[OK] Detailed report exported to:\n    {OUTPUT_REPORT_PATH}")


if __name__ == "__main__":
    compare_deals(CSV_PATH)
