import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const ProfitChart = ({ data }: { data: any[] }) => {
  return (
    <div className="mb-10">
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 40, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis
            domain={["auto", "auto"]}
            tickFormatter={(value) => value.toLocaleString()}
          />
          <Tooltip
            formatter={(value: number, name: string) => {
              let label = "";
              switch (name) {
                case "state":
                  label = "Zwrot z inwestycji";
                  break;
                default:
                  label = name;
              }
              return [`${value.toLocaleString()} PLN`, label];
            }}
            labelFormatter={(label) => `Rok: ${label}`}
          />
          <Legend
            formatter={(value) => {
              switch (value) {
                case "state":
                  return "Zwrot z inwestycji";
                default:
                  return value;
              }
            }}
          />
          <Bar
            dataKey="state"
            fill="#82ca9d"
            barSize={40}
            animationDuration={1500}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProfitChart;
