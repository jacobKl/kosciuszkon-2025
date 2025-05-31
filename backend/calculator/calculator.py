import os
from datetime import datetime

import yaml


class Calculator:
    def __init__(self, input=None):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data.yaml')
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        input = input or {}

        self.panel_installation_cost = input.get('panel_installation_cost', data.get('panel_installation_cost'))
        self.energy_price_buy_kwh = input.get('energy_price_buy_kwh', data.get('energy_price_buy_kwh'))
        self.energy_price_sell_kwh = input.get('energy_price_sell_kwh', data.get('energy_price_sell_kwh'))
        self.energy_price_growth = input.get('energy_price_growth', data.get('energy_price_growth'))
        self.energy_per_year = input.get('energy_per_year', data.get('energy_per_year'))
        self.hourly_production_kw = input.get('hourly_production_kw', data.get('hourly_production_kw'))
        self.consumption_level_percent = input.get('consumption_level_percent', data.get('consumption_level_percent'))

    def calculate_yearly_buy_price(self, year):
        current_year = datetime.now().year
        price = self.energy_price_buy_kwh

        while current_year + 1 <= year:
            current_year = current_year + 1
            price += price + (price * self.energy_price_growth)

        return price

    def calculate_yearly_sell_price(self, year):
        current_year = datetime.now().year
        price = self.energy_price_buy_kwh

        while current_year + 1 <= year:
            current_year = current_year + 1
            price += price + (price * self.energy_price_growth)

        return price

    def produced_energy_per_year(self):
        return self.hourly_production_kw * 24 * 365

    def cost_without_installation(self, year):
        return self.calculate_yearly_buy_price(year) * self.energy_per_year

    def self_consumption(self):
        return self.produced_energy_per_year() * self.consumption_level_percent

    def energy_into_grid(self):
        return self.produced_energy_per_year() - self.self_consumption()

    def energy_consumption(self):
        return self.energy_per_year - self.self_consumption()

    def profit(self, year):
        return self.calculate_yearly_sell_price(year) * self.energy_into_grid()

    def cost(self, year):
        return self.calculate_yearly_buy_price(year) * self.energy_consumption() - self.profit(year)

    def savings(self, year):
        return self.cost(year) - self.cost_without_installation(year)

    def to_result_dict(self, year):
        current_year = int(datetime.now().year)
        result = {
            "panel_installation_cost": self.panel_installation_cost,
            "energy_price_buy_kwh": self.energy_price_buy_kwh,
            "energy_price_sell_kwh": self.energy_price_sell_kwh,
            "energy_price_growth_percent": self.energy_price_growth,
            "used_energy_per_year": self.energy_per_year,
            "hourly_production_kw": self.hourly_production_kw,
            "yearly_production_kw": self.produced_energy_per_year(),
            "consumption_level_percent": self.consumption_level_percent,

            "produced_energy_per_year": self.produced_energy_per_year(),
            "self_consumption": self.self_consumption(),
            "energy_into_grid": self.energy_into_grid(),
            "energy_consumption": self.energy_consumption(),

            "statistics": {}
        }

        while current_year + 1 <= year:
            current_year += 1
            result["statistics"][current_year] = {
                "cost_without_installation": self.cost_without_installation(current_year),
                "profit": self.profit(current_year),
                "cost": self.cost(current_year),
                "savings": self.savings(current_year)
            }

        return result
