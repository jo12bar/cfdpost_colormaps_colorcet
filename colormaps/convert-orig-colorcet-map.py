import argparse
import csv
import pathlib

cli_parser = argparse.ArgumentParser(
    description="Convert original ColorCET colormap CSVs to a format to be ingested by colormaptranslation.py"
)

cli_parser.add_argument("input_directory", type=pathlib.Path)
cli_parser.add_argument("output_directory", type=pathlib.Path)

cli_args = cli_parser.parse_args()

in_dir: pathlib.Path = cli_args.input_directory
out_dir: pathlib.Path = cli_args.output_directory

in_files = in_dir.glob("*.csv")

for in_file in in_files:
    out_file = out_dir / in_file.name
    print(f"{in_file} ==> {out_file}")

    with open(in_file, mode="r", newline="") as in_csv_file:
        csvreader = csv.reader(in_csv_file, delimiter=",", quotechar='"')

        in_rows = [row for row in csvreader]

    row_scalar_delta = 1.0 / float(len(in_rows) - 1)
    scalar = 0.0

    out_fieldnames = ["scalar", "r", "g", "b"]

    with open(out_file, mode="x", newline="") as out_csv_file:
        writer = csv.DictWriter(out_csv_file, fieldnames=out_fieldnames)

        writer.writeheader()

        for in_row in in_rows:
            writer.writerow(
                {
                    "scalar": round(scalar, 18),
                    "r": in_row[0],
                    "g": in_row[1],
                    "b": in_row[2],
                }
            )

            scalar += row_scalar_delta
