import { createI18n } from "vue-i18n";

import de from "./locales/de";
import en from "./locales/en";
import ru from "./locales/ru";

export const supportedLocales = ["de", "en", "ru"] as const;
export type SupportedLocale = (typeof supportedLocales)[number];

function getInitialLocale(): SupportedLocale {
  const storedLocale = localStorage.getItem("tankteiler.locale");
  if (isSupportedLocale(storedLocale)) {
    return storedLocale;
  }

  const browserLocale = navigator.language.toLowerCase().split("-")[0];
  return isSupportedLocale(browserLocale) ? browserLocale : "en";
}

export function isSupportedLocale(
  value: string | null,
): value is SupportedLocale {
  return supportedLocales.includes(value as SupportedLocale);
}

export const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: "en",
  messages: { de, en, ru },
});
