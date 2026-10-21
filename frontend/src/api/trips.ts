export interface TripCalculationRequest {
  distance_km: string;
  consumption_l_per_100_km: string;
  fuel_price_chf_per_l: string;
  extra_costs_chf: string;
  passenger_count: number;
}

export interface TripCalculationResult {
  distance_km: string;
  liters: string;
  fuel_cost_chf: string;
  extra_costs_chf: string;
  total_cost_chf: string;
  passenger_count: number;
  passenger_share_chf: string;
  collected_total_chf: string;
  rounding_surplus_chf: string;
}

export async function calculateTrip(
  request: TripCalculationRequest,
): Promise<TripCalculationResult> {
  const response = await fetch("/api/v1/trips/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Trip calculation failed with status ${response.status}.`);
  }

  return (await response.json()) as TripCalculationResult;
}
