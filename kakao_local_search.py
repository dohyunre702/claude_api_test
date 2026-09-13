import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

KAKAO_API_KEY = os.getenv("KAKAO_REST_API_KEY")
SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"


def search_keyword(query: str, page: int = 1, size: int = 15) -> dict:
    if not KAKAO_API_KEY:
        raise RuntimeError("KAKAO_REST_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": query, "page": page, "size": size}

    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def print_results(data: dict) -> None:
    documents = data.get("documents", [])
    if not documents:
        print("검색 결과가 없습니다.")
        return

    for i, place in enumerate(documents, start=1):
        print(f"{i}. {place['place_name']}")
        print(f"   주소: {place['address_name']}")
        print(f"   전화: {place.get('phone') or '정보 없음'}")
        print(f"   링크: {place['place_url']}")
        print()


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = input("검색할 키워드를 입력하세요: ").strip()

    if not query:
        print("검색어가 필요합니다.")
        return

    data = search_keyword(query)
    print_results(data)


if __name__ == "__main__":
    main()
