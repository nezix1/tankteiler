import { defineStore } from "pinia";

import { i18n, isSupportedLocale, type SupportedLocale } from "../i18n";

export const useLocaleStore = defineStore("locale", {
  state: () => ({
    locale: i18n.global.locale.value as SupportedLocale,
  }),
  actions: {
    setLocale(locale: SupportedLocale) {
      this.locale = locale;
      i18n.global.locale.value = locale;
      localStorage.setItem("tankteiler.locale", locale);
      this.syncDocumentLanguage();
    },
    syncDocumentLanguage() {
      document.documentElement.lang = this.locale;
      document.title = "TankTeiler";
      document
        .querySelector('meta[name="description"]')
        ?.setAttribute("content", i18n.global.t("app.description"));
    },
    restoreLocale() {
      const storedLocale = localStorage.getItem("tankteiler.locale");
      if (isSupportedLocale(storedLocale)) {
        this.setLocale(storedLocale);
      }
    },
  },
});
