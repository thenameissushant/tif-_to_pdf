import os
import shutil
from pathlib import Path

from PIL import Image
import img2pdf

# Input and output folders
INPUT_ROOT  = r"C:\Users\Sample\path"
OUTPUT_ROOT = r"C:\Users\Sample\path"

def convert_tiff_to_pdf(tiff_path, pdf_path):
    try:
        with open(tiff_path, "rb") as f_in, open(pdf_path, "wb") as f_out:
            f_out.write(img2pdf.convert(f_in))
    except img2pdf.AlphaChannelError:
        try:
            with Image.open(tiff_path) as im:
                pages = []
                while True:
                    pages.append(im.convert("RGB"))
                    im.seek(im.tell() + 1)
        except EOFError:
            pass
        if pages:
            pages[0].save(pdf_path, save_all=True, append_images=pages[1:])
    except Exception as e:
        print(f"Couldn't convert {tiff_path.name}: {e}")

def process_folder():
    input_root = Path(INPUT_ROOT).resolve()
    output_root = Path(OUTPUT_ROOT).resolve()

    for file in input_root.rglob("*"):
        if file.is_file():
            rel = file.relative_to(input_root)
            out_file = output_root / rel
            out_file.parent.mkdir(parents=True, exist_ok=True)

            ext = file.suffix.lower()
            if ext in [".tif", ".tiff"]:
                out_pdf = out_file.with_suffix(".pdf")
                if not out_pdf.exists():
                    print(f"Converting: {rel}")
                    convert_tiff_to_pdf(file, out_pdf)
                else:
                    print(f"Already done: {rel}")
            elif ext == ".pdf":
                if not out_file.exists():
                    print(f"Copying PDF: {rel}")
                    shutil.copy2(file, out_file)
                else:
                    print(f"Exists: {rel}")
            else:
                print(f"Skipped: {rel}")

if __name__ == "__main__":
    process_folder()
    print("Done!")
