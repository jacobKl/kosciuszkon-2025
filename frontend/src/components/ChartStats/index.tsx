import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const ChartStats = ({ data }: { data: any }) => {
  return (
    <div className="mb-10">
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={data} margin={{ top: 20, right: 40, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis domain={["auto", "auto"]} tickFormatter={(value) => value.toLocaleString()} />
          <Tooltip
            formatter={(value: number, name: string) => {
              let label = "";
              switch (name) {
                case "cost_without_installation":
                  label = "Koszt bez instalacji";
                  break;
                case "profit":
                  label = "Zysk";
                  break;
                case "cost":
                  label = "Koszt";
                  break;
                case "savings":
                  label = "Oszczędności";
                  break;
                default:
                  label = name;
              }
              return [`${value.toLocaleString()} PLN`, label];
            }}
          />
          <Legend
            formatter={(value) => {
              switch (value) {
                case "cost_without_installation":
                  return "Koszt bez instalacji";
                case "profit":
                  return "Zysk";
                case "cost":
                  return "Koszt";
                case "savings":
                  return "Oszczędności";
                default:
                  return value;
              }
            }}
          />
          <Line type="monotone" dataKey="cost_without_installation" stroke="#8884d8" strokeWidth={2} dot={false} animationDuration={1500} />
          <Line type="monotone" dataKey="profit" stroke="#82ca9d" strokeWidth={2} dot={false} animationDuration={1500} />
          <Line type="monotone" dataKey="cost" stroke="#ffc658" strokeWidth={2} dot={false} animationDuration={1500} />
          <Line type="monotone" dataKey="savings" stroke="#ff7300" strokeWidth={2} dot={false} animationDuration={1500} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartStats;
