/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'oliviks.com' },
      { protocol: 'https', hostname: 'd2xsxph8kpxj0f.cloudfront.net' },
    ],
  },
};

export default nextConfig;
