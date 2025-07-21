/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode for better error detection
  reactStrictMode: true,
  
  // Optimize images from external sources
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'nextjs.org',
        pathname: '/icons/**',
      },
    ],
  },
  
  // Environment variables that should be available in the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  
  // Disable x-powered-by header for security
  poweredByHeader: false,
  
  // Enable SWC minification for better performance
  swcMinify: true,
}

module.exports = nextConfig