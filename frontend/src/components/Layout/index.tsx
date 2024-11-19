import React from 'react';

interface LayoutProps {
  sidebar: React.ReactNode;
  activeFilters?: React.ReactNode;
  children: React.ReactNode;
}

const Layout = ({ sidebar, activeFilters, children }: LayoutProps) => {
  return (
    <div className="flex h-screen bg-[#1D2333]">
      <div className="w-80 h-full overflow-y-auto border-r border-gray-700">
        {sidebar}
      </div>
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {activeFilters && (
          <div className="w-full bg-[#252B3D] border-b border-gray-700">
            <div className="p-4">
              {activeFilters}
            </div>
          </div>
        )}
        <div className="flex-1 overflow-auto p-4">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout; 