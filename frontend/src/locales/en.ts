export default {
  app: {
    name: "TankTeiler",
    description: "Estimate a trip's fuel cost and split it between passengers.",
    tagline: "Share the road. Split the cost.",
    guest: "Guest calculation",
  },
  language: {
    label: "Language",
    de: "Deutsch",
    en: "English",
    ru: "Русский",
  },
  form: {
    title: "Plan your trip",
    description:
      "Enter your route distance, vehicle consumption, and a fuel price to estimate the cost.",
    origin: "From (optional)",
    originPlaceholder: "e.g. Bern",
    destination: "To (optional)",
    destinationPlaceholder: "e.g. Zürich",
    distance: "Distance",
    distanceUnit: "km",
    consumption: "Fuel consumption",
    consumptionUnit: "L / 100 km",
    fuelType: "Fuel type",
    fuelTypes: {
      bleifrei_95: "Unleaded 95",
      bleifrei_98: "Unleaded 98",
      diesel: "Diesel",
    },
    fuelPrice: "Fuel price",
    priceUnit: "CHF / L",
    priceNote:
      "Enter the price yourself; no external price source is connected yet.",
    extraCosts: "Additional trip costs",
    extraCostsHint: "Toll, vignette, or other shared costs",
    extraCostsUnit: "CHF",
    passengers: "People sharing the cost",
    calculate: "Calculate trip cost",
    calculating: "Calculating…",
    validation: {
      required: "Please complete all required fields with valid values.",
      passengers: "Choose between 1 and 8 people.",
      price: "Fuel price must be between CHF 1.00 and CHF 3.50 per liter.",
      api: "The calculation service could not complete the request. Please try again.",
    },
  },
  result: {
    title: "Trip estimate",
    fuelUsed: "Estimated fuel used",
    fuelCost: "Fuel cost",
    extraCosts: "Additional costs",
    total: "Total trip cost",
    eachPays: "Each person pays",
    collected: "Total collected",
    surplus: "Rounding surplus",
    roundingNote:
      "Each person's share is rounded up to the next whole franc. The surplus is the amount collected above the estimated trip cost.",
    maps: "Open route in maps",
    googleMaps: "Google Maps",
    appleMaps: "Apple Maps",
    routeMissing: "Add both route locations to open a map.",
  },
  footer: {
    manualDistance:
      "Distance and fuel price are entered manually in this stage. Route lookup and verified fuel-price sources will be added later.",
  },
} as const;
