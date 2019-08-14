import json
import requests


class Region:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return str(self)

    def __str__(self):
        return u"({},{})".format(self.code, self.name).encode("utf-8").strip()


class Result:
    def __init__(self, region, result, year):
        self.region = region
        self.result = result
        self.year = year


def retrieve_regions(url):
    response = __make_get_request(url)
    region_json = response.json()
    raw_zip = zip(region_json["variables"][0]["values"], region_json["variables"][0]["valueTexts"])
    return map(lambda element: __create_region(element[0], element[1]), raw_zip)


def __create_region(code, name):
    return Region(code, name)


def retrieve_results(url, body):
    regions = retrieve_regions(url)
    response = __make_post_request(url, body)
    result_json = __clean_and_return_json(response)
    result_data = map(lambda d: __extract_result_data(d), result_json["data"])
    return __create_results(regions, result_data)


def __create_results(regions, result_data):
    return map(lambda rd: __create_result(__lookup_region(rd[0], regions), rd[2], rd[1]), result_data)


def __create_result(region, result, year):
    return Result(region, result, year)


def __make_get_request(url):
    return requests.get(url)


def __make_post_request(url, body):
    return requests.post(url, body)


def __clean_and_return_json(response):
    content_no_bom = response.content.decode("utf-8-sig")
    return json.loads(content_no_bom)


def __extract_result_data(data):
    return data["key"][0], data["key"][1], __convert_result_to_float(data["values"][0])


def __lookup_region(code, regions):
    for region in regions:
        if region.code == code:
            return region


def __convert_result_to_float(str_data):
    try:
        return float(str_data) / 100.0
    except (ValueError, TypeError):
        return 0.0
