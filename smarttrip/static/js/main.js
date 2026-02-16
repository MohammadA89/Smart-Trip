/* global L */

(() => {
  const $ = (selector) => document.querySelector(selector);

  const I18N = {
    en: {
      // Template/static UI (index.html data-i18n)
      app_title: "SmartTrip — Intelligent Hangout Recommendations",
      nav_engine: "Engine",
      nav_map: "Map",
      nav_results: "Results",
      hero_eyebrow: "Smart scoring • Real-world nearby places • Explanation-first",
      hero_title: "Find the best place to hang out — instantly, intelligently.",
      hero_sub:
        "Answer 5 quick questions. SmartTrip scores nearby options on distance, budget fit, group context, and activity match — then shows you the reason behind every recommendation.",
      kpi_personal: "Personal",
      kpi_personal_label: "Personalization",
      kpi_explain: "Explainable",
      kpi_explain_label: "Decision-making",
      kpi_fast: "Fast",
      kpi_fast_label: "Student-friendly",
      prefs_title: "Personalize",
      label_car: "Car availability",
      hint_car: "Affects distance tolerance",
      switch_car: "I have a car",
      label_people: "Number of people",
      hint_people: "Used to fit place vibe",
      label_search_area: "Search area",
      hint_search_area: "Nearby radius or whole city",
      mode_radius: "Nearby",
      mode_city: "City",
      label_radius: "Search radius",
      hint_radius: "How far to look for places",
      label_city: "City",
      hint_city: "Search across the whole city",
      label_with: "With",
      hint_with: "Solo / friends / family",
      group_solo: "Solo",
      group_friends: "Friends",
      group_family: "Family",
      label_budget: "Budget",
      hint_budget: "Low / medium / open",
      budget_low: "Low",
      budget_medium: "Medium",
      budget_open: "Open",
      label_activity: "Activity type",
      hint_activity: "Choose the main vibe",
      act_nature: "Nature",
      act_cafe: "Café",
      act_restaurant: "Restaurant",
      act_entertainment: "Entertainment",
      cta_label: "Find the Best Place",
      engine_title: "Decision Engine",
      engine_state: "Explainable",
      engine_desc:
        'A transparent scoring model that adapts to your conditions. You always see <span class="neon">why</span> a place wins.',
      w_distance: "Distance",
      w_activity: "Activity match",
      w_group: "Group context",
      w_budget: "Budget fit",
      chat_title: "Chat",
      chat_placeholder: "Example: “cozy cafe in Tehran with low budget”",
      chat_send: "Send",
      chat_hint: "Tip: mention a city (e.g., “in Tehran”) or a radius (e.g., “5 km”) and we’ll apply it automatically.",
      map_title: "Live Map",
      map_recenter: "Re-center",
      map_clear: "Clear",
      map_meta: "Dark map • Neon markers • Minimal controls",
      results_title: "Top Recommendations",
      results_empty: "Run a search to see results.",
      noscript: "SmartTrip needs JavaScript enabled for the interactive map and smart recommendations.",

      // Dynamic UI strings (main.js)
      status_ready: "Ready",
      status_searching: "Searching",
      chat_status_ready: "Ready",
      chat_status_thinking: "Thinking",
      cta_loading: "Finding the best place…",
      btn_use_location: "Use my location",
      btn_locating: "Locating…",
      btn_location_enabled: "Location enabled",
      unknown_place: "Unknown",
      unit_km: "km",
      hint_location_user: "Using your current location for nearby recommendations.",
      hint_location_city: "Using the selected city center until you allow location access.",
      hint_location_demo: "Using a demo location until you allow location access.",
      map_sub_ready: "Ready to search",
      map_sub_scoring: "Scoring places…",
      map_sub_top: "Top matches highlighted",
      map_sub_none: "No results",
      map_sub_backend: "Backend unavailable",
      data_prefix: "Data",
      results_meta_city: "{count} places • city {city}",
      results_meta_radius: "{count} places • radius {radius} km",
      toast_map_failed: "Map failed to load. Check your internet connection.",
      toast_type_city: "Type a city name to search the whole city.",
      toast_top_picks: "Top picks are ready — check the map and explanations.",
      toast_no_places: "No places found. Try a different activity or increase radius.",
      toast_backend_failed: "Failed to fetch recommendations. Is the backend running?",
      toast_geo_unsupported: "Geolocation is not supported in this browser.",
      toast_location_enabled: "Location enabled. Recommendations will be nearby.",
      toast_location_denied: "Location permission denied. Using demo location.",
      toast_chat_failed: "Chat failed. Please try again.",
      fallback_explanation: "Recommended based on your preferences.",
      score_title: "Smart recommendation score",
      card_category_title: "Category",
      card_distance_title: "Distance from you",
      card_show_on_map: "Show on map",
      card_explain_score: "Explain score",
      marker_popup_score: "Score",
      breakdown_activity: "Activity",
      breakdown_distance: "Distance",
      breakdown_group: "Group",
      breakdown_budget: "Budget",
      breakdown_people: "People",
      breakdown_quality: "Quality",
      toast_score: "Score: {score}/100",
      type_nature: "Nature",
      type_cafe: "Café",
      type_restaurant: "Restaurant",
      type_entertainment: "Entertainment",
      chip_car_yes: "Car: available",
      chip_car_no: "No car: prioritize nearby",
      chip_people: "People: {n}",
      chip_city: "City: {city}",
      chip_radius: "Radius: {km} km",
      chip_group: "Group: {group}",
      chip_budget: "Budget: {budget}",
      chip_activity: "Activity: {activity}",
      chat_welcome: "Tell me what you want. Example: “cozy cafe in Tehran with low budget”.",
    },
    fa: {
      app_title: "SmartTrip — پیشنهاد هوشمند مکان‌های تفریحی",
      nav_engine: "موتور",
      nav_map: "نقشه",
      nav_results: "نتایج",
      hero_eyebrow: "امتیازدهی هوشمند • مکان‌های واقعی • توضیح‌محور",
      hero_title: "بهترین جای دورهمی رو سریع و هوشمند پیدا کن.",
      hero_sub:
        "به چند سؤال کوتاه جواب بده. SmartTrip گزینه‌ها رو با توجه به فاصله، بودجه، نوع همراهی و نوع فعالیت امتیازدهی می‌کنه و دلیل هر پیشنهاد رو نشون می‌ده.",
      kpi_personal: "شخصی",
      kpi_personal_label: "شخصی‌سازی",
      kpi_explain: "قابل توضیح",
      kpi_explain_label: "شفافیت تصمیم",
      kpi_fast: "سریع",
      kpi_fast_label: "مناسب دانشجو",
      prefs_title: "شخصی‌سازی",
      label_car: "ماشین",
      hint_car: "روی تحمل فاصله اثر دارد",
      switch_car: "ماشین دارم",
      label_people: "تعداد نفرات",
      hint_people: "برای تناسب حال‌وهوای مکان",
      label_search_area: "محدوده جستجو",
      hint_search_area: "اطراف یا کل شهر",
      mode_radius: "اطراف",
      mode_city: "شهر",
      label_radius: "شعاع جستجو",
      hint_radius: "چقدر دورتر بگردیم",
      label_city: "شهر",
      hint_city: "جستجو در کل شهر",
      label_with: "همراهی",
      hint_with: "تنها / دوستان / خانواده",
      group_solo: "تنها",
      group_friends: "دوستان",
      group_family: "خانواده",
      label_budget: "بودجه",
      hint_budget: "کم / متوسط / باز",
      budget_low: "کم",
      budget_medium: "متوسط",
      budget_open: "باز",
      label_activity: "نوع فعالیت",
      hint_activity: "حس کلی رو انتخاب کن",
      act_nature: "طبیعت",
      act_cafe: "کافه",
      act_restaurant: "رستوران",
      act_entertainment: "سرگرمی",
      cta_label: "بهترین مکان رو پیدا کن",
      engine_title: "موتور تصمیم",
      engine_state: "قابل توضیح",
      engine_desc:
        'یک مدل امتیازدهی شفاف که با شرایط شما تطبیق می‌دهد. همیشه می‌بینید <span class="neon">چرا</span> یک مکان برنده شده است.',
      w_distance: "فاصله",
      w_activity: "تطابق فعالیت",
      w_group: "تناسب همراهی",
      w_budget: "تناسب بودجه",
      chat_title: "چت",
      chat_placeholder: "مثال: «کافه دنج توی تهران با بودجه کم»",
      chat_send: "ارسال",
      chat_hint: "نکته: شهر («توی تهران») یا شعاع («۵ کیلومتر») رو بگو تا خودکار اعمال کنیم.",
      map_title: "نقشه زنده",
      map_recenter: "مرکز",
      map_clear: "پاک کردن",
      map_meta: "نقشه تیره • مارکرهای نئونی • کنترل‌های کم",
      results_title: "بهترین پیشنهادها",
      results_empty: "برای دیدن نتایج جستجو کن.",
      noscript: "برای نقشه و پیشنهادهای هوشمند، JavaScript باید فعال باشد.",

      status_ready: "آماده",
      status_searching: "در حال جستجو",
      chat_status_ready: "آماده",
      chat_status_thinking: "در حال فکر کردن",
      cta_loading: "در حال پیدا کردن بهترین مکان…",
      btn_use_location: "استفاده از موقعیت من",
      btn_locating: "در حال پیدا کردن…",
      btn_location_enabled: "موقعیت فعال شد",
      unknown_place: "نامشخص",
      unit_km: "کیلومتر",
      hint_location_user: "برای پیشنهادهای اطراف، از موقعیت فعلی شما استفاده می‌کنیم.",
      hint_location_city: "تا وقتی موقعیت رو فعال نکنی، از مرکز شهر انتخاب‌شده استفاده می‌کنیم.",
      hint_location_demo: "تا وقتی موقعیت رو فعال نکنی، از یک موقعیت نمونه استفاده می‌کنیم.",
      map_sub_ready: "آماده برای جستجو",
      map_sub_scoring: "در حال امتیازدهی…",
      map_sub_top: "بهترین‌ها مشخص شدند",
      map_sub_none: "نتیجه‌ای پیدا نشد",
      map_sub_backend: "بک‌اند در دسترس نیست",
      data_prefix: "داده",
      results_meta_city: "{count} مکان • شهر {city}",
      results_meta_radius: "{count} مکان • شعاع {radius} کیلومتر",
      toast_map_failed: "نقشه لود نشد. اینترنت رو چک کن.",
      toast_type_city: "برای جستجو در کل شهر، نام شهر رو وارد کن.",
      toast_top_picks: "بهترین پیشنهادها آماده‌ست — نقشه و توضیح امتیاز رو ببین.",
      toast_no_places: "مکانی پیدا نشد. نوع فعالیت رو عوض کن یا شعاع رو بیشتر کن.",
      toast_backend_failed: "دریافت پیشنهادها ناموفق بود. بک‌اند اجراست؟",
      toast_geo_unsupported: "این مرورگر از موقعیت مکانی پشتیبانی نمی‌کند.",
      toast_location_enabled: "موقعیت فعال شد. پیشنهادها نزدیک شما خواهد بود.",
      toast_location_denied: "اجازه موقعیت داده نشد. از موقعیت نمونه استفاده می‌کنیم.",
      toast_chat_failed: "چت ناموفق بود. دوباره امتحان کن.",
      fallback_explanation: "بر اساس ترجیحات شما پیشنهاد شده.",
      score_title: "امتیاز پیشنهاد هوشمند",
      card_category_title: "دسته‌بندی",
      card_distance_title: "فاصله تا شما",
      card_show_on_map: "نمایش روی نقشه",
      card_explain_score: "توضیح امتیاز",
      marker_popup_score: "امتیاز",
      breakdown_activity: "فعالیت",
      breakdown_distance: "فاصله",
      breakdown_group: "همراهی",
      breakdown_budget: "بودجه",
      breakdown_people: "نفرات",
      breakdown_quality: "کیفیت",
      toast_score: "امتیاز: {score}/100",
      type_nature: "طبیعت",
      type_cafe: "کافه",
      type_restaurant: "رستوران",
      type_entertainment: "سرگرمی",
      chip_car_yes: "ماشین: دارم",
      chip_car_no: "ماشین: ندارم (نزدیک‌ترها مهم‌ترند)",
      chip_people: "نفرات: {n}",
      chip_city: "شهر: {city}",
      chip_radius: "شعاع: {km} کیلومتر",
      chip_group: "همراهی: {group}",
      chip_budget: "بودجه: {budget}",
      chip_activity: "فعالیت: {activity}",
      chat_welcome: "بگو دنبال چی هستی. مثال: «کافه دنج توی تهران با بودجه کم».",
    },
  };

  const CATEGORY_TREE = [
    {
      id: "food_drink",
      label: { en: "Food & Drink", fa: "غذا و نوشیدنی" },
      items: [
        { id: "restaurant", label: { en: "Restaurant", fa: "رستوران" } },
        { id: "fast_food", label: { en: "Fast Food", fa: "فست فود" } },
        { id: "cafe", label: { en: "Cafe", fa: "کافه" } },
        { id: "juice", label: { en: "Juice", fa: "آبمیوه" } },
        { id: "ice_cream", label: { en: "Ice Cream", fa: "بستنی" } },
      ],
    },
    {
      id: "fun",
      label: { en: "Fun & Entertainment", fa: "تفریح و سرگرمی" },
      items: [
        { id: "park", label: { en: "Park", fa: "پارک" } },
        { id: "attraction", label: { en: "Attraction", fa: "مکان دیدنی" } },
        { id: "nature_tourism", label: { en: "Nature Tourism", fa: "طبیعت گردی" } },
        { id: "historical", label: { en: "Historical", fa: "مکان تاریخی" } },
        { id: "cinema", label: { en: "Cinema", fa: "سینما" } },
        { id: "amusement_park", label: { en: "Amusement Park", fa: "شهربازی" } },
        { id: "theatre", label: { en: "Theatre", fa: "تئاتر" } },
        { id: "museum", label: { en: "Museum", fa: "موزه" } },
        { id: "pool", label: { en: "Pool", fa: "استخر" } },
      ],
    },
    {
      id: "travel",
      label: { en: "Travel", fa: "سفر" },
      items: [
        { id: "hotel", label: { en: "Hotel", fa: "هتل" } },
        { id: "eco_lodge", label: { en: "Eco Lodge", fa: "اقامتگاه بومگردی" } },
        { id: "hostel", label: { en: "Hostel", fa: "اقامتگاه" } },
      ],
    },
    {
      id: "shopping",
      label: { en: "Market & Mall", fa: "بازار و مرکز خرید" },
      items: [
        { id: "market", label: { en: "Market", fa: "بازار" } },
        { id: "shopping_mall", label: { en: "Shopping Mall", fa: "مرکز خرید" } },
      ],
    },
  ];

  const DEFAULT_SUBCATEGORIES = ["restaurant", "fast_food", "cafe"];

  const SUBCATEGORY_TO_PRIMARY_ACTIVITY = {
    restaurant: "restaurant",
    fast_food: "restaurant",
    cafe: "cafe",
    juice: "cafe",
    ice_cream: "cafe",
    park: "nature",
    attraction: "nature",
    nature_tourism: "nature",
    historical: "nature",
    cinema: "entertainment",
    amusement_park: "entertainment",
    theatre: "entertainment",
    museum: "entertainment",
    pool: "entertainment",
    hotel: "entertainment",
    eco_lodge: "nature",
    hostel: "entertainment",
    market: "entertainment",
    shopping_mall: "entertainment",
  };

  function normalizeLang(value) {
    const s = String(value || "").trim().toLowerCase();
    if (s.startsWith("fa")) return "fa";
    if (s === "farsi" || s === "persian") return "fa";
    return "en";
  }

  function fmt(template, params) {
    const src = String(template || "");
    const p = params && typeof params === "object" ? params : {};
    return src.replace(/\{(\w+)\}/g, (_, key) => (key in p ? String(p[key]) : ""));
  }

  function t(key) {
    const lang = state && state.lang ? state.lang : "en";
    return (I18N[lang] && I18N[lang][key]) || I18N.en[key] || String(key);
  }

  function tr(key, params) {
    return fmt(t(key), params);
  }

  function categoryText(label) {
    if (!label || typeof label !== "object") return "";
    return state.lang === "fa" ? label.fa || label.en || "" : label.en || label.fa || "";
  }

  function allSubcategoryIds() {
    return CATEGORY_TREE.flatMap((cat) => cat.items.map((item) => item.id));
  }

  function normalizeSubcategories(list) {
    const valid = new Set(allSubcategoryIds());
    const out = [];
    for (const item of Array.isArray(list) ? list : []) {
      const id = String(item || "").trim().toLowerCase();
      if (!id || !valid.has(id) || out.includes(id)) continue;
      out.push(id);
    }
    return out;
  }

  function primaryFromSubcategory(id) {
    return SUBCATEGORY_TO_PRIMARY_ACTIVITY[String(id || "").trim().toLowerCase()] || "nature";
  }

  const dom = {
    prefsForm: $("#prefsForm"),
    ctaBtn: $("#ctaBtn"),
    prefsStatus: $("#prefsStatus"),
    hasCar: $("#hasCar"),
    peopleCount: $("#peopleCount"),
    peopleCountLabel: $("#peopleCountLabel"),
    radiusKm: $("#radiusKm"),
    radiusLabel: $("#radiusLabel"),
    radiusField: $("#radiusField"),
    cityField: $("#cityField"),
    cityInput: $("#cityInput"),
    placeCategories: $("#placeCategories"),
    locationHint: $("#locationHint"),
    useLocationBtn: $("#useLocationBtn"),
    recenterBtn: $("#recenterBtn"),
    clearBtn: $("#clearBtn"),
    mapSub: $("#mapSub"),
    mapMeta: $("#mapMeta"),
    dataSourceMeta: $("#dataSourceMeta"),
    resultsMeta: $("#resultsMeta"),
    cards: $("#cards"),
    toast: $("#toast"),
    wDistance: $("#wDistance"),
    wActivity: $("#wActivity"),
    wGroup: $("#wGroup"),
    wBudget: $("#wBudget"),
    bDistance: $("#bDistance"),
    bActivity: $("#bActivity"),
    bGroup: $("#bGroup"),
    bBudget: $("#bBudget"),
    personalChips: $("#personalChips"),
    chatForm: $("#chatForm"),
    chatLog: $("#chatLog"),
    chatInput: $("#chatInput"),
    chatStatus: $("#chatStatus"),
  };

  const DEFAULT_ORIGIN = { lat: 35.6892, lon: 51.3890, source: "demo" };

  const state = {
    origin: { ...DEFAULT_ORIGIN },
    lastResults: [],
    lastRequestId: null,
    lastResponse: null,
    sessionId: null,
    lang: "en",
    isLoading: false,
    chatState: "ready", // "ready" | "thinking"
    locationState: "idle", // "idle" | "locating" | "enabled"
    markers: [],
    userMarker: null,
    activeCategory: CATEGORY_TREE[0].id,
    selectedSubcategories: normalizeSubcategories(DEFAULT_SUBCATEGORIES),
  };

  let map = null;
  let markerLayer = null;

  function setSelectedSubcategories(list) {
    const next = normalizeSubcategories(list);
    state.selectedSubcategories = next;
    syncCategoryCheckboxes();
  }

  function syncCategoryCheckboxes() {
    if (!dom.placeCategories) return;
    CATEGORY_TREE.forEach((category) => {
      const selected = new Set(state.selectedSubcategories);
      const itemIds = category.items.map((item) => item.id);
      const allChecked = itemIds.every((id) => selected.has(id));

      const allEl = dom.placeCategories.querySelector(
        `input.subcategory-all[data-category="${category.id}"]`
      );
      if (allEl instanceof HTMLInputElement) allEl.checked = allChecked;

      category.items.forEach((item) => {
        const el = dom.placeCategories.querySelector(
          `input.subcategory-checkbox[data-category="${category.id}"][value="${item.id}"]`
        );
        if (el instanceof HTMLInputElement) el.checked = selected.has(item.id);
      });
    });
  }

  function setActiveCategory(categoryId) {
    state.activeCategory = categoryId;
    if (!dom.placeCategories) return;
    dom.placeCategories.querySelectorAll(".category-tab").forEach((btn) => {
      if (!(btn instanceof HTMLButtonElement)) return;
      const isActive = btn.dataset.category === categoryId;
      btn.classList.toggle("is-active", isActive);
      btn.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
    dom.placeCategories.querySelectorAll(".category-panel").forEach((panel) => {
      if (!(panel instanceof HTMLElement)) return;
      panel.hidden = panel.dataset.category !== categoryId;
    });
  }

  function renderCategoryPicker() {
    if (!dom.placeCategories) return;
    const selected = new Set(state.selectedSubcategories);
    const selectAllText = state.lang === "fa" ? "انتخاب همه" : "Select all";

    const tabsHtml = CATEGORY_TREE.map((category) => {
      const isActive = category.id === state.activeCategory;
      return `<button class="category-tab${isActive ? " is-active" : ""}" type="button" data-category="${
        category.id
      }" aria-pressed="${isActive ? "true" : "false"}">${escapeHtml(
        categoryText(category.label)
      )}</button>`;
    }).join("");

    const panelsHtml = CATEGORY_TREE.map((category) => {
      const ids = category.items.map((item) => item.id);
      const allChecked = ids.every((id) => selected.has(id));
      const optionsHtml = category.items
        .map(
          (item) => `
          <label class="subcategory">
            <input class="subcategory-checkbox" type="checkbox" data-category="${category.id}" value="${
              item.id
            }" ${selected.has(item.id) ? "checked" : ""}/>
            <span>${escapeHtml(categoryText(item.label))}</span>
          </label>`
        )
        .join("");
      return `
        <div class="category-panel" data-category="${category.id}" ${category.id === state.activeCategory ? "" : "hidden"}>
          <div class="subcategory-list">
            <label class="subcategory is-all">
              <input class="subcategory-all" type="checkbox" data-category="${category.id}" ${
                allChecked ? "checked" : ""
              }/>
              <span>${escapeHtml(selectAllText)}</span>
            </label>
            ${optionsHtml}
          </div>
        </div>
      `;
    }).join("");

    dom.placeCategories.innerHTML = `<div class="category-tabs">${tabsHtml}</div><div class="category-panels">${panelsHtml}</div>`;

    dom.placeCategories.querySelectorAll(".category-tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (!(btn instanceof HTMLButtonElement)) return;
        const categoryId = btn.dataset.category || CATEGORY_TREE[0].id;
        setActiveCategory(categoryId);
        const category = CATEGORY_TREE.find((c) => c.id === categoryId);
        if (!category) return;
        const ids = category.items.map((item) => item.id);
        // Category switch is exclusive: keep only this category's subcategories.
        setSelectedSubcategories(ids);
        updateEngine(getPrefs());
      });
    });

    dom.placeCategories.querySelectorAll(".subcategory-all").forEach((el) => {
      el.addEventListener("change", () => {
        if (!(el instanceof HTMLInputElement)) return;
        const categoryId = String(el.dataset.category || "");
        const category = CATEGORY_TREE.find((c) => c.id === categoryId);
        if (!category) return;
        const ids = category.items.map((item) => item.id);
        if (el.checked) {
          // "Select all" is exclusive to this category.
          setSelectedSubcategories(ids);
        } else {
          setSelectedSubcategories([]);
        }
        updateEngine(getPrefs());
      });
    });

    dom.placeCategories.querySelectorAll(".subcategory-checkbox").forEach((el) => {
      el.addEventListener("change", () => {
        if (!(el instanceof HTMLInputElement)) return;
        const categoryId = String(el.dataset.category || "");
        const category = CATEGORY_TREE.find((c) => c.id === categoryId);
        if (!category) return;
        const id = String(el.value || "").trim().toLowerCase();
        // Keep edits scoped to active category only.
        const next = new Set(
          category.items
            .map((item) => item.id)
            .filter((itemId) => state.selectedSubcategories.includes(itemId))
        );
        if (el.checked) next.add(id);
        else next.delete(id);
        setSelectedSubcategories([...next]);
        updateEngine(getPrefs());
      });
    });

    syncCategoryCheckboxes();
  }

  function showToast(message) {
    if (!dom.toast) return;
    dom.toast.textContent = message;
    dom.toast.classList.add("toast--show");
    window.clearTimeout(showToast._t);
    showToast._t = window.setTimeout(() => dom.toast.classList.remove("toast--show"), 2800);
  }

  function getSessionId() {
    const key = "smarttrip_session_id";
    try {
      const existing = window.localStorage.getItem(key);
      if (existing) return existing;
      const id =
        (window.crypto && typeof window.crypto.randomUUID === "function"
          ? window.crypto.randomUUID()
          : `sid_${Date.now()}_${Math.random().toString(16).slice(2)}`);
      window.localStorage.setItem(key, id);
      return id;
    } catch {
      return `sid_${Date.now()}_${Math.random().toString(16).slice(2)}`;
    }
  }

  function detectInitialLang() {
    const key = "smarttrip_lang";
    try {
      const saved = window.localStorage.getItem(key);
      if (saved) return normalizeLang(saved);
    } catch {
      // ignore
    }

    const nav = (navigator.language || navigator.userLanguage || "").toLowerCase();
    if (nav.startsWith("fa")) return "fa";
    return "en";
  }

  function applyTranslations() {
    document.documentElement.lang = state.lang;
    document.documentElement.dir = state.lang === "fa" ? "rtl" : "ltr";

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (!key) return;
      el.textContent = t(key);
    });

    document.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      if (!key) return;
      el.innerHTML = t(key);
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      const key = el.getAttribute("data-i18n-placeholder");
      if (!key) return;
      if (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement) {
        el.setAttribute("placeholder", t(key));
      }
    });

    // Dynamic / state-driven labels
    renderCategoryPicker();
    updateLocationButton();
    setChatStatus(state.chatState === "thinking" ? t("chat_status_thinking") : t("chat_status_ready"));
    setLoading(state.isLoading);
    setOriginHint(state.origin.source);
    updateEngine(getPrefs());

    if (!state.lastResponse) {
      if (dom.resultsMeta) dom.resultsMeta.textContent = t("results_empty");
      if (dom.dataSourceMeta) dom.dataSourceMeta.textContent = `${t("data_prefix")}: —`;
      if (dom.mapSub) dom.mapSub.textContent = t("map_sub_ready");
    } else {
      updateResponseMeta();
    }

    // Keep language radios in sync.
    document.querySelectorAll('input[name="lang"]').forEach((el) => {
      if (!(el instanceof HTMLInputElement)) return;
      el.checked = el.value === state.lang;
    });
  }

  function setLang(lang) {
    state.lang = normalizeLang(lang);
    try {
      window.localStorage.setItem("smarttrip_lang", state.lang);
    } catch {
      // ignore
    }
    applyTranslations();
  }

  function setChatStatus(text) {
    if (!dom.chatStatus) return;
    dom.chatStatus.textContent = text;
  }

  function appendChat(role, text) {
    if (!dom.chatLog) return;
    const item = document.createElement("div");
    item.className = `chat__msg chat__msg--${role}`;
    item.textContent = String(text || "");
    dom.chatLog.appendChild(item);
    dom.chatLog.scrollTop = dom.chatLog.scrollHeight;
  }

  function setRadio(name, value) {
    const v = String(value || "");
    const el = document.querySelector(`input[name="${name}"][value="${v}"]`);
    if (el instanceof HTMLInputElement) el.checked = true;
  }

  function applyUpdates(updates) {
    if (!updates || typeof updates !== "object") return;

    if (typeof updates.has_car === "boolean" && dom.hasCar) dom.hasCar.checked = updates.has_car;
    if (typeof updates.people_count === "number" && dom.peopleCount) {
      const pc = clamp(Number(updates.people_count || 2), 1, 10);
      dom.peopleCount.value = String(Math.round(pc));
      updatePeopleLabel();
    }

    if (typeof updates.search_mode === "string") setRadio("search_mode", updates.search_mode);

    if (typeof updates.city === "string" && dom.cityInput) dom.cityInput.value = updates.city;

    if (typeof updates.radius_m === "number" && dom.radiusKm) {
      const km = clamp(Number(updates.radius_m) / 1000, 1, 15);
      const display = Math.round(km * 2) / 2;
      dom.radiusKm.value = String(display);
      updateRadiusLabel();
    }

    if (Array.isArray(updates.activities)) {
      setSelectedSubcategories(updates.activities);
    } else if (typeof updates.activity === "string") {
      const v = String(updates.activity || "").trim().toLowerCase();
      if (v === "cafe") setSelectedSubcategories(["cafe"]);
      else if (v === "restaurant") setSelectedSubcategories(["restaurant"]);
      else if (v === "entertainment") setSelectedSubcategories(["cinema"]);
      else setSelectedSubcategories(["park"]);
    }
    if (typeof updates.group_type === "string") setRadio("group_type", updates.group_type);
    if (typeof updates.budget === "string") setRadio("budget", updates.budget);

    const prefs = getPrefs();
    updateSearchUi(prefs);
    updateEngine(prefs);
  }

  async function sendFeedback(action, place) {
    const requestId = state.lastRequestId;
    const placeId = place && (place.place_id || place.placeId || place.id);
    if (!requestId || !placeId) return;

    try {
      await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: state.sessionId,
          request_id: requestId,
          action: String(action || "click"),
          place_id: String(placeId),
        }),
      });
    } catch {
      // ignore
    }
  }

  function getRadioValue(name, fallback) {
    const selected = document.querySelector(`input[name="${name}"]:checked`);
    return (selected && selected.value) || fallback;
  }

  function getPrefs() {
    const radiusKm = Number(dom.radiusKm?.value || 4.5);
    const safeRadiusKm = Number.isFinite(radiusKm) ? radiusKm : 4.5;
    const radiusM = Math.round(clamp(safeRadiusKm, 1, 15) * 1000);
    const searchMode = getRadioValue("search_mode", "radius");
    const cityRaw = dom.cityInput?.value || "";
    const city = String(cityRaw).trim();

    let activities = normalizeSubcategories(state.selectedSubcategories);
    if (!activities.length) {
      const active = CATEGORY_TREE.find((c) => c.id === state.activeCategory) || CATEGORY_TREE[0];
      activities = active ? active.items.map((item) => item.id) : ["park"];
      setSelectedSubcategories(activities);
    }
    const primaryActivity = primaryFromSubcategory(activities[0] || "park");

    return {
      has_car: !!dom.hasCar?.checked,
      people_count: Number(dom.peopleCount?.value || 3),
      radius_m: radiusM,
      search_mode: searchMode,
      city: searchMode === "city" && city ? city : undefined,
      group_type: getRadioValue("group_type", "friends"),
      budget: getRadioValue("budget", "medium"),
      activities,
      activity: primaryActivity,
    };
  }

  function labelGroup(value) {
    const v = String(value || "").toLowerCase();
    if (v === "solo") return t("group_solo");
    if (v === "family") return t("group_family");
    return t("group_friends");
  }

  function labelBudget(value) {
    const v = String(value || "").toLowerCase();
    if (v === "low") return t("budget_low");
    if (v === "open") return t("budget_open");
    return t("budget_medium");
  }

  function labelActivity(value) {
    const v = String(value || "").toLowerCase();
    if (v === "cafe") return t("act_cafe");
    if (v === "restaurant") return t("act_restaurant");
    if (v === "entertainment") return t("act_entertainment");
    if (v === "nature") return t("act_nature");
    for (const category of CATEGORY_TREE) {
      const item = category.items.find((it) => it.id === v);
      if (item) return categoryText(item.label);
    }
    return v || t("act_nature");
  }

  function labelDataSource(value) {
    const v = String(value || "").toLowerCase();
    if (v === "osm") return "OSM";
    if (v === "demo") return state.lang === "fa" ? "نمونه" : "Demo";
    if (v === "osm+demo") return state.lang === "fa" ? "OSM + نمونه" : "OSM + Demo";
    return value ? String(value) : "—";
  }

  function setLoading(isLoading) {
    state.isLoading = !!isLoading;
    if (!dom.ctaBtn) return;
    dom.ctaBtn.disabled = state.isLoading;
    const label = dom.ctaBtn.querySelector(".btn-primary__label");
    if (label) label.textContent = state.isLoading ? t("cta_loading") : t("cta_label");
    if (dom.prefsStatus) dom.prefsStatus.textContent = state.isLoading ? t("status_searching") : t("status_ready");
    if (dom.mapSub && state.isLoading) dom.mapSub.textContent = t("map_sub_scoring");
  }

  function iconSvg(type) {
    const t = String(type || "").toLowerCase();
    const primary = primaryFromSubcategory(t);
    if (primary === "cafe") {
      return `
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M4 8h12v5a6 6 0 0 1-6 6H8a4 4 0 0 1-4-4V8Z" stroke="currentColor" stroke-width="1.5" />
          <path d="M16 9h2a2 2 0 0 1 0 4h-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <path d="M6 4s1 1 1 2-1 2-1 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <path d="M10 4s1 1 1 2-1 2-1 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        </svg>`;
    }
    if (primary === "restaurant") {
      return `
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M7 3v8M10 3v8M7 7h3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <path d="M14 3v7a3 3 0 0 0 3 3v8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        </svg>`;
    }
    if (primary === "entertainment") {
      return `
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M4 7h16v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7Z" stroke="currentColor" stroke-width="1.5" />
          <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="currentColor" stroke-width="1.5" />
          <path d="M9 12l6 3-6 3v-6Z" fill="currentColor" />
        </svg>`;
    }
    return `
      <svg viewBox="0 0 24 24" fill="none">
        <path d="M12 2c3.5 3.4 6 7.2 6 11.2A6 6 0 1 1 6 13.2C6 9.2 8.5 5.4 12 2Z" stroke="currentColor" stroke-width="1.5" />
        <path d="M12 9v13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
      </svg>`;
  }

  function updatePeopleLabel() {
    if (!dom.peopleCount || !dom.peopleCountLabel) return;
    dom.peopleCountLabel.textContent = String(dom.peopleCount.value);
  }

  function updateRadiusLabel() {
    if (!dom.radiusKm || !dom.radiusLabel) return;
    const km = Number(dom.radiusKm.value || 4.5);
    const safeKm = Number.isFinite(km) ? km : 4.5;
    const display = Math.round(safeKm * 10) / 10;
    dom.radiusLabel.textContent = `${display} km`;
  }

  function updateSearchUi(prefs) {
    const mode = (prefs && prefs.search_mode) || "radius";
    const isCity = mode === "city";

    if (dom.cityField) dom.cityField.hidden = !isCity;
    if (dom.radiusField) dom.radiusField.hidden = isCity;
    if (dom.radiusKm) dom.radiusKm.disabled = isCity;
  }

  function setChips(prefs) {
    if (!dom.personalChips) return;
    const chips = [];
    chips.push(prefs.has_car ? t("chip_car_yes") : t("chip_car_no"));
    chips.push(tr("chip_people", { n: prefs.people_count }));
    if (prefs.search_mode === "city" && prefs.city) {
      chips.push(tr("chip_city", { city: prefs.city }));
    } else if (typeof prefs.radius_m === "number") {
      const km = prefs.radius_m / 1000;
      const display = Math.round(km * 10) / 10;
      chips.push(tr("chip_radius", { km: display }));
    }
    chips.push(tr("chip_group", { group: labelGroup(prefs.group_type) }));
    chips.push(tr("chip_budget", { budget: labelBudget(prefs.budget) }));
    const labels = (prefs.activities || []).map((id) => labelActivity(id));
    const activitySummary =
      labels.length <= 2
        ? labels.join(" / ")
        : `${labels.slice(0, 2).join(" / ")} +${labels.length - 2}`;
    chips.push(tr("chip_activity", { activity: activitySummary || labelActivity(prefs.activity) }));

    dom.personalChips.innerHTML = chips
      .map((text) => `<span class="chiplet">${escapeHtml(text)}</span>`)
      .join("");
  }

  function updateEngine(prefs) {
    // A UI-side weight visualization (not a claim of exact backend weights).
    let distance = prefs.has_car ? 26 : 38;
    let activity = 34;
    let group = prefs.group_type === "family" ? 22 : prefs.group_type === "solo" ? 16 : 20;
    let budget = prefs.budget === "open" ? 10 : 16;

    const sum = distance + activity + group + budget;
    distance = Math.round((distance / sum) * 100);
    activity = Math.round((activity / sum) * 100);
    group = Math.round((group / sum) * 100);
    budget = Math.max(0, 100 - distance - activity - group);

    if (dom.wDistance) dom.wDistance.textContent = `${distance}%`;
    if (dom.wActivity) dom.wActivity.textContent = `${activity}%`;
    if (dom.wGroup) dom.wGroup.textContent = `${group}%`;
    if (dom.wBudget) dom.wBudget.textContent = `${budget}%`;

    if (dom.bDistance) dom.bDistance.style.width = `${distance}%`;
    if (dom.bActivity) dom.bActivity.style.width = `${activity}%`;
    if (dom.bGroup) dom.bGroup.style.width = `${group}%`;
    if (dom.bBudget) dom.bBudget.style.width = `${budget}%`;

    setChips(prefs);
  }

  function initMap() {
    if (!window.L || !$("#map")) {
      showToast(t("toast_map_failed"));
      return;
    }

    map = L.map("map", {
      zoomControl: true,
      preferCanvas: true,
    });

    // Dark-themed basemap (CARTO).
    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      maxZoom: 19,
      subdomains: "abcd",
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
    }).addTo(map);

    markerLayer = L.layerGroup().addTo(map);

    setOrigin(state.origin.lat, state.origin.lon, state.origin.source);
  }

  function markerIcon(isTop) {
    const className = `neon-marker${isTop ? " neon-marker--top" : ""}`;
    return L.divIcon({
      className: "",
      html: `<div class="${className}"></div>`,
      iconSize: [18, 18],
      iconAnchor: [9, 9],
      popupAnchor: [0, -10],
    });
  }

  function userIcon() {
    return L.divIcon({
      className: "",
      html: '<div class="user-marker"></div>',
      iconSize: [16, 16],
      iconAnchor: [8, 8],
      popupAnchor: [0, -10],
    });
  }

  function setOriginHint(source) {
    if (!dom.locationHint) return;
    dom.locationHint.textContent =
      source === "user"
        ? t("hint_location_user")
        : source === "city"
        ? t("hint_location_city")
        : t("hint_location_demo");
  }

  function setOrigin(lat, lon, source) {
    state.origin = { lat, lon, source };
    setOriginHint(source);

    if (!map) return;

    map.setView([lat, lon], source === "user" ? 13 : 12, { animate: true });
    if (state.userMarker) {
      markerLayer.removeLayer(state.userMarker);
    }
    state.userMarker = L.marker([lat, lon], { icon: userIcon(), interactive: false }).addTo(
      markerLayer
    );
  }

  function clearResults() {
    state.lastResults = [];
    state.lastResponse = null;
    state.lastRequestId = null;
    if (dom.cards) dom.cards.innerHTML = "";
    if (dom.resultsMeta) dom.resultsMeta.textContent = t("results_empty");
    if (dom.dataSourceMeta) dom.dataSourceMeta.textContent = `${t("data_prefix")}: —`;
    if (dom.mapSub) dom.mapSub.textContent = t("map_sub_ready");

    if (markerLayer) {
      markerLayer.clearLayers();
      // Re-add user marker
      if (state.origin) {
        state.userMarker = L.marker([state.origin.lat, state.origin.lon], {
          icon: userIcon(),
          interactive: false,
        }).addTo(markerLayer);
      }
    }
  }

  function updateLocationButton() {
    if (!dom.useLocationBtn) return;
    if (state.locationState === "locating") {
      dom.useLocationBtn.textContent = t("btn_locating");
      return;
    }
    if (state.locationState === "enabled") {
      dom.useLocationBtn.textContent = t("btn_location_enabled");
      return;
    }
    dom.useLocationBtn.textContent = t("btn_use_location");
  }

  function updateResponseMeta() {
    const resp = state.lastResponse;
    const recs = state.lastResults || [];
    if (!resp) return;

    if (dom.resultsMeta) {
      if (resp.search_mode === "city" && resp.city) {
        dom.resultsMeta.textContent = tr("results_meta_city", { count: recs.length, city: resp.city });
      } else {
        const radiusKm = resp.radius_m ? (Number(resp.radius_m) / 1000).toFixed(1) : "—";
        dom.resultsMeta.textContent = tr("results_meta_radius", { count: recs.length, radius: radiusKm });
      }
    }

    if (dom.dataSourceMeta) {
      dom.dataSourceMeta.textContent = `${t("data_prefix")}: ${labelDataSource(resp.data_source)}`;
    }

    if (dom.mapSub) dom.mapSub.textContent = recs.length ? t("map_sub_top") : t("map_sub_none");
  }

  function renderCards(recs) {
    if (!dom.cards) return;
    dom.cards.innerHTML = "";

    recs.forEach((place, index) => {
      const type = place.type || "nature";
      const score = Number(place.score || 0);
      const distance = typeof place.distance_km === "number" ? place.distance_km : null;
      const rank = Number(place.rank || index + 1);
      const explanation = place.explanation || t("fallback_explanation");

      const card = document.createElement("article");
      card.className = `card${rank === 1 ? " card--top" : ""}`;
      card.tabIndex = 0;
      card.setAttribute("data-rank", String(rank));

      card.innerHTML = `
        <div class="card__top">
          <div class="card__title">
            <div class="card__icon" aria-hidden="true">${iconSvg(type)}</div>
          <div class="card__name" title="${escapeHtml(place.name || t("unknown_place"))}">${escapeHtml(
        place.name || t("unknown_place")
      )}</div>
          </div>
          <div class="score" title="${escapeHtml(t("score_title"))}">
            <span class="score__dot" aria-hidden="true"></span>
            <span class="mono">${score}</span>
          </div>
        </div>

        <div class="card__meta">
          <span class="meta-item" title="${escapeHtml(t("card_category_title"))}">
            ${tinyIcon("tag")}
            ${escapeHtml(typeLabel(type))}
          </span>
          <span class="meta-item" title="${escapeHtml(t("card_distance_title"))}">
            ${tinyIcon("pin")}
            ${distance !== null ? `${distance.toFixed(2)} ${escapeHtml(t("unit_km"))}` : "—"}
          </span>
        </div>

        <div class="scorebar" aria-hidden="true">
          <div class="scorebar__fill" data-width="${clamp(score, 0, 100)}"></div>
        </div>

        <p class="card__why">${escapeHtml(explanation)}</p>

        <div class="card__action">
          <button class="link" type="button" data-action="focus">${escapeHtml(t("card_show_on_map"))}</button>
          <button class="link" type="button" data-action="explain">${escapeHtml(t("card_explain_score"))}</button>
        </div>
      `;

      const onFocus = () => focusPlace(place);
      card.addEventListener("mouseenter", onFocus);
      card.addEventListener("focus", onFocus);
      card.addEventListener("click", (e) => {
        const target = e.target;
        if (!(target instanceof HTMLElement)) return;
        const action = target.getAttribute("data-action");
        if (action === "focus") {
          focusPlace(place);
          sendFeedback("click", place);
          return;
        }
        if (action === "explain") {
          showBreakdown(place);
          sendFeedback("explain", place);
          return;
        }
        // Clicking the card anywhere counts as interest.
        focusPlace(place);
        sendFeedback("click", place);
      });

      dom.cards.appendChild(card);
    });

    // Let scorebars animate after DOM insertion.
    requestAnimationFrame(() => {
      dom.cards.querySelectorAll(".scorebar__fill").forEach((el) => {
        const width = el.getAttribute("data-width") || "0";
        el.style.width = `${width}%`;
      });
    });
  }

  function showBreakdown(place) {
    const breakdown = place.breakdown || {};
    const items = [
      [t("breakdown_activity"), breakdown.activity, 30],
      [t("breakdown_distance"), breakdown.distance, 25],
      [t("breakdown_group"), breakdown.group, 20],
      [t("breakdown_budget"), breakdown.budget, 15],
      [t("breakdown_people"), breakdown.people, 10],
      [t("breakdown_quality"), breakdown.quality, 10],
    ];

    const lines = items
      .map(([label, value, max]) => {
        const v = Number(value || 0);
        const pct = Math.round((v / Number(max)) * 100);
        return `${label}: ${pct}%`;
      })
      .join(" • ");

    showToast(lines || tr("toast_score", { score: place.score || 0 }));
  }

  function focusPlace(place) {
    if (!map || !markerLayer) return;
    if (typeof place.lat !== "number" || typeof place.lon !== "number") return;
    map.panTo([place.lat, place.lon], { animate: true, duration: 0.45 });
  }

  function renderMarkers(recs) {
    if (!markerLayer) return;

    // Keep the user marker.
    markerLayer.clearLayers();
    state.userMarker = L.marker([state.origin.lat, state.origin.lon], {
      icon: userIcon(),
      interactive: false,
    }).addTo(markerLayer);

    recs.forEach((place, index) => {
      if (typeof place.lat !== "number" || typeof place.lon !== "number") return;
      const isTop = Number(place.rank || index + 1) === 1;
      const marker = L.marker([place.lat, place.lon], { icon: markerIcon(isTop) }).addTo(markerLayer);
      marker.bindPopup(
        `<strong>${escapeHtml(place.name || t("unknown_place"))}</strong><br/>${escapeHtml(
          t("marker_popup_score")
        )}: ${escapeHtml(String(place.score || 0))}`
      );
      marker.on("click", () => sendFeedback("click", place));
    });
  }

  async function runRecommendation() {
    const prefs = getPrefs();
    updateEngine(prefs);

    if (prefs.search_mode === "city" && !prefs.city) {
      showToast(t("toast_type_city"));
      if (dom.cityInput) dom.cityInput.focus();
      return;
    }

    if (!map) initMap();
    setLoading(true);
    if (dom.mapSub) dom.mapSub.textContent = t("map_sub_scoring");

    try {
      const payload = {
        ...prefs,
        lang: state.lang,
        session_id: state.sessionId,
        lat: state.origin.source === "user" ? state.origin.lat : undefined,
        lon: state.origin.source === "user" ? state.origin.lon : undefined,
      };

      const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const result = await response.json();

      state.lastRequestId = typeof result.request_id === "string" ? result.request_id : null;
      state.lastResponse = {
        search_mode: result.search_mode,
        city: result.city,
        radius_m: result.radius_m,
        data_source: result.data_source,
      };

      const recs = Array.isArray(result.recommendations) ? result.recommendations : [];
      state.lastResults = recs;

      if (dom.resultsMeta) {
        if (result.search_mode === "city" && result.city) {
          dom.resultsMeta.textContent = tr("results_meta_city", { count: recs.length, city: result.city });
        } else {
          const radiusKm = result.radius_m ? (Number(result.radius_m) / 1000).toFixed(1) : "—";
          dom.resultsMeta.textContent = tr("results_meta_radius", { count: recs.length, radius: radiusKm });
        }
      }

      if (dom.dataSourceMeta) {
        dom.dataSourceMeta.textContent = `${t("data_prefix")}: ${labelDataSource(result.data_source)}`;
      }
      if (dom.mapSub) dom.mapSub.textContent = recs.length ? t("map_sub_top") : t("map_sub_none");

      // If backend returns a real origin, respect it (demo fallback).
      if (result.origin && typeof result.origin.lat === "number" && typeof result.origin.lon === "number") {
        if (
          state.origin.source !== "user" &&
          (result.origin.source === "demo" || result.origin.source === "city")
        ) {
          setOrigin(result.origin.lat, result.origin.lon, result.origin.source);
        }
      }

      renderMarkers(recs);
      renderCards(recs);

      if (recs.length) {
        const top = recs[0];
        if (typeof top.lat === "number" && typeof top.lon === "number") {
          map.setView([top.lat, top.lon], 13, { animate: true });
        }
        showToast(t("toast_top_picks"));
      } else {
        showToast(t("toast_no_places"));
      }
    } catch (err) {
      showToast(t("toast_backend_failed"));
      if (dom.mapSub) dom.mapSub.textContent = t("map_sub_backend");
    } finally {
      setLoading(false);
    }
  }

  function requestLocation() {
    if (!navigator.geolocation) {
      showToast(t("toast_geo_unsupported"));
      return;
    }
    state.locationState = "locating";
    if (dom.useLocationBtn) dom.useLocationBtn.disabled = true;
    updateLocationButton();

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        setOrigin(lat, lon, "user");
        state.locationState = "enabled";
        updateLocationButton();
        showToast(t("toast_location_enabled"));
      },
      () => {
        state.locationState = "idle";
        updateLocationButton();
        showToast(t("toast_location_denied"));
      },
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 }
    );

    window.setTimeout(() => {
      if (dom.useLocationBtn) dom.useLocationBtn.disabled = false;
    }, 1200);
  }

  function typeLabel(type) {
    const kind = String(type || "").toLowerCase();
    for (const category of CATEGORY_TREE) {
      const item = category.items.find((it) => it.id === kind);
      if (item) return categoryText(item.label);
    }
    const primary = primaryFromSubcategory(kind);
    if (primary === "cafe") return t("type_cafe");
    if (primary === "restaurant") return t("type_restaurant");
    if (primary === "entertainment") return t("type_entertainment");
    return t("type_nature");
  }

  function tinyIcon(kind) {
    if (kind === "pin") {
      return `
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 21s7-4.4 7-11a7 7 0 1 0-14 0c0 6.6 7 11 7 11Z" stroke="currentColor" stroke-width="1.5" />
          <path d="M12 10.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" fill="currentColor" opacity="0.9" />
        </svg>`;
    }
    return `
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M4 8h16M7 8v-2a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        <path d="M7 12h10M7 16h7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
      </svg>`;
  }

  function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
  }

  function escapeHtml(input) {
    return String(input)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function wireEvents() {
    document.querySelectorAll('input[name="lang"]').forEach((el) => {
      el.addEventListener("change", () => {
        if (!(el instanceof HTMLInputElement)) return;
        if (el.checked) setLang(el.value);
      });
    });

    if (dom.peopleCount) dom.peopleCount.addEventListener("input", () => {
      updatePeopleLabel();
      updateEngine(getPrefs());
    });

    if (dom.radiusKm) dom.radiusKm.addEventListener("input", () => {
      updateRadiusLabel();
      updateEngine(getPrefs());
    });

    if (dom.cityInput) dom.cityInput.addEventListener("input", () => updateEngine(getPrefs()));

    document.querySelectorAll('input[name="search_mode"]').forEach((el) => {
      el.addEventListener("change", () => {
        const prefs = getPrefs();
        updateSearchUi(prefs);
        updateEngine(prefs);
        if (prefs.search_mode === "city" && dom.cityInput) dom.cityInput.focus();
      });
    });

    document.querySelectorAll('input[name="group_type"], input[name="budget"], #hasCar').forEach((el) => {
      el.addEventListener("change", () => updateEngine(getPrefs()));
    });

    if (dom.prefsForm) dom.prefsForm.addEventListener("submit", (e) => {
      e.preventDefault();
      runRecommendation();
    });

    if (dom.chatForm) dom.chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!dom.chatInput) return;
      const message = String(dom.chatInput.value || "").trim();
      if (!message) return;

      appendChat("user", message);
      dom.chatInput.value = "";
      state.chatState = "thinking";
      setChatStatus(t("chat_status_thinking"));

      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: state.sessionId,
            lang: state.lang,
            message,
            current: getPrefs(),
          }),
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
        if (result && result.reply) appendChat("assistant", result.reply);

        const updates = result && result.updates && typeof result.updates === "object" ? result.updates : null;
        if (updates) {
          applyUpdates(updates);
          // If chat provided usable preferences, run a search immediately.
          const prefs = getPrefs();
          const canRun = !(prefs.search_mode === "city" && !prefs.city);
          if (Object.keys(updates).length && canRun) runRecommendation();
        }
      } catch {
        appendChat("assistant", t("toast_chat_failed"));
      } finally {
        state.chatState = "ready";
        setChatStatus(t("chat_status_ready"));
      }
    });

    if (dom.useLocationBtn) dom.useLocationBtn.addEventListener("click", requestLocation);
    if (dom.recenterBtn) dom.recenterBtn.addEventListener("click", () => {
      if (!map) return;
      map.setView([state.origin.lat, state.origin.lon], state.origin.source === "user" ? 13 : 12, {
        animate: true,
      });
    });
    if (dom.clearBtn) dom.clearBtn.addEventListener("click", clearResults);
  }

  function boot() {
    state.sessionId = getSessionId();
    setSelectedSubcategories(state.selectedSubcategories);
    setLang(detectInitialLang());
    updatePeopleLabel();
    updateRadiusLabel();
    const prefs = getPrefs();
    updateSearchUi(prefs);
    initMap();
    wireEvents();

    if (dom.chatLog) {
      appendChat("assistant", t("chat_welcome"));
      state.chatState = "ready";
      setChatStatus(t("chat_status_ready"));
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
