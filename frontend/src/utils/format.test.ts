import { describe, expect, it } from "vitest";

import { formatCurrency, formatDecimal } from "./format";

describe("exact localized formatting", () => {
  it("formats CHF values with locale-specific grouping and decimal separators", () => {
    expect(formatCurrency("1234.50", "en")).toContain("1'234.50");
    expect(formatCurrency("1234.50", "de")).toContain("1'234.50");
    expect(formatCurrency("1234.50", "ru")).toContain("1 234,50");
  });

  it("localizes liters while preserving meaningful decimal precision", () => {
    expect(formatDecimal("1234.5000", "en")).toBe("1'234.5");
    expect(formatDecimal("12.3456", "de")).toBe("12.3456");
    expect(formatDecimal("12", "ru")).toBe("12");
  });
});
