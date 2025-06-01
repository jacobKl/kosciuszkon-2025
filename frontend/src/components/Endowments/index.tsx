import React from "react";

const Endowments = ({ data }: { data: any[] }) => {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Dostępne finansowania</h2>
      {data.length === 0 ? (
        <p className="text-gray-500">Brak znanych dofinansowań</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white rounded-2xl overflow-hidden">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="px-6 py-4 font-thin text-gray-600">Nazwa</th>
                <th className="px-6 py-4 font-thin text-gray-600">Strona</th>
              </tr>
            </thead>
            <tbody>
              {data.map((endowment, index) => (
                <tr key={index} className="border-t">
                  <td className="px-6 py-4 font-thin text-gray-600">{endowment.name}</td>
                  <td className="px-6 py-4">
                    <a href={endowment.url} target="_blank" rel="noopener noreferrer" className="button-primary">
                        Sprawdź
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Endowments;
