#!/bin/bash

# 프로젝트 디렉토리 생성
mkdir -p frontend/src/{components/{FilterSidebar,Screener,common},pages,styles} frontend/public

# 기본 파일 생성
touch frontend/src/{App.tsx,index.css,main.tsx} frontend/{package.json,tsconfig.json,vite.config.ts}

# package.json 내용 추가
cat <<EOL > frontend/package.json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.3.0",
    "@tanstack/react-query": "^5.0.0",
    "@tremor/react": "^1.0.0"
  },
  "devDependencies": {
    "typescript": "^4.9.4",
    "vite": "^4.0.0",
    "@vitejs/plugin-react": "^3.0.0"
  }
}
EOL

# tsconfig.json 내용 추가
cat <<EOL > frontend/tsconfig.json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "esnext",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"]
}
EOL

# vite.config.ts 내용 추가
cat <<EOL > frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    open: true,
  },
})
EOL

# main.tsx 내용 추가
cat <<EOL > frontend/src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
EOL

# App.tsx 내용 추가
cat <<EOL > frontend/src/App.tsx
import React from 'react'
import FilterSidebar from './components/FilterSidebar'
import Screener from './components/Screener'

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Intrinio Dashboard</h1>
      <FilterSidebar />
      <Screener />
    </div>
  )
}

export default App
EOL

# index.css 내용 추가
cat <<EOL > frontend/src/index.css
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
EOL

# FilterSidebar 컴포넌트 생성
cat <<EOL > frontend/src/components/FilterSidebar/index.tsx
import React, { useState } from 'react'
import { Tooltip } from '../common/Tooltip'
import { Button, Input } from '@tremor/react'

const categories = {
  성장성: [
    { key: 'revenuegrowth', label: '매출 성장률' },
    { key: 'netincomegrowth', label: '순이익 성장률' },
    // 나머지 성장성 지표 추가
  ],
  수익성: [
    { key: 'grossmargin', label: '매출 총이익률' },
    { key: 'operatingmargin', label: '영업 이익률' },
    // 나머지 수익성 지표 추가
  ],
  // 다른 카테고리도 동일하게 추가
}

const FilterSidebar: React.FC = () => {
  const [filters, setFilters] = useState<{ [key: string]: number | null }>({})

  const handleInputChange = (key: string, value: string) => {
    setFilters({
      ...filters,
      [key]: value ? parseFloat(value) : null,
    })
  }

  const resetFilters = () => {
    setFilters({})
  }

  const applyFilters = () => {
    // 필터 적용 로직 구현
  }

  return (
    <div className="filter-sidebar">
      {Object.keys(categories).map((category) => (
        <div key={category} className="filter-category">
          <h3>{category}</h3>
          {categories[category].map((metric) => (
            <div key={metric.key} className="filter-item">
              <label>
                {metric.label}
                <Tooltip content={`설명: ${metric.label}에 대한 추가 설명`}>
                  ?
                </Tooltip>
              </label>
              <Input
                type="number"
                step="0.01"
                value={filters[metric.key] ?? ''}
                onChange={(e) => handleInputChange(metric.key, e.target.value)}
              />
            </div>
          ))}
        </div>
      ))}
      <div className="filter-actions">
        <Button onClick={applyFilters}>검색</Button>
        <Button onClick={resetFilters} variant="secondary">
          초기화
        </Button>
      </div>
    </div>
  )
}

export default FilterSidebar
EOL

# Screener 컴포넌트 생성
cat <<EOL > frontend/src/components/Screener/index.tsx
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Table, TableHeader, TableBody, TableRow, TableCell } from '@tremor/react'

const Screener: React.FC = () => {
  const { data, isLoading, error } = useQuery(['screenerData'], fetchScreenerData)

  async function fetchScreenerData() {
    const response = await axios.get('/api/screener/routes.py') // 실제 API 엔드포인트로 수정
    return response.data
  }

  if (isLoading) return <div>로딩 중...</div>
  if (error) return <div>데이터를 불러오는 중 오류가 발생했습니다.</div>

  return (
    <div className="screener-container">
      <Table>
        <TableHeader>
          <TableRow>
            <TableCell>종목명</TableCell>
            <TableCell>매출 성장률 (%)</TableCell>
            <TableCell>순이익 성장률 (%)</TableCell>
            {/* 다른 지표들 추가 */}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item: any) => (
            <TableRow key={item.symbol}>
              <TableCell>{item.symbol}</TableCell>
              <TableCell>{item.revenuegrowth.toFixed(2)}</TableCell>
              <TableCell>{item.netincomegrowth.toFixed(2)}</TableCell>
              {/* 다른 지표들 추가 */}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

export default Screener
EOL

# Tooltip 컴포넌트 생성
cat <<EOL > frontend/src/components/common/Tooltip.tsx
import React from 'react'

interface TooltipProps {
  content: string
  children: React.ReactNode
}

const Tooltip: React.FC<TooltipProps> = ({ content, children }) => {
  return (
    <span className="tooltip">
      {children}
      <span className="tooltiptext">{content}</span>
    </span>
  )
}

export default Tooltip
EOL

# npm 패키지 설치
cd frontend
npm install