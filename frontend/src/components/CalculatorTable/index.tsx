import React from "react";

type EnergyStats = {
  panel_installation_cost: number;
  energy_price_buy_kwh: number;
  energy_price_sell_kwh: number;
  energy_price_growth_percent: number;
  used_energy_per_year: number;
  hourly_production_kw: number;
  yearly_production_kw: number;
  consumption_level_percent: number;
  produced_energy_per_year: number;
  self_consumption: number;
  energy_into_grid: number;
  energy_consumption: number;
};

type Props = {
  data: EnergyStats;
};

const CalculatorTable = ({ data }: Props) => {
  const formatNumber = (num: number, decimals = 2) =>
    num.toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });

  return (
    <table className="w-full table-auto border-collapse">
      <tbody>
        {[
          ["Wzrost ceny energii R/R", `${formatNumber(data.energy_price_growth_percent * 100)}%`],
          ["Roczne zużycie", `${formatNumber(data.used_energy_per_year)} kWh`],
          ["Produkcja na godzinę", `${formatNumber(data.hourly_production_kw)} kW`],
          ["Produkcja na rok", `${formatNumber(data.yearly_production_kw)} kWh`],
          ["Poziom konsumpcji", `${formatNumber(data.consumption_level_percent * 100)}%`],
          ["Własna konsumpcja", `${formatNumber(data.self_consumption)} kWh`],
          ["Energia wysłana do sieci", `${formatNumber(data.energy_into_grid)} kWh`],
          ["Zużycie energii", `${formatNumber(data.energy_consumption)} kWh`],
        ].map(([label, value]) => (
          <tr key={label} className="border-b border-primary last:border-b-0">
            <td className="py-3 pr-4 text-gray-700 font-thin">{label}</td>
            <td className="py-3 text-right text-gray-900">
              <b className="font-thin">{value}</b>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CalculatorTable;
