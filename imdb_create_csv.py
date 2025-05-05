import pandas as pd
import os
from imdb_scraper import extract_year_from_alt, launch_driver, get_imdb_children_with_driver, get_imdb_images_with_driver

def load_birth_years_from_basics(tsv_path):
    df = pd.read_csv(tsv_path, sep='\t', usecols=["nconst", "birthYear"])
    df = df[df["birthYear"] != "\\N"]
    return dict(zip(df["nconst"], df["birthYear"]))

def create_family_csv_combined(actor_id, name, byear, name_basics_path):
    driver = launch_driver()

    birth_years = load_birth_years_from_basics(name_basics_path)
    family_rows = []

    print(f"Getting images for {name}")
    parent_images = get_imdb_images_with_driver(actor_id, name, driver)
    family_rows.extend(format_image_rows(name, actor_id, byear, "self", parent_images))

    print(f"Getting children of {name}")
    children_info = get_imdb_children_with_driver(actor_id, driver)

    for child in children_info["children"]:
        cid = child["imdb_id"]
        cname = child["name"]
        cbyear = birth_years.get(cid)
        if cbyear:
            print(f"Getting images for child {cname}")
            child_images = get_imdb_images_with_driver(cid, cname, driver)
            family_rows.extend(format_image_rows(cname, cid, cbyear, "child", child_images))
        else:
            print(f"Birth year not found for child {cname} ({cid})")

    #driver.quit()
    save_family_csv(actor_id, family_rows)

def save_family_csv(actor_id, rows):
    output_dir = "data/families_csv"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"family_{actor_id}.csv")
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"CSV created: {output_path}")

def format_image_rows(name, imdb_id, byear, kinship, images):
    rows = []
    for url, alt in images:
        picyear = extract_year_from_alt(alt)
        age = int(picyear) - int(byear) if picyear and byear else None
        rows.append({
            "name": name,
            "imdb_id": imdb_id,
            "byear": byear,
            "image": '',
            "rect": None,
            "height": None,
            "width": None,
            "url": url,
            "pic_description": alt,
            "picyear": picyear,
            "age": age,
            "kinship": kinship
        })
    return rows

if __name__ == "__main__":
    create_family_csv_combined(
        actor_id="nm0000023",
        name="Judy Garland",
        byear="1922",
        name_basics_path="data/imdb_download/name.basics.tsv.gz"
    )
