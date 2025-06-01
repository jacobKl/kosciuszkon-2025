from enum import Enum


class Endowment(Enum):
    MY_ELECTRICITY = "Mój Prąd"
    CLEAN_AIR = "Czyste Powietrze"
    STOP_SMOG = "Stop Smog"
    THERMOMODERNIZATION_RELIEF = "Ulga termomodernizacyjna"
    THERMOMODERNIZATION_BONUS = "Premia termomodernizacyjna"


def get_endowment_url(endowment: Endowment) -> str:
    urls = {
        Endowment.MY_ELECTRICITY: "https://mojprad.gov.pl/",
        Endowment.CLEAN_AIR: "https://czystepowietrze.gov.pl/",
        Endowment.STOP_SMOG: "https://www.gov.pl/web/arimr/stop-smog-20---nowe-lepsze-zasady-od-31-marca2",
        Endowment.THERMOMODERNIZATION_RELIEF: "https://www.podatki.gov.pl/pit/ulgi-odliczenia-i-zwolnienia/ulga-termomodernizacyjna/",
        Endowment.THERMOMODERNIZATION_BONUS: "https://enerad.pl/premia-termomodernizacyjna-bgk/",
    }
    return urls.get(endowment, "#")


def get_description(endowment: Endowment) -> str:
    descriptions = {
        Endowment.MY_ELECTRICITY: "Dotacja do 50% kosztów inwestycji. Nie więcej niż 6.000 zł – 7.000 zł",
        Endowment.CLEAN_AIR: "Dotacja od 40% do 100% kosztów netto. Od 6.000 zł do 15.000 zł",
        Endowment.STOP_SMOG: "Do 100% kosztów inwestycji, nie więcej niż 53.000 zł",
        Endowment.THERMOMODERNIZATION_RELIEF: "Ulga podatkowa. Maksymalna kwota odpisu nie może przekroczyć 53.000 zł na podatnika",
        Endowment.THERMOMODERNIZATION_BONUS: "Dopłata do kredytu. Do 31% kosztów inwestycji",
    }
    return descriptions.get(endowment, "#")


def possible_endowments(hourly_production_kw: float) -> list:
    endowments = []

    if hourly_production_kw > 2 and hourly_production_kw < 10:
        endowments.append({
            "name": Endowment.MY_ELECTRICITY.value,
            "url": get_endowment_url(Endowment.MY_ELECTRICITY),
            "description": get_description(Endowment.MY_ELECTRICITY),
        })

    endowments.append({
        "name": Endowment.CLEAN_AIR.value,
        "url": get_endowment_url(Endowment.CLEAN_AIR),
        "description": get_description(Endowment.CLEAN_AIR),
    })

    endowments.append({
        "name": Endowment.STOP_SMOG.value,
        "url": get_endowment_url(Endowment.STOP_SMOG),
        "description": get_description(Endowment.STOP_SMOG),
    })

    endowments.append({
        "name": Endowment.THERMOMODERNIZATION_RELIEF.value,
        "url": get_endowment_url(Endowment.THERMOMODERNIZATION_RELIEF),
        "description": get_description(Endowment.THERMOMODERNIZATION_RELIEF),
    })

    endowments.append({
        "name": Endowment.THERMOMODERNIZATION_BONUS.value,
        "url": get_endowment_url(Endowment.THERMOMODERNIZATION_BONUS),
        "description": get_description(Endowment.THERMOMODERNIZATION_BONUS),
    })

    return endowments
