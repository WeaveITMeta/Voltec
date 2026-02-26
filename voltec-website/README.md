# Voltec Website

A high-tech, space-age website built with **Rust + Leptos + Trunk + TailwindCSS**.

## Theme
- **Primary**: Clean Industrial White (#FFFFFF)
- **Secondary**: Deep Black (#0A0A0A)
- **Accent**: Blue Xenon (#00BFFF)

## Prerequisites

1. **Rust** with WASM target:
   ```bash
   rustup target add wasm32-unknown-unknown
   ```

2. **Trunk** (WASM bundler):
   ```bash
   cargo install trunk
   ```

3. **Node.js** (for TailwindCSS):
   ```bash
   # Using pnpm (recommended)
   pnpm install
   ```

## Development

### Step 1: Build TailwindCSS
In one terminal, run the CSS watcher:
```bash
pnpm run css:watch
```

### Step 2: Start Trunk Dev Server
In another terminal:
```bash
trunk serve --open
```

The site will be available at `http://localhost:3000`

## Production Build

```bash
# Build CSS
pnpm run css:build

# Build WASM bundle
trunk build --release
```

Output will be in the `dist/` directory.

## Project Structure

```
voltec-website/
├── assets/
│   └── icons/          # Social media icons (SVG)
├── src/
│   └── main.rs         # Leptos application
├── styles/
│   ├── input.css       # TailwindCSS input
│   └── tailwind.css    # Generated CSS (gitignore this)
├── Cargo.toml          # Rust dependencies
├── index.html          # Trunk entry point
├── Trunk.toml          # Trunk configuration
├── tailwind.config.js  # TailwindCSS configuration
└── package.json        # Node dependencies
```

## Features

- ⚡ **WebAssembly** - Blazing fast client-side rendering
- 🎨 **TailwindCSS** - Utility-first styling with custom Voltec theme
- 🔄 **Reactive UI** - Leptos signals for state management
- 🎯 **SPA Routing** - Client-side navigation with leptos_router
- 🖼️ **Nano Banana Lab** - Procedural canvas-based visualizations
- 📱 **Responsive** - Mobile-first design
- ✨ **Xenon Glow Effects** - Custom animations and hover states

## Pages

- `/` - Home (Hero, Features, Stats, CTA)
- `/resources` - Documentation & Learning
- `/careers` - Job Listings
- `/products` - Product Catalog
- `/about` - Company Information
- `/nano` - Nano Banana Visualization Lab
- `/contact` - Contact Form
- `/privacy` - Privacy Policy
- `/terms` - Terms of Service

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Rust | Systems programming language |
| Leptos | Reactive web framework |
| Trunk | WASM bundler & dev server |
| TailwindCSS | Utility-first CSS |
| wasm-bindgen | JS/WASM interop |
| web-sys | Web API bindings |

---

**© 2026 Voltec Industries** - Powered by Rust & WebAssembly
