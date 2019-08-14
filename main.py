import string
import scb
import file

URL = "http://api.scb.se/OV0104/v1/doris/sv/ssd/START/ME/ME0104/ME0104D/ME0104T4"
QUERY = file.read_all_text("./electionquery.json")


def main():
    results = scb.retrieve_results(URL, QUERY)
    years = unique_years(results)
    for year in years:
        highest_result, region_names = highest_results(results, year)
        print_result_for_year(year, region_names, highest_result)


def unique_years(election_results):
    years = map(lambda r: r.year, election_results)
    return sorted(set(years))


def highest_results(election_results, year):
    year_results = results_for_year(election_results, year)
    max_result = max(map(lambda r: r.result, year_results))
    return max_result, map(lambda r: r.name, regions_with_result(year_results, max_result))


def results_for_year(election_results, year):
    return filter(lambda r: r.year == year, election_results)


def regions_with_result(election_results, result):
    filtered = filter(lambda r: r.result == result, election_results)
    return map(lambda r: r.region, filtered)


def print_result_for_year(year, regions, result):
    formatted_percentage = "{0:.1%}".format(result)
    print(str(year) + ": " + string.join(regions, ", ") + (": " if len(regions) > 1 else " ") + formatted_percentage)


main()
