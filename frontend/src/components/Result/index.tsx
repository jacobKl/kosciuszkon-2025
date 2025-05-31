import React from 'react'
import { useResultQuery } from '../../queries/useResultQuery';

import Card from '../Card';
import InfoCard from '../InfoCard';
import ChartStats from '../ChartStats';
import CalculatorTable from '../CalculatorTable';
import { useAppContext } from '../../context/AppContextProvider';

const Result = () => {
    const { detailedConfiguratorState } = useAppContext();
    const { data, isLoading } = useResultQuery(detailedConfiguratorState);

    if (isLoading) return <Card>
        ładowanie...
    </Card>

    return (
        <Card title="Rezultat" full={true}>
            <div className="w-full">
                <div className="grid grid-cols-3 gap-4 mb-4">
                    <InfoCard animate={true} value={data.panel_installation_cost} unit=" PLN" text={"Koszt instalacji"} />
                    <InfoCard value={data.energy_price_buy_kwh} unit=" PLN" text={"Koszt zakupu 1kWh"} />
                    <InfoCard value={data.energy_price_sell_kwh} unit=" PLN" text={"Cena sprzedaży 1kWh"} />
                </div>

                <CalculatorTable data={data} />

                <ChartStats data={data.statistics} />
            </div>
        </Card>
    );
}

export default Result;