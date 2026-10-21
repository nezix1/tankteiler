function localeTag(locale: string): string {
  if (locale === "de") return "de-CH";
  if (locale === "en") return "en-CH";
  return "ru-RU";
}

export function formatDecimal(value: string, locale: string): string {
  const [whole, fraction = ""] = value.split(".");
  const trimmedFraction = fraction.replace(/0+$/, "");
  const localizedLocale = localeTag(locale);
  const groupedWhole = new Intl.NumberFormat(localizedLocale, {
    maximumFractionDigits: 0,
  }).format(BigInt(whole));
  if (!trimmedFraction) return groupedWhole;

  const decimalSeparator = new Intl.NumberFormat(localizedLocale)
    .formatToParts(1.1)
    .find((part) => part.type === "decimal")?.value;
  return `${groupedWhole}${decimalSeparator ?? "."}${trimmedFraction}`;
}

export function formatCurrency(value: string, locale: string): string {
  const [whole, fraction = ""] = value.split(".");
  const localizedLocale = localeTag(locale);
  const groupedWhole = new Intl.NumberFormat(localizedLocale, {
    maximumFractionDigits: 0,
  }).format(BigInt(whole));
  const formattedParts = new Intl.NumberFormat(localizedLocale, {
    style: "currency",
    currency: "CHF",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).formatToParts(0);
  let insertedInteger = false;

  return formattedParts
    .map((part) => {
      if (part.type === "integer") {
        if (insertedInteger) return "";
        insertedInteger = true;
        return groupedWhole;
      }
      if (part.type === "fraction") {
        return fraction.padEnd(2, "0").slice(0, 2);
      }
      return part.value;
    })
    .join("");
}
