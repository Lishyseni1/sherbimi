const onlineCategories = [
  "Zhvillim Web", "Zhvillim Frontend", "Zhvillim Backend", "Full Stack Development",
  "Dizajn Grafik", "UI/UX Dizajn", "Logo Dizajn", "Brand Identity", "Marketing Digjital",
  "Menaxhim i Rrjeteve Sociale", "SEO", "Google Ads / Facebook Ads", "Copywriting",
  "Shkrim Artikujsh", "Përkthime", "Data Entry", "Virtual Assistant", "Mbështetje Administrative",
  "Krijim Prezantimesh", "Video Editim", "Motion Design", "Animacion 2D",
  "Montazh për TikTok / Reels / YouTube", "Fotomanipulim", "Ilustrime Digjitale",
  "Voice Over", "Transkriptim", "Konsulencë IT", "Testim i Webfaqeve",
  "Menaxhim Email Marketing", "Krijim Dyqanesh Online", "WordPress Development",
  "Shopify Support", "Programim Python", "Programim .NET", "Mësim Online / Tutor",
  "Konsulencë Biznesi", "Shërbime Kontabiliteti Online"
];

const fieldCategories = [
  "Elektricist", "Ujësjellës / Hidraulik", "Murator", "Piktor / Lyerje", "Punime Gipsi",
  "Keramist", "Montues Kuzhinash", "Montues Dyersh dhe Dritaresh", "Riparime Shtëpiake",
  "Pastrim Shtëpish", "Pastrim Zyrash", "Kopshtar", "Mirëmbajtje Oborri",
  "Servis Kompjuterësh në vend", "Servis Telefonash", "Instalues Kamerash",
  "Instalues Interneti / Rrjeti", "Fotograf Eventesh", "Videograf Eventesh", "DJ",
  "Këngëtar për evente", "Dekorues Eventesh", "Organizues Dasmash", "Cameraman",
  "Shofer Privat", "Transport i Vogël", "Asistent Teknik për Evente",
  "Grimer / Make-up Artist", "Frizer në vend", "Berber", "Estetiste", "Masazhist",
  "Trajner Personal", "Instruktor Fitnesi në vend", "Babysitter", "Kujdes për të Moshuar",
  "Roje / Security për evente", "Punëtor Ndërtimi", "Instalues Klimash",
  "Servis i Pajisjeve Shtëpiake"
];

const hybridCategories = [
  "Fotografi", "Videografi", "Konsulencë Marketingu", "Konsulencë Ligjore",
  "Konsulencë Kontabiliteti", "Arkitekt", "Dizajn Interieri", "Agjent Imobiliar",
  "Trajnime Private", "Tutor në shtëpi", "Teknik IT", "Specialist Rrjetesh",
  "Specialist Branding", "Menaxher Projekti Freelance", "Event Manager",
  "Social Media Content Creator", "SEO Specialist", "Web Designer", "Freelancer për Biznese Lokale"
];

function getElement(id) {
  return document.getElementById(id);
}

function setupNavbar() {
  const toggle = document.querySelector(".menu-toggle");
  const links = document.querySelector(".nav-links");
  if (!toggle || !links) return;
  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("show");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });
}

function renderTags(containerId, items) {
  const container = getElement(containerId);
  if (!container) return;
  container.innerHTML = items.map((item) => `<span class="tag">${item}</span>`).join("");
}

function setupServicesPage() {
  renderTags("onlineServices", onlineCategories);
  renderTags("fieldServices", fieldCategories);
  renderTags("hybridServices", hybridCategories);
}

document.addEventListener("DOMContentLoaded", () => {
  setupNavbar();
  setupServicesPage();
});
