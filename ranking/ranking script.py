import csv

raw_text = """
Poster for Ella McCay (2025)
★★★

Poster for Avatar: Fire and Ash (2025)
★★★½

Poster for Marty Supreme (2025)
★★★★

Poster for One Battle After Another (2025)
★★★★★

Poster for Wake Up Dead Man (2025)
★★★★

Poster for Roofman (2025)
★★★★

Poster for Hamlet (2025)
★★★

Poster for Frankenstein (2025)
★★★

Poster for No Other Choice (2025)
★★★★½

Poster for Hamnet (2025)
★★★

Poster for After the Hunt (2025)
★★★½

Poster for Bugonia (2025)
★★★★

Poster for Coolie (2025)
★★★

Poster for Caught Stealing (2025)
★★★½

Poster for Weapons (2025)You watched this film
★★★★

Poster for Superman (2025)
★★★★

Poster for KPop Demon Hunters (2025)
★★★★

Poster for 28 Years Later (2025)
★★★★½

Poster for Materialists (2025)
★½

Poster for The Mastermind (2025)
★★★½

Poster for Honey Don't! (2025)
★★★½

Poster for Sentimental Value (2025)
★★★★

Poster for It Was Just an Accident (2025)
★★★★

Poster for Pillion (2025)
★★★★½

Poster for Die My Love (2025)
★★★★

Poster for Eddington (2025)
★★★

Poster for Bring Her Back (2025)
★★★

Poster for Sinners (2025)
★★★★½

Poster for A Minecraft Movie (2025)
★★★★

Poster for Warfare (2025)
★★½

Poster for Black Bag (2025)
★★★½

Poster for Mickey 17 (2025)
★★★

Poster for Lurker (2025)
★★½

Poster for Train Dreams (2025)
"""

def star_converter(stars):
    match stars:
        case "½":
            return 1
        case "★":
            return 2
        case "★½":
            return 3
        case "★★":
            return 4
        case "★★½":
            return 5
        case "★★★":
            return 6
        case "★★★½":
            return 7
        case "★★★★":
            return 8
        case "★★★★½":
            return 9
        case "★★★★★":
            return 10
    

def split_text():
    film_list = []
    raw_text_list = raw_text.splitlines()
    raw_text_list = list(filter(None, raw_text_list))
    for line in raw_text_list:
        if line.startswith("Poster"):
            film_and_year = line.split("for")[1]
            film, year = film_and_year.split("(")
            year = year.replace(")", "")
        else:
            rating = star_converter(line)
            film_list.append({"title": film, "year": year, "rating": rating})

    sorted_film_list = sorted(film_list, key = lambda x: x["rating"])
    with open("2025_movies.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Year"])
        for film in sorted_film_list:
            writer.writerow([film["title"], film["year"]])


if __name__ == '__main__':
    # create_letterboxd_database()
    # get_databases()
    split_text()