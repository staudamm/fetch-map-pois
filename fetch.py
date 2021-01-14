import json
from googleplaces import GooglePlaces, types

API_KEY = 'AIzaSyB7D9c1Fb1hDD-hHUE1bh0mL0Xc1PMnyfc'
google_places = GooglePlaces(API_KEY)


category_to_subcats = {
    'bakery': [types.TYPE_BAKERY],
    'medical': [types.TYPE_DENTIST, types.TYPE_DOCTOR, types.TYPE_HOSPITAL],
    'culture': [types.TYPE_CHURCH, types.TYPE_MOVIE_THEATER, types.TYPE_ART_GALLERY, types.TYPE_MUSEUM],
    'gastronomy': [types.TYPE_RESTAURANT, types.TYPE_CAFE, types.TYPE_BAR],
    'post': [types.TYPE_POST_BOX, types.TYPE_POST_OFFICE],
    'shop': [types.TYPE_SHOE_STORE, types.TYPE_GROCERY_OR_SUPERMARKET]
}


def create_obj_dict(subcat, name, lat, lng):
    return {
        "type": "Feature",
        "properties": {
          "name": name,
          "subCat": subcat
        },
        "geometry": {
          "type": "Point",
          "coordinates": [lat, lng]
        }
      }


def fetch_for_category(category, coordinates):
    subcat_list = category_to_subcats[category]
    query_result = google_places.nearby_search(
        lat_lng=coordinates,
        types=subcat_list,
        radius=2000)

    feature_list = []
    for place in query_result.places:
        subcats = set(subcat_list) & set(place.types)
        feature_list.append(
            create_obj_dict(
                subcats.pop(),
                place.name,
                float(place.geo_location['lat']),
                float(place.geo_location['lng'])
            ))
    return {"type": "FeatureCollection", "features": feature_list}


def create_map_pois():
    project_lat = 53.945570041161204
    project_lng = 14.182379056191083
    lat_lng = {'lat': project_lat, 'lng': project_lng}

    pois = {}
    for cat in category_to_subcats.keys():
        pois[cat+"Pois"] = fetch_for_category(cat, lat_lng)

    with open('tst.json', 'w') as f:
        json.dump(pois, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    import tkinter
    tkinter._test()
