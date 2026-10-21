import { describe, expect, it } from "vitest";

import { parseDecimalToScaledInteger } from "./decimal";

describe("parseDecimalToScaledInteger", () => {
  it("parses decimal input without converting through floating point", () => {
    expect(parseDecimalToScaledInteger("123.45", 2)).toBe(12345n);
    expect(parseDecimalToScaledInteger("1.789", 3)).toBe(1789n);
  });

  it("rejects malformed and over-precision values", () => {
    expect(parseDecimalToScaledInteger("1,25", 2)).toBeNull();
    expect(parseDecimalToScaledInteger("1.001", 2)).toBeNull();
    expect(parseDecimalToScaledInteger("-1", 2)).toBeNull();
  });
});
