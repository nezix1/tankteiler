export default {
  app: {
    name: "TankTeiler",
    description: "Schätze die Treibstoffkosten einer Fahrt und teile sie auf.",
    tagline: "Gemeinsam fahren. Kosten fair teilen.",
    guest: "Berechnung als Gast",
  },
  language: {
    label: "Sprache",
    de: "Deutsch",
    en: "English",
    ru: "Русский",
  },
  form: {
    title: "Fahrt planen",
    description:
      "Gib die Streckenlänge, den Verbrauch und einen Treibstoffpreis ein, um die Kosten zu schätzen.",
    origin: "Von (optional)",
    originPlaceholder: "z. B. Bern",
    destination: "Nach (optional)",
    destinationPlaceholder: "z. B. Zürich",
    distance: "Strecke",
    distanceUnit: "km",
    consumption: "Treibstoffverbrauch",
    consumptionUnit: "L / 100 km",
    fuelType: "Treibstoffart",
    fuelTypes: {
      bleifrei_95: "Bleifrei 95",
      bleifrei_98: "Bleifrei 98",
      diesel: "Diesel",
    },
    fuelPrice: "Treibstoffpreis",
    priceUnit: "CHF / L",
    priceNote:
      "Gib den Preis selbst ein; eine externe Preisquelle ist noch nicht verbunden.",
    extraCosts: "Zusätzliche Fahrtkosten",
    extraCostsHint: "Maut, Vignette oder andere gemeinsame Kosten",
    extraCostsUnit: "CHF",
    passengers: "Personen, die die Kosten teilen",
    calculate: "Fahrtkosten berechnen",
    calculating: "Berechnung läuft…",
    validation: {
      required: "Bitte fülle alle Pflichtfelder mit gültigen Werten aus.",
      passengers: "Wähle zwischen 1 und 8 Personen.",
      price:
        "Der Treibstoffpreis muss zwischen CHF 1.00 und CHF 3.50 pro Liter liegen.",
      api: "Der Berechnungsdienst konnte die Anfrage nicht abschliessen. Bitte versuche es erneut.",
    },
  },
  result: {
    title: "Fahrtkostenschätzung",
    fuelUsed: "Geschätzter Verbrauch",
    fuelCost: "Treibstoffkosten",
    extraCosts: "Zusätzliche Kosten",
    total: "Fahrtkosten insgesamt",
    eachPays: "Anteil pro Person",
    collected: "Eingenommener Gesamtbetrag",
    surplus: "Rundungsüberschuss",
    roundingNote:
      "Der Anteil jeder Person wird auf den nächsten ganzen Franken aufgerundet. Der Überschuss ist der Betrag über den geschätzten Fahrtkosten.",
    maps: "Route in Karten öffnen",
    googleMaps: "Google Maps",
    appleMaps: "Apple Karten",
    routeMissing: "Gib Start und Ziel ein, um eine Karte zu öffnen.",
  },
  footer: {
    manualDistance:
      "Strecke und Treibstoffpreis werden in dieser Phase manuell eingegeben. Routensuche und geprüfte Preisquellen folgen später.",
  },
} as const;
