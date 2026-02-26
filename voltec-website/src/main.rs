use leptos::*;
use leptos_router::*;
use wasm_bindgen::prelude::*;
use web_sys::{CanvasRenderingContext2d, HtmlCanvasElement};

/* ============================================
   VOLTEC — THE ENERGY OPERATING SYSTEM
   Table of Contents:
   1. Main Entry Point
   2. App Component (Router)
   3. Navigation
   4. Footer
   5. Home Page (Hero + Flywheel + Products + Stats + CTA)
   6. Products Page (V-Series Catalog)
   7. Platform Page (V-OS + V-Mind + Developer)
   8. Solutions Page (Customer Segments)
   9. Company Page (Mission + Team + Careers)
   10. Resources Page
   11. Contact Page
   12. Legal Pages
   13. Shared Components (Cards, Stats, Particle BG, Icons)
   ============================================ */

// ============================================
// UTILITY: Number formatting with comma separators
// ============================================
fn format_number(n: i32) -> String {
    let s = n.to_string();
    let bytes = s.as_bytes();
    let mut result = String::new();
    for (i, &b) in bytes.iter().enumerate() {
        if i > 0 && (bytes.len() - i) % 3 == 0 {
            result.push(',');
        }
        result.push(b as char);
    }
    result
}

// ============================================
// 1. MAIN ENTRY POINT
// ============================================
fn main() {
    console_error_panic_hook::set_once();
    _ = console_log::init_with_level(log::Level::Debug);
    mount_to_body(|| view! { <App /> });
}

// ============================================
// 2. APP COMPONENT
// ============================================
#[component]
fn App() -> impl IntoView {
    view! {
        <Router>
            <div class="min-h-screen flex flex-col bg-voltec-white text-voltec-black font-sans">
                <Nav />
                <main class="flex-grow">
                    <Routes>
                        <Route path="/" view=HomePage />
                        <Route path="/products" view=ProductsPage />
                        <Route path="/platform" view=PlatformPage />
                        <Route path="/solutions" view=SolutionsPage />
                        <Route path="/company" view=CompanyPage />
                        <Route path="/resources" view=ResourcesPage />
                        <Route path="/contact" view=ContactPage />
                        <Route path="/privacy" view=PrivacyPage />
                        <Route path="/terms" view=TermsPage />
                    </Routes>
                </main>
                <Footer />
            </div>
        </Router>
    }
}

// ============================================
// 3. NAVIGATION
// ============================================
#[component]
fn Nav() -> impl IntoView {
    let (is_mobile_open, set_mobile_open) = create_signal(false);

    view! {
        <nav class="bg-voltec-black text-voltec-white px-6 py-4 sticky top-0 z-50 border-b border-voltec-blue/20">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <A href="/" class="flex items-center gap-3 group">
                    <div class="w-9 h-9 border border-voltec-blue rounded-sm flex items-center justify-center group-hover:bg-voltec-blue/10 transition-all duration-300">
                        <span class="font-display font-bold text-sm text-voltec-blue">"V"</span>
                    </div>
                    <span class="text-xl font-display font-bold tracking-widest hover:text-voltec-blue transition-colors">
                        "VOLTEC"
                    </span>
                </A>

                <ul class="hidden md:flex space-x-8 items-center text-sm tracking-wide">
                    <li><A href="/products" class="nav-link">"Products"</A></li>
                    <li><A href="/platform" class="nav-link">"Platform"</A></li>
                    <li><A href="/solutions" class="nav-link">"Solutions"</A></li>
                    <li><A href="/company" class="nav-link">"Company"</A></li>
                    <li><A href="/resources" class="nav-link">"Resources"</A></li>
                    <li>
                        <A href="/contact" class="bg-voltec-blue/10 border border-voltec-blue/40 text-voltec-blue px-4 py-2 rounded-sm text-xs font-semibold uppercase tracking-widest hover:bg-voltec-blue hover:text-white transition-all duration-300">
                            "Request Demo"
                        </A>
                    </li>
                </ul>

                <button
                    class="md:hidden text-voltec-white focus:outline-none p-2"
                    on:click=move |_| set_mobile_open.update(|v| *v = !*v)
                >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d=move || if is_mobile_open.get() { "M6 18L18 6M6 6l12 12" } else { "M4 6h16M4 12h16M4 18h16" } />
                    </svg>
                </button>
            </div>

            <div class=move || format!(
                "md:hidden overflow-hidden transition-all duration-300 {}",
                if is_mobile_open.get() { "max-h-96 mt-4" } else { "max-h-0" }
            )>
                <ul class="flex flex-col space-y-3 pb-4 text-sm">
                    <li><A href="/products" class="nav-link block py-1">"Products"</A></li>
                    <li><A href="/platform" class="nav-link block py-1">"Platform"</A></li>
                    <li><A href="/solutions" class="nav-link block py-1">"Solutions"</A></li>
                    <li><A href="/company" class="nav-link block py-1">"Company"</A></li>
                    <li><A href="/resources" class="nav-link block py-1">"Resources"</A></li>
                    <li><A href="/contact" class="text-voltec-blue font-semibold block py-1">"Request Demo"</A></li>
                </ul>
            </div>
        </nav>
    }
}

// ============================================
// 4. FOOTER
// ============================================
#[component]
fn Footer() -> impl IntoView {
    view! {
        <footer class="bg-voltec-black text-voltec-white py-16 border-t border-voltec-blue/10">
            <div class="max-w-7xl mx-auto px-6">
                <div class="grid md:grid-cols-5 gap-10">
                    <div class="md:col-span-2">
                        <div class="flex items-center gap-3 mb-4">
                            <div class="w-8 h-8 border border-voltec-blue rounded-sm flex items-center justify-center">
                                <span class="font-display font-bold text-xs text-voltec-blue">"V"</span>
                            </div>
                            <span class="text-lg font-display font-bold tracking-widest">"VOLTEC"</span>
                        </div>
                        <p class="text-voltec-white/40 text-sm leading-relaxed mb-6 max-w-xs">
                            "The Energy Operating System. Every device is a node in the world's largest industrial intelligence network."
                        </p>
                        <div class="flex space-x-3">
                            <SocialIcon href="https://x.com/voltec" icon_type="x" />
                            <SocialIcon href="https://linkedin.com/company/voltec" icon_type="linkedin" />
                            <SocialIcon href="https://github.com/voltec" icon_type="github" />
                            <SocialIcon href="https://youtube.com/@voltec" icon_type="youtube" />
                            <SocialIcon href="https://discord.gg/voltec" icon_type="discord" />
                        </div>
                    </div>

                    <div>
                        <h4 class="text-xs font-semibold uppercase tracking-widest text-voltec-blue mb-4">"Products"</h4>
                        <ul class="space-y-2 text-sm">
                            <li><a href="/products" class="footer-link">"V-Cell"</a></li>
                            <li><a href="/products" class="footer-link">"V-Pack"</a></li>
                            <li><a href="/products" class="footer-link">"V-Grid"</a></li>
                            <li><a href="/products" class="footer-link">"V-Fab"</a></li>
                            <li><a href="/products" class="footer-link">"V-Shield"</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="text-xs font-semibold uppercase tracking-widest text-voltec-blue mb-4">"Platform"</h4>
                        <ul class="space-y-2 text-sm">
                            <li><a href="/platform" class="footer-link">"V-OS"</a></li>
                            <li><a href="/platform" class="footer-link">"V-Mind"</a></li>
                            <li><a href="/platform" class="footer-link">"V-Store"</a></li>
                            <li><a href="/platform" class="footer-link">"Developer SDK"</a></li>
                            <li><a href="/platform" class="footer-link">"API Docs"</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="text-xs font-semibold uppercase tracking-widest text-voltec-blue mb-4">"Company"</h4>
                        <ul class="space-y-2 text-sm">
                            <li><a href="/company" class="footer-link">"About"</a></li>
                            <li><a href="/company" class="footer-link">"Careers"</a></li>
                            <li><a href="/resources" class="footer-link">"Resources"</a></li>
                            <li><a href="/contact" class="footer-link">"Contact"</a></li>
                            <li><a href="/privacy" class="footer-link">"Privacy"</a></li>
                            <li><a href="/terms" class="footer-link">"Terms"</a></li>
                        </ul>
                    </div>
                </div>

                <div class="border-t border-voltec-blue/10 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
                    <p class="text-voltec-white/30 text-xs">
                        "© 2026 Voltec Industries. All rights reserved."
                    </p>
                    <p class="text-voltec-white/20 text-xs mt-4 md:mt-0 font-mono">
                        "Rust + Leptos + WASM // V-OS r1.0"
                    </p>
                </div>
            </div>
        </footer>
    }
}

// ============================================
// 5. HOME PAGE
// ============================================
#[component]
fn HomePage() -> impl IntoView {
    let (nodes_count, set_nodes_count) = create_signal(12_847);

    // Simulate live counter
    set_interval(
        move || set_nodes_count.update(|n| *n += 1),
        std::time::Duration::from_millis(3000),
    );

    view! {
        <div>
            // HERO
            <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-voltec-black">
                <div class="absolute inset-0 grid-bg opacity-40"></div>
                <div class="absolute inset-0 bg-radial-glow"></div>
                <ParticleBackground />

                <div class="relative z-10 max-w-5xl mx-auto px-6 text-center">
                    <p class="text-voltec-blue text-xs md:text-sm font-mono tracking-[0.3em] mb-6 uppercase">
                        "The Energy Operating System"
                    </p>
                    <h1 class="text-5xl md:text-7xl lg:text-8xl font-display font-bold text-white mb-8 tracking-tight leading-none">
                        "Every device."<br />"One network."
                    </h1>
                    <p class="text-voltec-white/60 text-lg md:text-xl max-w-2xl mx-auto mb-12 leading-relaxed">
                        "Voltec builds the intelligent energy cells, autonomous platforms, and industrial OS that power the next generation of infrastructure — on Earth and off it."
                    </p>

                    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <A href="/contact" class="btn-primary">"Request a Demo"</A>
                        <A href="/products" class="btn-outline">"View Products"</A>
                    </div>

                    // Live Network Counter
                    <div class="mt-16 inline-flex items-center gap-3 bg-voltec-white/5 border border-voltec-blue/20 rounded-sm px-6 py-3">
                        <span class="w-2 h-2 bg-voltec-blue rounded-full animate-pulse-glow"></span>
                        <span class="text-voltec-white/50 text-sm font-mono">
                            "V-OS Network: "
                            <span class="text-voltec-blue font-semibold">{move || format_number(nodes_count.get())}</span>
                            " active nodes"
                        </span>
                    </div>
                </div>

                <div class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
                    <svg class="w-5 h-5 text-voltec-blue/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                    </svg>
                </div>
            </section>

            // CORE PRODUCTS STRIP
            <section class="py-24 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="text-center mb-16">
                        <p class="text-voltec-blue text-xs font-mono tracking-[0.3em] uppercase mb-3">"Tier 1 — Foundation"</p>
                        <h2 class="section-title mb-4">"The V-Series"</h2>
                        <p class="section-subtitle mx-auto">
                            "Three products. One breakthrough chemistry. An intelligent energy stack from cell to grid."
                        </p>
                    </div>

                    <div class="grid md:grid-cols-3 gap-8">
                        <ProductCardHome
                            name="V-Cell"
                            tagline="Solid-State Energy Cell"
                            spec="900 Wh/kg • 10,000+ cycles"
                            description="The fundamental unit. 3x energy density. No lithium dependency. Everything is built on V-Cell."
                        />
                        <ProductCardHome
                            name="V-Pack"
                            tagline="Modular Battery System"
                            spec="5 kWh – 5 MWh configurations"
                            description="Intelligent, self-monitoring packs. V-Mind predicts failures 72 hours out. 99.7% accuracy."
                        />
                        <ProductCardHome
                            name="V-Grid"
                            tagline="Distributed Energy Platform"
                            spec="1 MW – 1 GW • 99.99% uptime"
                            description="Self-optimizing energy mesh. AI-driven load balancing across thousands of nodes. No human intervention."
                        />
                    </div>

                    <div class="text-center mt-12">
                        <A href="/products" class="text-voltec-blue hover:text-voltec-blue-light transition-colors font-medium text-sm tracking-wide">
                            "View full product catalog →"
                        </A>
                    </div>
                </div>
            </section>

            // FLYWHEEL SECTION
            <section class="py-24 bg-voltec-black text-white relative overflow-hidden">
                <div class="absolute inset-0 grid-bg opacity-20"></div>
                <div class="max-w-7xl mx-auto px-6 relative z-10">
                    <div class="text-center mb-16">
                        <p class="text-voltec-blue text-xs font-mono tracking-[0.3em] uppercase mb-3">"Network Effect"</p>
                        <h2 class="text-4xl md:text-5xl font-display font-bold tracking-tight mb-4">"The Voltec Flywheel"</h2>
                        <p class="text-voltec-white/50 max-w-2xl mx-auto">
                            "Every device deployed makes the network smarter. Every improvement lowers cost. Every cost reduction opens new markets. The cycle never stops."
                        </p>
                    </div>

                    <div class="grid md:grid-cols-4 gap-6">
                        <FlywheelStep number="01" title="Better Cells" description="V-Cell chemistry delivers 3x density at lower cost per kWh." />
                        <FlywheelStep number="02" title="More Deployments" description="Lower cost drives adoption. More V-Packs and V-Grids in the field." />
                        <FlywheelStep number="03" title="More Data" description="Every V-OS device streams telemetry. The network grows smarter." />
                        <FlywheelStep number="04" title="Smarter AI" description="V-Mind improves with scale. Better predictions, lower costs. Repeat." />
                    </div>
                </div>
            </section>

            // STATS
            <section class="py-20 bg-voltec-white border-y border-voltec-gray-light">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                        <StatBlock number="900" unit="Wh/kg" label="V-Cell Energy Density" />
                        <StatBlock number="72" unit="hrs" label="Failure Prediction Window" />
                        <StatBlock number="99.99" unit="%" label="V-Grid Uptime SLA" />
                        <StatBlock number="10K" unit="+" label="V-Cell Cycle Life" />
                    </div>
                </div>
            </section>

            // PLATFORM PREVIEW
            <section class="py-24 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="grid md:grid-cols-2 gap-16 items-center">
                        <div>
                            <p class="text-voltec-blue text-xs font-mono tracking-[0.3em] uppercase mb-3">"Tier 2 — Platform"</p>
                            <h2 class="section-title mb-6">"V-OS: The Industrial Operating System"</h2>
                            <p class="text-voltec-gray/70 mb-6 leading-relaxed">
                                "Every Voltec device runs V-OS. Third-party developers build on it. "
                                "Open-source kernel. Proprietary AI and data layers. "
                                "Sub-millisecond control loops. Zero-trust security. OTA updates to every node."
                            </p>
                            <ul class="space-y-3 text-sm text-voltec-gray/60 mb-8">
                                <li class="flex items-center gap-3">
                                    <span class="w-1.5 h-1.5 bg-voltec-blue rounded-full"></span>
                                    "Open API Layer — REST + gRPC, full SDK"
                                </li>
                                <li class="flex items-center gap-3">
                                    <span class="w-1.5 h-1.5 bg-voltec-blue rounded-full"></span>
                                    "V-Store Marketplace — 80/20 revenue split for developers"
                                </li>
                                <li class="flex items-center gap-3">
                                    <span class="w-1.5 h-1.5 bg-voltec-blue rounded-full"></span>
                                    "V-Mind AI — Gets smarter with every connected node"
                                </li>
                            </ul>
                            <A href="/platform" class="btn-primary text-sm">"Explore the Platform"</A>
                        </div>
                        <div class="relative">
                            <VosTerminal />
                        </div>
                    </div>
                </div>
            </section>

            // CTA
            <section class="py-24 bg-voltec-black text-white relative overflow-hidden">
                <div class="absolute inset-0 bg-radial-glow opacity-50"></div>
                <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
                    <h2 class="text-4xl md:text-5xl font-display font-bold tracking-tight mb-6">
                        "Ready to connect?"
                    </h2>
                    <p class="text-voltec-white/50 mb-10 text-lg">
                        "Request a demo, download a datasheet, or talk to our engineering team."
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <A href="/contact" class="btn-primary">"Request a Demo"</A>
                        <A href="/products" class="btn-outline">"Download Datasheets"</A>
                    </div>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 6. PRODUCTS PAGE
// ============================================
#[component]
fn ProductsPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Products" subtitle="THE V-SERIES" />

            // Tier 1
            <section class="py-20 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6">
                    <TierHeader tier="Tier 1" name="Foundation" status="Shipping Now" />
                    <div class="grid md:grid-cols-3 gap-8 mt-10">
                        <ProductCardFull
                            name="V-Cell" tagline="Solid-State Energy Cell"
                            specs=vec!["900 Wh/kg target", "10,000+ cycles", "Stable to 300°C", "No lithium/cobalt", "Dry electrode mfg"]
                        />
                        <ProductCardFull
                            name="V-Pack" tagline="Modular Battery System"
                            specs=vec!["5 kWh – 5 MWh", "V-Mind integrated", "72-hr failure prediction", "99.7% accuracy", "Industrial / Defense configs"]
                        />
                        <ProductCardFull
                            name="V-Grid" tagline="Distributed Energy Platform"
                            specs=vec!["1 MW – 1 GW scale", "AI load balancing", "Self-healing mesh", "99.99% uptime SLA", "Industrial / Municipal / Defense"]
                        />
                    </div>
                </div>
            </section>

            // Tier 2
            <section class="py-20 bg-voltec-gray-light">
                <div class="max-w-7xl mx-auto px-6">
                    <TierHeader tier="Tier 2" name="Platform" status="18 Months" />
                    <div class="grid md:grid-cols-3 gap-8 mt-10">
                        <ProductCardFull
                            name="V-OS" tagline="Industrial Operating System"
                            specs=vec!["Real-time RTOS", "Open API (REST + gRPC)", "OTA updates", "Zero-trust security", "Developer SDK"]
                        />
                        <ProductCardFull
                            name="V-Mind" tagline="AI/ML Intelligence Engine"
                            specs=vec!["Predictive maintenance", "Energy optimization", "Anomaly detection", "Edge inference", "Data network effect"]
                        />
                        <ProductCardFull
                            name="V-Fab" tagline="Autonomous Manufacturing Cell"
                            specs=vec!["2,000 sq ft modular", "72-hr setup", "10K V-Cells/day", "95% automation", "V-Mind diagnostics"]
                        />
                    </div>
                </div>
            </section>

            // Tier 3
            <section class="py-20 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6">
                    <TierHeader tier="Tier 3" name="Horizon" status="3-5 Years" />
                    <div class="grid md:grid-cols-2 gap-8 mt-10 max-w-3xl mx-auto">
                        <ProductCardFull
                            name="V-Shield" tagline="Space-Grade Electronics"
                            specs=vec!["100 krad TID", "-40°C to +125°C", "MIL-STD-883", "10x cost (not 100x)", "Orbital qualified"]
                        />
                        <ProductCardFull
                            name="V-Orbit" tagline="Space Energy Packs"
                            specs=vec!["CubeSat to GEO", "100 Wh – 100 kWh", "Rad-hardened V-Cells", "Satellite bus ready", "Deep-space rated"]
                        />
                    </div>
                </div>
            </section>

            // CTA
            <section class="py-16 bg-voltec-black text-white">
                <div class="max-w-3xl mx-auto px-6 text-center">
                    <p class="text-voltec-white/50 mb-6">"All products ship with full technical datasheets. No marketing fluff."</p>
                    <A href="/contact" class="btn-primary">"Request Datasheets"</A>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 7. PLATFORM PAGE
// ============================================
#[component]
fn PlatformPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Platform" subtitle="V-OS ECOSYSTEM" />

            <section class="py-20 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="grid md:grid-cols-2 gap-16 items-start">
                        <div>
                            <h2 class="section-title mb-6">"V-OS"</h2>
                            <p class="text-voltec-gray/70 leading-relaxed mb-6">
                                "The industrial operating system. Every Voltec device runs V-OS. "
                                "Open-source kernel for adoption and trust. Proprietary AI and data layers for monetization and moat."
                            </p>
                            <div class="space-y-4">
                                <PlatformFeature title="Real-Time Control" desc="Sub-millisecond loops for energy management and automation." />
                                <PlatformFeature title="Open API" desc="REST + gRPC. Full SDK and cloud-based simulator." />
                                <PlatformFeature title="OTA Updates" desc="Push firmware and model updates to every connected device." />
                                <PlatformFeature title="Zero-Trust Security" desc="Hardware root of trust. Encrypted telemetry. Air-gap capable." />
                            </div>
                        </div>
                        <div>
                            <VosTerminal />
                        </div>
                    </div>
                </div>
            </section>

            <section class="py-20 bg-voltec-gray-light">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="text-center mb-12">
                        <h2 class="section-title mb-4">"V-Mind"</h2>
                        <p class="section-subtitle mx-auto">"The AI engine. Runs on every node. Gets smarter with scale."</p>
                    </div>
                    <div class="grid md:grid-cols-4 gap-6">
                        <MindCapability title="Predict" desc="72-hour failure forecasting at 99.7% accuracy." />
                        <MindCapability title="Optimize" desc="Real-time energy load balancing across distributed nodes." />
                        <MindCapability title="Detect" desc="Anomaly recognition across millions of sensor streams." />
                        <MindCapability title="Act" desc="Closed-loop autonomous control. No cloud dependency." />
                    </div>
                </div>
            </section>

            <section class="py-20 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6 text-center">
                    <h2 class="section-title mb-4">"Developer Ecosystem"</h2>
                    <p class="section-subtitle mx-auto mb-10">"Build on V-OS. Sell on V-Store. 80/20 revenue split."</p>
                    <div class="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
                        <div class="card-tech text-center">
                            <p class="font-display font-bold text-voltec-blue text-2xl mb-2">"SDK"</p>
                            <p class="text-sm text-voltec-gray/60">"Free V-OS SDK with full API access and documentation."</p>
                        </div>
                        <div class="card-tech text-center">
                            <p class="font-display font-bold text-voltec-blue text-2xl mb-2">"Simulator"</p>
                            <p class="text-sm text-voltec-gray/60">"Cloud-based dev environment. Test without hardware."</p>
                        </div>
                        <div class="card-tech text-center">
                            <p class="font-display font-bold text-voltec-blue text-2xl mb-2">"V-Store"</p>
                            <p class="text-sm text-voltec-gray/60">"Marketplace for third-party modules. Reach every V-OS device."</p>
                        </div>
                    </div>
                    <div class="mt-10">
                        <A href="/contact" class="btn-primary text-sm">"Join Developer Program"</A>
                    </div>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 8. SOLUTIONS PAGE
// ============================================
#[component]
fn SolutionsPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Solutions" subtitle="BY INDUSTRY" />

            <section class="py-20 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6 space-y-8">
                    <SolutionRow
                        industry="Manufacturing"
                        pain="Unplanned downtime costs $260K/hour."
                        solution="V-Pack + V-Mind predicts failures 72 hours in advance. 99.7% accuracy."
                        product="V-Pack Industrial"
                        cta="Calculate Downtime Savings"
                    />
                    <SolutionRow
                        industry="Energy & Utilities"
                        pain="Renewable intermittency creates grid instability. Storage is expensive and unintelligent."
                        solution="V-Grid self-optimizes across thousands of nodes. AI-driven, autonomous, self-healing."
                        product="V-Grid Municipal"
                        cta="See Grid ROI"
                    />
                    <SolutionRow
                        industry="Defense"
                        pain="Foreign supply chain dependency for critical energy and compute components."
                        solution="Vertically integrated. Domestic manufacturing. Hardened. Air-gapped. V-Pack Defense."
                        product="V-Pack Defense"
                        cta="Request Briefing"
                    />
                    <SolutionRow
                        industry="Data Centers"
                        pain="Power is 40% of OpEx. Cooling is another 20%."
                        solution="Solid-state V-Packs eliminate cooling needs. V-Grid cuts power costs by up to 50%."
                        product="V-Grid Data Center"
                        cta="Get Power Analysis"
                    />
                    <SolutionRow
                        industry="Space & Orbital"
                        pain="Radiation destroys commercial electronics. Space-grade parts cost 100x."
                        solution="V-Shield delivers space-qualified components at 10x current pricing."
                        product="V-Shield"
                        cta="Request Specs"
                    />
                </div>
            </section>
        </div>
    }
}

// ============================================
// 9. COMPANY PAGE
// ============================================
#[component]
fn CompanyPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Company" subtitle="VOLTEC INDUSTRIES" />

            <section class="py-20 bg-voltec-white">
                <div class="max-w-4xl mx-auto px-6">
                    <h2 class="section-title mb-6">"Mission"</h2>
                    <p class="text-xl text-voltec-gray/80 leading-relaxed mb-8">
                        "Make the fundamental energy unit that powers everything — on Earth and off it."
                    </p>
                    <p class="text-voltec-gray/60 leading-relaxed mb-12">
                        "Voltec is a deep-tech industrial company building the backbone of next-generation infrastructure. "
                        "We design, manufacture, and deploy intelligent energy cells, autonomous platforms, and the software "
                        "that connects them into the world's largest industrial intelligence network."
                    </p>

                    <div class="grid md:grid-cols-2 gap-8 mb-16">
                        <div class="card-tech">
                            <h3 class="font-semibold text-lg mb-3 text-voltec-blue">"Vertical Integration"</h3>
                            <p class="text-sm text-voltec-gray/60 leading-relaxed">
                                "Raw materials → cell fabrication → pack assembly → firmware → deployment → monitoring. "
                                "We own every step. No supply chain dependency."
                            </p>
                        </div>
                        <div class="card-tech">
                            <h3 class="font-semibold text-lg mb-3 text-voltec-blue">"Platform Transition"</h3>
                            <p class="text-sm text-voltec-gray/60 leading-relaxed">
                                "Hardware-heavy in Year 1. Platform-heavy by Year 5. "
                                "Hardware is the trojan horse. V-OS is the moat."
                            </p>
                        </div>
                    </div>

                    <h2 class="section-title mb-6">"Careers"</h2>
                    <p class="text-voltec-gray/60 mb-8">
                        "We hire people who've built things that went to space, survived a factory floor, or shipped code that controls physical systems."
                    </p>

                    <div class="space-y-4">
                        <JobCard title="Senior Cell Chemist" location="Austin, TX" team="Team V-Cell" />
                        <JobCard title="Embedded Systems Engineer" location="Remote" team="Team V-OS" />
                        <JobCard title="ML Engineer — Predictive Systems" location="Remote" team="Team V-Mind" />
                        <JobCard title="Robotics Engineer" location="Austin, TX" team="Team V-Fab" />
                        <JobCard title="Radiation Effects Engineer" location="Houston, TX" team="Team V-Shield" />
                    </div>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 10. RESOURCES PAGE
// ============================================
#[component]
fn ResourcesPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Resources" subtitle="DATASHEETS & RESEARCH" />

            <section class="py-20 bg-voltec-white">
                <div class="max-w-7xl mx-auto px-6">
                    <div class="grid md:grid-cols-3 gap-8">
                        <ResourceCard title="Product Datasheets" desc="Full technical specifications for every V-Series product." cta="Download" />
                        <ResourceCard title="V-OS Documentation" desc="API reference, SDK guides, and developer tutorials." cta="Read Docs" />
                        <ResourceCard title="Whitepapers" desc="Solid-state chemistry, V-Mind architecture, grid optimization research." cta="Access" />
                        <ResourceCard title="Case Studies" desc="Real-world deployments. ROI data. Customer testimonials." cta="Read" />
                        <ResourceCard title="Benchmark Reports" desc="V-Cell performance vs. lithium-ion. V-Grid vs. legacy storage." cta="Compare" />
                        <ResourceCard title="V-OS Changelog" desc="Release notes, feature updates, and security patches." cta="View" />
                    </div>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 11. CONTACT PAGE
// ============================================
#[component]
fn ContactPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Contact" subtitle="GET IN TOUCH" />

            <section class="py-20 bg-voltec-white">
                <div class="max-w-xl mx-auto px-6">
                    <form class="space-y-6">
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-widest mb-2 text-voltec-gray/60">"Name"</label>
                            <input type="text" class="w-full px-4 py-3 bg-voltec-gray-light border border-transparent rounded-sm focus:border-voltec-blue focus:outline-none transition-colors text-sm" />
                        </div>
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-widest mb-2 text-voltec-gray/60">"Email"</label>
                            <input type="email" class="w-full px-4 py-3 bg-voltec-gray-light border border-transparent rounded-sm focus:border-voltec-blue focus:outline-none transition-colors text-sm" />
                        </div>
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-widest mb-2 text-voltec-gray/60">"Company"</label>
                            <input type="text" class="w-full px-4 py-3 bg-voltec-gray-light border border-transparent rounded-sm focus:border-voltec-blue focus:outline-none transition-colors text-sm" />
                        </div>
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-widest mb-2 text-voltec-gray/60">"Interest"</label>
                            <select class="w-full px-4 py-3 bg-voltec-gray-light border border-transparent rounded-sm focus:border-voltec-blue focus:outline-none transition-colors text-sm">
                                <option>"Request a Demo"</option>
                                <option>"Product Inquiry"</option>
                                <option>"Partnership"</option>
                                <option>"Developer Program"</option>
                                <option>"Careers"</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold uppercase tracking-widest mb-2 text-voltec-gray/60">"Message"</label>
                            <textarea rows="5" class="w-full px-4 py-3 bg-voltec-gray-light border border-transparent rounded-sm focus:border-voltec-blue focus:outline-none transition-colors text-sm resize-none"></textarea>
                        </div>
                        <button type="submit" class="btn-primary w-full">"Send"</button>
                    </form>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 12. LEGAL PAGES
// ============================================
#[component]
fn PrivacyPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Privacy Policy" subtitle="LEGAL" />
            <section class="py-20 bg-voltec-white">
                <div class="max-w-3xl mx-auto px-6">
                    <p class="text-voltec-gray/70 leading-relaxed">
                        "This Privacy Policy describes how Voltec Industries collects, uses, and protects your information. "
                        "We collect only what's necessary. We never sell your data. Last updated: February 2026."
                    </p>
                </div>
            </section>
        </div>
    }
}

#[component]
fn TermsPage() -> impl IntoView {
    view! {
        <div>
            <PageHeader title="Terms of Service" subtitle="LEGAL" />
            <section class="py-20 bg-voltec-white">
                <div class="max-w-3xl mx-auto px-6">
                    <p class="text-voltec-gray/70 leading-relaxed">
                        "These Terms of Service govern your use of Voltec products and services. "
                        "By using our services, you agree to these terms. Last updated: February 2026."
                    </p>
                </div>
            </section>
        </div>
    }
}

// ============================================
// 13. SHARED COMPONENTS
// ============================================

// --- Page Header ---
#[component]
fn PageHeader(title: &'static str, subtitle: &'static str) -> impl IntoView {
    view! {
        <section class="py-20 bg-voltec-black text-white">
            <div class="max-w-7xl mx-auto px-6 text-center">
                <p class="text-voltec-blue text-xs font-mono tracking-[0.3em] uppercase mb-4">{subtitle}</p>
                <h1 class="text-5xl md:text-6xl font-display font-bold tracking-tight">{title}</h1>
            </div>
        </section>
    }
}

// --- Tier Header ---
#[component]
fn TierHeader(tier: &'static str, name: &'static str, status: &'static str) -> impl IntoView {
    view! {
        <div class="flex items-center gap-4 mb-2">
            <span class="text-voltec-blue text-xs font-mono tracking-widest uppercase">{tier}</span>
            <span class="h-px flex-grow bg-voltec-blue/20"></span>
            <span class="text-voltec-gray/40 text-xs font-mono">{status}</span>
        </div>
        <h3 class="text-2xl font-display font-bold tracking-tight">{name}</h3>
    }
}

// --- Home Product Card ---
#[component]
fn ProductCardHome(
    name: &'static str,
    tagline: &'static str,
    spec: &'static str,
    description: &'static str,
) -> impl IntoView {
    view! {
        <div class="card-tech group">
            <div class="flex items-center gap-3 mb-4">
                <span class="w-8 h-8 border border-voltec-blue/30 rounded-sm flex items-center justify-center text-voltec-blue font-display font-bold text-xs group-hover:bg-voltec-blue/10 transition-colors">
                    "V"
                </span>
                <div>
                    <p class="font-semibold text-lg">{name}</p>
                    <p class="text-voltec-gray/50 text-xs">{tagline}</p>
                </div>
            </div>
            <p class="text-voltec-blue text-xs font-mono mb-3">{spec}</p>
            <p class="text-voltec-gray/60 text-sm leading-relaxed">{description}</p>
        </div>
    }
}

// --- Full Product Card ---
#[component]
fn ProductCardFull(
    name: &'static str,
    tagline: &'static str,
    specs: Vec<&'static str>,
) -> impl IntoView {
    view! {
        <div class="card-tech">
            <p class="font-display font-bold text-xl mb-1">{name}</p>
            <p class="text-voltec-blue text-xs font-mono mb-4">{tagline}</p>
            <ul class="space-y-2">
                {specs.into_iter().map(|s| view! {
                    <li class="flex items-center gap-2 text-sm text-voltec-gray/60">
                        <span class="w-1 h-1 bg-voltec-blue rounded-full"></span>
                        {s}
                    </li>
                }).collect_view()}
            </ul>
        </div>
    }
}

// --- Flywheel Step ---
#[component]
fn FlywheelStep(number: &'static str, title: &'static str, description: &'static str) -> impl IntoView {
    view! {
        <div class="border border-voltec-blue/20 rounded-sm p-6 hover:border-voltec-blue/50 transition-colors">
            <span class="text-voltec-blue font-mono text-xs">{number}</span>
            <h3 class="font-semibold text-lg mt-2 mb-2">{title}</h3>
            <p class="text-voltec-white/40 text-sm leading-relaxed">{description}</p>
        </div>
    }
}

// --- Stat Block ---
#[component]
fn StatBlock(number: &'static str, unit: &'static str, label: &'static str) -> impl IntoView {
    view! {
        <div>
            <div class="flex items-baseline justify-center gap-1">
                <span class="text-3xl md:text-4xl font-display font-bold text-voltec-black">{number}</span>
                <span class="text-voltec-blue font-mono text-sm">{unit}</span>
            </div>
            <p class="text-voltec-gray/40 text-xs uppercase tracking-wider mt-1">{label}</p>
        </div>
    }
}

// --- Solution Row ---
#[component]
fn SolutionRow(
    industry: &'static str,
    pain: &'static str,
    solution: &'static str,
    product: &'static str,
    cta: &'static str,
) -> impl IntoView {
    view! {
        <div class="card-tech grid md:grid-cols-3 gap-6 items-center">
            <div>
                <p class="text-voltec-blue text-xs font-mono uppercase tracking-widest mb-1">{industry}</p>
                <p class="text-sm text-voltec-gray/60">{pain}</p>
            </div>
            <div>
                <p class="text-sm">{solution}</p>
                <p class="text-voltec-blue text-xs font-mono mt-2">"Product: " {product}</p>
            </div>
            <div class="text-right">
                <A href="/contact" class="btn-outline text-xs py-2 px-4">{cta}</A>
            </div>
        </div>
    }
}

// --- Platform Feature ---
#[component]
fn PlatformFeature(title: &'static str, desc: &'static str) -> impl IntoView {
    view! {
        <div class="flex items-start gap-3">
            <span class="w-1.5 h-1.5 bg-voltec-blue rounded-full mt-2 shrink-0"></span>
            <div>
                <p class="font-semibold text-sm">{title}</p>
                <p class="text-voltec-gray/50 text-sm">{desc}</p>
            </div>
        </div>
    }
}

// --- Mind Capability ---
#[component]
fn MindCapability(title: &'static str, desc: &'static str) -> impl IntoView {
    view! {
        <div class="card-tech text-center">
            <p class="font-display font-bold text-voltec-blue text-lg mb-2">{title}</p>
            <p class="text-sm text-voltec-gray/60">{desc}</p>
        </div>
    }
}

// --- Job Card ---
#[component]
fn JobCard(title: &'static str, location: &'static str, team: &'static str) -> impl IntoView {
    view! {
        <div class="card-tech flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
                <p class="font-semibold">{title}</p>
                <p class="text-voltec-gray/50 text-sm">{location} " • " {team}</p>
            </div>
            <A href="/contact" class="btn-outline text-xs py-2 px-4 text-center">"Apply"</A>
        </div>
    }
}

// --- Resource Card ---
#[component]
fn ResourceCard(title: &'static str, desc: &'static str, cta: &'static str) -> impl IntoView {
    view! {
        <div class="card-tech">
            <h3 class="font-semibold text-lg mb-2">{title}</h3>
            <p class="text-voltec-gray/60 text-sm mb-4">{desc}</p>
            <a href="#" class="text-voltec-blue hover:text-voltec-blue-light transition-colors text-sm font-medium">
                {cta} " →"
            </a>
        </div>
    }
}

// --- V-OS Terminal ---
#[component]
fn VosTerminal() -> impl IntoView {
    view! {
        <div class="bg-voltec-black rounded-sm border border-voltec-blue/20 overflow-hidden">
            <div class="flex items-center gap-2 px-4 py-3 border-b border-voltec-blue/10">
                <span class="w-2.5 h-2.5 rounded-full bg-voltec-blue/40"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-voltec-blue/20"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-voltec-blue/10"></span>
                <span class="text-voltec-white/30 text-xs font-mono ml-2">"v-os terminal r1.0"</span>
            </div>
            <div class="p-5 font-mono text-xs leading-relaxed">
                <p class="text-voltec-blue/60">"$ vos status --network"</p>
                <p class="text-voltec-white/70 mt-1">"V-OS Network Status"</p>
                <p class="text-voltec-white/40">"─────────────────────────"</p>
                <p class="text-voltec-white/60">"Nodes Online:    " <span class="text-voltec-blue">"12,847"</span></p>
                <p class="text-voltec-white/60">"V-Mind Status:   " <span class="text-green-400">"ACTIVE"</span></p>
                <p class="text-voltec-white/60">"Grid Load:       " <span class="text-voltec-blue">"73.2%"</span></p>
                <p class="text-voltec-white/60">"Predictions:     " <span class="text-voltec-blue">"2,341 active"</span></p>
                <p class="text-voltec-white/60">"Uptime:          " <span class="text-voltec-blue">"99.997%"</span></p>
                <p class="text-voltec-white/40">"─────────────────────────"</p>
                <p class="text-voltec-blue/60 mt-2">"$ vos deploy --pack v-pack-m --node 847"</p>
                <p class="text-green-400 mt-1">"✓ V-Pack M deployed to node 847"</p>
                <p class="text-voltec-white/40">"  V-Mind calibrating... done (1.2s)"</p>
                <p class="text-voltec-blue/60 mt-2">"$ _"</p>
            </div>
        </div>
    }
}

// --- Particle Background ---
#[component]
fn ParticleBackground() -> impl IntoView {
    let canvas_ref = create_node_ref::<leptos::html::Canvas>();

    create_effect(move |_| {
        if let Some(canvas) = canvas_ref.get() {
            let canvas_el: &HtmlCanvasElement = &canvas;
            canvas_el.set_width(1920);
            canvas_el.set_height(1080);

            if let Ok(Some(context)) = canvas_el.get_context("2d") {
                if let Ok(ctx) = context.dyn_into::<CanvasRenderingContext2d>() {
                    let width = canvas_el.width() as f64;
                    let height = canvas_el.height() as f64;

                    // Particles
                    for i in 0..120 {
                        let x = (i as f64 * 17.3) % width;
                        let y = (i as f64 * 13.7) % height;
                        let size = ((i % 3) as f64 + 0.5) * 1.2;
                        let alpha = 0.08 + (i % 10) as f64 * 0.04;
                        ctx.set_fill_style(&JsValue::from_str(&format!("rgba(0, 191, 255, {})", alpha)));
                        ctx.begin_path();
                        let _ = ctx.arc(x, y, size, 0.0, std::f64::consts::PI * 2.0);
                        ctx.fill();
                    }

                    // Connections
                    ctx.set_stroke_style(&JsValue::from_str("rgba(0, 191, 255, 0.04)"));
                    ctx.set_line_width(0.5);
                    for i in 0..40 {
                        let x1 = (i as f64 * 41.0) % width;
                        let y1 = (i as f64 * 37.0) % height;
                        let x2 = ((i + 10) as f64 * 31.0) % width;
                        let y2 = ((i + 15) as f64 * 29.0) % height;
                        ctx.begin_path();
                        ctx.move_to(x1, y1);
                        ctx.line_to(x2, y2);
                        ctx.stroke();
                    }
                }
            }
        }
    });

    view! {
        <canvas
            node_ref=canvas_ref
            class="absolute inset-0 w-full h-full opacity-50 pointer-events-none"
        ></canvas>
    }
}

// --- Social Icon ---
#[component]
fn SocialIcon(href: &'static str, icon_type: &'static str) -> impl IntoView {
    let icon_svg = match icon_type {
        "x" => view! {
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
        },
        "linkedin" => view! {
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
        },
        "github" => view! {
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
        },
        "youtube" => view! {
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
        },
        "discord" => view! {
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/>
            </svg>
        },
        _ => view! {
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/>
            </svg>
        },
    };

    view! {
        <a href=href target="_blank" rel="noopener noreferrer" class="social-icon">
            {icon_svg}
        </a>
    }
}
