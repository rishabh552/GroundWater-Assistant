"use client";

import React, { createContext, useContext, useState } from 'react';
import en from '../locales/en.json';
import ta from '../locales/ta.json';

type Locale = 'en' | 'ta';
type Translations = typeof en;

interface LanguageContextType {
    language: Locale;
    setLanguage: (lang: Locale) => void;
    t: (key: keyof Translations) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const translations: Record<Locale, Translations> = {
    en,
    ta
};

export function LanguageProvider({ children }: { children: React.ReactNode }) {
    // Default to English, could detect browser pref later
    const [language, setLanguage] = useState<Locale>('en');

    const t = (key: keyof Translations) => {
        return translations[language][key] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
}
