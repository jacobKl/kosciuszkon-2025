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

        self.panel_installation_cost = float(input.get('panel_installation_cost', data.get('panel_installation_cost')))
        self.energy_price_buy_kwh = float(input.get('energy_price_buy_kwh', data.get('energy_price_buy_kwh')))
        self.energy_price_sell_kwh = float(input.get('energy_price_sell_kwh', data.get('energy_price_sell_kwh')))
        self.energy_price_growth = float(input.get('energy_price_growth', data.get('energy_price_growth')))
        self.energy_per_year = float(input.get('energy_per_year', data.get('energy_per_year')))
        self.hourly_production_kw = float(input.get('hourly_production_kw', data.get('hourly_production_kw')))
        self.consumption_level_percent = float(
            input.get('consumption_level_percent', data.get('consumption_level_percent')))

    def calculate_yearly_buy_price(self, year):
        current_year = datetime.now().year
        price = self.energy_price_buy_kwh

        while current_year + 1 <= year:
            current_year = current_year + 1
            price = price + (1 * self.energy_price_growth)

        return price

    def calculate_yearly_sell_price(self, year):
        current_year = datetime.now().year
        price = self.energy_price_buy_kwh

        while current_year + 1 <= year:
            current_year = current_year + 1
            price = price + (1 * self.energy_price_growth)

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
        return self.cost_without_installation(year) - self.cost(year)

    def state(self, year):
        current_year = datetime.now().year
        savings_sum = 0

        while current_year + 1 <= year:
            current_year += 1
            savings_sum += self.savings(current_year)

        return savings_sum

    def to_result_dict(self, year):
        current_year = int(datetime.now().year)
        result = {
            "panel_installation_cost": round(self.panel_installation_cost, 2),
            "energy_price_buy_kwh": round(self.energy_price_buy_kwh, 2),
            "energy_price_sell_kwh": round(self.energy_price_sell_kwh, 2),
            "energy_price_growth_percent": round(self.energy_price_growth, 2),
            "used_energy_per_year": round(self.energy_per_year, 2),
            "hourly_production_kw": round(self.hourly_production_kw, 2),
            "yearly_production_kw": round(self.produced_energy_per_year(), 2),
            "consumption_level_percent": round(self.consumption_level_percent, 2),

            "produced_energy_per_year": round(self.produced_energy_per_year(), 2),
            "self_consumption": round(self.self_consumption(), 2),
            "energy_into_grid": round(self.energy_into_grid(), 2),
            "energy_consumption": round(self.energy_consumption(), 2),

            "statistics": []
        }

        while current_year + 1 <= year:
            current_year += 1
            result["statistics"].append({
                "year": current_year,
                "cost_without_installation": round(self.cost_without_installation(current_year), 2),
                "profit": round(self.profit(current_year), 2),
                "cost": round(self.cost(current_year), 2),
                "savings": round(self.savings(current_year), 2),
                "state": round(self.state(current_year), 2)
            })

        return result
