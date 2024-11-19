import { 
  Table,
  TableHead,
  TableRow,
  TableHeaderCell,
  TableBody,
  TableCell,
  Text
} from "@tremor/react";

interface ScreenerData {
  id: string;
  ticker: string;
  name: string;
  exchange: string;
  [key: string]: any;
}

interface ScreenerTableProps {
  data: ScreenerData[];
  isLoading: boolean;
}

const ScreenerTable = ({ data, isLoading }: ScreenerTableProps) => {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Text>데이터를 불러오는 중...</Text>
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="flex justify-center items-center h-64">
        <Text>데이터가 없습니다.</Text>
      </div>
    );
  }

  const columns = [
    { key: 'ticker', label: '티커' },
    { key: 'name', label: '기업명' },
    { key: 'exchange', label: '거래소' },
    { key: 'marketcap', label: '시가총액' },
    { key: 'operatingmargin', label: '영업이익률' },
    { key: 'revenuegrowth', label: '매출성장률' },
    { key: 'netincomegrowth', label: '순이익성장률' },
    { key: 'roe', label: 'ROE' },
    { key: 'pricetoearnings', label: 'P/E' },
    { key: 'pricetobook', label: 'P/B' },
    { key: 'evtoebitda', label: 'EV/EBITDA' }
  ];

  const formatValue = (value: any, key: string) => {
    if (value === null || value === undefined) return '-';
    
    const percentageMetrics = ['operatingmargin', 'revenuegrowth', 'netincomegrowth', 'roe'];
    if (percentageMetrics.includes(key)) {
      return `${Number(value).toFixed(2)}%`;
    }
    
    const ratioMetrics = ['pricetoearnings', 'pricetobook', 'evtoebitda'];
    if (ratioMetrics.includes(key)) {
      return Number(value).toFixed(2);
    }
    
    if (key === 'marketcap') {
      return `${(Number(value) / 100000000).toFixed(0)}억`;
    }
    
    return value;
  };

  return (
    <div className="overflow-x-auto">
      <Table>
        <TableHead>
          <TableRow>
            {columns.map(column => (
              <TableHeaderCell 
                key={column.key}
                className="bg-[#252B3D] text-white"
              >
                {column.label}
              </TableHeaderCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item) => (
            <TableRow key={item.id} className="hover:bg-[#2A3141]">
              {columns.map(column => (
                <TableCell 
                  key={`${item.id}-${column.key}`}
                  className="text-white"
                >
                  <Text>{formatValue(item[column.key], column.key)}</Text>
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ScreenerTable;
