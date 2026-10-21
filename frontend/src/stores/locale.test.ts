import { beforeEach, describe, expect, it } from "vitest";
import { createPinia, setActivePinia } from "pinia";

import { i18n } from "../i18n";
import { useLocaleStore } from "./locale";

describe("locale store", () => {
  beforeEach(() => {
    localStorage.clear();
    i18n.global.locale.value = "en";
    setActivePinia(createPinia());
  });

  it("changes locale, persists the selection, and updates document language", () => {
    const store = useLocaleStore();

    store.setLocale("de");

    expect(store.locale).toBe("de");
    expect(i18n.global.locale.value).toBe("de");
    expect(localStorage.getItem("tankteiler.locale")).toBe("de");
    expect(document.documentElement.lang).toBe("de");
  });

  it("restores a saved supported locale", () => {
    localStorage.setItem("tankteiler.locale", "ru");
    const store = useLocaleStore();

    store.restoreLocale();

    expect(store.locale).toBe("ru");
    expect(document.documentElement.lang).toBe("ru");
  });

  it("ignores an unsupported saved locale", () => {
    localStorage.setItem("tankteiler.locale", "fr");
    const store = useLocaleStore();

    store.restoreLocale();

    expect(store.locale).toBe("en");
  });
});
