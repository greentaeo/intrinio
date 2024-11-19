// Path: /frontend/src/components/FilterSidebar/Filter.tsx

import { useState } from 'react';
import { FilterProps, FilterValue } from './types';
import { NumberInput } from "@tremor/react";
import { Tooltip } from '../common/Tooltip';

export const Filter: React.FC<FilterProps> = ({ value, onChange }) => {
  const [localValue, setLocalValue] = useState<FilterValue>(() => ({
    min: value.currentValue?.min ?? null,
    max: value.currentValue?.max ?? null
  }));

  const handleApply = () => {
    if (localValue.min !== null || localValue.max !== null) {
      onChange(localValue);
    }
  };

  const handleReset = () => {
    const resetValue: FilterValue = { min: null, max: null };
    setLocalValue(resetValue);
    onChange(resetValue);
  };

  return (
    <div className="mb-4">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <Tooltip content={value.metric.tooltip || "설명"}>
            <label className="text-sm text-gray-200">
              {value.metric.kr} ({value.metric.unit})
            </label>
          </Tooltip>
          <button 
            onClick={handleReset} 
            className="text-xs text-gray-400 hover:text-gray-200"
          >
            초기화
          </button>
        </div>
        <div className="flex gap-2">
          <NumberInput
            className="w-full bg-[#252B3D]"
            value={localValue.min?.toString() ?? ''}
            onValueChange={(val: string | number) => {
              setLocalValue(prev => ({
                ...prev,
                min: val === '' || val === null ? null : Number(val)
              }));
            }}
            placeholder="최소"
            step={0.01}
            enableStepper={false}
          />
          <NumberInput
            className="w-full bg-[#252B3D]"
            value={localValue.max?.toString() ?? ''}
            onValueChange={(val: string | number) => {
              setLocalValue(prev => ({
                ...prev,
                max: val === '' || val === null ? null : Number(val)
              }));
            }}
            placeholder="최대"
            step={0.01}
            enableStepper={false}
          />
        </div>
        <button 
          onClick={handleApply}
          className="mt-2 px-3 py-1 bg-blue-600 text-sm rounded hover:bg-blue-700"
        >
          적용
        </button>
      </div>
    </div>
  );
};