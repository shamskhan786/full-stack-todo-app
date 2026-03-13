interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  accentColor: "blue" | "green" | "yellow" | "purple";
}

const colorMap = {
  blue: "bg-blue-50 text-blue-600 border-blue-100",
  green: "bg-green-50 text-green-600 border-green-100",
  yellow: "bg-yellow-50 text-yellow-600 border-yellow-100",
  purple: "bg-purple-50 text-purple-600 border-purple-100",
};

const iconBgMap = {
  blue: "bg-blue-100 text-blue-600",
  green: "bg-green-100 text-green-600",
  yellow: "bg-yellow-100 text-yellow-600",
  purple: "bg-purple-100 text-purple-600",
};

export default function StatsCard({ title, value, icon, accentColor }: StatsCardProps) {
  return (
    <div
      className={`rounded-xl border p-5 transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 ${colorMap[accentColor]} bg-white`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${iconBgMap[accentColor]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
