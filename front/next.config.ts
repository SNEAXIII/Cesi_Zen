import type { NextConfig } from 'next';
const API_CLIENT_HOST = process.env.API_CLIENT_HOST ?? 'localhost';
const API_SERVER_HOST = process.env.NODE_ENV === 'production' ? 'api' : 'localhost';
const API_PORT = process.env.API_PORT ?? '8000';
const nextConfig: NextConfig = {
  output: 'standalone',
};
export const CLIENT_API_URL: string = `http://${API_CLIENT_HOST}/api/back/`;
export const SERVER_API_URL: string = `http://${API_SERVER_HOST}:${API_PORT}`;
export default nextConfig;
