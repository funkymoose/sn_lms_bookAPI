from fastapi import FastAPI
import requests

app = FastAPI()

# cache = {}

@app.get("/book/{isbn}")
def get_book(isbn: str, API_KEY: str):

    if not API_KEY:
        raise HTTPException(
            status_code=400,
            detail="Missing Google API Key"
        )

    # url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"


    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={API_KEY}"

    response = requests.get(url, timeout=20)

    if response.status_code != 200:
        return {
            "success": False,
            "status": response.status_code,
            "error": response.text
        }

    data = response.json()

    if "items" not in data:
        return {
            "success": False,
            "message": "Book not found"
        }

    volume = data["items"][0]["volumeInfo"]

    result = {
        "title": volume.get("title"),
        "subtitle": volume.get("subtitle"),
        "authors": volume.get("authors", []),
        "categories": volume.get("categories",[]),
        "publisher": volume.get("publisher"),
        "publishedDate": volume.get("publishedDate"),
        "description": volume.get("description"),
        "pageCount":volume.get("pageCount"),
        "thumbnail": volume.get("imageLinks", {}).get("thumbnail"),
        "rating": volume.get("averageRating")
    }

    # SAVE TO CACHE
    cache[isbn] = result

    return {
        "source": "google",
        "data": result
    }
