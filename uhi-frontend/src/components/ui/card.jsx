import React from "react";

// ✅ Card wrapper
export const Card = ({ children, className = "" }) => {
  return (
    <div className={`bg-white shadow-lg rounded-xl p-6 ${className}`}>
      {children}
    </div>
  );
};

// ✅ Card content wrapper
export const CardContent = ({ children, className = "" }) => {
  return <div className={`p-2 ${className}`}>{children}</div>;
};
