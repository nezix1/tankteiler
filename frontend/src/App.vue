<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";

import { calculateTrip, type TripCalculationResult } from "./api/trips";
import { useLocaleStore } from "./stores/locale";
import { parseDecimalToScaledInteger } from "./utils/decimal";
import {
  formatCurrency as formatMoneyExact,
  formatDecimal,
} from "./utils/format";

const { t } = useI18n();
const localeStore = useLocaleStore();

const form = reactive({
  origin: "",
  destination: "",
  distanceKm: "",
  consumption: "",
  fuelType: "bleifrei_95",
  fuelPrice: "",
  extraCosts: "0",
  passengerCount: 2,
});

const result = ref<TripCalculationResult | null>(null);
const errorMessage = ref("");
const loading = ref(false);

const googleMapsUrl = computed(() => {
  if (!form.origin.trim() || !form.destination.trim()) return "";
  const params = new URLSearchParams({
    api: "1",
    origin: form.origin.trim(),
    destination: form.destination.trim(),
    travelmode: "driving",
  });
  return `https://www.google.com/maps/dir/?${params.toString()}`;
});

const appleMapsUrl = computed(() => {
  if (!form.origin.trim() || !form.destination.trim()) return "";
  const params = new URLSearchParams({
    saddr: form.origin.trim(),
    daddr: form.destination.trim(),
    dirflg: "d",
  });
  return `https://maps.apple.com/?${params.toString()}`;
});

function formatCurrency(amount: string): string {
  return formatMoneyExact(amount, localeStore.locale);
}

function formatLiters(amount: string): string {
  return formatDecimal(amount, localeStore.locale);
}

async function submitCalculation() {
  errorMessage.value = "";
  result.value = null;

  const distance = parseDecimalToScaledInteger(form.distanceKm, 2);
  const consumption = parseDecimalToScaledInteger(form.consumption, 2);
  const price = parseDecimalToScaledInteger(form.fuelPrice, 3);
  const extraCosts = parseDecimalToScaledInteger(form.extraCosts || "0", 2);
  if (
    distance === null ||
    consumption === null ||
    price === null ||
    extraCosts === null
  ) {
    errorMessage.value = t("form.validation.required");
    return;
  }
  if (distance <= 0n || consumption <= 0n || extraCosts < 0n) {
    errorMessage.value = t("form.validation.required");
    return;
  }
  if (
    !Number.isInteger(form.passengerCount) ||
    form.passengerCount < 1 ||
    form.passengerCount > 8
  ) {
    errorMessage.value = t("form.validation.passengers");
    return;
  }
  if (price < 1000n || price > 3500n) {
    errorMessage.value = t("form.validation.price");
    return;
  }

  loading.value = true;
  try {
    result.value = await calculateTrip({
      distance_km: form.distanceKm,
      consumption_l_per_100_km: form.consumption,
      fuel_price_chf_per_l: form.fuelPrice,
      extra_costs_chf: form.extraCosts || "0",
      passenger_count: form.passengerCount,
    });
  } catch {
    errorMessage.value = t("form.validation.api");
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main class="page-shell">
    <header class="topbar">
      <a class="brand" href="/" :aria-label="t('app.name')">
        <span class="brand-mark" aria-hidden="true">T</span>
        <span>{{ t("app.name") }}</span>
      </a>
      <label class="language-control">
        <span>{{ t("language.label") }}</span>
        <select
          :value="localeStore.locale"
          :aria-label="t('language.label')"
          @change="
            localeStore.setLocale(
              ($event.target as HTMLSelectElement).value as 'de' | 'en' | 'ru',
            )
          "
        >
          <option value="de">{{ t("language.de") }}</option>
          <option value="en">{{ t("language.en") }}</option>
          <option value="ru">{{ t("language.ru") }}</option>
        </select>
      </label>
    </header>

    <section class="hero">
      <p class="eyebrow">{{ t("app.guest") }}</p>
      <h1>{{ t("app.tagline") }}</h1>
    </section>

    <div class="content-grid">
      <section class="card form-card" :aria-labelledby="'trip-form-title'">
        <div class="section-heading">
          <div>
            <h2 id="trip-form-title">{{ t("form.title") }}</h2>
            <p>{{ t("form.description") }}</p>
          </div>
          <span class="step-badge" aria-hidden="true">01</span>
        </div>

        <form class="trip-form" @submit.prevent="submitCalculation">
          <div class="field-grid route-fields">
            <label class="field">
              <span>{{ t("form.origin") }}</span>
              <input
                v-model="form.origin"
                autocomplete="street-address"
                :placeholder="t('form.originPlaceholder')"
              />
            </label>
            <label class="field">
              <span>{{ t("form.destination") }}</span>
              <input
                v-model="form.destination"
                autocomplete="street-address"
                :placeholder="t('form.destinationPlaceholder')"
              />
            </label>
          </div>

          <div class="field-grid">
            <label class="field">
              <span>{{ t("form.distance") }}</span>
              <span class="input-with-unit">
                <input
                  v-model="form.distanceKm"
                  type="text"
                  inputmode="decimal"
                  required
                />
                <span>{{ t("form.distanceUnit") }}</span>
              </span>
            </label>
            <label class="field">
              <span>{{ t("form.consumption") }}</span>
              <span class="input-with-unit">
                <input
                  v-model="form.consumption"
                  type="text"
                  inputmode="decimal"
                  required
                />
                <span>{{ t("form.consumptionUnit") }}</span>
              </span>
            </label>
          </div>

          <div class="field-grid">
            <label class="field">
              <span>{{ t("form.fuelType") }}</span>
              <select v-model="form.fuelType">
                <option value="bleifrei_95">
                  {{ t("form.fuelTypes.bleifrei_95") }}
                </option>
                <option value="bleifrei_98">
                  {{ t("form.fuelTypes.bleifrei_98") }}
                </option>
                <option value="diesel">{{ t("form.fuelTypes.diesel") }}</option>
              </select>
            </label>
            <label class="field">
              <span>{{ t("form.fuelPrice") }}</span>
              <span class="input-with-unit">
                <input
                  v-model="form.fuelPrice"
                  type="text"
                  inputmode="decimal"
                  required
                />
                <span>{{ t("form.priceUnit") }}</span>
              </span>
            </label>
          </div>
          <p class="field-hint">{{ t("form.priceNote") }}</p>

          <div class="field-grid">
            <label class="field">
              <span>{{ t("form.extraCosts") }}</span>
              <span class="input-with-unit">
                <input
                  v-model="form.extraCosts"
                  type="text"
                  inputmode="decimal"
                />
                <span>{{ t("form.extraCostsUnit") }}</span>
              </span>
              <span class="field-hint">{{ t("form.extraCostsHint") }}</span>
            </label>
            <label class="field">
              <span>{{ t("form.passengers") }}</span>
              <select v-model.number="form.passengerCount">
                <option v-for="count in 8" :key="count" :value="count">
                  {{ count }}
                </option>
              </select>
            </label>
          </div>

          <p v-if="errorMessage" class="error-message" role="alert">
            {{ errorMessage }}
          </p>
          <button class="primary-button" type="submit" :disabled="loading">
            <span>{{
              loading ? t("form.calculating") : t("form.calculate")
            }}</span>
            <span aria-hidden="true">↗</span>
          </button>
        </form>
      </section>

      <section class="card result-card" aria-live="polite">
        <div class="section-heading">
          <div>
            <p class="eyebrow">{{ t("result.title") }}</p>
            <h2>{{ result ? formatCurrency(result.total_cost_chf) : "—" }}</h2>
          </div>
          <span class="result-icon" aria-hidden="true">↗</span>
        </div>

        <template v-if="result">
          <dl class="result-list">
            <div class="result-row">
              <dt>{{ t("result.fuelUsed") }}</dt>
              <dd>{{ formatLiters(result.liters) }} L</dd>
            </div>
            <div class="result-row">
              <dt>{{ t("result.fuelCost") }}</dt>
              <dd>{{ formatCurrency(result.fuel_cost_chf) }}</dd>
            </div>
            <div class="result-row">
              <dt>{{ t("result.extraCosts") }}</dt>
              <dd>{{ formatCurrency(result.extra_costs_chf) }}</dd>
            </div>
            <div class="result-row total-row">
              <dt>{{ t("result.total") }}</dt>
              <dd>{{ formatCurrency(result.total_cost_chf) }}</dd>
            </div>
          </dl>

          <div class="share-panel">
            <p>{{ t("result.eachPays") }}</p>
            <strong>{{ formatCurrency(result.passenger_share_chf) }}</strong>
            <span>{{ t("result.roundingNote") }}</span>
          </div>
          <dl class="result-list compact-list">
            <div class="result-row">
              <dt>{{ t("result.collected") }}</dt>
              <dd>{{ formatCurrency(result.collected_total_chf) }}</dd>
            </div>
            <div class="result-row">
              <dt>{{ t("result.surplus") }}</dt>
              <dd>{{ formatCurrency(result.rounding_surplus_chf) }}</dd>
            </div>
          </dl>
        </template>

        <div class="map-links">
          <h3>{{ t("result.maps") }}</h3>
          <p v-if="!googleMapsUrl">{{ t("result.routeMissing") }}</p>
          <div v-else class="map-buttons">
            <a :href="googleMapsUrl" target="_blank" rel="noreferrer">
              {{ t("result.googleMaps") }} <span aria-hidden="true">↗</span>
            </a>
            <a :href="appleMapsUrl" target="_blank" rel="noreferrer">
              {{ t("result.appleMaps") }} <span aria-hidden="true">↗</span>
            </a>
          </div>
        </div>
      </section>
    </div>

    <footer class="page-footer">
      <span class="footer-dot" aria-hidden="true"></span>
      <p>{{ t("footer.manualDistance") }}</p>
    </footer>
  </main>
</template>
