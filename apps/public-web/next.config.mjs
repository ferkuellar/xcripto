/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  // Public news content is fetched server-side from the XMIP backend public API.
  // No rewrites/proxy: the backend is the source of truth for canonical/OG/JSON-LD.
};

export default nextConfig;
