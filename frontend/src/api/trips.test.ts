import { afterEach, describe, expect, it, vi } from "vitest";

import { calculateTrip } from "./trips";

describe("calculateTrip", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts exact numeric strings to the guest calculation endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ total_cost_chf: "17.40" }),
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = {
      distance_km: "100.50",
      consumption_l_per_100_km: "6.20",
      fuel_price_chf_per_l: "1.789",
      extra_costs_chf: "2.50",
      passenger_count: 3,
    };

    await expect(calculateTrip(request)).resolves.toEqual({
      total_cost_chf: "17.40",
    });
    expect(fetchMock).toHaveBeenCalledWith("/api/v1/trips/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
  });

  it("surfaces unsuccessful API status to the caller", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: false, status: 422 }),
    );

    await expect(
      calculateTrip({
        distance_km: "100",
        consumption_l_per_100_km: "6",
        fuel_price_chf_per_l: "1.8",
        extra_costs_chf: "0",
        passenger_count: 2,
      }),
    ).rejects.toThrow("Trip calculation failed with status 422.");
  });
});
