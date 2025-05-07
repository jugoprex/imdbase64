import pandas as pd
import os
from imdb_scraper import extract_year_from_alt, launch_driver, get_imdb_children_with_driver, get_imdb_images_with_driver

def load_data_from_basics(tsv_path="data/imdb_download/name.basics.tsv.gz"):
    df = pd.read_csv(tsv_path, sep='\t', usecols=["nconst", "primaryName", "birthYear"])
    df = df[df["birthYear"] != "\\N"]
    df = df[df["primaryName"] != "\\N"]
    return df

def create_family_csv_combined(actor_id, name, byear, birth_years, driver):
    family_rows = []

    print(f"Getting children of {name}")

    # if they dont have children, skip
    children_info = get_imdb_children_with_driver(actor_id, driver)
    if not children_info["children"]:
        print(f"No children found for {name} ({actor_id})")
        return 0

    print(f"Getting images for {name} ({actor_id})")
    parent_images = get_imdb_images_with_driver(actor_id, name, driver)
    family_rows.extend(format_image_rows(name, actor_id, byear, "parent", parent_images))

    children_with_images = False  # Track if any child has images
    for child in children_info["children"]:
        cid = child["imdb_id"]
        cname = child["name"]
        cbyear = birth_years.loc[birth_years["nconst"] == cid, "birthYear"].values
        cbyear = cbyear[0] if len(cbyear) > 0 else None
        if cbyear:
            print(f"Getting images for child {cname} ({cid})")
            child_images = get_imdb_images_with_driver(cid, cname, driver)
            if child_images:
                children_with_images = True
                family_rows.extend(format_image_rows(cname, cid, cbyear, "child", child_images))
        else:
            print(f"Birth year not found for child {cname} ({cid})")
    if children_with_images:
        save_family_csv(actor_id, family_rows)
        return 1
    else:
        print(f"No images found for children of {name} ({actor_id})")
        return 0

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

def process_multiple_people(limit=None):
    """
    Process multiple people from the IMDb basics database.

    :param limit: Maximum number of people to process (for testing).
    """
    driver = launch_driver()
    people = load_data_from_basics()
    count = 0
    for i, person in people.iterrows():
        actor_id = person["nconst"]
        name = person["primaryName"]
        byear = person["birthYear"]
        print(f"Processing {name} ({actor_id})")
        try:
            res = create_family_csv_combined(actor_id, name, byear, people, driver)
            count += res
        except Exception as e:
            print(f"Error processing {name} ({actor_id}): {e}")
        if limit and count >= limit:
            print(f"Processed {limit} people, stopping.")
            break

    driver.quit()

if __name__ == "__main__":
    process_multiple_people(limit=150)
