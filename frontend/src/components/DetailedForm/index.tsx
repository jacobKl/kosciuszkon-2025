import React from 'react'
import Card from '../Card';

type DetailedConfigurationState = {
  panel_installation_cost: number | null;
  energy_price_buy_kwh: number | null;
  energy_price_sell_kwh: number | null;
  energy_price_growth: number | null;
  energy_per_year: number | null;
  hourly_production_kw: number | null;
  consumption_level: number | null;
};

const DetailedForm = () => {
    return (<Card full={true}>todo</Card>);
}

export default DetailedForm;