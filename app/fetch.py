
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Existing SchemeSaathi download folder
DOWNLOAD_DIR = BASE_DIR / "data" / "downloads"

# Separate PashuSeva download folder
PASHUSEVA_DOWNLOAD_DIR = DOWNLOAD_DIR / "pashuseva"


SCHEME_DOCUMENTS = [
    {
        "name": "pm_kisan_guidelines.pdf",
        "url": "https://pmkisan.gov.in/Documents/RevisedPM-KISANOperationalGuidelines%28English%29.pdf"
    },
    {
        "name": "pm_kisan_maandhan.pdf",
        "url": "https://pmkisan.gov.in/Documents/PM-KMY%20-%20Operational%20Guidelines.pdf"
    },
    {
        "name": "nmsa_guidelines.pdf",
        "url": "https://nmsa.dac.gov.in/pdfdoc/NMSA_Guidelines_English.pdf"
    }
]


PASHUSEVA_DOCUMENTS = [
    {
        "name": "nddb_handbook.pdf",
        "url": "https://www.nddb.coop/sites/default/files/handbook_of_good_dairy_husbandry_practices_low.pdf"
    },
    {
        "name": "animal_nutrition_booklet.pdf",
        "url": "https://www.nddb.coop/sites/default/files/Animal-Nutrition-booklet.pdf"
    },
    {
        "name": "quality_control_manual.pdf",
        "url": "https://www.nddb.coop/sites/default/files/Quality-Control-Manual-for-CFP.pdf"
    }
]


def download_document(url, filename, target_dir):

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        if "application/pdf" not in response.headers.get(
            "Content-Type", ""
        ).lower():
            raise ValueError("URL did not return a PDF document")

        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / filename

        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"Downloaded successfully: {filename}")
        return True

    except requests.exceptions.Timeout:
        print(f"Timeout error: {filename}")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")

    except (OSError, ValueError) as error:
        print(f"Download error: {error}")

    return False


def fetch_documents(documents, target_dir):

    successful_downloads = 0

    for document in documents:

        try:
            if not document["url"]:
                print(f"Missing URL: {document['name']}")
                continue

            if download_document(
                document["url"],
                document["name"],
                target_dir
            ):
                successful_downloads += 1

        except (KeyError, TypeError) as error:
            print(f"Invalid document entry: {error}")

    print(f"\nTotal successful downloads: {successful_downloads}")


def fetch_pashuseva_documents():
    fetch_documents(
        PASHUSEVA_DOCUMENTS,
        PASHUSEVA_DOWNLOAD_DIR
    )


def fetch_scheme_documents():
    fetch_documents(
        SCHEME_DOCUMENTS,
        DOWNLOAD_DIR
    )


if __name__ == "__main__":
    fetch_pashuseva_documents()
