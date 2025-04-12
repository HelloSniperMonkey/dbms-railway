import React from 'react';

export const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = ({ children, ...props }) => {
    return (
        <button {...props} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            {children}
        </button>
    );
};

export const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = ({ ...props }) => {
    return (
        <input {...props} className="border rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
    );
};

export const Card: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => {
    return (
        <div className="border rounded shadow p-4">
            <h2 className="font-bold text-lg">{title}</h2>
            <div>{children}</div>
        </div>
    );
};