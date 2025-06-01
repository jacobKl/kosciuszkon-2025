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
        Endowment.STOP_SMOG: "https://www.gov.pl/web/gios/stop-smog",
        Endowment.THERMOMODERNIZATION_RELIEF: "https://www.gov.pl/web/finanse/ulga-termomodernizacyjna",
        Endowment.THERMOMODERNIZATION_BONUS: "https://www.bgk.pl/programs/termomodernization-and-renovation-bonus/",
    }
    return urls.get(endowment, "#")


def get_image_url(endowment: Endowment) -> str:
    image_urls = {
        Endowment.MY_ELECTRICITY: "https://mojprad.gov.pl/wp-content/uploads/2025/02/logo.webp",
        Endowment.CLEAN_AIR: "https://czystepowietrze.gov.pl/wp-content/uploads/2020/01/logo-czyste-powietrze.png",
        Endowment.STOP_SMOG: "https://czystepowietrze.gov.pl/wp-content/uploads/2020/01/logo-stop-smog.png",
        Endowment.THERMOMODERNIZATION_RELIEF: "https://www.gov.pl/web/finanse/logo-ulga-termomodernizacyjna.png",
        Endowment.THERMOMODERNIZATION_BONUS: "https://www.bgk.pl/wp-content/uploads/2020/01/logo-premia-termomodernizacyjna.png",
    }
    return image_urls.get(endowment, "#")
