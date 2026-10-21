export function parseDecimalToScaledInteger(
  value: string,
  decimalPlaces: number,
): bigint | null {
  const normalized = value.trim();
  const match = /^(\d+)(?:\.(\d+))?$/.exec(normalized);
  if (!match) return null;

  const fraction = match[2] ?? "";
  if (fraction.length > decimalPlaces) return null;
  const scale = 10n ** BigInt(decimalPlaces);
  const whole = BigInt(match[1]);
  const fractional = BigInt(
    (fraction + "0".repeat(decimalPlaces)).slice(0, decimalPlaces) || "0",
  );
  return whole * scale + fractional;
}
