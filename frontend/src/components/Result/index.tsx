import React from "react";
import {useResultQuery} from "../../queries/useResultQuery";

import Card from "../Card";
import InfoCard from "../InfoCard";
import ChartStats from "../ChartStats";
import CalculatorTable from "../CalculatorTable";
import ProfitChart from "../ProfitChart";
import Endowments from "../Endowments";

import {useAppContext} from "../../context/AppContextProvider";

const Result = () => {
    const {detailedConfiguratorState} = useAppContext();
    const {data, isLoading} = useResultQuery(detailedConfiguratorState);

    if (isLoading) return <Card>ładowanie...</Card>;

    return (
        <Card title="Rezultat" full={true} url={data.pdf_url}>
            <div className="w-full flex flex-col gap-6">
                <div className="grid grid-cols-3 gap-4 mb-4">
                    <InfoCard value={data.panel_installation_cost} unit=" PLN" text={"Koszt instalacji"}/>
                    <InfoCard value={data.energy_price_buy_kwh} unit=" PLN" text={"Koszt zakupu 1kWh"}/>
                    <InfoCard value={data.energy_price_sell_kwh} unit=" PLN" text={"Cena sprzedaży 1kWh"}/>
                </div>

                <CalculatorTable data={data}/>

                <div className="py-3 px-2 rounded shadow bg-gray-100">
                    <h2 className="text-center mb-4 text-xl font-thin">Statysyki</h2>
                    <ChartStats data={data.statistics}/>
                </div>

                <div className="py-3 px-2 rounded shadow bg-gray-100">
                    <h2 className="text-center mb-4 text-xl font-thin">Zwrot kosztów inwestycji</h2>
                    <ProfitChart data={data.statistics}/>
                </div>

                <Endowments data={data.endowments}/>
            </div>
        </Card>
    );
};

export default Result;
