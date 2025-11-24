const input = document.getElementById("global-search-input");
const resultsContainer = document.getElementById("global-search-results");

// Datos inyectados desde base.html
const roomsRaw = window.ROOMS_FOR_SEARCH || [];
const servicesRaw = window.SERVICES_FOR_SEARCH || [];
const activitiesRaw = window.ACTIVITIES_FOR_SEARCH || [];
const packagesRaw = window.PACKAGES_FOR_SEARCH || [];

// Normalizamos todo a { id, label, type }
const items = [
  ...roomsRaw.map(r => ({
    id: r.id,
    label: r.nombre || r.name || `Habitación ${r.id}`,
    type: "habitacion",
  })),
  ...servicesRaw.map(s => ({
    id: s.id,
    label: s.nombre || s.name || `Servicio ${s.id}`,
    type: "servicio",
  })),
  ...activitiesRaw.map(a => ({
    id: a.id,
    label: a.nombre || a.name || `Actividad ${a.id}`,
    type: "actividad",
  })),
  ...packagesRaw.map(p => ({
    id: p.id,
    label: p.nombre || p.name || `Paquete ${p.id}`,
    type: "paquete",
  })),
];

if (!items.length) {
  console.warn("No hay datos para el buscador global (items está vacío).");
}

// A dónde querés ir al clickear un resultado
function handleSearchResultClick(type, id) {
  let url = "/";

  switch (type) {
    case "habitacion":
      url = `/habitaciones#${id}`;
      break;
    case "servicio":
      url = `/servicios#${id}`;
      break;
    case "actividad":
      url = `/actividades#${id}`;
      break;
    case "paquete":
      url = `/paquetes#${id}`;
      break;
    default:
      url = "/";
  }

  window.location.href = url;
}

function renderResults(query) {
  const q = query.trim().toLowerCase();

  if (!q) {
    resultsContainer.style.display = "none";
    resultsContainer.innerHTML = "";
    return;
  }

  const matches = items
    .filter(item => item.label && item.label.toLowerCase().includes(q))
    .slice(0, 5); 

  if (!matches.length) {
    resultsContainer.style.display = "none";
    resultsContainer.innerHTML = "";
    return;
  }

  resultsContainer.innerHTML = matches
    .map(
      item => `
      <div class="search__results-item"
           data-id="${item.id}"
           data-type="${item.type}">
        <span>${item.label}</span>
        <span class="search__results-item-type">${item.type}</span>
      </div>
    `
    )
    .join("");

  resultsContainer.style.display = "block";

  document.querySelectorAll(".search__results-item").forEach(el => {
    el.addEventListener("click", () => {
      const id = el.getAttribute("data-id");
      const type = el.getAttribute("data-type");
      handleSearchResultClick(type, id);
    });
  });
}

if (input && resultsContainer) {
  input.addEventListener("input", e => {
    renderResults(e.target.value);
  });

  document.addEventListener("click", e => {
    if (!resultsContainer.contains(e.target) && e.target !== input) {
      resultsContainer.style.display = "none";
    }
  });
}