import { MetricOption } from './types';

// 시가총액 범위 옵션 정의
export const MARKET_CAP_RANGES: MetricOption[] = [
  {
    key: 'mega',
    label: '초대형주 ($20B 이상)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'marketcap',
        operator: 'gte',
        value: '20000000000000'
      }]
    },
    tooltip: '시가총액 20조원 이상 기업'
  },
  {
    key: 'large',
    label: '대형주 (5조원 ~ 10조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'marketcap',
        operator: 'gt~lt',
        value: '5000000000000~10000000000000'
      }]
    },
    tooltip: '시가총액 5조원 이상 10조원 이하 기업'
  },
  {
    key: 'mid_large',
    label: '중대형주 (1조원 ~ 5조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'marketcap',
        operator: 'gt~lt',
        value: '1000000000000~5000000000000'
      }]
    },
    tooltip: '시가총액 1조원 이상 5조원 미만 기업'
  },
  {
    key: 'mid',
    label: '중형주 (5천억원 ~ 1조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'marketcap',
        operator: 'gt~lt',
        value: '500000000000~1000000000000'
      }]
    },
    tooltip: '시가총액 5천억원 이상 1조원 이하 기업'
  },
  {
    key: 'small',
    label: '소형주 (1천억원 ~ 5천억원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'marketcap',
        operator: 'gt~lt',
        value: '100000000000~500000000000'
      }]
    },
    tooltip: '시가총액 1천억원 이상 5천억원 이하 기업'
  },
  {
    key: 'micro',
    label: '제로형주 (1천억원 미만)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'marketcap',
        operator: 'lt',
        value: '100000000000'
      }]
    },
    tooltip: '시가총액 1천억원 미만 기업'
  }
] as const;

// Enterprise Value 범위 옵션 정의
export const ENTERPRISE_VALUE_RANGES: MetricOption[] = [
  {
    key: 'mega_ev',
    label: '초대형 (20조원 이상)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'enterprisevalue',
        operator: 'gte',
        value: '20000000000000'
      }]
    },
    tooltip: '기업가치 20조원 이상 기업'
  },
  {
    key: 'large_ev',
    label: '대형 (10조원 ~ 20조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'enterprisevalue',
        operator: 'gt~lt',
        value: '10000000000000~20000000000000'
      }]
    },
    tooltip: '기업가치 10조원 이상 20조원 이하 기업'
  },
  {
    key: 'mid_large_ev',
    label: '중대형 (5조원 ~ 10조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'enterprisevalue',
        operator: 'gt~lt',
        value: '5000000000000~10000000000000'
      }]
    },
    tooltip: '기업가치 5조원 이상 10조원 이하 기업'
  },
  {
    key: 'mid_ev',
    label: '중형 (1조원 ~ 5조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'enterprisevalue',
        operator: 'gt~lt',
        value: '1000000000000~5000000000000'
      }]
    },
    tooltip: '기업가치 1조원 이상 5조원 이하 기업'
  },
  {
    key: 'small_ev',
    label: '소형 (5천억원 ~ 1조원)',
    value: {
      operator: 'AND',
      clauses: [{
        field: 'enterprisevalue',
        operator: 'gt~lt',
        value: '500000000000~1000000000000'
      }]
    },
    tooltip: '기업가치 5천억원 이상 1조원 이하 기업'
  }
];

// constants.ts 파일에서 METRICS_BY_CATEGORY 타입을 정의
export type MetricsByCategory = {
  [key: string]: {
    key: string;
    kr: string;
    en: string;
    englishLabel: string;
    tooltip: string;
    inputType: string;
    unit: string;
  }[];
};

export const METRICS_BY_CATEGORY: MetricsByCategory = {
  "시가총액 지표": [
    {
      key: "marketcap",
      kr: "시가총액",
      en: "Market Cap",
      englishLabel: "Market Capitalization",
      tooltip: "발행주식수 × 주가",
      inputType: "select",
      options: MARKET_CAP_RANGES,
      unit: "USD"
    },
    {
      key: "enterprisevalue",
      kr: "기업가치(EV)",
      en: "Enterprise Value",
      englishLabel: "Enterprise Value",
      tooltip: "시가총액 + 순차입금",
      inputType: "select",
      options: ENTERPRISE_VALUE_RANGES,
      unit: "USD"
    }
  ],
  "성장성 지표": [
    {
      key: "revenuegrowth",
      kr: "매출 성장률",
      en: "Revenue Growth",
      englishLabel: "Revenue Growth Rate",
      tooltip: "전년 대비 매출 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "netincomegrowth",
      kr: "순이익 성장률",
      en: "Net Income Growth",
      englishLabel: "Net Income Growth Rate",
      tooltip: "전년 대비 순이익 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "epsgrowth",
      kr: "EPS 성장률",
      en: "EPS Growth",
      englishLabel: "Earnings Per Share Growth",
      tooltip: "전년 대비 주당순이익 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "ebitdagrowth",
      kr: "EBITDA 성장률",
      en: "EBITDA Growth",
      englishLabel: "EBITDA Growth Rate",
      tooltip: "전년 대비 EBITDA 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "ebitgrowth",
      kr: "EBIT 성장률",
      en: "EBIT Growth",
      englishLabel: "EBIT Growth Rate",
      tooltip: "전년 대비 영업이익 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "ocfgrowth",
      kr: "영업현금흐름 성장률",
      en: "OCF Growth",
      englishLabel: "Operating Cash Flow Growth",
      tooltip: "전년 대비 영업현금흐름 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "fcffgrowth",
      kr: "잉여현금흐름 성장률",
      en: "FCFF Growth",
      englishLabel: "Free Cash Flow Growth",
      tooltip: "전년 대비 잉여현금흐름 성장률",
      inputType: "number",
      unit: "%"
    }
  ],
  "수익성 지표": [
    {
      key: "grossmargin",
      kr: "매출총이익률",
      en: "Gross Margin",
      englishLabel: "Gross Profit Margin",
      tooltip: "매출총이익 / 매출액",
      inputType: "number",
      unit: "%"
    },
    {
      key: "operatingmargin",
      kr: "영업이익률",
      en: "Operating Margin",
      englishLabel: "Operating Profit Margin",
      tooltip: "영업이익 / 매출액",
      inputType: "number",
      unit: "%"
    },
    {
      key: "profitmargin",
      kr: "순이익률",
      en: "Profit Margin",
      englishLabel: "Net Profit Margin",
      tooltip: "당기순이익 / 매출액",
      inputType: "number",
      unit: "%"
    },
    {
      key: "ebitdamargin",
      kr: "EBITDA 마진",
      en: "EBITDA Margin",
      englishLabel: "EBITDA Margin",
      tooltip: "EBITDA / 매출액",
      inputType: "number",
      unit: "%"
    },
    {
      key: "roe",
      kr: "자기자본이익률",
      en: "ROE",
      englishLabel: "Return on Equity",
      tooltip: "당기순이익 / 자기자본",
      inputType: "number",
      unit: "%"
    },
    {
      key: "roa",
      kr: "총자산이익률",
      en: "ROA",
      englishLabel: "Return on Assets",
      tooltip: "당기순이익 / 총자산",
      inputType: "number",
      unit: "%"
    },
    {
      key: "roic",
      kr: "투하자본수익률",
      en: "ROIC",
      englishLabel: "Return on Invested Capital",
      tooltip: "NOPAT / 투하자본",
      inputType: "number",
      unit: "%"
    }
  ],
  "재무안정성 지표": [
    {
      key: "currentratio",
      kr: "유동비",
      en: "Current Ratio",
      englishLabel: "Current Ratio",
      tooltip: "유동자산 / 유동부채",
      inputType: "number",
      unit: "%"
    },
    {
      key: "quickratio",
      kr: "당좌비율",
      en: "Quick Ratio",
      englishLabel: "Quick Ratio",
      tooltip: "(유동자산 - 재고자산) / 유동부채",
      inputType: "number",
      unit: "%"
    },
    {
      key: "debttoequity",
      kr: "부채비율",
      en: "Debt to Equity",
      englishLabel: "Debt to Equity Ratio",
      tooltip: "총부채 / 자기자본",
      inputType: "number",
      unit: "%"
    },
    {
      key: "debttoebitda",
      kr: "부채/EBITDA",
      en: "Debt to EBITDA",
      englishLabel: "Debt to EBITDA",
      tooltip: "총부채 / EBITDA",
      inputType: "number",
      unit: "x"
    },
    {
      key: "netdebttoebitda",
      kr: "순부채/EBITDA",
      en: "Net Debt to EBITDA",
      englishLabel: "Net Debt to EBITDA",
      tooltip: "(총부채 - 현금성자산) / EBITDA",
      inputType: "number",
      unit: "x"
    },
    {
      key: "ebittointerestex",
      kr: "이자보상배율",
      en: "Interest Coverage",
      englishLabel: "Interest Coverage Ratio",
      tooltip: "EBIT / 이자비용",
      inputType: "number",
      unit: "x"
    },
    {
      key: "altmanzscore",
      kr: "알트만 Z-Score",
      en: "Altman Z-Score",
      englishLabel: "Altman Z-Score",
      tooltip: "기업의 부도험을 나타내는 지표",
      inputType: "number",
      unit: "score"
    }
  ],
  "밸류에이션 지표": [
    {
      key: "pricetoearnings",
      kr: "P/E 비율",
      en: "P/E Ratio",
      englishLabel: "Price to Earnings Ratio",
      tooltip: "주가 / 주당순이익",
      inputType: "number",
      unit: "x"
    },
    {
      key: "pricetobook",
      kr: "P/B 비율",
      en: "P/B Ratio",
      englishLabel: "Price to Book Ratio",
      tooltip: "주가 / 주당순자산",
      inputType: "number",
      unit: "x"
    },
    {
      key: "evtoebitda",
      kr: "EV/EBITDA",
      en: "EV/EBITDA",
      englishLabel: "Enterprise Value to EBITDA",
      tooltip: "기업가치 / EBITDA",
      inputType: "number",
      unit: "x"
    },
    {
      key: "pricetorevenue",
      kr: "P/S 비율",
      en: "P/S Ratio",
      englishLabel: "Price to Sales Ratio",
      tooltip: "시가총액 / 매출액",
      inputType: "number",
      unit: "x"
    },
    {
      key: "dividendyield",
      kr: "배당수익률",
      en: "Dividend Yield",
      englishLabel: "Dividend Yield",
      tooltip: "주당배당금 / 주가",
      inputType: "number",
      unit: "%"
    },
    {
      key: "earningsyield",
      kr: "이익수익률",
      en: "Earnings Yield",
      englishLabel: "Earnings Yield",
      tooltip: "주당순이익 / 주가 (P/E의 역수)",
      inputType: "number",
      unit: "%"
    }
  ],
  "현금흐름 지표": [
    {
      key: "freecashflow",
      kr: "잉여현금흐름",
      en: "Free Cash Flow",
      englishLabel: "Free Cash Flow",
      tooltip: "영업현금흐름 - 설비투자",
      inputType: "number",
      unit: "B"
    },
    {
      key: "ocfgrowth",
      kr: "영업현금흐름 성장률",
      en: "OCF Growth",
      englishLabel: "Operating Cash Flow Growth",
      tooltip: "전년 대비 영업현금흐름 성장률",
      inputType: "number",
      unit: "%"
    },
    {
      key: "capex",
      kr: "설비투자",
      en: "Capital Expenditure",
      englishLabel: "Capital Expenditure",
      tooltip: "유형자산 취득을 위한 투자금액",
      inputType: "number",
      unit: "B"
    },
    {
      key: "ocftocapex",
      kr: "OCF/CAPEX",
      en: "OCF/CAPEX",
      englishLabel: "Operating Cash Flow to CAPEX",
      tooltip: "영업현금흐름 / 설비투자",
      inputType: "number",
      unit: "x"
    }
  ]
};

// 지표 단위 정의
export const METRIC_UNITS = {
  PERCENTAGE: [
    'revenuegrowth', 'netincomegrowth', 'epsgrowth', 'ebitdagrowth',
    'ebitgrowth', 'ocfgrowth', 'fcffgrowth', 'grossmargin', 
    'operatingmargin', 'profitmargin', 'ebitdamargin', 'roe', 'roa',
    'roic', 'currentratio', 'quickratio', 'debttoequity', 'ltdebttoequity',
    'debttototalcapital', 'dividendyield', 'earningsyield'
  ],
  MULTIPLE: [
    'debttoebitda', 'netdebttoebitda', 'ebittointerestex',
    'pricetoearnings', 'pricetobook', 'evtoebitda', 'pricetorevenue',
    'ocftocapex'
  ],
  CURRENCY: [
    'marketcap', 'enterprisevalue', 'freecashflow', 'capex', 'nwc'
  ],
  SCORE: ['altmanzscore']
} as const;

// 카테고리 매핑
export const CATEGORY_MAPPING = {
  "시가총액 지표": "MarketCap",
  "성장성 지표": "Growth",
  "수익성 지표": "Profitability",
  "재무안정성 지표": "Financial_Stability",
  "류에이션 지표": "Valuation",
  "현금흐름 지표": "Cash_Flow"
};

// 역방향 매핑
export const REVERSE_CATEGORY_MAPPING = Object.entries(CATEGORY_MAPPING)
  .reduce((acc, [kr, en]) => ({...acc, [en]: kr}), {} as Record<string, string>);