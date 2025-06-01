
type OptionProp = {
  value: string | number;
  label: string;
};

type SelectProps = {
  options: OptionProp[];
  value: string | number;
  onChange: (value: string) => void;
};

const Select = ({ options, value, onChange }: SelectProps) => {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="h-12 w-full border-b-[1px] border-gray-200 text-gray-900 bg-transparent focus:outline-none focus:border-primary"
    >
      {options.map((single, ix) => (
        <option key={ix} value={single.value}>
          {single.label}
        </option>
      ))}
    </select>
  );
};

export default Select;
