# This is a sample Python script.
import asyncio
import json
from pathlib import Path

import httpx


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


async def get_country_details():
    overpass_url = 'https://overpass-api.de/api/interpreter'
    overpass_query = """
    [out:json];
    (
      relation["type"="boundary"]["boundary"="administrative"]["admin_level"="2"];
    );
    out center tags;
    """

    # Send the query to Overpass API
    async with httpx.AsyncClient() as client:
        response = await client.post(overpass_url, data={"data": overpass_query})
        response.raise_for_status()
        data = response.json()

    # Parse the results
    country_data = []
    for element in data.get('elements', []):
        country_info = {
            "name": element.get("tags", {}).get("name:en"),
            "iso_code": element.get("tags", {}).get("ISO3166-1"),
            "latitude": element.get("center", {}).get("lat"),
            "longitude": element.get("center", {}).get("lon"),
        }
        if country_info["name"] and country_info["latitude"] and country_info["longitude"]:
            country_data.append(country_info)

    # Save to JSON file
    with open("country_all.json", "w") as f:
        json.dump(country_data, f, indent=4)

    return {"status": "success", "file": "country_all.json"}


def get_count_for_country():
    json_file_path = Path('country_all.json')
    sorted_json_file_path = Path("country_sorted.json")

    try:
        # Open and read the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        sorted_data = sorted(data, key=lambda x: x.get("name", "").lower())

        with open(sorted_json_file_path, "w") as sorted_file:
            json.dump(sorted_data, sorted_file, indent=4)

        return {"status": "success", "data": data}
    except FileNotFoundError:
        return {"status": "error", "message": "File not found"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Error decoding JSON"}


def get_state_for_country():
    ...


async def test_get_state_for_malaysia():
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = """
        [out:json];
        area["name"="Malaysia"]->.country;
        (
          relation["admin_level"="4"](area.country);
        );
        out center;
        """

    async with httpx.AsyncClient() as client:
        response = await client.post(overpass_url, data={"data": overpass_query})
        response.raise_for_status()
        data = response.json()

    # Parse the results
    state_data = []
    for element in data.get("elements", []):
        state_info = {
            "name": element.get("tags", {}).get("name"),
            "latitude": element.get("center", {}).get("lat"),
            "longitude": element.get("center", {}).get("lon")
        }
        if state_info["name"] and state_info["latitude"] and state_info["longitude"]:
            state_data.append(state_info)

    # Save to JSON file
    with open("malaysia_states.json", "w", encoding="utf-8") as f:
        json.dump(state_data, f, ensure_ascii=False, indent=4)

    return {"status": "success", "file": "malaysia_states.json"}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # asyncio.run(get_country_details())
    asyncio.run(test_get_state_for_malaysia())
    # get_count_for_country()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
